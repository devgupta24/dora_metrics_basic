"""
ETL Pipeline module for DORA metrics
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple


class DORAMetricsPipeline:
    """ETL Pipeline for DORA metrics"""
    
    def __init__(self):
        """Initialize the pipeline"""
        self.raw_data = None
        self.processed_data = None
 
    def extract_raw_data(self) -> pd.DataFrame:
        """
        Extract raw data - simulates data extraction from source
        
        Returns:
            Raw dataframe with sample data
        """
        print("📥 Extracting raw data...")
        
        # Generate sample DORA metrics data
        dates = [datetime.now() - timedelta(days=i) for i in range(30)]
        
        data = {
            'metric_id': list(range(1, 31)),
            'metric_name': ['deployment_frequency'] * 10 + 
                          ['lead_time_for_changes'] * 10 + 
                          ['mean_time_to_recovery'] * 10,
            'value': np.random.uniform(1, 100, 30).round(2),
            'timestamp': dates,
            'team': np.random.choice(['team_a', 'team_b', 'team_c'], 30),
            'environment': np.random.choice(['production', 'staging'], 30)
        }
        
        self.raw_data = pd.DataFrame(data)
        print(f"✓ Extracted {len(self.raw_data)} rows of raw data\n")
        return self.raw_data
    
    def validate_data_quality(self) -> Tuple[int, int]:
        """
        Validate data quality - check for nulls and duplicates
        
        Returns:
            Tuple of (null_count, duplicate_count)
        """
        print("🔍 Validating data quality...")
        
        null_count = self.raw_data.isnull().sum().sum()
        duplicate_count = self.raw_data.duplicated().sum()
        
        print(f"✓ Null values: {null_count}")
        print(f"✓ Duplicate rows: {duplicate_count}\n")
        
        return null_count, duplicate_count
    
    def transform_data(self) -> pd.DataFrame:
        """
        Transform and clean the data
        
        Returns:
            Transformed dataframe
        """
        print("⚙️  Transforming data...")
        
        # Create a copy for transformation
        df = self.raw_data.copy()
        
        # Convert timestamp to datetime if not already
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Add derived columns
        df['date'] = df['timestamp'].dt.date
        df['week'] = df['timestamp'].dt.isocalendar().week
        df['month'] = df['timestamp'].dt.month
        
        # Normalize values to 0-100 scale
        df['normalized_value'] = ((df['value'] - df['value'].min()) / 
                                   (df['value'].max() - df['value'].min()) * 100).round(2)
        
        self.processed_data = df
        print(f"✓ Transformed data with {len(df.columns)} columns\n")
        
        return self.processed_data
    
    def aggregate_metrics(self) -> pd.DataFrame:
        """
        Aggregate metrics by team and metric name
        
        Returns:
            Aggregated dataframe
        """
        print("📊 Aggregating metrics...")
        
        aggregated = self.processed_data.groupby(
            ['metric_name', 'team']
        ).agg({
            'value': ['mean', 'min', 'max', 'std', 'count'],
            'timestamp': ['first', 'last']
        }).reset_index()
        
        aggregated.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                             for col in aggregated.columns.values]
        
        print(f"✓ Aggregated to {len(aggregated)} metric groups\n")
        
        return aggregated
    
    def run_pipeline(self) -> pd.DataFrame:
        """
        Run the complete ETL pipeline
        
        Returns:
            Final processed dataframe
        """
        print("\n" + "="*50)
        print("STARTING ETL PIPELINE")
        print("="*50 + "\n")
        
        # Extract
        self.extract_raw_data()
        
        # Validate
        self.validate_data_quality()
        
        # Transform
        self.transform_data()
        
        # Aggregate
        aggregated = self.aggregate_metrics()
        
        print("="*50)
        print("ETL PIPELINE COMPLETE")
        print("="*50 + "\n")
        
        return self.processed_data
    
    def get_processed_dataframe(self) -> pd.DataFrame:
        """
        Get the processed dataframe
        
        Returns:
            Processed dataframe
        """
        if self.processed_data is None:
            return self.run_pipeline()
        return self.processed_data
    
    def get_raw_dataframe(self) -> pd.DataFrame:
        """
        Get the raw dataframe
        
        Returns:
            Raw dataframe
        """
        if self.raw_data is None:
            self.extract_raw_data()
        return self.raw_data


def extract_dora_metrics() -> pd.DataFrame:
    """
    Main function to extract DORA metrics
    
    Returns:
        Processed DORA metrics dataframe
    """
    pipeline = DORAMetricsPipeline()
    return pipeline.run_pipeline()
