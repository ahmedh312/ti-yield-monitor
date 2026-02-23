import sqlite3
import random
import time
import os
import datetime

def simulate_wafer_scan():
    db_path = os.path.join(os.path.dirname(__file__), "ti_factory_data.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure table has the correct columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manufacturing_yield (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yield_status TEXT NOT NULL,
            temp_c REAL,
            pressure_psi REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    print(f"Live Simulation Started | Correlation Mode Active")
    
    try:
        while True:
            # 1. Generate Realistic Sensor Data
            # Normal range is 195-205, but we let it drift higher occasionally
            temp = round(random.uniform(195.0, 210.0), 2)
            pressure = round(random.uniform(28.0, 32.0), 2)
            
            # 2. Logic: If temp > 208, the wafer fails quality control
            if temp > 208.0:
                status = "FAIL"
            else:
                # Otherwise, 95% pass rate
                status = "PASS" if random.random() < 0.95 else "FAIL"

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")

            # 3. Insert all data 
            cursor.execute("""
                INSERT INTO manufacturing_yield (yield_status, temp_c, pressure_psi, timestamp) 
                VALUES (?, ?, ?, ?)
            """, (status, temp, pressure, timestamp))
            
            conn.commit()

            cursor.execute("SELECT COUNT(*) FROM manufacturing_yield")
            total_count = cursor.fetchone()[0]
            
            print(f" Scanned: {status} | Temp: {temp}°C | Time: {timestamp} | Total Wafers: {total_count}")
            time.sleep(1) # Faster updates for a better demo
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped.")
    finally:
        conn.close()

if __name__ == "__main__":
    simulate_wafer_scan()