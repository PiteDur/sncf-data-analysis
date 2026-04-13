"""
Network Analysis for French Railway Network (SNCF)
Analyzes stations and lines to create network visualizations
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins
import geopandas as gpd
from shapely.geometry import Point, LineString
import os
import warnings
warnings.filterwarnings('ignore')


class RailwayNetworkAnalyzer:
    """Analyzes the French railway network structure"""
    
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
        
        # Parse GeoJSON shapes for lines
        self.lines_df['geometry'] = self.lines_df['Geo Shape'].apply(self._parse_geojson)
        self.lines_df['coordinates'] = self.lines_df['geometry'].apply(
            lambda x: [[coord[1], coord[0]] for coord in x.coords] if x is not None else None
        )
        
        print(f"  Loaded {len(self.lines_df)} line segments")
        
        return self.stations_df, self.lines_df
    
    def _parse_geojson(self, geojson_str):
        """Parse GeoJSON string to LineString geometry"""
        try:
            if pd.isna(geojson_str):
                return None
            geojson_obj = json.loads(geojson_str)
            if geojson_obj.get('type') == 'LineString':
                coords = geojson_obj['coordinates']
                return LineString(coords)
        except:
            return None
        return None
    
    def compute_network_stats(self):
        """Compute descriptive statistics about the network"""
        print("\nComputing network statistics...")
        
        self.network_stats = {
            'total_stations': len(self.stations_df),
            'total_lines': len(self.lines_df),
            'stations_by_segment': self.stations_df['Segment(s) DRG'].value_counts().to_dict(),
            'lines_by_status': self.lines_df['LIBELLE'].value_counts().to_dict(),
        }
        
        # Statistical summary
        self.network_stats['stations_lat_range'] = {
            'min': self.stations_df['lat'].min(),
            'max': self.stations_df['lat'].max(),
            'mean': self.stations_df['lat'].mean()
        }
        
        self.network_stats['stations_lon_range'] = {
            'min': self.stations_df['lon'].min(),
            'max': self.stations_df['lon'].max(),
            'mean': self.stations_df['lon'].mean()
        }
        
        return self.network_stats
    
    def compute_lines_per_station(self):
        """
        Count lines passing through each station by analyzing line coordinates
        and matching with station positions
        """
        print("\nMatching stations with lines...")
        
        # Initialize line count
        self.stations_df['num_lines'] = 0
        
        # For each station, count how many lines pass through it
        for idx, station in self.stations_df.iterrows():
            station_point = Point(station['lon'], station['lat'])
            
            # Check proximity to line endpoints
            count = 0
            for _, line in self.lines_df.iterrows():
                if line['geometry'] is None:
                    continue
                
                # Create buffer around station (0.01 degrees ≈ 1 km)
                buffer = station_point.buffer(0.015)
                if line['geometry'].intersects(buffer):
                    count += 1
            
            self.stations_df.at[idx, 'num_lines'] = count
        
        print(f"  Stations with lines info computed")
        print(f"  Average lines per station: {self.stations_df['num_lines'].mean():.2f}")
        
        return self.stations_df
    
    def create_network_map(self, output_file='network_map.html'):
        """Create interactive folium map of the railway network"""
        print(f"\nCreating interactive map: {output_file}...")
        
        # Center of France
        center_lat = self.stations_df['lat'].mean()
        center_lon = self.stations_df['lon'].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add station points
        for idx, row in self.stations_df.iterrows():
            popup_text = f"""<b>{row['Nom_Gare']}</b><br>
            Lines: {int(row['num_lines'])}<br>
            Segment: {row['Segment(s) DRG']}"""
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=min(3 + row['num_lines']/10, 12),
                popup=popup_text,
                color='blue',
                fill=True,
                fillColor='blue',
                fillOpacity=0.6,
                weight=2
            ).add_to(m)
        
        # Add lines
        colors = {
            'Exploitée': 'green',
            'Fermée': 'red',
            'Neutralisée': 'orange',
            'Fermée non déposée (Plus utilisable)': 'gray'
        }
        
        for idx, row in self.lines_df.iterrows():
            if row['geometry'] is not None and len(row['coordinates']) > 0:
                color = colors.get(row['LIBELLE'], 'blue')
                folium.PolyLine(
                    locations=row['coordinates'],
                    color=color,
                    weight=2,
                    opacity=0.7,
                    popup=f"Line {row['CODE_LIGNE']}: {row['LIBELLE']}"
                ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: 150px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p style="margin: 0;"><b>Railway Network Legend</b></p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:green"></i> Operated Lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> Closed Lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> Neutralized Lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:gray"></i> Unusable Lines</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        m.save(output_file)
        print(f"  Map saved to {output_file}")
        
        return m
    
    def create_lines_per_station_map(self, output_file='lines_per_station_map.html'):
        """Create map showing stations sized by number of lines"""
        print(f"\nCreating lines-per-station map: {output_file}...")
        
        center_lat = self.stations_df['lat'].mean()
        center_lon = self.stations_df['lon'].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add stations with size proportional to lines
        max_lines = self.stations_df['num_lines'].max()
        
        for idx, row in self.stations_df.iterrows():
            if row['num_lines'] == 0:
                continue
            
            # Size based on number of lines
            radius = 3 + (row['num_lines'] / max_lines) * 15
            
            # Color intensity based on lines
            if row['num_lines'] >= 10:
                color = 'darkred'
            elif row['num_lines'] >= 5:
                color = 'red'
            elif row['num_lines'] >= 3:
                color = 'orange'
            else:
                color = 'blue'
            
            popup_text = f"""<b>{row['Nom_Gare']}</b><br>
            <b>Lines:</b> {int(row['num_lines'])}<br>
            Segment: {row['Segment(s) DRG']}<br>
            UIC Code: {row['Code_UIC']}"""
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                popup=popup_text,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=1
            ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 250px; height: 200px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <p style="margin: 0;"><b>Lines per Station</b></p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:darkred"></i> 10+ lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:red"></i> 5-9 lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:orange"></i> 3-4 lines</p>
        <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:blue"></i> 1-2 lines</p>
        <p style="margin: 10px 0;"><i>Size represents number of lines</i></p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        m.save(output_file)
        print(f"  Map saved to {output_file}")
        
        return m
    
    def create_distribution_plots(self, output_dir='plots'):
        """Create statistical distribution plots"""
        print(f"\nCreating distribution plots...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Lines per station distribution
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Railway Network Statistics', fontsize=16)
        
        # Plot 1: Distribution of lines per station
        axes[0, 0].hist(self.stations_df['num_lines'], bins=20, color='steelblue', edgecolor='black')
        axes[0, 0].set_xlabel('Number of Lines')
        axes[0, 0].set_ylabel('Number of Stations')
        axes[0, 0].set_title('Distribution of Lines per Station')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Top 15 stations by lines
        top_stations = self.stations_df.nlargest(15, 'num_lines')
        axes[0, 1].barh(range(len(top_stations)), top_stations['num_lines'])
        axes[0, 1].set_yticks(range(len(top_stations)))
        axes[0, 1].set_yticklabels(top_stations['Nom_Gare'], fontsize=9)
        axes[0, 1].set_xlabel('Number of Lines')
        axes[0, 1].set_title('Top 15 Stations by Line Count')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Plot 3: Stations by segment
        segment_counts = self.stations_df['Segment(s) DRG'].value_counts()
        axes[1, 0].bar(segment_counts.index, segment_counts.values, color='coral', edgecolor='black')
        axes[1, 0].set_xlabel('DRG Segment')
        axes[1, 0].set_ylabel('Number of Stations')
        axes[1, 0].set_title('Stations by Segment')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Lines by status
        line_status = self.lines_df['LIBELLE'].value_counts()
        axes[1, 1].bar(range(len(line_status)), line_status.values, color='mediumpurple', edgecolor='black')
        axes[1, 1].set_xticks(range(len(line_status)))
        axes[1, 1].set_xticklabels(line_status.index, rotation=45, ha='right', fontsize=8)
        axes[1, 1].set_ylabel('Number of Line Segments')
        axes[1, 1].set_title('Line Segments by Status')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plot_path = os.path.join(output_dir, 'network_statistics.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"  Plots saved to {plot_path}")
        plt.close()
    
    def generate_report(self, output_file='network_analysis_report.txt'):
        """Generate a text report of the analysis"""
        print(f"\nGenerating report: {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("FRENCH RAILWAY NETWORK ANALYSIS REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("1. NETWORK OVERVIEW\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Stations: {self.network_stats['total_stations']}\n")
            f.write(f"Total Line Segments: {self.network_stats['total_lines']}\n")
            f.write(f"Average Lines per Station: {self.stations_df['num_lines'].mean():.2f}\n")
            f.write(f"Median Lines per Station: {self.stations_df['num_lines'].median():.0f}\n")
            f.write(f"Max Lines at Single Station: {self.stations_df['num_lines'].max():.0f}\n\n")
            
            f.write("2. GEOGRAPHIC COVERAGE\n")
            f.write("-" * 70 + "\n")
            f.write(f"Latitude Range: {self.network_stats['stations_lat_range']['min']:.4f} to {self.network_stats['stations_lat_range']['max']:.4f}\n")
            f.write(f"Longitude Range: {self.network_stats['stations_lon_range']['min']:.4f} to {self.network_stats['stations_lon_range']['max']:.4f}\n\n")
            
            f.write("3. STATIONS BY SEGMENT\n")
            f.write("-" * 70 + "\n")
            for segment, count in sorted(self.network_stats['stations_by_segment'].items()):
                f.write(f"  Segment {segment}: {count} stations\n")
            f.write("\n")
            
            f.write("4. LINE STATUS DISTRIBUTION\n")
            f.write("-" * 70 + "\n")
            for status, count in sorted(self.network_stats['lines_by_status'].items()):
                f.write(f"  {status}: {count} segments\n")
            f.write("\n")
            
            f.write("5. TOP STATIONS BY LINE COUNT\n")
            f.write("-" * 70 + "\n")
            top_10 = self.stations_df.nlargest(10, 'num_lines')
            for rank, (idx, row) in enumerate(top_10.iterrows(), 1):
                f.write(f"  {rank:2d}. {row['Nom_Gare']:30s} - {int(row['num_lines']):2d} lines\n")
            f.write("\n")
            
            f.write("6. DATA QUALITY NOTES\n")
            f.write("-" * 70 + "\n")
            f.write(f"Stations with no lines: {len(self.stations_df[self.stations_df['num_lines'] == 0])}\n")
            f.write(f"Invalid line geometries: {self.lines_df['geometry'].isna().sum()}\n")
            f.write("\n")
        
        print(f"  Report saved to {output_file}")
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        self.load_data()
        self.compute_network_stats()
        self.compute_lines_per_station()
        self.create_network_map()
        self.create_lines_per_station_map()
        self.create_distribution_plots()
        self.generate_report()
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)


if __name__ == "__main__":
    analyzer = RailwayNetworkAnalyzer(data_dir='../data')
    analyzer.run_full_analysis()
