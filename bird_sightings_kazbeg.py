import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

import utils


def run():
    # List of species we want a map for
    SPECIES = utils.get_analysis_species()

    # Load Georgia map file
    df_georgia = utils.load_georgia_map(type='kazbeg')

    # Load bird sightings
    df = utils.load_ebird_data(filter=True, region='GE-MM')

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax = [ax1, ax2]

    # Produce map of sightings for each bird
    for index, bird in enumerate(SPECIES):
        # Get only that bird
        df_bird = df.copy()
        df_bird = df_bird.loc[(df_bird['SCIENTIFIC NAME'] == bird),
                            ['SAMPLING EVENT IDENTIFIER', 'LATITUDE', 'LONGITUDE']]
        df_bird.columns = ['ID', 'Lat', 'Lon']

        # Get count of sightings
        sighting_count = df_bird.shape[0]

        # Convert to GeoPandas
        geometry = [Point(xy) for xy in zip(df_bird.Lon, df_bird.Lat)]
        df_bird = df_bird.drop(['Lon', 'Lat'], axis=1)
        gdf = gpd.GeoDataFrame(df_bird, crs="EPSG:4326", geometry=geometry)

        # Plot Georgia map
        df_georgia.plot(ax=ax[index], color='#ccd7e8', edgecolor='black', linewidth=0.3)

        # Plot sightings
        gdf.plot(ax=ax[index], color='#2c5ba3')

        # Add detail to subplot
        ax[index].axis('off')
        ax[index].set_title(f'{bird}')

    # Save figure
    plt.suptitle('Bird Sightings In Mtskheta-Mtianeti')
    fig.savefig(f'./fig/regional_sightings.png', bbox_inches='tight')


if __name__ == '__main__':
    run()