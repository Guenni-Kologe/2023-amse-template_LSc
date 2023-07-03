import pandas as pd
import sqlite3

stops_df = pd.read_csv("exercises/stops.txt", dtype={"stop_id": str, "stop_name": str, "stop_lat": float, "stop_lon": float, "zone_id": str})

stops_df["stop_name"] = stops_df["stop_name"].str.encode("unicode_escape").str.decode("unicode_escape")
stops_df = stops_df[(stops_df["zone_id"] == "2001") &
                    (stops_df["stop_lat"] >= -90) &
                    (stops_df["stop_lat"] <= 90) &
                    (stops_df["stop_lon"] >= -90) &
                    (stops_df["stop_lon"] <= 90)]

stops_df.dropna(subset=["stop_name", "stop_lat", "stop_lon"], inplace=True)

columns_to_keep = ["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"]

conn = sqlite3.connect("exercises/gtfs.sqlite")
stops_df[columns_to_keep].to_sql("stops", conn, if_exists="replace", index=False)
conn.close()

