# ti-yield-monitor

<img width="1680" height="919" alt="image" src="https://github.com/user-attachments/assets/3c20042a-19ec-451a-ad79-9ddca444814e" />

Project Overview:
This project is a full-stack Industrial IoT (IIoT) simulation designed to monitor semiconductor wafer production. 
It tracks manufacturing "Pass/Fail" rates in real-time, providing process engineers with a live dashboard to detect production excursions (drops in yield) immediately.

SemiconductorProject/
├── backend/
│   ├── app.py              # Flask API
│   └── ti_factory_data.db  # SQLite Database
├── scripts/
│   ├── simulator.py        # Live Wafer Simulation
│   └── factory_manager.py  # Audit & Initialization Tool
├── frontend/
│   ├── src/
│   │   └── App.jsx         # React Dashboard
│   └── package.json
└── README.md               # Project Documentation

_________________________________________________________________________________________________________________________________________


How to Run:
1. Install dependencies: `pip install -r requirements.txt`
2. Start the simulator: `python simulator.py`
3. Start the backend: `python app.py`
4. Start the frontend: `npm run dev`

_________________________________________________________________________________________________________________________________________

Key Capabilities:
Real-Time Data Streaming: A Python-based factory simulator generates wafer-level data.

Automated Audit Reporting: A management CLI tool for bulk data initialization and system auditing.

Dynamic Visualization: A React dashboard featuring a yield trend and distribution analysis.

Root Cause Analysis: Designed to correlate process variables (simulated) with output quality.

_________________________________________________________________________________________________________________________________________


Tech Stack
Frontend: React.js, Recharts (Data Visualization), CSS3

Backend: Flask (Python), REST API

Database: SQLite3 (Relational Data Storage)

Data Science: Pandas (Rolling window calculations & ETL)

_________________________________________________________________________________________________________________________________________

System Architecture
Simulator (simulator.py): Models the factory floor, inserting wafer results into the DB every second.

Factory Manager (factory_manager.py): An administrative tool used for bulk loading historical data and generating audit reports.

Backend API (app.py): Processes raw SQL data into 10-wafer rolling averages for smooth visualization.

Frontend Dashboard (App.jsx): Polls the API every 2 seconds to update the UI without page refreshes.

_________________________________________________________________________________________________________________________________________

Business Logic: The Rolling Yield
To mimic a real TI production environment, the system calculates yield using a Rolling Window. Instead of showing a static average, 
the dashboard calculates the pass rate of the last 10 wafers at every point in time. This ensures that a sudden equipment failure is 
visible on the graph within seconds, rather than being buried in historical averages.

_________________________________________________________________________________________________________________________________________

Future Enhancements
Sensor Integration: Adding live Pressure/Temperature sensor correlation charts.

Predictive Maintenance: Using Machine Learning to predict failures before they occur based on sensor drift.

Alerting System: Integration with Twilio/Email to alert engineers when yield drops below 85%.
