"""
Main Pipeline for SNCF Railway Network Analysis
Orchestrates network analysis and synthetic delay data generation
"""

import sys
import os
import pandas as pd
from network_analysis import RailwayNetworkAnalyzer
from generate_delays import SyntheticDelayDataGenerator


def main():
    """Run complete analysis pipeline"""
    
    print("\n" + "=" * 70)
    print("SNCF RAILWAY NETWORK ANALYSIS")
    print("=" * 70 + "\n")
    
    # Step 1: Network Analysis
    print("\n[STEP 1] ANALYZING RAILWAY NETWORK")
    print("-" * 70)
    
    analyzer = RailwayNetworkAnalyzer(data_dir='../data')
    analyzer.run_full_analysis()
    
    # Step 2: Generate Synthetic Delay Data
    print("\n[STEP 2] GENERATING SYNTHETIC DELAY DATA")
    print("-" * 70)
    
    # Load network data for delay generation
    stations_df = analyzer.stations_df
    lines_df = analyzer.lines_df
    
    # Create synthetic data generator
    generator = SyntheticDelayDataGenerator(stations_df, lines_df, random_seed=42)
    
    # Generate delays (Jan 2025 - Jan 2026, ~15,000 trains/day)
    generator.run_full_generation(
        start_date='2025-01-01',
        end_date='2026-01-31',
        trains_per_day=15000,
        output_format='parquet'  # More efficient for large datasets
    )
    
    print("\n" + "=" * 70)
    print("COMPLETE PIPELINE FINISHED SUCCESSFULLY")
    print("=" * 70)
    print("\nGenerated Files:")
    print("  - network_map.html (interactive railway network map)")
    print("  - lines_per_station_map.html (stations sized by line count)")
    print("  - network_analysis_report.txt (network statistics)")
    print("  - plots/network_statistics.png (distribution plots)")
    print("  - ../data/synthetic/train_delays_synthetic_2025_2026.parquet (delay data)")
    print("  - delay_statistics.txt (delay data statistics)")


if __name__ == "__main__":
    main()
