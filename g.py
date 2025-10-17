import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

def generate_smart_meter_data(num_meters, start_date, end_date, interval_minutes):
    """
    Generates smart meter data including measurements and events
    
    Args:
        num_meters (int): Number of smart meters to simulate
        start_date (str): Start date in 'dd:mm:yyyy HH:MM' format
        end_date (str): End date in 'dd:mm:yyyy HH:MM' format
        interval_minutes (int): Measurement interval (15 or 30 minutes)
    
    Returns:
        tuple: (measurements DataFrame, events DataFrame)
    """
    # Parse dates
    start = datetime.strptime(start_date, '%d:%m:%Y %H:%M')
    end = datetime.strptime(end_date, '%d:%m:%Y %H:%M')
    
    # Generate meter IDs
    meter_ids = [str(uuid.uuid4()) for _ in range(num_meters)]
    
    # Define measurements and events
    measurement_columns = [
        'meter_id', 'timestamp',
        'active_energy_import_kwh', 'reactive_energy_import_kvarh',
        'active_energy_export_kwh', 'reactive_energy_export_kvarh',
        'voltage_phase1_v', 'voltage_phase2_v', 'voltage_phase3_v',
        'current_phase1_a', 'current_phase2_a', 'current_phase3_a',
        'maximum_demand_kw', 'power_factor'
    ]
    
    event_types = [
        'POWER_OUTAGE', 'VOLTAGE_SAG', 'VOLTAGE_SWELL', 
        'TAMPER_DETECTED', 'METER_COVER_OPENED', 
        'CURRENT_IMBALANCE', 'PHASE_FAILURE', 
        'HIGH_TEMPERATURE', 'METER_RESET'
    ]
    
    # Initialize data structures
    all_measurements = []
    all_events = []
    
    # Base parameters for realistic simulation
    BASE_VOLTAGE = 230.0
    MAX_CURRENT = 100.0
    MAX_DEMAND_FACTOR = 0.8
    
    for meter_id in meter_ids:
        # Initialize meter-specific parameters
        current_time = start
        last_energy_import = 0.0
        max_demand = 0.0
        cumulative_energy_import = 0.0
        cumulative_energy_export = 0.0
        abnormality_factor = 1.0 if random.random() > 0.3 else random.uniform(0.7, 1.3)
        has_abnormality = abnormality_factor != 1.0
        
        # Time series generation
        while current_time <= end:
            # Base load pattern (time-dependent)
            hour = current_time.hour
            if 0 <= hour < 6:       # Night
                load_factor = 0.3
            elif 6 <= hour < 9:     # Morning peak
                load_factor = 0.8
            elif 9 <= hour < 17:    # Daytime
                load_factor = 0.6
            elif 17 <= hour < 20:   # Evening peak
                load_factor = 0.9
            else:                   # Night
                load_factor = 0.4
            
            # Add randomness
            load_factor *= random.uniform(0.95, 1.05)
            load_factor = min(max(load_factor, 0.2), 1.0)
            
            # Apply abnormality factor
            current_load_factor = load_factor * abnormality_factor
            
            # Calculate measurements -------------------------------------------------
            interval_hours = interval_minutes / 60.0
            
            # Energy calculations (cumulative)
            active_energy_import = cumulative_energy_import + (current_load_factor * 2.5 * interval_hours)
            cumulative_energy_import = active_energy_import
            
            # Export energy (for some meters)
            export_factor = 0.3 if random.random() > 0.7 else 0.0
            active_energy_export = cumulative_energy_export + (export_factor * 1.5 * interval_hours)
            cumulative_energy_export = active_energy_export
            
            # Reactive energy (proportional to active)
            reactive_energy_import = active_energy_import * 0.15
            reactive_energy_export = active_energy_export * 0.1
            
            # Voltage (with small variations)
            voltage_phase1 = BASE_VOLTAGE * random.uniform(0.98, 1.02)
            voltage_phase2 = BASE_VOLTAGE * random.uniform(0.98, 1.02)
            voltage_phase3 = BASE_VOLTAGE * random.uniform(0.98, 1.02)
            
            # Current (proportional to load)
            current_phase1 = MAX_CURRENT * current_load_factor * random.uniform(0.95, 1.05)
            current_phase2 = MAX_CURRENT * current_load_factor * random.uniform(0.95, 1.05)
            current_phase3 = MAX_CURRENT * current_load_factor * random.uniform(0.95, 1.05)
            
            # Power factor (near unity with small variations)
            power_factor = random.uniform(0.92, 0.99)
            
            # Maximum demand calculation
            current_demand = current_load_factor * MAX_CURRENT * BASE_VOLTAGE / 1000  # kW
            max_demand = max(max_demand, current_demand * MAX_DEMAND_FACTOR)
            
            # Create measurements entry
            measurement = [
                meter_id, current_time,
                active_energy_import, reactive_energy_import,
                active_energy_export, reactive_energy_export,
                voltage_phase1, voltage_phase2, voltage_phase3,
                current_phase1, current_phase2, current_phase3,
                max_demand, power_factor
            ]
            all_measurements.append(measurement)
            
            # Generate events ---------------------------------------------------------
            # Abnormal condition events
            if has_abnormality and random.random() > 0.95:
                if abnormality_factor > 1.2:
                    event_type = 'VOLTAGE_SWELL'
                    description = f"Voltage swell detected ({voltage_phase1:.1f}V)"
                elif abnormality_factor < 0.8:
                    event_type = 'VOLTAGE_SAG'
                    description = f"Voltage sag detected ({voltage_phase1:.1f}V)"
                elif random.random() > 0.5:
                    event_type = 'CURRENT_IMBALANCE'
                    description = f"Current imbalance ({current_phase1:.1f}A, {current_phase2:.1f}A, {current_phase3:.1f}A)"
                else:
                    event_type = 'PHASE_FAILURE'
                    description = "Phase failure detected"
                
                all_events.append([meter_id, current_time, event_type, description])
            
            # Random events
            if random.random() > 0.995:  # ~0.5% probability per interval
                event_type = random.choice(event_types)
                
                if event_type == 'POWER_OUTAGE':
                    description = "Power outage detected"
                elif event_type == 'TAMPER_DETECTED':
                    description = "Meter tampering detected"
                elif event_type == 'METER_COVER_OPENED':
                    description = "Meter cover opened"
                elif event_type == 'HIGH_TEMPERATURE':
                    description = f"High temperature ({random.randint(45, 70)}°C)"
                elif event_type == 'METER_RESET':
                    description = "Meter reset performed"
                else:
                    description = event_type.replace('_', ' ').title()
                
                all_events.append([meter_id, current_time, event_type, description])
            
            # Move to next interval
            current_time += timedelta(minutes=interval_minutes)
    
    # Create DataFrames
    measurements_df = pd.DataFrame(all_measurements, columns=measurement_columns)
    events_df = pd.DataFrame(all_events, columns=['meter_id', 'timestamp', 'event_type', 'event_description'])
    
    return measurements_df, events_df

def main():
    """Main function to execute the simulation"""
    # User inputs
    num_meters = int(input("Enter number of smart meters: "))
    start_date = input("Enter start date (dd:mm:yyyy HH:MM): ")
    end_date = input("Enter end date (dd:mm:yyyy HH:MM): ")
    interval = int(input("Enter interval in minutes (15 or 30): "))
    
    # Generate data
    measurements, events = generate_smart_meter_data(
        num_meters, start_date, end_date, interval
    )
    
    # Save to CSV
    measurements.to_csv('./smart_meter_measurements.csv', index=False)
    events.to_csv('./smart_meter_events.csv', index=False)
    
    print(f"\nGenerated {len(measurements)} measurements and {len(events)} events")
    print("Files saved:")
    print("- smart_meter_measurements.csv")
    print("- smart_meter_events.csv")
    
    # Display sample data
    print("\nSample measurements:")
    print(measurements.head(3))
    print("\nSample events:")
    print(events.head(3))

if __name__ == "__main__":
    main()