import pandas as pd
import matplotlib.pyplot as plt

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

# Produce time of day plots for each bird
for bird in SPECIES:
    df_bird = df.copy()
    # Get times of observations for species
    df_bird = df_bird.loc[(df_bird['SCIENTIFIC NAME']) == bird,
                          ['OBSERVATION DATE', 'TIME OBSERVATIONS STARTED', 'DURATION MINUTES']]
    df_bird['Start Hour'] = df_bird['TIME OBSERVATIONS STARTED'].str[:2].astype('int')

    # Bin times
    counts = pd.DataFrame(range(24), columns=['Hour'])
    counts['Observations'] = counts['Hour'].apply(lambda x: df_bird.loc[df_bird['Start Hour'] == x].shape[0])

    # Plot on bar chart
    fig, ax = plt.subplots(figsize=(12,4))
    plt.bar(data=counts, x='Hour', height='Observations', figure=fig)
    plt.title(f'Start Time of {bird} Observations')
    plt.ylabel('Observations')
    plt.xlabel('Starting Time of Observation')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Save figure
    fig.savefig(f'./fig/{bird.lower().replace(" ", "_")}_time_simple.png', bbox_inches='tight')