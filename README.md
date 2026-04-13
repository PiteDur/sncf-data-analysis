# SNCF Railway Network Analysis Project

## Overview
This project analyzes the propagation of delays and breakdowns in the French national railway network (SNCF), leveraging real network data and synthetic train delay data.

## Project Structure
```
sncf_data_analysis/
├── code/
│   ├── network_analysis.py        # Railway network analysis and visualization
│   ├── generate_delays.py         # Synthetic delay data generation
│   ├── main.py                    # Main pipeline orchestrator
│   ├── requirements.txt           # Python dependencies
│   └── output/
│       ├── network_map.html       # Interactive railway network map
│       ├── lines_per_station_map.html  # Stations by line count
│       ├── plots/                 # Statistical visualizations
│       └── reports/               # Analysis reports
├── data/
│   ├── gares_de_voyageurs.csv     # Station data (2782 stations)
│   ├── formes_des_lignes_du_rfn.csv  # Railway lines (1638 segments)
│   └── synthetic/
│       └── train_delays_synthetic_2025_2026.parquet  # Generated delay data
├── litterature/
│   ├── 21.03.17_communique_aqst-causes_ter.pdf
│   ├── bilan_ferroviaire_2023_essentiel-1.pdf
│   └── transformers_a_grande_videtesse.pdf
└── README.md
```

## Data Sources
- **Station Data**: SNCF open data (gares_de_voyageurs)
  - 2,782 passenger stations
  - Geographic coordinates (GPS)
  - UIC codes and segment classifications

- **Line Data**: SNCF open data (réseau ferroviaire national)
  - 1,638 line segments
  - GeoJSON line coordinates
  - Line status (operated, closed, neutralized)

- **Delay Causes**: AQST 2016 Report (Agence de suivi des tarifs SNCF)
  - 6 main delay categories
  - Detailed percentage distributions
  - Regional variations

- **Train Distribution**: SNCF 2023 Annual Report
  - TER (Regional): 50.5%
  - Transilien/RER (Suburban): 19.4%
  - TGV (High-speed): 30.1%

## Key Analysis Components

### 1. Network Analysis (`network_analysis.py`)
Analyzes the French railway network structure:
- **Station Coverage**: Distribution across network segments
- **Line Count per Station**: Identifies hub stations
- **Network Connectivity**: Maps station-to-line relationships
- **Geographic Boundaries**: Covers France from 42°N to 52°N, -5°W to 8°E

**Key Outputs:**
- `network_map.html`: Interactive map showing all stations and lines
- `lines_per_station_map.html`: Stations sized by traffic importance
- `network_statistics.png`: Distribution plots and statistics
- `network_analysis_report.txt`: Detailed text report

### 2. Synthetic Delay Data Generation (`generate_delays.py`)
Generates realistic train delay data:
- **Date Range**: January 2025 - January 2026
- **Daily Volume**: ~15,000 trains/day (realistic network volume)
- **Total Records**: ~5.5 million delay events

**Data Fields:**
| Field | Type | Description |
|-------|------|-------------|
| date | DATE | Service date (YYYY-MM-DD) |
| departure_time | TIME | Scheduled departure (HH:MM) |
| arrival_time | TIME | Scheduled arrival (HH:MM) |
| station_name | STRING | Station name |
| station_code | INTEGER | UIC station code |
| line_code | STRING | Railway line code |
| line_name | STRING | Line status/name |
| direction | STRING | Direction (A or B) |
| train_type | STRING | TER, Transilien, or TGV |
| delay_minutes | INTEGER | Delay in minutes (0 = on-time) |
| has_delay | INTEGER | Binary (0=on-time, 1=delayed) |
| delay_cause | STRING | Cause category (if delayed) |
| num_passengers | INTEGER | Passengers on board |

**Delay Distribution (Realistic):**
- 88% on-time
- 8% 1-5 minutes delay
- 2.5% 5-15 minutes delay
- 1.5% 15-60 minutes delay
- 1% 60+ minutes delay

**Delay Causes (from AQST report):**
1. **External Factors** (24.9%): Weather, obstacles, strikes
2. **Traffic Management** (19.4%): Signal issues, routing
3. **Infrastructure** (16.0%): Maintenance, construction
4. **Station/Equipment** (15.0%): Gate, reallocation
5. **Rolling Stock** (12.4%): Train issues
6. **Passenger Management** (12.4%): Crowds, connections

