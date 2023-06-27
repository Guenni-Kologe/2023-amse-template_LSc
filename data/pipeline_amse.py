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

# Save the edited data into the SQLite Database
engine = sa.create_engine(f'sqlite:///{db_path}')

vehicle_data.to_sql("vehicle", engine, if_exists="replace", index=False) # Save the data to a SQL databases
county_data.to_sql("county", engine, if_exists="replace", index=False)

# Query the needed data from the SQLite Database and store it in a DataFrame
query = sa.text("""
SELECT c.note AS County, c.einwohner AS Inhabitants, v.Pkw AS "Registered Vehicles", v.Ackerschlepper AS Ackerschlepper
FROM county AS c
JOIN vehicle AS v ON c.note = v.county
""")

conn = engine.connect() # Execute the query and fetch the data
result = conn.execute(query)
data = result.fetchall()

df = pd.DataFrame(data, columns=["County", "Inhabitants", "Registered Vehicles", "Ackerschlepper"]) # Create the DataFrame

# Perform exploratory analysis

filtered_df_pkw = df[df["Registered Vehicles"].notnull() & (df["Registered Vehicles"] != "-")] # Filter out non-integers and NULLs, we do this in this step as otherwise we would need to store a '0' in our DB 
filtered_df_ackerschlepper = df[df["Ackerschlepper"].notnull() & (df["Ackerschlepper"] != "-")] # or use dropna() which would drop a column even if it would only lack one value

max_registered_vehicles = filtered_df_pkw["Registered Vehicles"].astype(int).max() # Convert max_registered_vehicles and max_inhabitants to integers and get the maximum value
max_inhabitants = filtered_df_pkw["Inhabitants"].astype(int).max()

num_ticks = 10 # Set the desired number of tick marks

x_ticks_pkw = list(range(0, max_registered_vehicles + 1, max_registered_vehicles // num_ticks)) # Define the tick positions for the x-axis
x_ticks_ackerschlepper = list(range(0, filtered_df_ackerschlepper["Ackerschlepper"].astype(int).max() + 1, filtered_df_ackerschlepper["Ackerschlepper"].astype(int).max() // num_ticks))


max_inhabitants = filtered_df_pkw["Inhabitants"].astype(int).max() # Again convert inhabitants into integers and then get the maximum

y_ticks = list(range(0, max_inhabitants + 1, max_inhabitants // num_ticks))

# Plot the counties inhabitants and their amount of registered vehicles
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

# Show the plot
plt.tight_layout()
plt.show()
