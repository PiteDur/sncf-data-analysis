#!/usr/bin/env python3
"""
Quick Start Guide - SNCF Railway Network Analysis
"""

import os
import sys

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║         SNCF RAILWAY NETWORK DELAY ANALYSIS - QUICK START                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROJECT OVERVIEW
────────────────────────────────────────────────────────────────────────────────
This project analyzes delay propagation in the French railway network using:
  • Real network topology (2,782 stations × 1,638 line segments)  
  • Realistic synthetic delay data (5.5M+ records for 2025-2026)
  • SNCF train distributions and actual delay causes

DIRECTORY STRUCTURE
────────────────────────────────────────────────────────────────────────────────
sncf_data_analysis/
├── code/                           # Python scripts
│   ├── network_analysis.py        # Advanced network analysis
│   ├── network_analysis_fast.py   # Optimized version
│   ├── generate_delays.py          # Synthetic data generator
│   ├── main_fast.py               # Main pipeline (recommended)
│   ├── requirements.txt            # Dependencies
│   └── plots/                      # Generated visualizations
│
├── data/
│   ├── gares_de_voyageurs.csv     # Station list (SNCF)
│   ├── formes_des_lignes_du_rfn.csv  # Line data (SNCF)
│   └── synthetic/                 # Generated data
│       └── train_delays_synthetic_2025_2026.parquet
│
├── litterature/                    # Reference documents
│   ├── 21.03.17_communique_aqst-causes_ter.pdf
│   ├── bilan_ferroviaire_2023_essentiel-1.pdf
│   └── transformers_a_grande_videtesse.pdf
│
├── README.md                       # Full project documentation
├── DATA_DICTIONARY.md              # Field descriptions
└── QUICK_START.md                  # This file

INSTALLATION
────────────────────────────────────────────────────────────────────────────────

1. INSTALL DEPENDENCIES
   cd code/
   pip install -r requirements.txt

2. VERIFY INSTALLATION
   python -c "import pandas, numpy, matplotlib, folium, geopandas; print('✓ OK')"

RUNNING THE PIPELINE
────────────────────────────────────────────────────────────────────────────────

OPTION A: FAST PIPELINE (Recommended) - ~3-5 minutes
python main_fast.py

OPTION B: ADVANCED PIPELINE - ~10+ minutes (more detailed analysis)
python main.py

OUTPUT FILES
────────────────────────────────────────────────────────────────────────────────

After running, you'll get:

NETWORKS & MAPS (HTML - Open in browser)
  ✓ network_map.html              - Full railway network visualization
  ✓ lines_per_station_map.html    - Station importance heatmap

VISUALIZATIONS (PNG)
  ✓ plots/network_statistics.png  - 4-panel distribution analysis

REPORTS (TXT)
  ✓ network_analysis_report.txt   - Network metrics & statistics
  ✓ delay_statistics.txt          - Synthetic delay summary

DATA (Parquet Format - Binary, efficient)
  ✓ ../data/synthetic/train_delays_synthetic_2025_2026.parquet (~200-300 MB)
    - Read with: pd.read_parquet('path/file.parquet')

QUICK ANALYSIS EXAMPLES
────────────────────────────────────────────────────────────────────────────────

# Load stations and explore
import pandas as pd

df_stations = pd.read_csv('../data/gares_de_voyageurs.csv', sep=';')
print(f"Total stations: {len(df_stations)}")
print("Top 5 hub stations:")
print(df_stations.nlargest(5, 'num_lines')[['Nom_Gare', 'num_lines']])

# Load synthetic delay data
df_delays = pd.read_parquet('../data/synthetic/train_delays_synthetic_2025_2026.parquet')
print(f"Total records: {len(df_delays):,}")
print(f"On-time: {(1-df_delays['has_delay']).mean()*100:.1f}%")
print(f"Delayed: {df_delays['has_delay'].mean()*100:.1f}%")
print(f"Avg delay (when delayed): {df_delays[df_delays['has_delay']==1]['delay_minutes'].mean():.1f} min")

