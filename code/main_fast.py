"""
Fast Pipeline for SNCF Railway Network Analysis
Uses optimized algorithms for speed
"""

import sys
import os
import pandas as pd
from network_analysis_fast import FastRailwayNetworkAnalyzer
from generate_delays import SyntheticDelayDataGenerator


def main():
    """Run optimized analysis pipeline"""
    
    print("\n" + "=" * 70)
    print("SNCF RAILWAY NETWORK ANALYSIS (FAST)")
    print("=" * 70 + "\n")
    
    # Step 1: Fast Network Analysis
    print("\n[STEP 1] ANALYZING RAILWAY NETWORK")
    print("-" * 70)
    
    analyzer = FastRailwayNetworkAnalyzer(data_dir='../data')
    analyzer.run_analysis()
    
    # Step 2: Generate Synthetic Delay Data
    print("\n[STEP 2] GENERATING SYNTHETIC DELAY DATA")
    print("-" * 70)
    
    # Load network data
    stations_df = analyzer.stations_df
    lines_df = analyzer.lines_df
    
    # Create delay data generator
    generator = SyntheticDelayDataGenerator(stations_df, lines_df, random_seed=42)
    
    # Generate and save delays
    generator.run_full_generation(
        start_date='2025-01-01',
        end_date='2026-01-31',
        trains_per_day=15000,
        output_format='parquet'
    )
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
