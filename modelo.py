import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score
from matplotlib.pyplot import rcParamsDefault
import seaborn as plt

df=pd.read_csv('modelof1.csv')

print("Dataset loaded. Shape:", df.shape)
print("\nFirst few rows:")
print(df.head())

#======TARGET======
df['podium']=(df['positionOrder']<=3).astype(int)
print("\nPodium:")
print(df['podium'].value_counts())

#======FEATURE ENGINEERING======
df=df.sort_values(['driverId','year','round']).reset_index(drop=True)

df['prev_5_avg_position']=df.groupby('driverId')['positionOrder'].shift(1).rolling(window=5, min_periods=1).mean()
df['prev_5_avg_points']=df.groupby('driverId')['points'].shift(1).rolling(window=5,min_periods=1).mean()

#Historical performance in circuit
circuit_perform=df.groupby(['driverId','circuitId']).agg({
    'positionOrder':'mean'
}).reset_index()
circuit_perform.columns=['driverId','circuitId','circuit_avg_position']
df=df.merge(circuit_perform, on=['driverId','circuitId'], how= 'left')

#Qualifying position
df['grid_position']=pd.to_numeric(df['grid'],errors='coerce')

print('\nFeatures were created.')