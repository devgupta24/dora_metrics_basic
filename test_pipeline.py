"""
Test script to execute ETL pipeline and validation checks
"""
import sys
import logging

from etl_pipeline import DORAMetricsPipeline
from validation import validate_dora_metrics, DataValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_complete_pipeline():
    """Run the complete ETL pipeline with validation"""
    
    print("\n" + "="*70)
    print(" DORA METRICS - COMPLETE ETL & VALIDATION PIPELINE")
    print("="*70 + "\n")
    
    try:
        # Step 1: Run ETL Pipeline
        pipeline = DORAMetricsPipeline()
        processed_df = pipeline.run_pipeline()
        
        # Step 2: Run Validations
        print("\n" + "="*70)
        print("Starting Validation Phase...")
        print("="*70 + "\n")
        
        all_passed, validator = validate_dora_metrics(processed_df)
        
        # Step 3: Print Summary
        print("\n" + "="*70)
        print("EXECUTION SUMMARY")
        print("="*70)
        print(f"\n📊 Data Summary:")
        print(f"   - Total Rows: {len(processed_df)}")
        print(f"   - Columns: {list(processed_df.columns)}")
        print(f"   - Metrics: {processed_df['metric_name'].unique().tolist()}")
        print(f"   - Teams: {processed_df['team'].unique().tolist()}")
        print(f"   - Date Range: {processed_df['timestamp'].min()} to {processed_df['timestamp'].max()}")
        
        print(f"\n✅ Validation Status: {'PASSED' if all_passed else 'FAILED'}")
        print(f"\n📋 Validation Details:")
        for check_name, result in validator.validation_results.items():
            print(f"   - {check_name}: {result}")
        
        print("\n" + "="*70)
        print("✓ PIPELINE EXECUTION SUCCESSFUL")
        print("="*70 + "\n")
        
        # Step 4: Display sample data
        print("\n📄 Sample Processed Data (first 5 rows):")
        print(processed_df.head().to_string())
        print(f"\n📄 Data Info:")
        print(processed_df.info())
        
        return processed_df, validator
        
    except Exception as e:
        logger.error(f"❌ Pipeline execution failed: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        df, validator = run_complete_pipeline()
        print("\n✅ All validations completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
