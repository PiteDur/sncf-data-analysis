"""
SNCF Railway Network Delay Analysis - Data Dictionary
Complete documentation of all data fields and schema
"""

# =============================================================================
# NETWORK DATA
# =============================================================================

STATIONS_DATA_FIELDS = {
    'Nom_Gare': {
        'type': 'string',
        'description': 'Station name',
        'example': 'Paris-Gare-de-Lyon'
    },
    'Trigramme': {
        'type': 'string',
        'description': '3-letter station code',
        'example': 'PGL'
    },
    'Segment(s) DRG': {
        'type': 'string',
        'description': 'DRG Segment classification (A/B/C)',
        'values': ['A', 'B', 'C'],
        'note': 'A = International hub, B = Strategic, C = Regional'
    },
    'Position géographique': {
        'type': 'string (lat, lon)',
        'description': 'GPS coordinates',
        'format': 'latitude, longitude',
        'example': '48.843, 2.376'
    },
    'Code commune': {
        'type': 'integer',
        'description': 'INSEE municipality code',
        'example': 75056
    },
    'Code_UIC': {
        'type': 'integer',
        'description': 'International UIC station code',
        'note': 'Unique identifier for railway stations'
    },
    'Id_Gare': {
        'type': 'string (UUID)',
        'description': 'Unique station identifier',
        'format': 'UUID'
    },
    'lat': {
        'type': 'float',
        'description': 'Latitude (parsed from Position géographique)',
        'range': [42.0, 52.0]
    },
    'lon': {
        'type': 'float',
        'description': 'Longitude (parsed from Position géographique)',
        'range': [-5.0, 8.0]
    },
    'num_lines': {
        'type': 'integer',
        'description': 'Number of railway lines serving this station',
        'range': [0, 25],
        'note': 'Computed from line coordinates proximity'
    }
}

LINES_DATA_FIELDS = {
    'Geo Point': {
        'type': 'string (lat, lon)',
        'description': 'Central point of line segment',
        'format': 'latitude, longitude'
    },
    'Geo Shape': {
        'type': 'string (GeoJSON)',
        'description': 'Complete line geometry as GeoJSON LineString',
        'format': '{type: "LineString", coordinates: [[lon, lat], ...]}'
    },
    'CODE_LIGNE': {
        'type': 'string',
        'description': 'Railway line code',
        'example': '001000'
    },
    'LIBELLE': {
        'type': 'string',
        'description': 'Line status',
        'values': [
            'Exploitée',
            'Fermée',
            'Neutralisée',
            'Fermée non déposée (Plus utilisable)'
        ]
    },
    'MNEMO': {
        'type': 'string',
        'description': 'Line mnemonic',
        'example': 'EXPLOITE'
    },
    'mnemo_type': {
        'type': 'string',
        'description': 'Type indicator',
        'values': ['Ligne', 'Gare']
    },
    'PK_DEBUT_R': {
        'type': 'string',
        'description': 'Starting position in km',
        'format': 'XXX+YYY'
    },
    'PK_FIN_R': {
        'type': 'string',
        'description': 'Ending position in km',
        'format': 'XXX+YYY'
    },
    'RG_TRONCON': {
        'type': 'integer',
        'description': 'Section rank',
        'note': 'Order of sections on the line'
    },
    'coordinates': {
        'type': 'list of [lat, lon]',
        'description': 'Parsed coordinates from Geo Shape',
        'format': '[[lat1, lon1], [lat2, lon2], ...]'
    }
}

# =============================================================================
# SYNTHETIC DELAY DATA
# =============================================================================

