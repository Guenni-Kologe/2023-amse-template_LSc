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
* Data URL: https://data.deutschebahn.com/dataset/data-haltestellen/resource/21edf505-e97d-4c99-bcc9-a46e85f8620f.html
* Data Type: CSV

This data set contains all important information about the stops of the German Railways (Deutsche Bahn) in Germany.

### Datasource2: Kraftfahrzeugbestand
* Metadata URL: https://mobilithek.info/offers/-8395690728355365851
* Data URL: https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv
* Data Type: CSV

This dataset contains data on how many motor vehicles are registered in the respective counties of Germany.

### Datasource3: Einwohner (Landkreis)
* Metadata URL: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html
* Data URL: https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.destatis.de%2FDE%2FThemen%2FLaender-Regionen%2FRegionales%2FGemeindeverzeichnis%2FAdministrativ%2F04-kreise.xlsx%3F__blob%3DpublicationFile&wdOrigin=BROWSELINK
* Data Type: CSV

This dataset contains data on the different counties in Germany, such as the count of the inhabitants.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Example Issue [#1][i1]
2. ...

[i1]: https://github.com/jvalue/2023-amse-template/issues/1
