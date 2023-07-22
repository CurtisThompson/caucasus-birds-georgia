import requests
import json
from time import sleep

import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt
import plotly.express as px

import utils

RANDOM_STATE = 0


# Obtains elevation via API call for entire DataFrame
def request_elevation_dataframe(df):
    lat_lon_combs = df[['LATITUDE', 'LONGITUDE']].drop_duplicates().reset_index(drop=True)
    for i in range(0, lat_lon_combs.shape[0]+1, 100):
        # Get values for API call
        df_call = lat_lon_combs.iloc[i:i+100]
        call = '|'.join([str(r['LATITUDE'])+','+str(r['LONGITUDE']) for i, r in df_call.iterrows()])
        
        # Make API call
        try:
            res = requests.get(f'https://api.opentopodata.org/v1/test-dataset?locations={call}')
            res = json.loads(res.content)['results']
        except:
            res = []
            print(f'Failed to retrieve elevation')
        
        # Process results
        for row in res:
            lat = row['location']['lat']
            lon = row['location']['lng']
            elevation = row['elevation']
            df.loc[(df['LATITUDE']==lat) & (df['LONGITUDE']==lon), 'ELEVATION'] = elevation
    sleep(1)
    return df


def run():
    # List of species we want a map for
    SPECIES = utils.get_analysis_species()

    # Load bird sightings
    df = utils.load_ebird_data(filter=True, region='GE-MM')

    # Group by checklist and get main stats
    dfg = df.groupby('SAMPLING EVENT IDENTIFIER')[['LATITUDE', 'LONGITUDE', 'OBSERVATION DATE',
                                                'TIME OBSERVATIONS STARTED', 'OBSERVER ID',
                                                'PROTOCOL TYPE', 'PROTOCOL CODE', 'DURATION MINUTES',
                                                'EFFORT DISTANCE KM', 'NUMBER OBSERVERS',
                                                'ALL SPECIES REPORTED']].min().reset_index()

    # Add column for whether caucasian birds are in the checklist
    for bird in SPECIES:
        dfg[bird] = dfg['SAMPLING EVENT IDENTIFIER'].apply(
            lambda x: df.loc[(df['SCIENTIFIC NAME'] == bird) & (df['SAMPLING EVENT IDENTIFIER'] == x)].shape[0]
        )

    # Extra calculated features
    dfg['MONTH'] = dfg['OBSERVATION DATE'].apply(lambda x: int(x[5:7]))
    dfg['HOUR'] = dfg['TIME OBSERVATIONS STARTED'].apply(lambda x: int(x[:2]))
    dfg['KMPH'] = dfg['EFFORT DISTANCE KM'] * 60 / dfg['DURATION MINUTES']

    # Round latitude and longitude to 4 decimal places
    dfg['LATITUDE'] = dfg['LATITUDE'].round(4)
    dfg['LONGITUDE'] = dfg['LONGITUDE'].round(4)

    # Get elevation via API
    dfg = request_elevation_dataframe(dfg)

    # Training columns for models (note: predicted classes are species)
    MODEL_COLS = ['LATITUDE', 'LONGITUDE', 'MONTH', 'HOUR', 'DURATION MINUTES', 'EFFORT DISTANCE KM',
                'NUMBER OBSERVERS', 'KMPH', 'ELEVATION']

    # Split into train and validation
    dfg_train, dfg_valid = train_test_split(dfg, train_size=0.9, random_state=RANDOM_STATE)

    # Fit models (one per species)
    models = [XGBClassifier().fit(dfg_train[MODEL_COLS], dfg_train[bird]) for bird in SPECIES]

    # Calculate F1 score for validation
    for index, bird in enumerate(SPECIES):
        print(bird, f1_score(dfg_valid[bird], models[index].predict(dfg_valid[MODEL_COLS])))

    # Plot partial dependence
    for index, bird in enumerate(SPECIES):
        fig, ax = plt.subplots(1, 1, figsize=(16,16))
        PartialDependenceDisplay.from_estimator(models[index], dfg_train[MODEL_COLS], MODEL_COLS, ax=ax, random_state=RANDOM_STATE)
        plt.suptitle(f'Partial Dependence Plots for {bird}')
        plt.savefig(f'./fig/{bird.lower().replace(" ", "_")}_partial_dependence_all.png', bbox_inches='tight')

    # Create coordinate range DataFrame (for predictions)
    lat_range = np.arange(42.60, 42.70, 0.01)
    lon_range = np.arange(44.55, 44.70, 0.01)
    coord_range = []
    for i in lat_range:
        for j in lon_range:
            coord_range.append((i, j))
    dfm = pd.DataFrame(coord_range, columns=['LATITUDE', 'LONGITUDE'])

    # Add in dummy values
    dfm['MONTH'] = 7
    dfm['HOUR'] = 7
    dfm['DURATION MINUTES'] = 120
    dfm['EFFORT DISTANCE KM'] = 2
    dfm['NUMBER OBSERVERS'] = 1
    dfm['KMPH'] = dfm['EFFORT DISTANCE KM'] * 60 / dfm['DURATION MINUTES']
    dfm = request_elevation_dataframe(dfm)

    # Predict occurence and plot on map
    for index, bird in enumerate(SPECIES):
        dfm['Occurence'] = models[index].predict_proba(dfm[MODEL_COLS])[:,1]
        fig = px.density_mapbox(dfm, lat='LATITUDE', lon='LONGITUDE', z='Occurence', radius=100,
                                center=dict(lat=42.6571, lon=44.6401), zoom=11, opacity=0.6,
                                mapbox_style="open-street-map")
        fig.write_image(f'./fig/{bird.lower().replace(" ", "_")}_modelled_map.png')


if __name__ == '__main__':
    run()