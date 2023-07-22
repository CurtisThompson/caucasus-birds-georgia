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
# Filter for the specific region
df = df.loc[df['STATE CODE'] == 'GE-MM']

for bird in SPECIES:
    # Find checklists with and without bird
    checklists = list(df['SAMPLING EVENT IDENTIFIER'].unique())
    checklists_y = list(df.loc[df['SCIENTIFIC NAME'] == bird, 'SAMPLING EVENT IDENTIFIER'].unique())
    checklists_n = [x for x in checklists if x not in checklists_y]

    # Get count of all species that appear
    species_y = df.loc[df['SAMPLING EVENT IDENTIFIER'].isin(checklists_y), ['COMMON NAME']].value_counts()
    # Normalise counts
    species_y = species_y / len(checklists_y)

    # Get count of all species that do not appear
    species_n = df.loc[df['SAMPLING EVENT IDENTIFIER'].isin(checklists_n), ['COMMON NAME']].value_counts()
    # Normalise counts
    species_n = species_n / len(checklists_n)

    # Create plot of top species for both
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    top_y = species_y[:10][::-1].reset_index().rename(columns={0:'OCCURENCE'})
    top_y.plot(kind='barh', ax=ax[0])
    ax[0].set_yticklabels(top_y['COMMON NAME'])
    top_n = species_n[:10][::-1].reset_index().rename(columns={0:'OCCURENCE'})
    top_n.plot(kind='barh', ax=ax[1])
    ax[1].set_yticklabels(top_n['COMMON NAME'])

    # Make plot look good visually
    plt.tight_layout()
    ax[0].grid()
    ax[1].grid()
    ax[0].set_xlim(0, 1)
    ax[1].set_xlim(0, 1)
    ax[0].get_legend().remove()
    ax[1].get_legend().remove()
    ax[0].set_title('Species Present With Bird')
    ax[1].set_title('Species Present Without Bird')
    ax[0].set_xlabel('Frequency')
    ax[1].set_xlabel('Frequency')
    fig.savefig(f'./fig/{bird.lower().replace(" ", "_")}_indicators.png', bbox_inches='tight')