SYNTHETIC_DELAY_FIELDS = {
    'date': {
        'type': 'date',
        'description': 'Service date',
        'format': 'YYYY-MM-DD',
        'range': '2025-01-01 to 2026-01-31'
    },
    'departure_time': {
        'type': 'time',
        'description': 'Scheduled departure time',
        'format': 'HH:MM',
        'range': '05:00 to 23:30',
        'note': 'Operating hours of SNCF network'
    },
    'arrival_time': {
        'type': 'time',
        'description': 'Scheduled arrival time',
        'format': 'HH:MM',
        'note': 'Departure + Journey duration (30 min to 4 hours)'
    },
    'station_name': {
        'type': 'string',
        'description': 'Name of affected station',
        'example': 'Paris-Gare-de-Lyon'
    },
    'station_code': {
        'type': 'integer',
        'description': 'UIC station code',
        'reference': 'Code_UIC from stations data'
    },
    'line_code': {
        'type': 'string',
        'description': 'Railway line code',
        'example': '001000',
        'reference': 'CODE_LIGNE from lines data'
    },
    'line_name': {
        'type': 'string',
        'description': 'Line status/name',
        'reference': 'LIBELLE from lines data'
    },
    'direction': {
        'type': 'string',
        'description': 'Train direction',
        'values': ['Direction A', 'Direction B'],
        'note': 'A and B represent opposite directions on line'
    },
    'train_type': {
        'type': 'string',
        'description': 'Type of train',
        'values': ['TER', 'Transilien', 'TGV'],
        'distribution': {
            'TER': 0.505,
            'Transilien': 0.194,
            'TGV': 0.301
        }
    },
    'delay_minutes': {
        'type': 'integer',
        'description': 'Delay in minutes',
        'range': [0, 180],
        'distribution': {
            'no_delay': 0.88,
            'minor (1-5 min)': 0.08,
            'low (5-15 min)': 0.025,
            'medium (15-60 min)': 0.015,
            'severe (60+ min)': 0.010
        }
    },
    'has_delay': {
        'type': 'integer (binary)',
        'description': 'Indicator for any delay',
        'values': [0, 1],
        'note': '0=on-time (delay_minutes=0), 1=delayed (delay_minutes>0)'
    },
    'delay_cause': {
        'type': 'string',
        'description': 'Reason for delay (if delayed)',
        'values': [
            'Aucun retard',
            'Météo (intempéries)',
            'Obstacles/intrusions',
            'Mouvements sociaux/grèves',
            'Gestion du trafic',
            'Infrastructure et travaux',
            'Gestion des gares',
            'Matériel roulant',
            'Affluence/correspondances',
            'Cause inconnue'
        ],
        'note': 'Weights based on AQST 2016 TER report'
    },
    'num_passengers': {
        'type': 'integer',
        'description': 'Number of passengers on board',
        'note': 'Calculated from occupancy rate × train capacity',
        'by_train_type': {
            'TER': {
                'capacity': 350,
                'occupancy_range': [0.15, 0.60],
                'occupancy_mean': 0.38
            },
            'Transilien': {
                'capacity': 800,
                'occupancy_range': [0.20, 0.65],
                'occupancy_mean': 0.35
            },
            'TGV': {
                'capacity': 900,
                'occupancy_range': [0.60, 0.90],
                'occupancy_mean': 0.77
            }
        }
    }
}

# =============================================================================
# STATISTICS AND DISTRIBUTIONS
# =============================================================================

DELAY_CAUSES_DISTRIBUTION = {
    'Météo (intempéries)': {
        'percentage': 9.96,
        'category': 'External Factors',
        'examples': ['Snow', 'Flooding', 'Wind damage']
    },
    'Obstacles/intrusions': {
        'percentage': 8.72,
        'category': 'External Factors',
        'examples': ['Objects on track', 'Trespassing', 'Animals']
    },
    'Mouvements sociaux/grèves': {
        'percentage': 6.18,
        'category': 'External Factors',
        'examples': ['Strikes', 'Labor actions']
    },
    'Gestion du trafic': {
        'percentage': 19.4,
        'category': 'Traffic Management',
        'examples': ['Signal issues', 'Routing problems', 'Congestion']
    },
    'Infrastructure et travaux': {
        'percentage': 16.0,
        'category': 'Infrastructure',
        'examples': ['Maintenance', 'Road works', 'Track issues']
    },
    'Gestion des gares': {
        'percentage': 15.0,
        'category': 'Station Management',
        'examples': ['Gate issues', 'Equipment reallocation']
    },
    'Matériel roulant': {
        'percentage': 12.4,
        'category': 'Rolling Stock',
        'examples': ['Train breakdown', 'Mechanical issues']
    },
    'Affluence/correspondances': {
        'percentage': 12.4,
        'category': 'Passenger Management',
        'examples': ['Crowding', 'Connection delays', 'Disabilities']
    }
}

