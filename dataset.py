import pandas as pd
import csv

circuits=pd.read_csv('circuits.csv')
constructor_results=pd.read_csv('constructor_results.csv')
constructors_standings=pd.read_csv('constructor_standings.csv')
constructors=pd.read_csv('constructors.csv')
driver_standings=pd.read_csv('driver_standings.csv')
drivers=pd.read_csv('drivers.csv')
lap_times=pd.read_csv('lap_times.csv')
pit_stops=pd.read_csv('pit_stops.csv')
qualifying=pd.read_csv('qualifying.csv')
races=pd.read_csv('races.csv')
results=pd.read_csv('results.csv')
seasons=pd.read_csv('seasons.csv')
sprint_results=pd.read_csv('sprint_results.csv')
status=pd.read_csv('status.csv')

#Cleaning and preparing data for analysis

races=races.merge(circuits,on='circuitId',how='left',suffixes=("","_circuit"))

df=(results
.merge(races, on='raceId',how='left',suffixes=("","_race"))
.merge(drivers, on='driverId',how='left',suffixes=("","_driver"))
.merge(constructors, on='constructorId',how='left',suffixes=("","_constructor")))

lap_agg=lap_times.groupby(['raceId','driverId']).agg(
    laps_count=("lap", "count"),
    best_laps_time=("milliseconds", "min")
).reset_index()

df=df.merge(lap_agg,on=['raceId','driverId'],how='left',suffixes=("","_lapagg"))

pit_agg=pit_stops.groupby(['raceId','driverId']).agg(
    pit_stops_count=("stop", "count"),  
    total_pit_time=("duration", "sum")
).reset_index()

df=df.merge(pit_agg,on=['raceId','driverId'],how='left',suffixes=("","_pitagg"))

df.to_csv('modelof1.csv',index=False,quoting=csv.QUOTE_NONNUMERIC)



