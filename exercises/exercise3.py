import pandas as pd
import sqlite3

df = pd.read_csv("https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv", delimiter=";", encoding='iso-8859-1', skiprows=6, skipfooter=4, engine='python')

df.columns.values[0] = 'date'
df.columns.values[1] = 'CIN'
df.columns.values[2] = 'name'
df.columns.values[12] = 'petrol'
df.columns.values[22] = 'diesel'
df.columns.values[32] = 'gas'
df.columns.values[42] = 'electro'
df.columns.values[52] = 'hybrid'
df.columns.values[62] = 'plugInHybrid'
df.columns.values[72] = 'others'

# Drop all other columns
columns_to_keep = ['date', 'CIN', 'name', 'petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']
df = df.loc[:, columns_to_keep]

# print("Step 1: ")
# print(df)

# Validate CINs
df['CIN'] = df['CIN'].astype(str).str.zfill(5)

# print("Step 2: ")
# print(df)

# Validate athe rest
numeric_columns = ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']

# print("Step 3: ")
# print(df)

filtered_df = df[(df[numeric_columns] != '-')]
df[numeric_columns] = filtered_df[numeric_columns]
df = df.dropna()

# print("Step 4: ")
# print(df)

df[numeric_columns] = df[numeric_columns].astype(int)

# print("Step 5: ")
# print(df)

# Drop rows with numeric values less than or equal to zero
filtered_df = df[(df[numeric_columns] > 0)]
df[numeric_columns] = filtered_df[numeric_columns]
df = df.dropna()


# print("Step : 6")
# print(df)

# Write data into SQLite database
conn = sqlite3.connect("cars.sqlite")
df.to_sql("cars", conn, if_exists="replace", index=False)

# Close the database connection
conn.close()