TRAIN_TYPE_STATISTICS = {
    'TER': {
        'percentage_of_traffic': 50.5,
        'yearly_train_km': 195000000,
        'average_capacity': 350,
        'typical_occupancy': 0.38,
        'routes': 'Regional connections, shorter distances'
    },
    'Transilien': {
        'percentage_of_traffic': 19.4,
        'yearly_train_km': 75000000,
        'average_capacity': 800,
        'typical_occupancy': 0.35,
        'routes': 'Suburban/RER connections, commuter traffic'
    },
    'TGV': {
        'percentage_of_traffic': 30.1,
        'yearly_train_km': 116000000,
        'average_capacity': 900,
        'typical_occupancy': 0.77,
        'routes': 'High-speed intercity connections'
    }
}

# =============================================================================
# DATA GENERATION PARAMETERS
# =============================================================================

GENERATION_PARAMETERS = {
    'date_range': {
        'start': '2025-01-01',
        'end': '2026-01-31',
        'total_days': 397
    },
    'daily_volume': {
        'target_trains_per_day': 15000,
        'variation': 0.10,  # ±10% daily variation
        'expected_total_records': 5475000
    },
    'time_distribution': {
        'operations_start': '05:00',
        'operations_end': '23:30',
        'journey_duration_range_minutes': [30, 240]
    },
    'delay_severity': {
        'on_time': 0.88,
        'minor_1_5_min': 0.08,
        'low_5_15_min': 0.025,
        'medium_15_60_min': 0.015,
        'severe_60_plus_min': 0.010
    },
    'random_seed': 42
}

# =============================================================================
# DATA QUALITY NOTES
# =============================================================================

DATA_QUALITY = {
    'stations': {
        'total_records': 2782,
        'with_coordinates': 2782,
        'coverage': 'All of metropolitan France',
        'notes': 'All stations have valid GPS coordinates'
    },
    'lines': {
        'total_records': 1638,
        'with_valid_geometries': 1638,
        'coverage': 'Entire SNCF network',
        'notes': 'GeoJSON geometries verified'
    },
    'synthetic_delays': {
        'total_records': '~5,475,000',
        'date_coverage': '14 months',
        'geographic_coverage': 'All network stations',
        'notes': [
            'Generated using realistic distributions',
            'Causes weighted by AQST report',
            'Train mix based on 2023 SNCF data',
            'Occupancy rates from annual reports'
        ]
    }
}

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

USAGE_EXAMPLES = """
# Load and explore stations
import pandas as pd
df_stations = pd.read_csv('../data/gares_de_voyageurs.csv', sep=';')
print(f"Stations: {len(df_stations)}")
print(f"Top 5 by lines: {df_stations.nlargest(5, 'num_lines')[['Nom_Gare', 'num_lines']]}")

# Load and explore delays
df_delays = pd.read_parquet('../data/synthetic/train_delays_synthetic_2025_2026.parquet')
print(f"Total records: {len(df_delays)}")
print(f"Delay rate: {df_delays['has_delay'].mean()*100:.2f}%")
print(f"Avg delay (delayed only): {df_delays[df_delays['has_delay']==1]['delay_minutes'].mean():.1f} min")

# Analyze delays by cause
cause_dist = df_delays[df_delays['has_delay']==1]['delay_cause'].value_counts(normalize=True)
print(cause_dist)

# Analyze by train type
train_dist = df_delays['train_type'].value_counts(normalize=True)
print(train_dist)

# Time series analysis
df_delays['date'] = pd.to_datetime(df_delays['date'])
daily_stats = df_delays.groupby('date').agg({
    'has_delay': 'sum',
    'delay_minutes': ['mean', 'max'],
    'num_passengers': 'sum'
})
"""
