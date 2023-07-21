import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt

RANDOM_STATE = 0

# List of species we want a map for
SPECIES = ['Lyrurus mlokosiewiczi', 'Tetraogallus caucasicus']

# Load bird sightings
df = pd.read_csv('./data/ebd_GE_relMay-2023.txt', delimiter='\t')
# Remove unapproved checklists
df = df.loc[df['APPROVED'] == 1]
df.drop(['APPROVED', 'REVIEWED'], axis=1)
# Remove long checklists as we cannot pinpoint location or time
df = df.loc[(df['EFFORT DISTANCE KM'] <= 5)
             & (df['DURATION MINUTES'] <= 300)]
# Filter for the specific region
df = df.loc[df['STATE CODE'] == 'GE-MM']

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

# Debug stats
print(dfg.columns)
print(dfg.shape)
print(dfg['Lyrurus mlokosiewiczi'].sum())
print(dfg['Tetraogallus caucasicus'].sum())
print()

# Extra calculated features
dfg['MONTH'] = dfg['OBSERVATION DATE'].apply(lambda x: int(x[5:7]))
dfg['HOUR'] = dfg['TIME OBSERVATIONS STARTED'].apply(lambda x: int(x[:2]))
dfg['KMPH'] = dfg['EFFORT DISTANCE KM'] * 60 / dfg['DURATION MINUTES']

# Training columns for models (note: predicted classes are species)
MODEL_COLS = ['LATITUDE', 'LONGITUDE', 'MONTH', 'HOUR', 'DURATION MINUTES', 'EFFORT DISTANCE KM',
              'NUMBER OBSERVERS', 'KMPH']

# Debug stats
print(dfg[MODEL_COLS + SPECIES])

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