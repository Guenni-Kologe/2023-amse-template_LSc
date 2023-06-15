import pandas as pd
import sqlalchemy as sa
import ssl
import os
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'data.sqlite')
engine = sa.create_engine(f'sqlite:///{db_path}')

# Load the vehicle data
vehicle_data = pd.read_csv('https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0020_00.csv', sep=';', encoding='iso-8859-1', skiprows=5, skipfooter=5, engine='python')

# Rename the first three columns
vehicle_data.columns = ['col1', 'col2', 'county'] + list(vehicle_data.columns[3:])

# Drop col1 and col2
vehicle_data.drop(['col1', 'col2'], axis=1, inplace=True)

# Adjust the column 'county' of vehicle_data
vehicle_data['county'] = vehicle_data['county'].str.split(',').str[0]

# Load the county data
county_data = pd.read_csv('https://downloads.suche-postleitzahl.org/v2/public/plz_einwohner.csv')

# Remove numbers from the 'note' column in county_data
for nbr in range(0, 10):
    county_data['note'] = county_data['note'].str.replace(f'{nbr}', '')

#Remove the first Space, which stays after the number cleaning
county_data['note'] = county_data['note'].str.replace(' ', '', n=1)

# Group by 'note' and sum the 'einwohner' values
county_data = county_data.groupby('note', as_index=False)['einwohner'].sum()

# Drop unnecessary columns from county_data
#county_data = county_data.iloc[:, 1:]

# Connect a database
engine = sa.create_engine(f'sqlite:///{db_path}')

# Save the data to a SQL databases
vehicle_data.to_sql("vehicle", engine, if_exists="replace", index=False)
county_data.to_sql("county", engine, if_exists="replace", index=False)

# Query the data
query = sa.text("""
SELECT c.note AS County, c.einwohner AS Inhabitants, v.Pkw AS "Registered Vehicles", v.Ackerschlepper AS Ackerschlepper
FROM county AS c
JOIN vehicle AS v ON c.note = v.county
""")

# Execute the query and fetch the data
conn = engine.connect()
result = conn.execute(query)
data = result.fetchall()

# Create a DataFrame
df = pd.DataFrame(data, columns=["County", "Inhabitants", "Registered Vehicles", "Ackerschlepper"])

# Perform exploratory analysis

# Filter out non-integer values in "Registered Vehicles" column
filtered_df_pkw = df[df["Registered Vehicles"].notnull() & (df["Registered Vehicles"] != "-")]
# Filter out non-integer values in "Ackerschlepper" column
filtered_df_ackerschlepper = df[df["Ackerschlepper"].notnull() & (df["Ackerschlepper"] != "-")]

# Convert max_registered_vehicles and max_inhabitants to integers
max_registered_vehicles = filtered_df_pkw["Registered Vehicles"].astype(int).max()
max_inhabitants = filtered_df_pkw["Inhabitants"].astype(int).max()

#print(filtered_df_pkw["Inhabitants"].astype(int).max())
#print(" <- max | Inhabitants | min - >")
#print(filtered_df_pkw["Inhabitants"].astype(int).min())

#print(filtered_df_pkw["Registered Vehicles"].astype(int).max())
#print(" <- max | Pkw | min - >")
#print(filtered_df_pkw["Registered Vehicles"].astype(int).min())

min_registered_vehicles = filtered_df_pkw["Registered Vehicles"].astype(int).min()
# Set the desired number of tick marks
num_ticks = 10

