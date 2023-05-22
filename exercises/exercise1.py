import pandas as pd
import sqlalchemy as sa
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'airports.sqlite')

df = pd.read_csv('https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv', sep="; ", engine='python')

engine = sa.create_engine(f'sqlite:///{db_path}')

dtypes = {
    'column_1': sa.Integer(),
    'column_2': sa.String(),
    'column_3': sa.String(),
    'column_4': sa.String(),
    'column_5': sa.String(),
    'column_6': sa.String(),
    'column_7': sa.Float(),
    'column_8': sa.Float(),
    'column_9': sa.Integer(),
    'column_10': sa.Float(),
    'column_11': sa.String(),
    'column_12': sa.String(),
    'geo_punkt': sa.String()
}

print(df)

df.to_sql("airports", engine, if_exists="replace", index=False, dtype=dtypes)