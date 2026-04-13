# EXTRACTED DATA FROM PDF DOCUMENTS FOR SNCF DATA ANALYSIS
# ============================================================================

# ============================================================================
# 1. DELAY CAUSES (Causes de Retard) - TER 2016 Data
# ============================================================================
# SOURCE: 21.03.17_communique_aqst-causes_ter.pdf
# This is the first published analysis of TER delay causes by AQST

DELAY_CAUSES_NATIONAL_2016 = {
    'description': 'National delay causes distribution for TER trains in 2016',
    'year': 2016,
    'source': 'AQST (Autorité de la Qualité de Service dans les Transports)',
    'unit': 'percentage of causes',
    'data': {
        'Externes au transport': {
            'percentage': 24.9,
            'description': 'External transport causes (weather, obstacles, suspicious packages, malice, social movements, etc.)',
            'french': 'Externes au transport'
        },
        'Gestion de trafic': {
            'percentage': 19.4,
            'description': 'Traffic management (rail line circulation and network interactions)',
            'french': 'Gestion de trafic'
        },
        'Infrastructure': {
            'percentage': 16.0,
            'description': 'Railway infrastructure (maintenance and works)',
            'french': 'Infrastructures ferroviaires'
        },
        'Gestion en gare et réutilisation de matériel': {
            'percentage': 15.0,
            'description': 'Station management and equipment reallocation (crew and material reassignment)',
            'french': 'Gestion en gare et réutilisation de matériel'
        },
        'Transporteur ou matériel roulant': {
            'percentage': 12.4,
            'description': 'Operator or rolling stock issues',
            'french': 'Transporteur ou matériel roulant'
        },
        'Prise en compte voyageurs': {
            'percentage': 12.4,
            'description': 'Passenger considerations (crowd management, disabled persons, connections)',
            'french': 'Prise en compte voyageurs'
        }
    },
    'total': 100.1,  # Rounding discrepancy in original
    'geographic_variations': {
        'best_performance': 'Grand Est',
        'best_delay_rate': '5.1%',
        'worst_performance': 'PACA (Provence-Alpes-Côte d\'Azur)',
        'worst_delay_rate': '15.1%',
        'description': 'Delay rates (>5min 59s) in 2016 by region'
    },
    'key_notes': [
        'First published analysis of TER delay causes',
        'Regional public councils and SNCF collaborated on this analysis',
        'Best results obtained when all delay causes are controlled',
        'Success depends on efforts in all delay cause categories',
        'Punctuality seems little dependent on traffic intensity (trains per hour)'
    ]
}

# Delay cause categories definition
DELAY_CAUSES_TYPOLOGY = {
    'Gestion du trafic': 'Traffic management - circulation on rail lines and interactions between networks',
    'Gestions en gare et réutilisation de matériel': 'Station management and material reuse - crew and material reallocation',
    'Matériel roulant': 'Rolling stock',
    'Prise en compte des voyageurs': 'Passenger considerations - crowd management, disabled persons, connections',
    'Infrastructures ferroviaires': 'Railway infrastructure - maintenance and works',
    'Externes au transport': 'External transport - weather, track obstacles, suspicious packages, malice, social movements, etc.'
}


# ============================================================================
# 2. TRAIN TYPE DISTRIBUTION - 2023 Data
# ============================================================================
# SOURCE: bilan_ferroviaire_2023_essentiel-1.pdf
# Key metrics on train services and network usage

