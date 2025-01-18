import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TrafficVisualizer:
    def __init__(self, excel_file='traffic_data.xlsx'):
        self.excel_file = excel_file
        self.data = pd.read_excel(self.excel_file)
        
    def create_bar_graph(self, figure, lanes):
        figure.clear()
        
        # Create 2x2 subplots for the four lanes
        for idx, lane in enumerate(lanes, 1):
            ax = figure.add_subplot(2, 2, idx)
            
            # Filter data for the current lane
            lane_data = self.data[self.data['Lane'] == lane]
            
            # Get vehicle columns (exclude non-vehicle columns)
            vehicle_columns = ['Cars', 'Trucks', 'People', 'Bicycles', 'Motorcycles', 'Buses']
            
            # Create bar graph
            x = range(len(vehicle_columns))
            values = [lane_data[col].iloc[0] for col in vehicle_columns]
            ax.bar(x, values, color='skyblue')
            
            # Customize the subplot
            ax.set_title(f'{lane} Traffic Distribution')
            ax.set_xticks(x)
            ax.set_xticklabels(vehicle_columns, rotation=45)
            ax.set_ylabel('Count')
        
        figure.tight_layout()
    
    def create_line_graph(self, figure, lanes):
        figure.clear()
        
        # Create 2x2 subplots for the four lanes
        for idx, lane in enumerate(lanes, 1):
            ax = figure.add_subplot(2, 2, idx)
            
            # Filter data for the current lane
            lane_data = self.data[self.data['Lane'] == lane]
            
            # Get vehicle columns
            vehicle_columns = ['Cars', 'Trucks', 'People', 'Bicycles', 'Motorcycles', 'Buses']
            values = [lane_data[col].iloc[0] for col in vehicle_columns]
            
            # Create line graph
            ax.plot(vehicle_columns, values, marker='o', linestyle='-', linewidth=2, markersize=8)
            
            # Customize the subplot
            ax.set_title(f'{lane} Traffic Trend')
            ax.set_xticklabels(vehicle_columns, rotation=45)
            ax.set_ylabel('Count')
            ax.grid(True)
        
        figure.tight_layout()
    
    def create_heat_graph(self, figure, lanes):
        figure.clear()
        
        # Create 2x2 subplots for the four lanes
        for idx, lane in enumerate(lanes, 1):
            ax = figure.add_subplot(2, 2, idx)
            
            # Filter data for the current lane
            lane_data = self.data[self.data['Lane'] == lane]
            
            # Get vehicle columns and create heatmap data
            vehicle_columns = ['Cars', 'Trucks', 'People', 'Bicycles', 'Motorcycles', 'Buses']
            heatmap_data = lane_data[vehicle_columns].iloc[0].values.reshape(1, -1)
            
            # Create heatmap
            sns.heatmap(heatmap_data, 
                       ax=ax,
                       xticklabels=vehicle_columns,
                       yticklabels=['Density'],
                       cmap='YlOrRd',
                       annot=True,
                       fmt='.0f')
            
            # Customize the subplot
            ax.set_title(f'{lane} Traffic Heatmap')
            ax.set_xticklabels(vehicle_columns, rotation=45)
        
        figure.tight_layout()

class GraphVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Data Visualizer")
        self.root.geometry("1200x800")
        
        # Initialize visualizer
        self.visualizer = TrafficVisualizer()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create controls frame
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        # Create graph type selector
        ttk.Label(self.controls_frame, text="Select Graph Type:").pack(side=tk.LEFT, padx=5)
        self.graph_type = ttk.Combobox(self.controls_frame, 
                                      values=["Bar Graph", "Line Graph", "Heat Map"],
                                      state="readonly")
        self.graph_type.pack(side=tk.LEFT, padx=5)
        self.graph_type.set("Bar Graph")
        self.graph_type.bind('<<ComboboxSelected>>', self.update_graph)
        
        # Create refresh button
        ttk.Button(self.controls_frame, text="Refresh Data", 
                  command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        
        # Create matplotlib figure
        self.figure = plt.Figure(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial graph display
        self.update_graph()
    
    def update_graph(self, event=None):
        lanes = ['Lane_1', 'Lane_2', 'Lane_3', 'Lane_4']
        graph_type = self.graph_type.get()
        
        if graph_type == "Bar Graph":
            self.visualizer.create_bar_graph(self.figure, lanes)
        elif graph_type == "Line Graph":
            self.visualizer.create_line_graph(self.figure, lanes)
        else:  # Heat Map
            self.visualizer.create_heat_graph(self.figure, lanes)
        
        self.canvas.draw()
    
    def refresh_data(self):
        try:
            self.visualizer = TrafficVisualizer()  # Reload data from Excel
            self.update_graph()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error refreshing data: {str(e)}")

def main():
    root = tk.Tk()
    app = GraphVisualizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()