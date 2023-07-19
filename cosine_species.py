import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

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

# Get a list of checklists and species
checklists = list(df['SAMPLING EVENT IDENTIFIER'].unique())
species = list(df['SCIENTIFIC NAME'].unique())

# Build these into a matrix
df_check = pd.DataFrame(index=checklists, columns=species)
df_check = df_check.fillna(0)

# Fill in the matrix cells if species appears in checklist
for index, row in df.iterrows():
    spec = row['SCIENTIFIC NAME']
    chck = row['SAMPLING EVENT IDENTIFIER']
    df_check.loc[chck, spec] = 1

# Create figure with two subplots
fig, ax = plt.subplots(1, 2, figsize=(20,12))

for index, bird in enumerate(SPECIES):
    col_bird = df_check[bird]
    col_other = df_check.copy().drop(bird, axis=1)
    similarities = []

    # Find similarities
    for col in col_other:
        similarities.append((col,
                             cosine_similarity(col_bird.values.reshape(1,-1), col_other[col].values.reshape(1,-1))[0][0]))
    
    # Sort by largest to smallest
    similarities.sort(key=lambda x: -x[1])

    # Get top 10
    similarities = similarities[:20]
    df_sim = pd.DataFrame(similarities, columns=['Scientific Name', 'Similarity'])

    # Find common name
    df_sim['Common Name'] = df_sim['Scientific Name'].apply(lambda x: df.loc[df['SCIENTIFIC NAME'] == x, 'COMMON NAME'].max())
    
    # Invert DataFrame
    df_sim = df_sim.iloc[::-1]

    # Plot bar chart
    df_sim.plot(kind='barh', ax=ax[index], y='Similarity', x='Common Name')
    ax[index].set_title(f'{bird} Similars')


fig.savefig(f'./fig/cosine_similars.png', bbox_inches='tight')