import pandas as pd
import sqlalchemy as sa
import os
import matplotlib.pyplot as plt

# Retrieve the both datasets from the internet
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'data.sqlite')
engine = sa.create_engine(f'sqlite:///{db_path}')

vehicle_data = pd.read_csv('https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv', sep=';', encoding='iso-8859-1', skiprows=5, skipfooter=5, engine='python')
vehicle_data.columns = ['col1', 'col2', 'county'] + list(vehicle_data.columns[3:]) # Rename the first three columns
vehicle_data.drop(['col1', 'col2'], axis=1, inplace=True) # Drop col1 and col2
vehicle_data['county'] = vehicle_data['county'].str.split(',').str[0] # Get rid of the values after the comma (e.g., Kreisfreie Stadt etc.)


county_data = pd.read_csv('https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv')

for nbr in range(0, 10):
    county_data['note'] = county_data['note'].str.replace(f'{nbr}', '') # Remove the ZIP-Code from the 'note' column in county_data

county_data['note'] = county_data['note'].str.replace(' ', '', n=1) # Remove the first Space, which stays after the number cleaning
county_data = county_data.groupby('note', as_index=False)['einwohner'].sum() # Group by 'note' and sum the 'einwohner' values


# Replace empty strings with NaN (missing values)
vehicle_data["Pkw"] = vehicle_data["Pkw"].replace("", float("nan"))
vehicle_data["Kraftomnibusse"] = vehicle_data["Kraftomnibusse"].replace("", float("nan"))

# Convert the new columns to integer type
county_data["einwohner"] = pd.to_numeric(county_data["einwohner"], errors="coerce").astype(pd.Int64Dtype())
vehicle_data["Pkw"] = pd.to_numeric(vehicle_data["Pkw"], errors="coerce").astype(pd.Int64Dtype())
vehicle_data["Kraftomnibusse"] = pd.to_numeric(vehicle_data["Kraftomnibusse"], errors="coerce").astype(pd.Int64Dtype())

# Group Vehicle Data
vehicle_data = vehicle_data.groupby('county', as_index=False).agg({'Pkw': 'sum', 'Kraftomnibusse': 'sum'})

# Save the edited data into the SQLite Database
engine = sa.create_engine(f'sqlite:///{db_path}')

vehicle_data.to_sql("vehicle", engine, if_exists="replace", index=False) # Save the data to a SQL databases
county_data.to_sql("county", engine, if_exists="replace", index=False)

# Query the needed data from the SQLite Database and store it in a DataFrame
query = sa.text("""
SELECT DISTINCT c.note AS County, c.einwohner AS Inhabitants, v.Pkw AS "Registered Vehicles", v.Kraftomnibusse AS "Buses"
FROM county AS c
RIGHT OUTER JOIN vehicle AS v ON c.note = v.county
""")

conn = engine.connect() # Execute the query and fetch the data
result = conn.execute(query)
data = result.fetchall()

df = pd.DataFrame(data, columns=["County", "Inhabitants", "Registered Vehicles", "Registered Buses"]) # Create the DataFrame
df["Inhabitants"] = pd.to_numeric(df["Inhabitants"], errors="coerce").astype(pd.Int64Dtype())
df["Registered Vehicles"] = pd.to_numeric(df["Registered Vehicles"], errors="coerce").astype(pd.Int64Dtype())
df["Registered Buses"] = pd.to_numeric(df["Registered Buses"], errors="coerce").astype(pd.Int64Dtype())
df.to_sql("result", engine, if_exists="replace", index=False)

conn.close()