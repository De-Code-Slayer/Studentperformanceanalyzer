import pandas as pd
import numpy as np

def analyze_data(input_path, output_path):
    # Load dataset
    df = pd.read_csv(input_path)
    
    # Drop columns with missing values
    df.dropna(axis=1, inplace=True)
    
    # Remove outliers using Z-score
    z = np.abs((df - df.mean()) / df.std())
    threshold = 3
    df = df[(z < threshold).all(axis=1)]
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    return output_path
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class StatisticalAnalyzer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def encode_categorical_data(self):
        # Find all columns with categorical data
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        
        # Encode each column
        for column in categorical_columns:
            label_encoder = LabelEncoder()
            self.data[column] = label_encoder.fit_transform(self.data[column])
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)

    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
    def calculate_missing_values(self):
        # Calculate missing values for each column
        return self.data.isnull().sum().to_dict()
    


