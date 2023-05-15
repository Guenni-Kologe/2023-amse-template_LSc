# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This project refers to the connection between cars per inhabitant and the availability of railroad stops (Deutsche Bahn) in the respective counties. The aim is to identify counties that have a sparse rail infrastructure and to identify whether they have a higher number of registered cars. 

## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The results of the project will help identify counties that substitute private vehicles for their sparsely developed rail networks. The results of this analysis should help to expand the rail network in those counties that have a particularly high ratio of vehicles per inhabitant, in order to achieve that after a successful expansion of the rail network fewer private motor vehicles are needed. This could result in more people using public transport and therefore less pollutants, less noise and fewer accidents due to private vehicles.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: DB Haltetestellen
* Metadata URL: https://data.deutschebahn.com/dataset/data-haltestellen.html
* Data URL: https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV
* Data Type: CSV

This data set contains all important information about the stops of the German Railways (Deutsche Bahn) in Germany.

### Datasource2: Kraftfahrzeugbestand
* Metadata URL: https://mobilithek.info/offers/-8395690728355365851
* Data URL: https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv
* Data Type: CSV

This dataset contains data on how many motor vehicles are registered in the respective counties of Germany.

### Datasource3: Einwohner (Landkreis)
* Metadata URL: hhttps://www.suche-postleitzahl.org/downloads#google_vignette
* Data URL: https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv
* Data Type: CSV

This dataset contains data on the different counties in Germany, such as the count of the inhabitants.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Set Datapipeline
2. Analyze data
3. More to come

[i1]: https://github.com/jvalue/2023-amse-template/issues/1
