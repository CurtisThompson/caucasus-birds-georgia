import pandas as pd
import matplotlib.pyplot as plt

import utils


def run():
    # List of species we want a map for
    SPECIES = utils.get_analysis_species()

    # Load bird sightings
    df = utils.load_ebird_data(filter=True, region=None)

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


if __name__ == '__main__':
    run()