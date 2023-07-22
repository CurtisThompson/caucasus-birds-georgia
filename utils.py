import pandas as pd
import geopandas as gpd


# List of species for analysis
def get_analysis_species():
    return ['Lyrurus mlokosiewiczi', 'Tetraogallus caucasicus']


# Load in eBird data
def load_ebird_data(filter=True, region=None):
    # Load raw data
    df = pd.read_csv('./data/ebd_GE_relMay-2023.txt', delimiter='\t')

    if filter:
        # Remove unapproved checklists
        df = df.loc[df['APPROVED'] == 1]
        df.drop(['APPROVED', 'REVIEWED'], axis=1)

        # Remove long checklists as we cannot pinpoint location or time
        df = df.loc[(df['EFFORT DISTANCE KM'] <= 5)
                    & (df['DURATION MINUTES'] <= 300)]
        
        # Filter for the specific region
        if region != None:
            df = df.loc[df['STATE CODE'] == 'GE-MM']

    return df


# Load map of Georgia
def load_georgia_map(type='p2'):
    if type.lower() == 'p1':
        return gpd.read_file('./data/geoBoundaries-GEO-ADM1.geojson')
    if type.lower() == 'p2':
        return gpd.read_file('./data/geoBoundaries-GEO-ADM2.geojson')
    if type.lower() == 'kazbeg':
        return gpd.read_file('./data/geoBoundaries-GEO-ADM2-KAZBEG.geojson')

    # If no acceptable type, return p2 but with debug message
    print('Type not found, returning precision 2')
    return gpd.read_file('./data/geoBoundaries-GEO-ADM2.geojson')