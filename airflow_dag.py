"""
Airflow DAG for DORA metrics ETL and validation
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import logging

from etl_pipeline import DORAMetricsPipeline
from validation import validate_dora_metrics, DataValidator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default arguments for the DAG
default_args = {
    'owner': 'data-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),
}

# Define the DAG
dag = DAG(
    'dora_metrics_pipeline',
    default_args=default_args,
    description='ETL and Validation pipeline for DORA metrics',
    schedule_interval='@daily',
    catchup=False,
)

# Global variable to store dataframe between tasks
context_data = {}


def extract_task(**context):
    """Extract task - run ETL pipeline"""
    logger.info("🚀 Starting Extract Task")
    
    pipeline = DORAMetricsPipeline()
    raw_df = pipeline.extract_raw_data()
    
    # Store in context for next task
    context_data['raw_df'] = raw_df
    
    logger.info(f"✓ Extraction complete. Rows: {len(raw_df)}")
    return len(raw_df)


def transform_task(**context):
    """Transform task - transform and clean data"""
    logger.info("🔄 Starting Transform Task")
    
    pipeline = DORAMetricsPipeline()
    
    # Use the raw data from previous task if available
    if 'raw_df' in context_data:
        pipeline.raw_data = context_data['raw_df']
    else:
        pipeline.extract_raw_data()
    
    # Validate data quality
    null_count, duplicate_count = pipeline.validate_data_quality()
    
    # Transform data
    processed_df = pipeline.transform_data()
    
    # Store for validation task
    context_data['processed_df'] = processed_df
    
    logger.info(f"✓ Transform complete. Nulls: {null_count}, Duplicates: {duplicate_count}")
    return {
        'rows_processed': len(processed_df),
        'null_count': null_count,
        'duplicate_count': duplicate_count
    }


def validation_task(**context):
    """Validation task - run all validation checks"""
    logger.info("✅ Starting Validation Task")
    
    if 'processed_df' not in context_data:
        raise ValueError("No processed dataframe available for validation")
    
    processed_df = context_data['processed_df']
    
    # Run validation
    all_passed, validator = validate_dora_metrics(processed_df)
    
    # Log validation results
    logger.info(f"Validation Results: {validator.validation_results}")
    
    if not all_passed:
        logger.warning("⚠️  Some validation checks failed!")
        raise ValueError("Data validation failed - see logs for details")
    
    logger.info("✓ All validations passed!")
    
    return {
        'validation_passed': all_passed,
        'validation_results': validator.validation_results
    }


def aggregate_task(**context):
    """Aggregate task - create summary metrics"""
    logger.info("📊 Starting Aggregation Task")
    
    if 'processed_df' not in context_data:
        raise ValueError("No processed dataframe available for aggregation")
    
    pipeline = DORAMetricsPipeline()
    pipeline.processed_data = context_data['processed_df']
    
    aggregated = pipeline.aggregate_metrics()
    
    logger.info(f"✓ Aggregation complete. Summary groups: {len(aggregated)}")
    
    return len(aggregated)


def summary_task(**context):
    """Summary task - print final summary"""
    logger.info("\n" + "="*60)
    logger.info("DORA METRICS PIPELINE EXECUTION SUMMARY")
    logger.info("="*60)
    
    if 'processed_df' in context_data:
        df = context_data['processed_df']
        logger.info(f"✓ Total rows processed: {len(df)}")
        logger.info(f"✓ Metrics collected: {df['metric_name'].nunique()}")
        logger.info(f"✓ Teams tracked: {df['team'].nunique()}")
        logger.info(f"✓ Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        logger.info(f"✓ Value range: {df['value'].min():.2f} to {df['value'].max():.2f}")
    
    logger.info("="*60)
    logger.info("✓ PIPELINE EXECUTION COMPLETE")
    logger.info("="*60 + "\n")


# Define tasks
extract = PythonOperator(
    task_id='extract_metrics',
    python_callable=extract_task,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform_metrics',
    python_callable=transform_task,
    dag=dag,
)

validate = PythonOperator(
    task_id='validate_metrics',
    python_callable=validation_task,
    dag=dag,
)

aggregate = PythonOperator(
    task_id='aggregate_metrics',
    python_callable=aggregate_task,
    dag=dag,
)

summary = PythonOperator(
    task_id='pipeline_summary',
    python_callable=summary_task,
    dag=dag,
)

# Define task dependencies
extract >> transform >> validate >> aggregate >> summary
