import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

import utils

# List of species we want a map for
SPECIES = utils.get_analysis_species()

# Load Georgia map file
df_georgia = utils.load_georgia_map(type='p1')

# Load bird sightings
df = utils.load_ebird_data(filter=True, region=None)

# Produce map of sightings for each bird
for bird in SPECIES:
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
    fig, ax = plt.subplots()
    df_georgia.plot(ax=ax, color='#ccd7e8', edgecolor='black', linewidth=0.3)

    # Plot sightings
    gdf.plot(ax=ax, color='#2c5ba3')

    # Save figure
    plt.axis('off')
    plt.title(f'{bird} Sightings ({sighting_count} Total)')
    fig.savefig(f'./fig/{bird.lower().replace(" ", "_")}_sightings.png', bbox_inches='tight')