# Define the tick positions for the x-axis
x_ticks_pkw = list(range(0, max_registered_vehicles + 1, max_registered_vehicles // num_ticks))
x_ticks_ackerschlepper = list(range(0, filtered_df_ackerschlepper["Ackerschlepper"].astype(int).max() + 1, filtered_df_ackerschlepper["Ackerschlepper"].astype(int).max() // num_ticks))

# Calculate the range of values in the "Inhabitants" column
min_inhabitants = filtered_df_pkw["Inhabitants"].astype(int).min()
max_inhabitants = filtered_df_pkw["Inhabitants"].astype(int).max()

# Calculate the step size for y-axis ticks
y_range = max_inhabitants - min_inhabitants
y_tick_step = y_range // num_ticks

# Define the tick positions for the y-axis
y_ticks = list(range(min_inhabitants, max_inhabitants + 1, y_tick_step))

# Plot the counties and their amount of registered vehicles
plt.figure(figsize=(18, 6))

# Plot for Pkw
plt.subplot(1, 2, 1)
plt.scatter(filtered_df_pkw["Registered Vehicles"].astype(int), filtered_df_pkw["Inhabitants"].astype(int))
plt.xlabel("Registered Vehicles (Pkw)")
plt.ylabel("Inhabitants")
plt.title("County Analysis - Pkw")
plt.xticks(x_ticks_pkw)
plt.yticks(y_ticks)
plt.ticklabel_format(style="plain")
total_points_pkw = len(filtered_df_pkw)
plt.text(0.95, 0.95, f"Total Counties: {total_points_pkw}", transform=plt.gca().transAxes, ha='right', va='top')
highest_ratio_county_pkw = filtered_df_pkw.loc[(filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)) == (filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)).max(), "County"].iloc[0]
highest_ratio_value_pkw = (filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)).max()
lowest_ratio_county_pkw = filtered_df_pkw.loc[(filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)) == (filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)).min(), "County"].iloc[0]
lowest_ratio_value_pkw = (filtered_df_pkw["Registered Vehicles"].astype(int) / filtered_df_pkw["Inhabitants"].astype(int)).min()
plt.text(0.95, 0.90, f"Most Pkw per Inhabitant: {highest_ratio_county_pkw} ({highest_ratio_value_pkw:.2f})", transform=plt.gca().transAxes, ha='right', va='top')
plt.text(0.95, 0.85, f"Lowest Pkw per Inhabitant: {lowest_ratio_county_pkw} ({lowest_ratio_value_pkw:.2f})", transform=plt.gca().transAxes, ha='right', va='top')
filtered_df_pkw.to_sql("result_pkw", engine, if_exists="replace", index=False)

# Plot for Ackerschlepper
plt.subplot(1, 2, 2)
plt.scatter(filtered_df_ackerschlepper["Ackerschlepper"].astype(int), filtered_df_ackerschlepper["Inhabitants"].astype(int))
plt.xlabel("Tractors")
plt.ylabel("Inhabitants")
plt.title("County Analysis - Ackerschlepper")
plt.xticks(x_ticks_ackerschlepper)
plt.yticks(y_ticks)
plt.ticklabel_format(style="plain")
total_points_ackerschlepper = len(filtered_df_ackerschlepper)
plt.text(0.95, 0.95, f"Total Counties: {total_points_ackerschlepper}", transform=plt.gca().transAxes, ha='right', va='top')
highest_ratio_county_ackerschlepper = filtered_df_ackerschlepper.loc[(filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)) == (filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)).max(), "County"].iloc[0]
highest_ratio_value_ackerschlepper = (filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)).max()
lowest_ratio_county_ackerschlepper = filtered_df_ackerschlepper.loc[(filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)) == (filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)).min(), "County"].iloc[0]
lowest_ratio_value_ackerschlepper = (filtered_df_ackerschlepper["Ackerschlepper"].astype(int) / filtered_df_ackerschlepper["Inhabitants"].astype(int)).min()
plt.text(0.95, 0.90, f"Most Tractors per Inhabitant: {highest_ratio_county_ackerschlepper} ({highest_ratio_value_ackerschlepper:.2f})", transform=plt.gca().transAxes, ha='right', va='top')
plt.text(0.95, 0.85, f"Lowest Tractors per Inhabitant: {lowest_ratio_county_ackerschlepper} ({lowest_ratio_value_ackerschlepper:.2f})", transform=plt.gca().transAxes, ha='right', va='top')
filtered_df_ackerschlepper.to_sql("result_ackerschlepper", engine, if_exists="replace", index=False)

plt.tight_layout()
plt.show()
