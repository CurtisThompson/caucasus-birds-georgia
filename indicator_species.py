import matplotlib.pyplot as plt

import utils

# List of species we want a map for
SPECIES = utils.get_analysis_species()

# Load bird sightings
df = utils.load_ebird_data(filter=True, region='GE-MM')

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
    for subax in ax:
        subax.grid()
        subax.set_xlim(0, 1)
        subax.get_legend().remove()
        subax.set_xlabel('Frequency')
    ax[0].set_title('Species Present With Bird')
    ax[1].set_title('Species Present Without Bird')
    fig.savefig(f'./fig/{bird.lower().replace(" ", "_")}_indicators.png', bbox_inches='tight')