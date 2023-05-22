import pandas as pd
import sqlalchemy as sa


db_path = 'airports.sqlite'

df = pd.read_csv('https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv', sep="; ", engine='python')

engine = sa.create_engine(f'sqlite:///{db_path}')

print(df)

df.to_sql("airports", engine, if_exists="replace", index=False,)