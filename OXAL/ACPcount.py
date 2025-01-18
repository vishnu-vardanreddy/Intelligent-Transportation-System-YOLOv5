import random
from time import sleep

def generate_traffic():
    """Generate random counts of vehicles and people for each lane"""
    lanes = {}
    for i in range(1, 4):
        lanes[f'lane_{i}'] = {
            'cars': random.randint(0, 10),
            'trucks': random.randint(0, 5),
            'people': random.randint(0, 15)
        }
    return lanes

def calculate_total_units(lane_data):
    """Calculate total traffic units giving different weights to different types"""
    # Weights: truck = 2, car = 1, person = 0.5
    return (lane_data['trucks'] * 2) + lane_data['cars'] + (lane_data['people'] * 0.5)

def determine_signals(lanes):
    """Determine signal colors based on traffic density"""
    # Calculate total units for each lane
    traffic_density = {}
    for lane, data in lanes.items():
        traffic_density[lane] = calculate_total_units(data)
    
    # Sort lanes by traffic density
    sorted_lanes = dict(sorted(traffic_density.items(), key=lambda x: x[1], reverse=True))
    
    # Assign colors
    signals = {lane: 'red' for lane in lanes.keys()}
    
    # Highest traffic lane gets green
    highest_lane = list(sorted_lanes.keys())[0]
    signals[highest_lane] = 'green'
    
    # Second highest gets orange
    if len(sorted_lanes) > 1:
        second_lane = list(sorted_lanes.keys())[1]
        signals[second_lane] = 'orange'
    
    return signals, traffic_density

def display_traffic_status(lanes, signals, traffic_density):
    """Display the current traffic status and signals"""
    print("\n=== Traffic Status ===")
    print("\nVehicle Counts:")
    for lane, data in lanes.items():
        print(f"\n{lane.upper()}:")
        print(f"Cars: {data['cars']}")
        print(f"Trucks: {data['trucks']}")
        print(f"People: {data['people']}")
        print(f"Total Traffic Units: {traffic_density[lane]:.1f}")
        print(f"Signal: {signals[lane].upper()}")
    print("\n" + "="*20)

def main():
    while True:
        # Generate random traffic
        lanes = generate_traffic()
        
        # Determine signals
        signals, traffic_density = determine_signals(lanes)
        
        # Display status
        display_traffic_status(lanes, signals, traffic_density)
        
        # Wait for 3 seconds before next update
        print("\nUpdating in 3 seconds...")
        sleep(3)
        print("\n" * 50)  # Clear screen

if __name__ == "__main__":
    try:
        print("Traffic Signal Control System")
        print("Press Ctrl+C to stop")
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")