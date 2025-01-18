import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from tkinter import messagebox
import os
import subprocess
from tkinter import scrolledtext
from traffic_data_generator import TrafficDataProcessor
from traffic_visualizer import GraphVisualizerGUI

class ApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GPU Interface")
        self.root.geometry("1000x800")
        
        # Initialize Traffic Data Processor
        self.traffic_processor = TrafficDataProcessor()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title label
        title_label = ttk.Label(self.main_frame, text="GPU Interface", 
                              font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=50)
        
        # Create main option buttons
        self.create_button("ACP Model", self.acp_model_click)
        self.create_button("DataSets", self.datasets_click)
        self.create_button("GraphSet", self.graphset_click)
        
        # Create output text area
        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=50, pady=10)
        
        # Store reference to graph window
        self.graph_window = None
        
    def create_button(self, text, command):
        btn = ttk.Button(self.buttons_frame, text=text, command=command)
        btn.pack(fill=tk.X, pady=10, ipady=20)
        
    def acp_model_click(self):
        try:
            # Create file dialog to select image or video
            file_path = filedialog.askopenfilename(
                title="Select File",
                filetypes=[
                    ("Media files", "*.jpg *.jpeg *.png *.bmp *.gif *.mp4 *.avi *.mov"),
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                    ("Video files", "*.mp4 *.avi *.mov")
                ]
            )
            
            if file_path:
                # Clear previous output
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Processing file...\n")
                self.root.update()
                
                # Construct the YOLO command
                conda_python_path = "python"  # Update this path if needed
                yolo_command = f"{conda_python_path} detect.py --source {file_path}"
                
                # Execute the command
                process = subprocess.Popen(
                    yolo_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Get output and errors
                output, errors = process.communicate()
                
                # Display output
                self.output_text.insert(tk.END, "Command Output:\n")
                self.output_text.insert(tk.END, output)
                
                if errors:
                    self.output_text.insert(tk.END, "\nErrors:\n")
                    self.output_text.insert(tk.END, errors)
                
        except Exception as e:
            self.output_text.insert(tk.END, f"\nError occurred: {str(e)}\n")
            messagebox.showerror("Error", f"Error processing file: {str(e)}")
        
    def datasets_click(self):
        try:
            # Clear previous output
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Generating traffic data...\n")
            self.root.update()
            
            # Generate the traffic data Excel file
            excel_file = self.traffic_processor.generate_excel_report()
            
            # Show success message in output area
            self.output_text.insert(tk.END, f"\nTraffic data has been generated successfully!\n")
            self.output_text.insert(tk.END, f"File saved as: {excel_file}\n")
            
            # Open the generated Excel file
            if os.path.exists(excel_file):
                if os.name == 'nt':  # Windows
                    os.startfile(excel_file)
                elif os.name == 'darwin':  # macOS
                    os.system(f"open {excel_file}")
                else:  # Linux
                    os.system(f"xdg-open {excel_file}")
                
                self.output_text.insert(tk.END, "\nOpened Excel file for viewing.\n")
            else:
                self.output_text.insert(tk.END, "\nError: Excel file not found after generation.\n")
                
        except Exception as e:
            error_message = f"Error generating traffic data: {str(e)}"
            self.output_text.insert(tk.END, f"\n{error_message}\n")
            messagebox.showerror("Error", error_message)
    
    def on_graph_window_close(self):
        """Handle graph window closing"""
        if self.graph_window:
            self.graph_window.destroy()
            self.graph_window = None
        
    def graphset_click(self):
        try:
            # Check if traffic_data.xlsx exists
            if not os.path.exists('traffic_data.xlsx'):
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "No traffic data found. Generating new data...\n")
                self.traffic_processor.generate_excel_report()
                self.output_text.insert(tk.END, "Traffic data generated successfully.\n")
            
            # If graph window already exists, bring it to front
            if self.graph_window and self.graph_window.winfo_exists():
                self.graph_window.lift()
                self.graph_window.focus_force()
                return
            
            # Create new graph window
            self.graph_window = tk.Toplevel(self.root)
            self.graph_window.protocol("WM_DELETE_WINDOW", self.on_graph_window_close)
            GraphVisualizerGUI(self.graph_window)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Opened graph visualization window.\n")
            self.output_text.insert(tk.END, "You can select different graph types from the dropdown menu.\n")
            
        except Exception as e:
            error_message = f"Error opening graph visualization: {str(e)}"
            self.output_text.insert(tk.END, f"\n{error_message}\n")
            messagebox.showerror("Error", error_message)

def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()