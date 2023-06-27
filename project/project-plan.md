# Project Plan

## Summary

<!-- Describe your data science project in max. 5 sentences. -->
This project refers to the connection between cars per inhabitant and the amount of registered vehicles in the respective counties. The aim is to identify counties that have a relatively low population, but a lot of registered vehicles. With that reached, the aim is to compare different vehicle types (e.g. Cars and Tractors) to see if there is a correlation between the population and the amount of registered vehicle types. The Asumption here is that in hardly populated areas public transportation is not that widespread and therefore more vehicles per inhabitant are registered.

## Rationale

<!-- Outline the impact of the analysis, e.g. which pains it solves. -->
The results of the project will help to identify counties that have alot of private vehicles. This could be an indicator for a lack of public transportation or in more general this could be a subject to examine. The project could help the Government or public transportation companies to identify counties with a vast potential for improvement. This could ultimately result in more people using public transport and therefore less pollutants, less noise and fewer accidents due to private vehicles.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Kraftfahrzeugbestand
* Metadata URL: https://mobilithek.info/offers/-8395690728355365851
* Data URL: https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv
* Data Type: CSV

This dataset contains data on how many motor vehicles are registered in the respective counties of Germany. They are devided into different categories, such as for example Cars and Tractors.

### Datasource2: Einwohner (Landkreis)
* Metadata URL: hhttps://www.suche-postleitzahl.org/downloads#google_vignette
* Data URL: https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv
* Data Type: CSV

This dataset contains data on the different counties in Germany. In the context of this project the count of the inhabitants of the respective county is of interest.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Search for datasets
2. Retrieve the data into a SQL-File
3. Browse the data to get an overview and make a plan how to combine the tables
4. Edit the datasets to match each other for the JOIN
5. Plot the relevant data
6. Insert some interesting text in the plot

[i1]: https://github.com/Guenni-Kologe/2023-amse-template_LSc
