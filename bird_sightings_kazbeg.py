import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# List of species we want a map for
SPECIES = ['Lyrurus mlokosiewiczi', 'Tetraogallus caucasicus']

# Load Georgia map file
df_georgia = gpd.read_file('./data/geoBoundaries-GEO-ADM2-KAZBEG.geojson')

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