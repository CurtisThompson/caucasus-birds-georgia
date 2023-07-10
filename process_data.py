import pandas as pd

# Import data
df = pd.read_csv('./data/ebd_GE_relMay-2023.txt', delimiter='\t')

#print(df.columns)
columns_needed = ['TAXONOMIC ORDER', 'CATEGORY', 'COMMON NAME', 'SCIENTIFIC NAME',
                  'SUBSPECIES COMMON NAME', 'COUNTRY CODE', 'STATE CODE',
                  'COUNTY CODE', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE',
                  'TIME OBSERVATIONS STARTED', 'OBSERVER ID', 'PROTOCOL TYPE',
                  'DURATION MINUTES', 'EFFORT DISTANCE KM', 'NUMBER OBSERVERS',
                  'ALL SPECIES REPORTED', 'OBSERVATION COUNT', 'SPECIES COMMENTS',
                  'APPROVED', 'REVIEWED', 'SAMPLING EVENT IDENTIFIER']

# Get checklist IDs that contain a caucasian grouse
checklists = df.loc[(df['SCIENTIFIC NAME'] == 'Lyrurus mlokosiewiczi')
                    | (df['SCIENTIFIC NAME'] == 'Tetraogallus caucasicus'),
                    'SAMPLING EVENT IDENTIFIER']

# Filter for those checklists (select only needed columns too)
df_check = df.loc[df['SAMPLING EVENT IDENTIFIER'].isin(checklists),
                  columns_needed]

# Remove unapproved checklists
df_check = df_check.loc[df_check['APPROVED'] == 1]
df_check.drop(['APPROVED', 'REVIEWED'], axis=1)

# Remove long checklists as we cannot pinpoint location or time
df_check = df_check.loc[(df_check['EFFORT DISTANCE KM'] <= 5)
                         & (df_check['DURATION MINUTES'] <= 300)]

# Output some stats on data
print('Checklists          ', len(df_check['SAMPLING EVENT IDENTIFIER'].unique()))
print('Caucasian Grouse    ', (df_check['SCIENTIFIC NAME'] == 'Lyrurus mlokosiewiczi').sum())
print('Caucasian Snowcock  ', (df_check['SCIENTIFIC NAME'] == 'Tetraogallus caucasicus').sum())
print('Species Observations', df_check.shape[0])

# Save data
df_check.to_csv('./data/cleaned_data.csv', index=False)