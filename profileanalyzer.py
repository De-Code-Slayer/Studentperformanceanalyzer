import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from ydata_profiling import ProfileReport

from sklearn.metrics import mean_squared_error, r2_score

import matplotlib.pyplot as plt

import seaborn as sns



df=pd.read_csv('/kaggle/input/student-performance-factors/StudentPerformanceFactors.csv')



for column in df.select_dtypes(include=['object']).columns: 

    unique_values = df[column].unique()

    mapping = {value: i for i, value in enumerate(unique_values)}

    df[column] = df[column].map(mapping)





profile = ProfileReport(df)
profile.to_file("templates/dashboard.html")