TRAIN_TYPE_DISTRIBUTION_2023 = {
    'description': 'Distribution of railway traffic by train type and service - 2023',
    'year': 2023,
    'source': 'Bilan Ferroviaire 2023 - Autorité de Régulation des Transports (ART)',
    'unit': 'millions of trains.km',
    
    # By service type
    'by_service_type': {
        'TER': {
            'trains_km': 195,  # millions
            'percentage_of_total': 50.5,  # Approximately 195/386
            'description': 'Train Express Régional (Regional trains)',
            'breakdown': {
                'lignes_2_4': 83,  # millions (lines 2-4, most used)
                'lignes_5_6': 55,  # estimated
                'lignes_7_9': 57   # estimated
            }
        },
        'Transilien_and_RER': {
            'trains_km': 'Not separately isolated',
            'percentage_of_total': 'Part of conventioned services',
            'description': 'Transilien (Île-de-France conventional services) and RER',
            'note': 'Declined -4% from 2022 and -7% from 2019'
        },
        'TGV_and_GLV': {
            'trains_km': 'Included in SLO',
            'percentage_of_total': 'Part of freely organized services (SLO)',
            'description': 'TGV (high-speed) and GLV (large-scale trains)',
            'note': 'Part of the 30% SLO services by trains.km'
        },
        'Intercités': {
            'trains_km': 'Stable with 2022',
            'percentage_of_total': 'Part of conventioned services',
            'description': 'Long-distance regional services',
            'note': 'Merged with TER for analysis purposes'
        },
        'Freely_Organized_Services_SLO': {
            'trains_km': 116,  # millions (estimated: 386 - 270)
            'percentage_of_total': 30.0,
            'description': 'Services librement organisés (high-speed domestic and international)',
            'includes': ['TGV domestiques', 'TGV internationaux (Eurostar, Thalys)'],
            'decline_since_2019': -3.0,  # percent
            'note': 'Decline mainly due to cancellations and social movements'
        },
        'Conventioned_Services': {
            'trains_km': 270,  # millions (365 - 95 international)
            'percentage_of_total': 70.0,
            'description': 'Services conventionally organized (TER, Transilien, RER, Intercités)',
            'components': {
                'TER_and_Intercités': 195,
                'Île_de_France': 75
            }
        }
    },
    
    # By network usage
    'network_usage': {
        'total_trains_km': 386,
        'percentage_on_40_percent_network': 80.0,
        'description': '80% of traffic occurs on 40% of the national railway network',
        'highest_traffic_categories': ['Lignes 2-4 (most used)', 'RTE-T Central corridors']
    },
    
    # Regional distribution for TER
    'regional_ter_distribution': {
        'employees': {
            'total': 29000,
            'description': 'TER employment in 2023'
        },
        'by_region': {
            'Île-de-France': 14147,
            'Auvergne-Rhône-Alpes': 3291,
            'Grand Est': 3134,
            'Hauts-de-France': 2527,
            'Nouvelle-Aquitaine': 2389,
            'Occitanie': 2175,
            'Provence-Alpes-Côte-d\'Azur': 1654,
            'Normandie': 1605,
            'Bourgogne-Franche-Comté': 1552,
            'Centre-Val de Loire': 1125,
            'Pays de la Loire': 925,
            'Bretagne': 'Not specified in text'
        }
    },
    
    # Passenger distribution
    'passenger_distribution': {
        'total_passagers_km': 107_000_000_000,  # 107 billion
        'by_service': {
            'Freely_Organized_SLO': {
                'percentage': 61,  # of passengers.km
                'description': 'High-speed and international services'
            },
            'TER_and_Intercités': {
                'percentage': 'Significant portion of conventioned 39%',
                'description': 'Strong growth (+21% vs 2019)'
            },
            'Transilien_RER': {
                'percentage': 'Part of conventioned 39%',
                'description': 'Still below 2019 levels (-9%)'
            }
        }
    },
    
    # Frequency and occupation rates
    'occupation_rates': {
        'SLO_domestic_international': '77%',
        'TER_long_distance': '38%',
        'TER_proximity': '28%',
        'Transilien_and_RER': '35%'
    },
    
    'key_metrics': {
        'average_seats_per_circulation': 544,
        'average_passengers_per_circulation': 'Over 550 for SLO',
        'offer_trains_km': 386_000_000,  # 386 million
        'offer_seats_km': 210_000_000_000,  # 210 billion
        'average_occupancy_rate': '51%'
    }
}

# ============================================================================
# 3. DETAILED TRAIN TYPE PERCENTAGES FOR DATA GENERATION
# ============================================================================

