import subprocess
import sys
import time

def run_step(step_name, command):
    print(f"\n==========================================================")
    print(f"--> [RUNNING] {step_name}")
    print(f"--> Command: {command}")
    print(f"==========================================================")
    
    start_time = time.time()
    result = subprocess.run(command, shell=True)
    duration = time.time() - start_time

    if result.returncode != 0:
        print(f"\n[ERROR] {step_name} failed with exit code {result.returncode}!")
        sys.exit(result.returncode)
    
    print(f"[SUCCESS] {step_name} completed in {duration:.2f} seconds.")

def main():
    print("==========================================================")
    print("  RETAIL LAKEHOUSE PIPELINE: 10.5M+ ROW RUNNER (DOCKER) ")
    print("==========================================================")

    # Step 1: Ingestion
    run_step("1/5: Ingesting 10.5M+ Rows into Bronze Parquet Lake", "python generate_dirty_data.py")

    # Step 2: Audit
    run_step("2/5: Profiling Raw Data Lake (Data Audit)", "python audit_lakehouse.py")

    # Step 3: dbt Transformations
    run_step("3/5: Executing dbt Staging & Mart Models", "dbt run --profiles-dir .")

    # Step 4: dbt Data Quality Assertions
    run_step("4/5: Executing dbt Quality Contract Tests", "dbt test --profiles-dir .")

    # Step 5: Analytics Insights
    run_step("5/5: Generating Executive Financial Analytics", "python analytics_insights.py")

    print("\n==========================================================")
    print("    PIPELINE RUN COMPLETED SUCCESSFULLY  ")
    print("==========================================================")

if __name__ == "__main__":
    main()