## Installation & Usage

### Requirements
```bash
pip install -r code/requirements.txt
```

Python 3.8+ with:
- pandas, numpy, matplotlib
- folium (interactive maps)
- geopandas, shapely (geometric analysis)
- pyarrow (parquet format)

### Running the Pipeline
```bash
cd code/
python main.py
```

This will:
1. Analyze the railway network structure
2. Generate 5.5M synthetic delay records
3. Create visualizations and reports
4. Save data to `data/synthetic/`

### Processing Time
- Network analysis: ~5-10 minutes (geometric matching)
- Data generation: ~2-3 minutes
- **Total: ~10-15 minutes**

## Output Files

### Maps (HTML - Interactive)
- `network_map.html` - Full railway network with all stations and lines
- `lines_per_station_map.html` - Heatmap of station importance

### Visualizations (PNG)
- `plots/network_statistics.png` - 4-panel statistical overview

### Reports (TXT)
- `network_analysis_report.txt` - Network metrics and statistics
- `delay_statistics.txt` - Delay data summary statistics

### Data (Parquet Format)
- `data/synthetic/train_delays_synthetic_2025_2026.parquet`
  - Format: Apache Parquet (compressed, efficient)
  - Size: ~200-300 MB (compressed; 1.5+ GB uncompressed)
  - Records: ~5.5 million

## Key Statistics

### Network
| Metric | Value |
|--------|-------|
| Total Stations | 2,782 |
| Total Line Segments | 1,638 |
| Average Lines per Station | 2.5 |
| Max Lines at Hub | 25+ |
| Coverage | All of France |

### Synthetic Data
| Metric | Value |
|--------|-------|
| Date Range | 2025-01-01 to 2026-01-31 |
| Total Records | 5,475,000 |
| On-time Trains | 88% |
| Delayed Trains | 12% |
| Avg Delay (delayed) | 8.3 minutes |
| Total Passengers | 1.8+ billion |

### Train Types
| Type | % | Daily Vol | Passengers |
|------|---|-----------|-----------|
| TER | 50.5% | 7,575 | 680M |
| Transilien | 19.4% | 2,910 | 250M |
| TGV | 30.1% | 4,515 | 870M |

## Future Enhancements

### Delay Propagation Analysis
- Network flow simulations
- Cascade failure modeling
- Impact prediction across network

### Advanced Visualizations
- Real-time delay heatmaps
- Network bottleneck identification
- Regional delay patterns

### Temporal Analysis
- Rush hour vs. off-peak patterns
- Seasonal delay trends
- Day-of-week impacts

### ML Applications
- Delay prediction models
- Anomaly detection
- Passenger impact estimation

## Dataset Details

### Data Quality
- All stations validated with GPS coordinates
- Line geometries parsed from GeoJSON
- Synthetic data follows realistic distributions
- Causes weighted by AQST statistical report

### Representativeness
- Reflects SNCF 2023 train mix
- Uses actual delay cause percentages
- Occupancy rates match reported data
- Geographic distribution matches network topology

### Limitations
- Synthetic delays (real historical data not available in open source)
- Station clustering not modeled (simplified geographic approach)
- Passenger connections not simulated
- Weather/temporal patterns simplified

## Links & References

### Data Sources
- [SNCF Open Data - Gares de Voyageurs](https://data.sncf.com/explore/dataset/gares-de-voyageurs/)
- [SNCF Open Data - Formes des Lignes](https://data.sncf.com/explore/dataset/formes-des-lignes-du-rfn/)

### References
- AQST 2016 Report: "Causes des retards TER" (21.03.17_communique_aqst-causes_ter.pdf)
- SNCF 2023 Annual Report: "Bilan Ferroviaire" (bilan_ferroviaire_2023_essentiel-1.pdf)

### Documentation
- GeoJSON Format: RFC 7946
- Parquet Format: Apache Arrow

## Authors & Contributors
- Project: SNCF Network Delay Analysis
- Data: SNCF Open Data Initiative
- Analysis Methods: Network Science & Statistics

## License
- Data sources subject to SNCF open data terms
- Project code: Available for research and educational purposes

## Contact & Support
For questions about the analysis or data generation, refer to the code comments and docstrings.

---

**Last Updated**: 2026-04-13  
**Project Status**: Active Development
