# SNCF Data Analysis - Extracted Information Summary

**Extraction Date:** April 13, 2026  
**Documents Analyzed:** 2 PDF files

---

## 1. DELAY CAUSES (Causes de Retard) - TER 2016

### Source
- **Document:** 21.03.17_communique_aqst-causes_ter.pdf
- **Organization:** AQST (Autorité de la Qualité de Service dans les Transports)
- **Year:** 2016
- **Significance:** First published comprehensive analysis of TER delay causes

### Delay Cause Distribution (National Level)

| Rank | Cause | Percentage | French Term |
|------|-------|-----------|------------|
| 1 | External Transport | **24.9%** | Externes au transport |
| 2 | Traffic Management | **19.4%** | Gestion de trafic |
| 3 | Infrastructure | **16.0%** | Infrastructures ferroviaires |
| 4 | Station Management & Equipment | **15.0%** | Gestion en gare et réutilisation |
| 5 | Operator/Rolling Stock | **12.4%** | Transporteur ou matériel roulant |
| 6 | Passenger Management | **12.4%** | Prise en compte voyageurs |
| | **TOTAL** | **100.1%** | (rounding) |

### Detailed Cause Descriptions

1. **Externes au transport (24.9%)** - External causes
   - Weather conditions
   - Track obstacles
   - Suspicious packages
   - Malicious acts
   - Social movements
   - External factors beyond railway system control

2. **Gestion de trafic (19.4%)** - Traffic Management
   - Rail line circulation management
   - Network interaction coordination
   - Signal and scheduling issues

3. **Infrastructures ferroviaires (16.0%)** - Infrastructure
   - Maintenance activities
   - Infrastructure works
   - Track conditions

4. **Gestion en gare et réutilisation de matériel (15.0%)** - Station Management
   - Crew management
   - Material reassignment
   - Station operations

5. **Transporteur ou matériel roulant (12.4%)** - Operator/Rolling Stock
   - Operator issues
   - Rolling stock (train) mechanical problems
   - Equipment failures

6. **Prise en compte voyageurs (12.4%)** - Passenger Management
   - Crowd management operations
   - Assistance for disabled passengers
   - Connection management

### Geographic Variation

**Best Performance:** Grand Est
- Delay rate (>5min 59s): **5.1%**

**Worst Performance:** Provence-Alpes-Côte-d'Azur (PACA)
- Delay rate (>5min 59s): **15.1%**

**Finding:** 3x difference between best and worst regions - suggests regional factors are important

### Key Insights

✓ **Best results occur when all delay cause categories are simultaneously controlled**
- Success is not achieved by focusing on single cause
- Multi-domain effort required

✓ **No strong correlation between delay performance and traffic intensity**
- Number of trains per hour does not determine delay performance
- Operational management is more critical than capacity

✓ **All regions can improve within their current capacity**
- Delay control is achievable with proper management

---

## 2. TRAIN TYPE DISTRIBUTION - 2023

### Source
- **Document:** bilan_ferroviaire_2023_essentiel-1.pdf
- **Organization:** Autorité de Régulation des Transports (ART)
- **Year:** 2023
- **Scope:** National French railway network

### Overall Distribution

**Total Railway Traffic:** 386 million trains.km

| Service Type | Trains.km | Percentage | Characteristic |
|--------------|-----------|-----------|-----------------|
| **TER (Regional)** | 195M | **50.5%** | Most frequent, lower occupancy |
| **Transilien/RER** | 75M | **19.4%** | Île-de-France only, suburban |
| **TGV & SLO** | 116M | **30.1%** | High-speed, higher capacity |
| **Total** | **386M** | **100.0%** | |

### Detailed Breakdown

#### 1. TER (Train Express Régional) - 50.5%
- **Trains.km:** 195 million
- **Coverage:** Entire France except Île-de-France
- **Employment:** 29,000 people (2023)
- **Characteristics:**
  - Highest frequency of service
  - Lowest occupancy rates
  - Most commonly delayed
  - Essential for regional connectivity

