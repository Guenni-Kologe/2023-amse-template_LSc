import pandas as pd
import sqlalchemy as sa
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'data.sqlite')

# Load the station data
station_data = pd.read_csv('https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV', sep=';')

# Load the vehicle data
vehicle_data = pd.read_csv('https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv', sep=';', encoding='iso-8859-1', skiprows=5, skipfooter=5)


# Load the county data
county_data = pd.read_csv('https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv')

# Connect a database
engine = sa.create_engine(f'sqlite:///{db_path}')

# Save the data to a SQL database
print(vehicle_data)
station_data.to_sql("stations", engine, if_exists="replace", index=False)
vehicle_data.to_sql("vehicle", engine, if_exists="replace", index=False)
county_data.to_sql("county", engine, if_exists="replace", index=False)
