import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder

class StatisticalAnalyzer:
    def __init__(self, filepath):
        """Initialize the class with a file path."""
        self.data = pd.read_csv(filepath)

    def describe_data(self):
        """Return descriptive statistics for numerical columns."""
        return self.data.describe()

    def check_missing_values(self):
        """Check for missing values in the dataset."""
        return self.data.isnull().sum()

    def fill_missing_values(self, method='mean'):
        """Fill missing values using the specified method (mean, median, mode)."""
        for column in self.data.columns:
            if self.data[column].isnull().any():
                if pd.api.types.is_numeric_dtype(self.data[column]):
                    if method == 'mean':
                        self.data[column].fillna(self.data[column].mean(), inplace=True)
                    elif method == 'median':
                        self.data[column].fillna(self.data[column].median(), inplace=True)
                    elif method == 'mode':
                        self.data[column].fillna(self.data[column].mode()[0], inplace=True)
                else:
                    # For non-numeric columns, use mode to fill missing values if mode exists
                    mode_value = self.data[column].mode()
                    if not mode_value.empty:
                        self.data[column].fillna(mode_value[0], inplace=True)
                    else:
                        # If no mode, fill with a default value (e.g., 'Unknown')
                        self.data[column].fillna('Unknown', inplace=True)

    def encode_categorical_data(self):
        """Encode categorical data into numerical format."""
        label_encoders = {}
        for column in self.data.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            self.data[column] = le.fit_transform(self.data[column].astype(str))
            label_encoders[column] = le
        return label_encoders

    def correlation_matrix(self):
        """Compute and return the correlation matrix for numeric columns."""
        return self.data.select_dtypes(include=[np.number]).corr()

    def perform_ttest(self, col1, col2):
        """Perform a t-test between two columns."""
        if col1 not in self.data.columns or col2 not in self.data.columns:
            raise ValueError("Both columns must exist in the dataset.")

        return stats.ttest_ind(self.data[col1].dropna(), self.data[col2].dropna())

    def frequency_distribution(self, column):
        """Return the frequency distribution for a specified column."""
        if column not in self.data.columns:
            raise ValueError("Column must exist in the dataset.")

        return self.data[column].value_counts()

    def normalize_data(self, columns=None):
        """Normalize specified columns (default is all numerical columns)."""
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns

        self.data[columns] = (self.data[columns] - self.data[columns].min()) / (self.data[columns].max() - self.data[columns].min())
        return self.data[columns]

    def save_cleaned_data(self, output_path):
        """Save the cleaned and processed data to a new CSV file."""
        self.data.to_csv(output_path, index=False)

# Example usage:
# analyzer = StatisticalAnalyzer('data/StudentPerformanceFactors.csv')
# print(analyzer.describe_data())
# analyzer.fill_missing_values(method='mean')
# analyzer.encode_categorical_data()
# print(analyzer.correlation_matrix())