**Regional Distribution (by employment levels):**
- Île-de-France: 14,147 (48.8%) - overlaps with Transilien
- Auvergne-Rhône-Alpes: 3,291 (11.3%)
- Grand Est: 3,134 (10.8%)
- Hauts-de-France: 2,527 (8.7%)
- Nouvelle-Aquitaine: 2,389 (8.2%)
- Occitanie: 2,175 (7.5%)
- Provence-Alpes-Côte-d'Azur: 1,654 (5.7%)
- Normandie: 1,605 (5.5%)
- Bourgogne-Franche-Comté: 1,552 (5.3%)
- Centre-Val de Loire: 1,125 (3.9%)
- Pays de la Loire: 925 (3.2%)

#### 2. Transilien & RER - 19.4%
- **Trains.km:** 75 million
- **Coverage:** Île-de-France region only
- **Characteristics:**
  - Suburban commuter services
  - Medium occupancy (35%)
  - RATP and SNCF joint operation
  - Still recovering post-pandemic

#### 3. Freely Organized Services (SLO) - 30.1%
- **Trains.km:** 116 million
- **Composition:**
  - TGV domestique (~55%)
  - International services (Eurostar, Renfe, Trenitalia): (~45%)
- **Characteristics:**
  - High-speed services
  - Highest occupancy (77%)
  - Lower frequency
  - Commercial operation

---

## 3. KEY METRICS FOR DATA GENERATION

### Occupancy Rates (2023)

| Service Type | Occupancy | Avg Passengers/Train |
|--------------|-----------|-------------------|
| TGV High-Speed | **77%** | ~419 |
| TER Long-Distance (100+ km) | **38%** | ~206 |
| TER Proximity (<100 km) | **28%** | ~152 |
| Transilien/RER | **35%** | ~190 |
| **Average (All)** | **51%** | 277 |

### Passenger Distribution (107 Billion Passenger.km Total)

| Service | Percentage | Passenger.km | Trend vs 2019 |
|---------|-----------|-------------|--------------|
| **Freely Organized (SLO)** | **61%** | 65.3B | +8% |
| **TER & Intercités** | **24%** | 25.7B | **+21%** ✓ |
| **Transilien/RER** | **15%** | 16.1B | **-9%** ✗ |

**Key Finding:** TER has recovered strongly (+21% vs 2019), but Île-de-France suburban still lags.

### Growth Trends (Year-over-Year)

#### 2023 vs 2022
- Overall passenger growth: **+5%**
- TER growth: Strong in all regions (10%+ in some)
- Transilien/RER: Minimal growth (+2%)

#### 2023 vs 2019 (Pre-Pandemic Recovery)
- TER/Intercités: **+21%** ✓ Recovered well
- SLO (High-Speed): **+8%** ✓ Strong recovery
- Transilien/RER: **-9%** ✗ Still below pre-pandemic

### Impact of Social Movements
- March 2023: -8% to -15% decrease in monthly ridership (strikes)
- Recovery: Offset by strong growth in other months

---

## 4. RECOMMENDED PARAMETERS FOR SYNTHETIC DATA GENERATION

### Delay Causes Distribution
Use the AQST 2016 distribution with these weights:

```
Delay Causes:
├── Externes au transport: 24.9%
├── Gestion de trafic: 19.4%
├── Infrastructure: 16.0%
├── Gestion en gare et réutilisation: 15.0%
├── Transporteur/matériel: 12.4%
└── Prise en compte voyageurs: 12.4%
```

**Adjustments to consider:**
- Increase external causes during storm seasons
- Increase traffic management issues during peak hours
- Regional variations: worst case up to 3x difference from best case

### Train Type Distribution
Primary split:
- **Conventioned (Public Service):** 70%
  - TER: 72.2% (195M / 270M)
  - Transilien/RER: 27.8% (75M / 270M)
