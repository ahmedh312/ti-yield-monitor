from tokenize import group

from flask import Flask, jsonify
from flask import send_file
from flask_cors import CORS
from io import BytesIO
import sqlite3
import pandas as pd
import os
import datetime

app = Flask(__name__)
CORS(app) # allows your React app to talk to this API

def get_yield_data():
    import os
    db_path = os.path.join(os.path.dirname(__file__), "ti_factory_data.db")
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT yield_status, COUNT(*) as count FROM manufacturing_yield GROUP BY yield_status", conn)
    conn.close()
    
    # Convert dataframe to a simple dictionary for JSON
    data = dict(zip(df['yield_status'], df['count']))
    return data

@app.route('/api/yield', methods=['GET'])
def yield_api():
    stats = get_yield_data()
    return jsonify(stats)

@app.route('/api/reset', methods=['POST'])
def reset_data():
    try:
        db_path = os.path.join(os.path.dirname(__file__), "ti_factory_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM manufacturing_yield")
        conn.commit()
        conn.close()
        return jsonify({"message": "Database reset successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_trend_data():
    db_path = os.path.join(os.path.dirname(__file__), "ti_factory_data.db")
    conn = sqlite3.connect(db_path)
    # query pulls the last 50 scans to calculate a moving trend
    df = pd.read_sql_query("SELECT yield_status FROM manufacturing_yield ORDER BY id DESC LIMIT 50", conn)
    conn.close()
    
    if df.empty:
        return []

    # Calculate yield in "windows" of 10 to create line points
    trend = []
    for i in range(0, len(df), 5):
        window = df.iloc[i:i+10]
        passes = len(window[window['yield_status'] == 'PASS'])
        yield_pct = (passes / len(window)) * 100 if len(window) > 0 else 0
        if 'temp_c' in group.columns:
            avg_temp = group['temp_c'].mean()
        else:
            avg_temp = 200.0 # Default fallback if column is missing

            time_label = str(group.iloc[-1]['timestamp'])
        trend.append({"time": f"-{i}s", "yield": round(yield_pct, 1), "temp": round(float(avg_temp), 1)})

    
    return trend[::-1] # Reverse to show oldest to newest

@app.route('/api/stats', methods=['GET'])
def get_all_stats():
    try:
        conn = sqlite3.connect("ti_factory_data.db")
        
        # 1. Get Counts for the Pie Chart
        df_counts = pd.read_sql_query(
            "SELECT yield_status, COUNT(*) as count FROM manufacturing_yield GROUP BY yield_status", 
            conn
        )
        counts = dict(zip(df_counts['yield_status'], df_counts['count']))
        
        # 2. Get data for Trend
        # Note: Added a fallback for 'timestamp' in case column naming is slightly off
        df = pd.read_sql_query(
            "SELECT yield_status, timestamp FROM manufacturing_yield ORDER BY id ASC", 
            conn
        )
        conn.close()
        
        # 3. Process Trend (Keep last 100 rows)
        df = df.tail(100)
        trend_data = []
        
        if not df.empty:
            # group by 10, but use len(group) for the math so it works for the "leftover" wafers
            for i in range(0, len(df), 10):
                group = df.iloc[i : i + 10]
                passes = len(group[group['yield_status'] == 'PASS'])
                yield_pct = (passes / len(group)) * 100
                
                # Get time from the last item in the group
                label_time = group.iloc[-1]['timestamp'] if 'timestamp' in group.columns else f"Pt {i}"
                
                trend_data.append({
                    "time": label_time, 
                    "yield": round(yield_pct, 1)
                })

        return jsonify({
            "counts": {
                "PASS": int(counts.get("PASS", 0)), 
                "FAIL": int(counts.get("FAIL", 0))
            },
            "trend": trend_data
        })

    except Exception as e:
        print(f"Error in get_all_stats: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/export', methods=['GET'])
def export_report():
    try:
        conn = sqlite3.connect("ti_factory_data.db")
        df = pd.read_sql_query("SELECT * FROM manufacturing_yield", conn)
        conn.close()

        # 1. Create the CSV string
        csv_data = df.to_csv(index=False)
        
        # 2. Convert string to BYTES
        byte_output = BytesIO()
        byte_output.write(csv_data.encode('utf-8'))
        byte_output.seek(0)
        
        return send_file(
            byte_output,
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"TI_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        )
    except Exception as e:
        print(f"Export Error: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