# Analyze by cause
print("\\nTop delay causes:")
print(df_delays[df_delays['has_delay']==1]['delay_cause'].value_counts().head(10))

# Temporal analysis
df_delays['date'] = pd.to_datetime(df_delays['date'])
daily = df_delays.groupby('date').agg({
    'has_delay': 'sum',
    'delay_minutes': 'mean',
    'num_passengers': 'sum'
})
print(f"\\nAverage delays per day: {daily['has_delay'].mean():.0f}")

# Train type analysis
print("\\nTrain distribution:")
print(df_delays['train_type'].value_counts(normalize=True))

KEY STATISTICS
────────────────────────────────────────────────────────────────────────────────

NETWORK
  • Total Stations: 2,782
  • Total Lines: 1,638 segments
  • Average Lines/Station: 3.6
  • Biggest Hub: 25+ lines
  • Coverage: Entire France

DELAYS (Synthetic Data)
  • Date Range: Jan 2025 - Jan 2026 (14 months)
  • Daily Volume: ~15,000 trains
  • Total Records: 5,940,000
  • On-time Rate: 88%
  • Delay Rate: 12%
  • Average Delay: 8.3 minutes (when delayed)
  • Max Delay: 180 minutes (3 hours)
  • Total Passengers: 1.8+ billion

TRAIN TYPES
  • TER (Regional): 50.5%
  • Transilien (Suburban): 19.4%
  • TGV (High-Speed): 30.1%

TOP DELAY CAUSES
  1. Traffic Management: 19.4%
  2. Infrastructure: 16.0%
  3. Station Mgmt: 15.0%
  4. Weather: 10.0%
  5. Rolling Stock: 12.4%

COMMON ISSUES & SOLUTIONS
────────────────────────────────────────────────────────────────────────────────

"ModuleNotFoundError: No module named 'XXX'"
  → Solution: pip install -r requirements.txt

"File not found: ../data/..."
  → Solution: Make sure you're in the code/ directory when running python

"ValueError: probabilities do not sum to 1"
  → This should be fixed. If you see it, the distributions need rebalancing.

"MemoryError when loading parquet"
  → Solution: Use df = pd.read_parquet(file, engine='pyarrow', 
              columns=['col1', 'col2'])  # Read only needed columns

NEXT STEPS
────────────────────────────────────────────────────────────────────────────────

1. EXPLORE THE RESULTS
   - Open the HTML maps in a web browser
   - Read the TXT reports for statistics
   - View the PNG plots

2. ANALYZE THE DATA
   - Use the examples above to explore delay patterns
   - Check delay_statistics.txt for summary tables
   - Modify analysis scripts to focus on specific lines/stations

3. EXTEND THE PROJECT
   - Add network flow simulations
   - Build delay prediction models
   - Create real-time monitoring dashboards
   - Implement cascade failure analysis

4. DOCUMENTATION
   - Read README.md for complete project information
   - Check DATA_DICTIONARY.md for all field definitions
   - Review PDF reports in litterature/ folder

PERFORMANCE NOTES
────────────────────────────────────────────────────────────────────────────────

Task                    Time        Memory      Note
─────────────────────   ─────────   ──────────  ────────────────────────────────
Load CSV data           < 1 sec     50 MB       Fast
Network analysis        2-3 min     200 MB      Geometric matching
Generate delays         2-3 min     500 MB      5.9M records
Create maps             < 1 min     150 MB      Folium rendering
Create plots            < 1 min     100 MB      Matplotlib
Save parquet            < 1 min     ~250 MB     Compressed output

Total runtime: ~5-7 minutes (fast pipeline)

SUPPORT & DOCUMENTATION
────────────────────────────────────────────────────────────────────────────────

For detailed information:
  • README.md              - Full project documentation
  • DATA_DICTIONARY.md     - All field definitions
  • code/XXX.py docstrings - Code documentation
  • litterature/*.pdf      - Reference documents

Questions about the data or analysis? Check the DATA_DICTIONARY.md file.

────────────────────────────────────────────────────────────────────────────────
Happy exploring! 🚄
""")
