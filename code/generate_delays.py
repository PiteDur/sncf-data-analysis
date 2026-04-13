"""
Synthetic Train Delay Data Generator
Generates realistic delay data for the French railway network
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random


class SyntheticDelayDataGenerator:
    """Generates synthetic delay data for trains"""
    
    # Delay causes and their probabilities (from AQST 2016 report, normalized to 1.0)
    DELAY_CAUSES = {
        'Météo (intempéries)': 0.0996,
        'Obstacles/intrusions': 0.0872,
        'Mouvements sociaux/grèves': 0.0618,
        'Gestion du trafic': 0.1940,
        'Infrastructure et travaux': 0.1600,
        'Gestion des gares': 0.1500,
        'Matériel roulant': 0.1240,
        'Affluence/correspondances': 0.1234,
    }
    
    # Train types and their distribution (2023 data)
    TRAIN_TYPES = {
        'TER': 0.505,
        'Transilien': 0.194,
        'TGV': 0.301
    }
    
    # Occupancy rates by train type
    OCCUPANCY_RATES = {
        'TER': {'min': 0.15, 'max': 0.60, 'mean': 0.38},
        'Transilien': {'min': 0.20, 'max': 0.65, 'mean': 0.35},
        'TGV': {'min': 0.60, 'max': 0.90, 'mean': 0.77}
    }
    
    # Average capacity by train type
    TRAIN_CAPACITY = {
        'TER': 350,
        'Transilien': 800,
        'TGV': 900
    }
    
    # Delay severity distribution (must sum to exactly 1.0)
    DELAY_DISTRIBUTION = {
        'no_delay': 0.880,   # 88% on-time
        'minor': 0.080,      # 1-5 min, 8%
        'low': 0.025,        # 5-15 min, 2.5%
        'medium': 0.013,     # 15-60 min, 1.3%
        'severe': 0.002      # 60+ min, 0.2%
    }
    
    def __init__(self, stations_df, lines_df, random_seed=42):
        """Initialize generator with network data"""
        self.stations_df = stations_df
        self.lines_df = lines_df
        self.random_seed = random_seed
        np.random.seed(random_seed)
        random.seed(random_seed)
        self.data = None
        
    def _sample_delay_minutes(self):
        """Sample delay duration based on severity distribution"""
        # Normalize probabilities to ensure they sum to 1.0
        probs = np.array(list(self.DELAY_DISTRIBUTION.values()))
        probs = probs / probs.sum()
        severity = np.random.choice(
            list(self.DELAY_DISTRIBUTION.keys()),
            p=probs
        )
        
        if severity == 'no_delay':
            return 0
        elif severity == 'minor':
            return np.random.randint(1, 6)
        elif severity == 'low':
            return np.random.randint(5, 16)
        elif severity == 'medium':
            return np.random.randint(15, 61)
        else:  # severe
            return np.random.randint(60, 181)
    
    def _sample_train_type(self):
        """Sample train type based on distribution"""
        # Normalize probabilities to ensure they sum to 1.0
        probs = np.array(list(self.TRAIN_TYPES.values()))
        probs = probs / probs.sum()
        return np.random.choice(
            list(self.TRAIN_TYPES.keys()),
            p=probs
        )
    
    def _sample_delay_cause(self):
        """Sample delay cause (only if there's a delay)"""
        if np.random.random() < 0.05:  # 5% chance of missing cause
            return 'Cause inconnue'
        # Normalize probabilities to ensure they sum to 1.0
        probs = np.array(list(self.DELAY_CAUSES.values()))
        probs = probs / probs.sum()
        return np.random.choice(
            list(self.DELAY_CAUSES.keys()),
            p=probs
        )
    
    def _get_random_station(self):
        """Get random station from the network"""
        return self.stations_df.sample(n=1).iloc[0]
    
    def _get_random_line(self):
        """Get random line from the network"""
        return self.lines_df.sample(n=1).iloc[0]
    
    def _generate_time_pair(self):
        """Generate departure and arrival time"""
        # Trains run from 5:00 to 23:30
        departure_hour = np.random.randint(5, 23)
        departure_minute = np.random.randint(0, 60)
        
        # Journey duration: 30 min to 4 hours depending on type
        journey_duration = np.random.randint(30, 241)  # minutes
        
        departure = f"{departure_hour:02d}:{departure_minute:02d}"
        
        total_minutes = departure_hour * 60 + departure_minute + journey_duration
        arrival_hour = (total_minutes // 60) % 24
        arrival_minute = total_minutes % 60
        
        arrival = f"{arrival_hour:02d}:{arrival_minute:02d}"
        
        return departure, arrival
    
    def _sample_passengers(self, train_type):
        """Sample number of passengers based on train type and occupancy"""
        occupancy = np.random.normal(
            self.OCCUPANCY_RATES[train_type]['mean'],
            (self.OCCUPANCY_RATES[train_type]['max'] - self.OCCUPANCY_RATES[train_type]['min']) / 4
        )
        occupancy = np.clip(occupancy, self.OCCUPANCY_RATES[train_type]['min'], self.OCCUPANCY_RATES[train_type]['max'])
        
        capacity = self.TRAIN_CAPACITY[train_type]
        return int(capacity * occupancy)
    
    def generate_delays(self, start_date='2025-01-01', end_date='2026-01-31', trains_per_day=15000):
        """
        Generate synthetic delay data
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            trains_per_day: Approximate number of trains per day
        """
        print(f"Generating synthetic delay data from {start_date} to {end_date}...")
        print(f"  Trains per day: {trains_per_day}")
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        num_days = (end - start).days + 1
        total_records = trains_per_day * num_days
        
        print(f"  Total records to generate: {total_records:,}")
        
        records = []
        
        for day_offset in range(num_days):
            current_date = start + timedelta(days=day_offset)
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Slight variation in trains per day (±10%)
            daily_trains = int(trains_per_day * np.random.uniform(0.9, 1.1))
            
            for _ in range(daily_trains):
                # Sample basic attributes
                train_type = self._sample_train_type()
                delay_minutes = self._sample_delay_minutes()
                has_delay = 1 if delay_minutes > 0 else 0
                
                # Get random station and line
                station = self._get_random_station()
                line = self._get_random_line()
                
                # Generate times
                departure, arrival = self._generate_time_pair()
                
                # Sample cause if delayed
                delay_cause = self._sample_delay_cause() if has_delay else 'Aucun retard'
                
                # Sample passengers
                passengers = self._sample_passengers(train_type)
                
                # Direction (next/previous station on line)
                direction_idx = np.random.randint(0, 2)
                direction = f"Direction {'A' if direction_idx == 0 else 'B'}"
                
                records.append({
                    'date': date_str,
                    'departure_time': departure,
                    'arrival_time': arrival,
                    'station_name': station['Nom_Gare'],
                    'station_code': station['Code_UIC'],
                    'line_code': line['CODE_LIGNE'],
                    'line_name': line['LIBELLE'],
                    'direction': direction,
                    'train_type': train_type,
                    'delay_minutes': delay_minutes,
                    'has_delay': has_delay,
                    'delay_cause': delay_cause,
                    'num_passengers': passengers
                })
            
            # Progress update every 30 days
            if (day_offset + 1) % 30 == 0:
                print(f"    Generated {len(records):,} records ({day_offset + 1}/{num_days} days)")
        
        self.data = pd.DataFrame(records)
        print(f"\nTotal records generated: {len(self.data):,}")
        
        return self.data
    
    def save_data(self, output_format='csv', output_dir='../data/synthetic'):
        """
        Save generated data
        
        Args:
            output_format: 'csv', 'parquet', or 'json'
            output_dir: Output directory
        """
        if self.data is None:
            raise ValueError("No data generated yet. Call generate_delays() first.")
        
        os.makedirs(output_dir, exist_ok=True)
        
        filename_base = 'train_delays_synthetic_2025_2026'
        
        print(f"\nSaving data as {output_format}...")
        
        if output_format == 'csv':
            filepath = os.path.join(output_dir, f'{filename_base}.csv')
            self.data.to_csv(filepath, index=False)
            file_size = os.path.getsize(filepath) / (1024 * 1024)
        
        elif output_format == 'parquet':
            filepath = os.path.join(output_dir, f'{filename_base}.parquet')
            self.data.to_parquet(filepath, index=False, compression='snappy')
            file_size = os.path.getsize(filepath) / (1024 * 1024)
        
        elif output_format == 'json':
            filepath = os.path.join(output_dir, f'{filename_base}.json')
            self.data.to_json(filepath, orient='records', date_format='iso')
            file_size = os.path.getsize(filepath) / (1024 * 1024)
        
        else:
            raise ValueError(f"Unknown format: {output_format}")
        
        print(f"  Saved to: {filepath}")
        print(f"  File size: {file_size:.2f} MB")
        
        return filepath
    
    def generate_statistics_report(self, output_file='delay_statistics.txt'):
        """Generate statistics report"""
        if self.data is None:
            raise ValueError("No data generated yet.")
        
        print(f"\nGenerating statistics report: {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("SYNTHETIC TRAIN DELAY DATA STATISTICS\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("1. DATASET OVERVIEW\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Records: {len(self.data):,}\n")
            f.write(f"Date Range: {self.data['date'].min()} to {self.data['date'].max()}\n")
            f.write(f"Total Days: {len(self.data['date'].unique())}\n")
            f.write(f"Average Trains per Day: {len(self.data) / len(self.data['date'].unique()):.0f}\n\n")
            
            f.write("2. DELAY STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Trains with Delays: {self.data['has_delay'].sum():,} ({self.data['has_delay'].mean()*100:.2f}%)\n")
            f.write(f"On-time Trains: {(1-self.data['has_delay']).sum():,} ({(1-self.data['has_delay']).mean()*100:.2f}%)\n")
            f.write(f"Average Delay (all): {self.data['delay_minutes'].mean():.2f} minutes\n")
            f.write(f"Average Delay (delayed only): {self.data[self.data['has_delay']==1]['delay_minutes'].mean():.2f} minutes\n")
            f.write(f"Median Delay (delayed only): {self.data[self.data['has_delay']==1]['delay_minutes'].median():.0f} minutes\n")
            f.write(f"Max Delay: {self.data['delay_minutes'].max()} minutes\n\n")
            
            f.write("3. TRAIN TYPE DISTRIBUTION\n")
            f.write("-" * 70 + "\n")
            for train_type, count in self.data['train_type'].value_counts().items():
                pct = count / len(self.data) * 100
                f.write(f"  {train_type:15s}: {count:8,} trains ({pct:5.2f}%)\n")
            f.write("\n")
            
            f.write("4. DELAY CAUSES DISTRIBUTION\n")
            f.write("-" * 70 + "\n")
            delayed_data = self.data[self.data['has_delay'] == 1]
            for cause, count in delayed_data['delay_cause'].value_counts().items():
                pct = count / len(delayed_data) * 100
                f.write(f"  {cause:40s}: {count:6,} ({pct:5.2f}%)\n")
            f.write("\n")
            
            f.write("5. PASSENGER STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Passengers: {self.data['num_passengers'].sum():,}\n")
            f.write(f"Average per Train: {self.data['num_passengers'].mean():.0f}\n")
            f.write(f"Min per Train: {self.data['num_passengers'].min()}\n")
            f.write(f"Max per Train: {self.data['num_passengers'].max()}\n\n")
            
            f.write("6. PASSENGER-DELAY IMPACT\n")
            f.write("-" * 70 + "\n")
            delayed_transit = self.data[self.data['has_delay'] > 0]['num_passengers'].sum()
            total_transit = self.data['num_passengers'].sum()
            f.write(f"Passengers on Delayed Trains: {delayed_transit:,}\n")
            f.write(f"Percentage of Total: {delayed_transit/total_transit*100:.2f}%\n")
            f.write(f"Person-minutes of Delay: {(self.data['num_passengers'] * self.data['delay_minutes']).sum():,}\n\n")
            
            f.write("7. TEMPORAL DISTRIBUTION\n")
            f.write("-" * 70 + "\n")
            hourly_delays = self.data[self.data['has_delay'] > 0].groupby(
                pd.to_datetime(self.data[self.data['has_delay'] > 0]['departure_time'], format='%H:%M').dt.hour
            ).size()
            f.write("Peak Delay Hours:\n")
            for hour, count in hourly_delays.nlargest(5).items():
                f.write(f"  {hour:02d}:00 - {hour:02d}:59: {count:6,} delayed trains\n")
            f.write("\n")
            
            f.write("8. TOP AFFECTED ROUTES\n")
            f.write("-" * 70 + "\n")
            delayed_routes = self.data[self.data['has_delay'] > 0].groupby(
                ['station_name', 'line_code']
            ).size().nlargest(10)
            for rank, ((station, line), count) in enumerate(delayed_routes.items(), 1):
                f.write(f"  {rank:2d}. {str(station):30s} (Line {str(line):6s}): {count:6,} delays\n")
            f.write("\n")
        
        print(f"  Report saved to {output_file}")
    
    def run_full_generation(self, start_date='2025-01-01', end_date='2026-01-31', 
                           trains_per_day=15000, output_format='parquet'):
        """Run complete generation pipeline"""
        self.generate_delays(start_date, end_date, trains_per_day)
        self.save_data(output_format=output_format)
        self.generate_statistics_report()
        
        print("\n" + "=" * 70)
        print("DATA GENERATION COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    # Load network data
    print("Loading network data...")
    stations_df = pd.read_csv('../data/gares_de_voyageurs.csv', sep=';')
    lines_df = pd.read_csv('../data/formes_des_lignes_du_rfn.csv', sep=';')
    
    # Generate delays
    generator = SyntheticDelayDataGenerator(stations_df, lines_df)
    generator.run_full_generation(output_format='parquet')
