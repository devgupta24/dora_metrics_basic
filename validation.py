"""
Data validation module for DORA metrics pipeline
"""
import pandas as pd
from typing import Dict, List, Tuple


class DataValidator:
    """Validator class for data quality checks"""
    
    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize validator with a dataframe
        
        Args:
            dataframe: pandas DataFrame to validate
        """
        self.df = dataframe
        self.validation_results = {}
    
    def check_null_values(self) -> Dict[str, int]:
        """
        Check for null values in each column
        
        Returns:
            Dictionary with column names and null counts
        """
        result = self.df.isnull().sum().to_dict()
        self.validation_results['null_check'] = result
        print(f"✓ Null values check: {result}")
        print("Stability Improvement Release")
        return result
    
    def check_duplicate_rows(self) -> int:
        """
        Check for duplicate rows
        
        Returns:
            Count of duplicate rows
        """
        duplicates = self.df.duplicated().sum()
        self.validation_results['duplicate_check'] = duplicates
        print(f"✓ Duplicate rows check: {duplicates} duplicates found")
        return duplicates
    
    def check_schema(self, required_columns: List[str]) -> Tuple[bool, List[str]]:
        """
        Check if dataframe has required columns
        
        Args:
            required_columns: List of required column names
            
        Returns:
            Tuple of (is_valid, missing_columns)
        """
        missing = [col for col in required_columns if col not in self.df.columns]
        is_valid = len(missing) == 0
        self.validation_results['schema_check'] = {
            'valid': is_valid,
            'missing_columns': missing
        }
        print(f"✓ Schema check: {'PASSED' if is_valid else 'FAILED'}")
        if missing:
            print(f"  Missing columns: {missing}")
        return is_valid, missing
    
    def check_data_types(self, expected_types: Dict[str, str]) -> Dict[str, str]:
        """
        Check if columns have expected data types
        
        Args:
            expected_types: Dictionary with column names and expected types
            
        Returns:
            Dictionary with validation results
        """
        result = {}
        for col, expected_type in expected_types.items():
            if col in self.df.columns:
                actual_type = str(self.df[col].dtype)
                is_match = expected_type in actual_type
                result[col] = {
                    'expected': expected_type,
                    'actual': actual_type,
                    'match': is_match
                }
        self.validation_results['type_check'] = result
        print(f"✓ Data types check completed")
        return result
    
    def check_value_ranges(self, column: str, min_val=None, max_val=None) -> Dict:
        """
        Check if numerical column values are within expected range
        
        Args:
            column: Column name to check
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
            
        Returns:
            Dictionary with range validation results
        """
        if column not in self.df.columns:
            return {'error': f'Column {column} not found'}
        
        result = {
            'column': column,
            'min_value': self.df[column].min(),
            'max_value': self.df[column].max(),
            'within_range': True
        }
        
        if min_val is not None and (self.df[column] < min_val).any():
            result['within_range'] = False
        if max_val is not None and (self.df[column] > max_val).any():
            result['within_range'] = False
        
        self.validation_results[f'range_check_{column}'] = result
        print(f"✓ Range check for {column}: {result['within_range']}")
        return result
    
    def run_all_validations(self, required_columns: List[str] = None, 
                           expected_types: Dict[str, str] = None) -> Dict:
        """
        Run all validation checks
        
        Args:
            required_columns: List of required columns
            expected_types: Dictionary of expected data types
            
        Returns:
            Dictionary with all validation results
        """
        print("\n" + "="*50)
        print("RUNNING VALIDATION CHECKS")
        print("="*50)
        
        
        self.check_null_values()
        self.check_duplicate_rows()
        
        if required_columns:
            self.check_schema(required_columns)
        
        if expected_types:
            self.check_data_types(expected_types)
        
        print("\n" + "="*50)
        print("VALIDATION COMPLETE")
        print("="*50 + "\n")
        
        return self.validation_results


def validate_dora_metrics(dataframe: pd.DataFrame) -> bool:
    """
    Validate DORA metrics dataframe
    
    Args:
        dataframe: The metrics dataframe to validate
        
    Returns:
        Boolean indicating if all validations passed
    """
    required_cols = ['metric_id', 'metric_name', 'value', 'timestamp']
    expected_types = {
        'metric_id': 'int',
        'value': 'float',
        'timestamp': 'datetime'
    }
    
    validator = DataValidator(dataframe)
    validator.run_all_validations(required_cols, expected_types)
    
    # Check if all validations passed
    has_nulls = any(validator.validation_results.get('null_check', {}).values())
    has_duplicates = validator.validation_results.get('duplicate_check', 0) > 0
    schema_valid = validator.validation_results.get('schema_check', {}).get('valid', False)
    
    all_passed = not (has_nulls or has_duplicates) and schema_valid
    
    return all_passed, validator
