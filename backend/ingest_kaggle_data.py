import os
import glob
import subprocess
import pandas as pd
import sqlite3

def download_and_convert():
    print("Downloading IBM HR Analytics dataset from Kaggle...")
    
    # 1. Download dataset using kaggle CLI
    # The KAGGLE_API_TOKEN environment variable MUST be set
    if not os.environ.get("KAGGLE_API_TOKEN"):
        raise ValueError("KAGGLE_API_TOKEN environment variable is not set!")
        
    subprocess.run([
        "kaggle", "datasets", "download", "-d", 
        "pavansubhasht/ibm-hr-analytics-attrition-dataset", "--unzip"
    ], check=True)
    
    # 2. Find the downloaded CSV
    csv_files = glob.glob("*.csv")
    if not csv_files:
        raise FileNotFoundError("No CSV file found after unzipping the Kaggle dataset.")
        
    csv_file = csv_files[0]
    print(f"Found CSV file: {csv_file}")
    
    # 3. Read into pandas DataFrame
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} rows from CSV.")
    
    # 4. Save to SQLite database
    db_path = "/opt/ragapp/config/ibm_hr.db"
    conn = sqlite3.connect(db_path)
    
    # Save the dataframe to a table named 'employees'
    df.to_sql("employees", conn, if_exists="replace", index=False)
    conn.close()
    
    print(f"Successfully converted dataset and saved to {db_path}!")
    
    # Cleanup downloaded csv
    os.remove(csv_file)

if __name__ == "__main__":
    download_and_convert()
