"""
Optimized Network Analysis for French Railway Network (SNCF)
Faster version with simplified line matching
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
import os
import warnings
warnings.filterwarnings('ignore')


class FastRailwayNetworkAnalyzer:
    """Fast railway network analyzer with simplified geometric matching"""
    
    def __init__(self, data_dir='../data'):
        """Initialize analyzer with data paths"""
        self.data_dir = data_dir
        self.stations_df = None
        self.lines_df = None
        self.network_stats = {}
        
    def load_data(self):
        """Load and parse station and line data"""
        print("Loading railway data...")
        
        # Load stations
        stations_path = os.path.join(self.data_dir, 'gares_de_voyageurs.csv')
        self.stations_df = pd.read_csv(stations_path, sep=';')
        
        # Parse geographical coordinates for stations
        self.stations_df[['lat', 'lon']] = self.stations_df['Position géographique'].str.split(', ', expand=True)
        self.stations_df['lat'] = self.stations_df['lat'].astype(float)
        self.stations_df['lon'] = self.stations_df['lon'].astype(float)
        
        print(f"  Loaded {len(self.stations_df)} stations")
        
        # Load lines
        lines_path = os.path.join(self.data_dir, 'formes_des_lignes_du_rfn.csv')
        self.lines_df = pd.read_csv(lines_path, sep=';')
        
        # Parse GeoJSON coordinates
        self.lines_df['coordinates'] = self.lines_df['Geo Shape'].apply(self._extract_coordinates)
        
        print(f"  Loaded {len(self.lines_df)} line segments")
        
        return self.stations_df, self.lines_df
    
    def _extract_coordinates(self, geojson_str):
        """Extract coordinates from GeoJSON string"""
        try:
            if pd.isna(geojson_str):
                return None
            geojson_obj = json.loads(geojson_str)
            if geojson_obj.get('type') == 'LineString':
                coords = geojson_obj['coordinates']
                return [[coord[1], coord[0]] for coord in coords]  # lat, lon order
        except:
            return None
        return None
    
    def compute_lines_per_station_fast(self):
        """
        Fast line counting: for each station, count lines based on
        if station coordinates are within the bounding box of line coordinates
        """
        print("\nMatching stations with lines (fast method)...")
        
        self.stations_df['num_lines'] = 0
        
        for idx, line in self.lines_df.iterrows():
            if line['coordinates'] is None or len(line['coordinates']) < 2:
                continue
            
            coords = np.array(line['coordinates'])
            lat_min, lat_max = coords[:, 0].min(), coords[:, 0].max()
            lon_min, lon_max = coords[:, 1].min(), coords[:, 1].max()
            
            # Add buffer (0.02 degrees ~= 2 km)
            buffer = 0.02
            
            matches = self.stations_df[
                (self.stations_df['lat'] >= lat_min - buffer) &
                (self.stations_df['lat'] <= lat_max + buffer) &
                (self.stations_df['lon'] >= lon_min - buffer) &
                (self.stations_df['lon'] <= lon_max + buffer)
            ]
            
            self.stations_df.loc[matches.index, 'num_lines'] += 1
            
            if (idx + 1) % 200 == 0:
                print(f"    Processed {idx + 1}/{len(self.lines_df)} line segments")
        
        print(f"  Average lines per station: {self.stations_df['num_lines'].mean():.2f}")
        return self.stations_df
    
    def compute_network_stats(self):
        """Compute network statistics"""
        print("\nComputing network statistics...")
        
        self.network_stats = {
            'total_stations': len(self.stations_df),
            'total_lines': len(self.lines_df),
            'stations_by_segment': self.stations_df['Segment(s) DRG'].value_counts().to_dict(),
            'lines_by_status': self.lines_df['LIBELLE'].value_counts().to_dict(),
        }
        
        return self.network_stats
    
    def create_network_map(self, output_file='network_map.html'):
        """Create interactive folium map"""
        print(f"\nCreating network map: {output_file}...")
        
        center_lat = self.stations_df['lat'].mean()
        center_lon = self.stations_df['lon'].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add stations
        for idx, row in self.stations_df.iterrows():
            popup_text = f"{row['Nom_Gare']}<br>Lines: {int(row['num_lines'])}"
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=min(3 + row['num_lines']/10, 12),
                popup=popup_text,
                color='blue',
                fill=True,
                fillColor='blue',
                fillOpacity=0.6,
                weight=1
            ).add_to(m)
        
        # Add lines
        colors = {
            'Exploitée': 'green',
            'Fermée': 'red',
            'Neutralisée': 'orange',
            'Fermée non déposée (Plus utilisable)': 'gray'
        }
        
        for idx, row in self.lines_df.iterrows():
            if row['coordinates'] is not None and len(row['coordinates']) > 1:
                color = colors.get(row['LIBELLE'], 'blue')
                folium.PolyLine(
                    locations=row['coordinates'],
                    color=color,
                    weight=1,
                    opacity=0.6
                ).add_to(m)
        
        m.save(output_file)
        print(f"  Map saved to {output_file}")
        return m
    
    def create_station_importance_map(self, output_file='lines_per_station_map.html'):
        """Map showing stations sized by importance"""
        print(f"\nCreating station importance map: {output_file}...")
        
        center_lat = self.stations_df['lat'].mean()
        center_lon = self.stations_df['lon'].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        max_lines = self.stations_df['num_lines'].max()
        
        for idx, row in self.stations_df.iterrows():
            if row['num_lines'] == 0:
                continue
            
            radius = 3 + (row['num_lines'] / max_lines) * 15
            
            if row['num_lines'] >= 10:
                color = 'darkred'
            elif row['num_lines'] >= 5:
                color = 'red'
            elif row['num_lines'] >= 3:
                color = 'orange'
            else:
                color = 'blue'
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                popup=f"{row['Nom_Gare']}: {int(row['num_lines'])} lines",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=1
            ).add_to(m)
        
        m.save(output_file)
        print(f"  Map saved to {output_file}")
        return m
    
    def create_plots(self, output_dir='plots'):
        """Create distribution plots"""
        print(f"\nCreating plots...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Railway Network Statistics', fontsize=16)
        
        # Top stations
        top_stations = self.stations_df.nlargest(15, 'num_lines')
        axes[0, 1].barh(range(len(top_stations)), top_stations['num_lines'])
        axes[0, 1].set_yticks(range(len(top_stations)))
        axes[0, 1].set_yticklabels(top_stations['Nom_Gare'], fontsize=8)
        axes[0, 1].set_title('Top 15 Stations by Line Count')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Distribution
        axes[0, 0].hist(self.stations_df['num_lines'], bins=20, color='steelblue', edgecolor='black')
        axes[0, 0].set_title('Lines per Station Distribution')
        axes[0, 0].set_xlabel('Number of Lines')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Segments
        segment_counts = self.stations_df['Segment(s) DRG'].value_counts()
        axes[1, 0].bar(segment_counts.index, segment_counts.values)
        axes[1, 0].set_title('Stations by Segment')
        axes[1, 0].set_ylabel('Count')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Line status
        line_status = self.lines_df['LIBELLE'].value_counts()
        axes[1, 1].bar(range(len(line_status)), line_status.values)
        axes[1, 1].set_xticks(range(len(line_status)))
        axes[1, 1].set_xticklabels(line_status.index, rotation=45, ha='right', fontsize=8)
        axes[1, 1].set_title('Line Segments by Status')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'network_statistics.png'), dpi=150, bbox_inches='tight')
        print(f"  Plots saved to {output_dir}/")
        plt.close()
    
    def generate_report(self, output_file='network_analysis_report.txt'):
        """Generate text report"""
        print(f"\nGenerating report...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("FRENCH RAILWAY NETWORK ANALYSIS\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("NETWORK OVERVIEW\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Stations: {len(self.stations_df)}\n")
            f.write(f"Total Line Segments: {len(self.lines_df)}\n")
            f.write(f"Average Lines per Station: {self.stations_df['num_lines'].mean():.2f}\n")
            f.write(f"Max Lines: {self.stations_df['num_lines'].max():.0f}\n\n")
            
            f.write("TOP 10 STATIONS\n")
            f.write("-" * 70 + "\n")
            for rank, (idx, row) in enumerate(self.stations_df.nlargest(10, 'num_lines').iterrows(), 1):
                f.write(f"{rank:2d}. {row['Nom_Gare']:35s} - {int(row['num_lines']):2d} lines\n")
            f.write("\n")
            
            f.write("STATIONS BY SEGMENT\n")
            f.write("-" * 70 + "\n")
            for segment, count in sorted(self.network_stats['stations_by_segment'].items()):
                f.write(f"  {segment}: {count}\n")
            f.write("\n")
        
        print(f"  Report saved to {output_file}")
    
    def run_analysis(self):
        """Run complete analysis"""
        self.load_data()
        self.compute_network_stats()
        self.compute_lines_per_station_fast()
        self.create_network_map()
        self.create_station_importance_map()
        self.create_plots()
        self.generate_report()
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    analyzer = FastRailwayNetworkAnalyzer(data_dir='../data')
    analyzer.run_analysis()
