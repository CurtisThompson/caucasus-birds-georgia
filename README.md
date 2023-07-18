# Caucasian Grouse and Snowcock Sightings In Georgia

## Background Information

The caucasian grouse _(Lyrurus mlokosiewiczi)_ and the caucasian snowcock _(tetraogallus caucasicus)_ are two birds endemic to the Caucasus Mountains, meaning that they can only be found in the wild in this region.

As of July 2023 there are only [572 sightings](https://ebird.org/species/caugro1) of the caucasian grouse on eBird, and [487 sightings](https://ebird.org/species/causno1/) of the caucasian snowcock. In comparison, the black grouse has over 9,000 sightings while the red grouse has almost 30,000 sightings. The two caucasian species are less-studied then many of their Eurasian relatives.

The caucasian grouse is typically found in the altitunidal range ["between upper limits of mountain forests _(Picea orientalis, Betula)_ and subalpine meadows with rhododendron _(Rhododendron caucasicum)_ thickets and stunted birch"](https://doi.org/10.2173/bow.caugro1.01.1). After the chicks hatch in the summer, the females often move to more open meadows with the young while the males move to more protected ravines.

The caucasian snowcock [inhabits areas of the mountains between the treeline and the permanent snow areas](https://birdsoftheworld.org/bow/species/causno1/cur/habitat). During breeding season this is typically between 2400m and 3500m above sea level on north-facing slopes and cliffs. After breeding season they have been known to climb to higher altitudes before descending in autumn and winter.

The Caucasus Mountains themselves span a length of 1200km from the Black Sea to the Caspian Sea, and reach to a height of 5,642m at the peak of Mount Elbrus (the tallest mountain in Europe). This is a huge potential range for the birds.

## Data

Data on bird sightings is from the [eBird Basic Dataset as provided by Cornell Lab](https://science.ebird.org/en/use-ebird-data/download-ebird-data-products). Under the terms of use of the data, the original files cannot be stored on GitHub and so have been included in the `.gitignore`. If you wish to re-run this analysis you will need to download the from eBird and store it in the correct file path.

GeoJSON data for creating maps of Georgia are from [Humanitarian Data Exchange](https://data.humdata.org/dataset/geoboundaries-admin-boundaries-for-georgia). There provide maps of the country at three different resolutions. The relevant files have been stored in the `data` folder.

## Caucasian Grouse and Snowcock Sightings

The first step in sighting these two birds is to look at where they have been sighted in the past. This can be achieved relatively simply by filtering the eBird data for Georgian sightings of the two birds and plotting them on a map.

To ensure that locations are accurate (within a few kilometers) we have filtered out any sightings where the birder travelled over 5km. We have also removed sightings that took place over the timeline of more than 5 hours to keep consistent with future analysis.

The code for the filtering and map plotting can be found in `bird_sightings.py`.

![Caucasian grouse sightings in Georgia](./fig/lyrurus_mlokosiewiczi_sightings.png)

![Caucasian snowcock sightings in Georgia](./fig/tetraogallus_caucasicus_sightings.png)

As we can see, sightings for both birds are primarily concentrated in the Mtskheta-Mtianeti region in the north-east of the country. Therefore we will now focus our analysis on this area. The below figure shows the sightings in just the Mtskheta-Mtianeti region.

![Mtskheta-Mtianeti sightings](./fig/regional_sightings.png)

## Time of Sightings

The time of bird sightings is also important. Different species are most active at different times of the day and your chance of seeing the birds will change along with this.

In `time_of_day.py` we create two simple plots of when the species were sighted based on the hour that the observations started.

![Graph of times of Caucasian grouse sightings](./fig/lyrurus_mlokosiewiczi_time_simple.png)

![Graph of times of Caucasian snowcock sightings](./fig/tetraogallus_caucasicus_time_simple.png)

These graphs are not perfect for two reasons. Firstly, an observation on eBird can span multiple hours. If the start time is 10:00 and the duration is 2.5 hours then the bird could have been spotted at any combination of 10am, 11am, or 12pm.

Secondly, observers may be out looking for the birds more commonly at certain times. While most observations of the birds are in the morning, this does not show whether observers are out more in the morning or whether the birds are more likely to be seen in the morning.