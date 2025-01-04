import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_visualizations(data_path, output_folder):
    df = pd.read_csv(data_path)
    
    # Heatmap
    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    heatmap_path = os.path.join(output_folder, 'heatmap.png')
    plt.savefig(heatmap_path)
    plt.close()
