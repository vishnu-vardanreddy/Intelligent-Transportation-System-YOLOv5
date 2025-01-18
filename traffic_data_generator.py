import pandas as pd
from datetime import datetime
import os
import random

class TrafficDataProcessor:
    def __init__(self):
        self.excel_file = 'traffic_data.xlsx'
        self.lanes = ['Lane_1', 'Lane_2', 'Lane_3', 'Lane_4']
        
    def generate_random_traffic(self):
        """Generate random traffic data for each lane with more realistic patterns"""
        current_time = datetime.now()
        
        # Time-based multipliers to simulate rush hour patterns
        hour = current_time.hour
        if 7 <= hour <= 10:  # Morning rush hour
            multiplier = 1.5
        elif 16 <= hour <= 19:  # Evening rush hour
            multiplier = 1.8
        else:  # Normal hours
            multiplier = 1.0
        
        data_rows = []
        for lane in self.lanes:
            # Base random ranges for each vehicle type
            data = {
                'Date': current_time.strftime('%Y-%m-%d'),
                'Time': current_time.strftime('%H:%M:%S'),
                'Lane': lane,
                # Cars: Most common, higher range
                'Cars': random.randint(10, 30) * multiplier,
                # Trucks: Less common than cars
                'Trucks': random.randint(3, 12) * multiplier,
                # People: Variable depending on area
                'People': random.randint(5, 25) * multiplier,
                # Bicycles: Moderate numbers
                'Bicycles': random.randint(2, 15) * multiplier,
                # Motorcycles: Similar to bicycles
                'Motorcycles': random.randint(3, 18) * multiplier,
                # Buses: Least common
                'Buses': random.randint(1, 8) * multiplier
            }
            
            # Round all vehicle counts to integers
            for key in ['Cars', 'Trucks', 'People', 'Bicycles', 'Motorcycles', 'Buses']:
                data[key] = round(data[key])
            
            # Calculate total vehicles (excluding people)
            data['Total_Vehicles'] = (
                data['Cars'] + 
                data['Trucks'] + 
                data['Bicycles'] + 
                data['Motorcycles'] + 
                data['Buses']
            )
            
            # Calculate traffic density (weighted sum)
            data['Traffic_Density'] = (
                data['Cars'] * 1.0 +      # Base weight for cars
                data['Trucks'] * 2.5 +    # Trucks take more space
                data['People'] * 0.3 +    # People take less space
                data['Bicycles'] * 0.5 +  # Bicycles take little space
                data['Motorcycles'] * 0.7 + # Motorcycles take moderate space
                data['Buses'] * 3.0       # Buses take the most space
            )
            
            # Add some randomization to simulate real-world variations
            lane_factor = random.uniform(0.8, 1.2)
            data['Traffic_Density'] *= lane_factor
            
            # Determine signal color based on traffic density
            data['Signal_Status'] = 'Red'  # Default signal color
            
            data_rows.append(data)
            
        # Sort data rows by traffic density and assign signals
        sorted_data = sorted(data_rows, key=lambda x: x['Traffic_Density'], reverse=True)
        sorted_data[0]['Signal_Status'] = 'Green'  # Highest traffic gets green
        sorted_data[1]['Signal_Status'] = 'Orange'  # Second highest gets orange
        
        return pd.DataFrame(data_rows)
    
    def generate_excel_report(self):
        """Generate and save traffic data to Excel file with formatting"""
        # Generate traffic data
        df = self.generate_random_traffic()
        
        # Create Excel writer object
        with pd.ExcelWriter(self.excel_file, engine='xlsxwriter') as writer:
            # Write the main data
            df.to_excel(writer, sheet_name='Traffic_Data', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Traffic_Data']
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D3D3D3',
                'border': 1,
                'align': 'center'
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'align': 'center'
            })
            
            number_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'num_format': '0'  # Show integers without decimals
            })
            
            # Apply formats
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
                # Set column widths and formats
                if value in ['Date']:
                    worksheet.set_column(col_num, col_num, 12)
                elif value in ['Time', 'Signal_Status']:
                    worksheet.set_column(col_num, col_num, 10)
                elif value in ['Lane']:
                    worksheet.set_column(col_num, col_num, 8)
                elif value in ['Traffic_Density']:
                    worksheet.set_column(col_num, col_num, 15)
                else:
                    worksheet.set_column(col_num, col_num, 10)
            
            # Add conditional formatting for signal status
            worksheet.conditional_format(1, df.columns.get_loc('Signal_Status'), 
                                      len(df) + 1, df.columns.get_loc('Signal_Status'), 
                                      {'type': 'text',
                                       'criteria': 'containing',
                                       'value': 'Green',
                                       'format': workbook.add_format({'bg_color': '#90EE90'})})
            
            worksheet.conditional_format(1, df.columns.get_loc('Signal_Status'), 
                                      len(df) + 1, df.columns.get_loc('Signal_Status'), 
                                      {'type': 'text',
                                       'criteria': 'containing',
                                       'value': 'Orange',
                                       'format': workbook.add_format({'bg_color': '#FFA500'})})
            
            worksheet.conditional_format(1, df.columns.get_loc('Signal_Status'), 
                                      len(df) + 1, df.columns.get_loc('Signal_Status'), 
                                      {'type': 'text',
                                       'criteria': 'containing',
                                       'value': 'Red',
                                       'format': workbook.add_format({'bg_color': '#FF6B6B'})})
        
        return self.excel_file

def main():
    processor = TrafficDataProcessor()
    excel_file = processor.generate_excel_report()
    print(f"Excel file '{excel_file}' has been generated successfully!")
    
if __name__ == "__main__":
    main()