- **Freely Organized (Commercial):** 30%
  - TGV Domestic: ~55%
  - International: ~45%

### Regional Weights
Use TER employment percentages as proxies for service volume:
- Scale regions 1-11 based on employee count
- Île-de-France: ~49% base weight (but Transilien separate)
- Other regions: 1-11% each

### Occupancy Generation
Use service-type-specific occupancy rates:
- SLO (High-speed): 77%
- TER long-distance: 38%
- TER proximity: 28%
- Transilien: 35%

**Peak Hour Adjustment:** Add 10+ percentage points to base occupancy

### Temporal Patterns
- **Baseline:** 5% annual growth in ridership post-2022
- **Peak hours:** Higher occupancy, more delays
- **Off-peak:** Lower occupancy but more delays per train (service optimization)
- **Seasonal:** Consider weather impact on "Externes au transport" causes

---

## 5. SUPPORTING STATISTICS (2023)

### Network Utilization
- **Total Network:** 27,586 km of lines
- **Network Concentration:** 80% of traffic on 40% of network
- **Average Utilization:** 45 trains/day per km of line (vs 54 in Europe)

### Schedule Reliability (2023)
- **TER/Intercités:** Fréquentation growth +5% driven by reliability improvements
- **Freight trains** (for context): 16.7% delayed >30 min
- **Passenger trains:** Generally better punctuality than freight

### Employment Impact
- **Total Railway Sector:** 150,000+ people
- **SNCF Group:** ~95% of railway employment
- **TER Activity:** 29,000 dedicated employees
- **Regional Range:** 800-4,500 TER employees per region

---

## 6. FILES CREATED

Three output files have been created in the workspace:

1. **`extracted_data_summary.py`** - Python module with structured data
   - Direct import for data generation scripts
   - All metrics as Python dictionaries

2. **`extracted_data.json`** - JSON format
   - Machine-readable format
   - Suitable for configuration files
   - Easy integration with APIs

3. **`markdown_summary.md`** - This file
   - Human-readable overview
   - Documentation format
   - Reference guide

---

## 7. USAGE EXAMPLES

### For Python Data Generation

```python
# Import the Python module
from extracted_data_summary import DELAY_CAUSES_NATIONAL_2016, TRAIN_TYPE_DISTRIBUTION_2023

# Generate delay cause
cause_weights = {cause: data['percentage']/100 
                for cause, data in DELAY_CAUSES_NATIONAL_2016['data'].items()}
delay_cause = np.random.choice(list(cause_weights.keys()), p=list(cause_weights.values()))

# Generate train type
train_type_weights = {'TER': 0.505, 'Transilien': 0.194, 'TGV': 0.301}
train_type = np.random.choice(list(train_type_weights.keys()), p=list(train_type_weights.values()))
```

### For Configuration

```json
{
  "delay_causes": [
    {"name": "Externes au transport", "percentage": 24.9},
    {"name": "Gestion de trafic", "percentage": 19.4},
    ...
  ],
  "train_types": {
    "TER": 0.505,
    "Transilien": 0.194,
    "TGV": 0.301
  }
}
```

---

## 8. DATA QUALITY NOTES

### AQST 2016 Delay Data
- **Strengths:** First official comprehensive analysis
- **Limitations:** Data from 2016 (8 years old)
- **Use Case:** Baseline for delay cause distribution, regional patterns

### 2023 Bilan Ferroviaire Data
- **Strengths:** Current, comprehensive, official statistics
- **Limitations:** Aggregated data, may not show all patterns
- **Use Case:** Train type distribution, regional variation, current trends

### Combining Both
- Use 2016 delay causes as distribution baseline
- Apply 2023 regional weights from TER employment
- Cross-validate with 2023 punctuality metrics where available

---

## END OF SUMMARY

**For Questions or Additional Analysis:**
- Refer to the full PDF extraction in `pdf_extraction_output.txt`
- Check JSON and Python files for programmatic access
- All source documents are in the `litterature/` folder