TRAIN_TYPE_PERCENTAGE_BREAKDOWN = {
    'description': 'Simplified breakdown for synthetic data generation',
    'estimation_method': 'Based on trains.km distribution and regional employment data',
    'year': 2023,
    
    'primary_split': {
        'Conventioned_Services': {
            'percentage': 70,
            'trains_km': 270,
            'description': 'Public service obligations - TER, Intercités, Transilien, RER'
        },
        'Freely_Organized_Services': {
            'percentage': 30,
            'trains_km': 116,
            'description': 'Commercial services - TGV, international trains'
        }
    },
    
    'secondary_split_conventioned': {
        'TER': {
            'percentage': 72.2,  # 195/270
            'trains_km': 195,
            'description': 'Regional Express Trains - most frequent service type'
        },
        'Transilien_RER': {
            'percentage': 27.8,  # 75/270
            'trains_km': 75,
            'description': 'Île-de-France suburban services'
        }
    },
    
    'secondary_split_slo': {
        'TGV_Domestique': {
            'percentage': 55,  # Estimated dominant portion
            'description': 'High-speed domestic trains'
        },
        'International_Services': {
            'percentage': 30,  # Eurostar, Thalys, etc.
            'description': 'International high-speed and long-distance'
        },
        'Other_Commercial': {
            'percentage': 15,
            'description': 'Other commercial services'
        }
    }
}

# ============================================================================
# 4. PUNCTUALITY DATA FOR VALIDATION
# ============================================================================

PUNCTUALITY_DATA_2023 = {
    'source': 'bilan_ferroviaire_2023_essentiel-1.pdf',
    'year': 2023,
    
    'freight_trains': {
        'delay_30min': 16.7,  # percent
        'delay_5min': 55.0,   # percent
        'trend': 'Degradation of 0.8 points vs 2022'
    },
    
    'passenger_trains': {
        'note': 'Degradation observed for all services except international trains',
        'conventional_trains': 'Delays increased more strongly during peak hours',
        'distribution': 'Distribution of delay causes stable, split equally between operators and infrastructure managers'
    }
}

# ============================================================================
# 5. SUMMARY FOR PYTHON DATA GENERATION
# ============================================================================

SUMMARY_FOR_DATA_GENERATION = """
RECOMMENDED DISTRIBUTION FOR SYNTHETIC TER DATA GENERATION:

1. **DELAY CAUSES Distribution** (Use AQST 2016 baseline, adjust for current trends):
   - Externes au transport: 24.9% - weather, obstacles, social movements
   - Gestion de trafic: 19.4% - traffic management issues
   - Infrastructure: 16.0% - maintenance and works
   - Gestion en gare et réutilisation: 15.0% - station and equipment issues
   - Transporteur/matériel: 12.4% - operator and rolling stock
   - Prise en compte voyageurs: 12.4% - passenger-related delays

2. **TRAIN TYPE DISTRIBUTION** (2023 realistic split):
   - TER (Regional): 72.2% of conventioned services
   - Transilien/RER (Suburban): 27.8% of conventioned services
   - Note: Freely organized services (30% overall) much less relevant for local TER analysis

3. **REGIONAL DISTRIBUTION** (TER employment as proxy for service volume):
   - Use the regional employee counts as weight factors
   - Major hub: Île-de-France (~49% of TER employment)
   - Significant regions: Auvergne-Rhône-Alpes (11.4%), Grand Est (10.8%)
   
4. **OCCUPANCY RATES** (for realistic passenger generation):
   - TER long-distance lines (100+ km): 38%
   - TER proximity lines: 28%
   - Peak hours typically 10+ percentage points higher
   
5. **HISTORICAL CONTEXT**:
   - 2023: 5% increase in passenger frequency vs 2022
   - TER fréquentation increased in all regions (10%+ in some)
   - Note: Social movements impact seen in March 2023 (-8% to -15% monthly fréquentation)

6. **PUNCTUALITY BASELINE**:
   - Freight trains: ~16.7% with delays >30 min (reference for comparison)
   - Passenger trains: Lower delay thresholds typically used (5-15 min)
"""

if __name__ == '__main__':
    print("=" * 80)
    print("SNCF DATA EXTRACTION SUMMARY")
    print("=" * 80)
    print(SUMMARY_FOR_DATA_GENERATION)
    print("\n" + "=" * 80)
    print("Detailed data available as module attributes")
    print("=" * 80)
