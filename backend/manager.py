import pandas as pd
import sqlite3
import random
import os
from datetime import datetime

DB_NAME = "ti_factory_data.db"

def initialize_factory(num_records=500):
    """ETL: Wipes the old DB and loads 500 fresh records."""
    print(f"🛠️ Initializing factory with {num_records} wafers...")
    data = []
    for i in range(num_records):
        temp = random.uniform(195.0, 210.0) # Matching simulator ranges
        pressure = random.uniform(28.0, 32.0)
        
        # Logic: FAIL if temp > 208
        status = "FAIL" if temp > 208 else ("PASS" if random.random() < 0.95 else "FAIL")
        
        data.append({
            "temp_c": round(temp, 2),
            "pressure_psi": round(pressure, 2),
            "yield_status": status,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    df = pd.DataFrame(data)
    conn = sqlite3.connect(DB_NAME)
    
    # use index=True and index_label='id' to create the ID column 
    # that the Simulator and Backend expect.
    df.to_sql('manufacturing_yield', conn, if_exists='replace', index=True, index_label='id')
    conn.close()
    print("✅ Factory initialized.")

def run_audit():
    """Audit: Quickly checks current yield stats from the CLI."""
    if not os.path.exists(DB_NAME):
        print("❌ Database not found. Run initialize first.")
        return

    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM manufacturing_yield", conn)
    conn.close()

    if df.empty:
        print("⚠️ Database is empty.")
    else:
        total = len(df)
        passes = len(df[df['yield_status'] == 'PASS'])
        yield_rate = (passes / total) * 100
        print(f"\n--- TI FACTORY AUDIT REPORT ---")
        print(f"Total Wafers Scanned: {total}")
        print(f"Current Global Yield: {yield_rate:.2f}%")
        # Updated to show 'id' instead of 'wafer_id'
        print(f"Last 5 Scans:\n{df.tail(5)[['id', 'yield_status', 'temp_c', 'timestamp']]}\n")

if __name__ == "__main__":
    print("1. Initialize/Reset Factory (Bulk Load)")
    print("2. Run Audit Report")
    choice = input("Enter choice (1/2): ")
    
    if choice == "1":
        initialize_factory()
    elif choice == "2":
        run_audit()
