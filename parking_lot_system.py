#!/usr/bin/env python3
"""
Parking Lot Management System
A console-based application for managing vehicle entry and exit records using file handling.

Features:
- Vehicle Entry with automatic time recording
- Vehicle Exit with automatic time recording  
- Display all parking records
- File-based data persistence
- Error handling and validation
- Duplicate entry prevention
- Clean formatted output
"""

import os
import datetime
import sys

# Constants
PARKING_FILE = "parking_records.txt"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_current_time():
    """Get current timestamp in formatted string."""
    return datetime.datetime.now().strftime(TIME_FORMAT)


def file_exists():
    """Check if parking records file exists."""
    return os.path.exists(PARKING_FILE)


def create_file_if_not_exists():
    """Create parking records file if it doesn't exist."""
    if not file_exists():
        try:
            with open(PARKING_FILE, 'w') as f:
                f.write("VehicleNumber,Time,Status\n")  # Header row
            print(f"Created new parking records file: {PARKING_FILE}")
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    return True


def is_vehicle_parked(vehicle_number):
    """
    Check if a vehicle is currently parked (has IN but no OUT record).
    
    Args:
        vehicle_number (str): The vehicle number to check
        
    Returns:
        bool: True if vehicle is parked, False otherwise
    """
    if not file_exists():
        return False
    
    try:
        with open(PARKING_FILE, 'r') as f:
            lines = f.readlines()
        
        # Count IN and OUT records for this vehicle
        in_count = 0
        out_count = 0
        
        for line in lines[1:]:  # Skip header
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    file_vehicle_number = parts[0].strip()
                    status = parts[2].strip().upper()
                    
                    if file_vehicle_number.upper() == vehicle_number.upper():
                        if status == 'IN':
                            in_count += 1
                        elif status == 'OUT':
                            out_count += 1
        
        # Vehicle is parked if there are more IN records than OUT records
        return in_count > out_count
        
    except Exception as e:
        print(f"Error checking vehicle status: {e}")
        return False


def record_vehicle_entry():
    """Record vehicle entry with current timestamp."""
    print("\n" + "="*50)
    print("VEHICLE ENTRY")
    print("="*50)
    
    # Get vehicle number from user
    vehicle_number = input("Enter Vehicle Number: ").strip()
    
    if not vehicle_number:
        print("Error: Vehicle number cannot be empty!")
        return
    
    # Check if vehicle is already parked
    if is_vehicle_parked(vehicle_number):
        print(f"Error: Vehicle {vehicle_number} is already parked!")
        print("Please record exit before entering again.")
        return
    
    # Get current time
    current_time = get_current_time()
    
    # Write to file
    try:
        with open(PARKING_FILE, 'a') as f:
            f.write(f"{vehicle_number},{current_time},IN\n")
        
        print(f"✓ Vehicle Entry Recorded Successfully!")
        print(f"  Vehicle Number: {vehicle_number}")
        print(f"  Entry Time: {current_time}")
        
    except Exception as e:
        print(f"Error recording entry: {e}")


def record_vehicle_exit():
    """Record vehicle exit with current timestamp."""
    print("\n" + "="*50)
    print("VEHICLE EXIT")
    print("="*50)
    
    # Get vehicle number from user
    vehicle_number = input("Enter Vehicle Number: ").strip()
    
    if not vehicle_number:
        print("Error: Vehicle number cannot be empty!")
        return
    
    # Check if vehicle exists and is parked
    if not is_vehicle_parked(vehicle_number):
        print(f"Error: Vehicle {vehicle_number} is not currently parked!")
        print("Please record entry first.")
        return
    
    # Get current time
    current_time = get_current_time()
    
    # Write to file
    try:
        with open(PARKING_FILE, 'a') as f:
            f.write(f"{vehicle_number},{current_time},OUT\n")
        
        print(f"✓ Vehicle Exit Recorded Successfully!")
        print(f"  Vehicle Number: {vehicle_number}")
        print(f"  Exit Time: {current_time}")
        
    except Exception as e:
        print(f"Error recording exit: {e}")


def display_parking_records():
    """Display all parking records in a formatted table."""
    print("\n" + "="*80)
    print("PARKING RECORDS")
    print("="*80)
    
    if not file_exists():
        print("No parking records found. File does not exist.")
        return
    
    try:
        with open(PARKING_FILE, 'r') as f:
            lines = f.readlines()
        
        if len(lines) <= 1:  # Only header exists
            print("No parking records found.")
            return
        
        # Print table header
        print(f"{'Vehicle Number':<15} {'Time':<20} {'Status':<10}")
        print("-" * 80)
        
        # Print records (skip header)
        for line in lines[1:]:
            if line.strip():
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    vehicle_number = parts[0].strip()
                    time = parts[1].strip()
                    status = parts[2].strip().upper()
                    
                    # Color coding for status
                    if status == 'IN':
                        status_display = f"IN"
                    elif status == 'OUT':
                        status_display = f"OUT"
                    else:
                        status_display = status
                    
                    print(f"{vehicle_number:<15} {time:<20} {status_display:<10}")
        
        print("-" * 80)
        print(f"Total Records: {len(lines) - 1}")
        
    except Exception as e:
        print(f"Error reading parking records: {e}")


def show_menu():
    """Display the main menu and get user choice."""
    print("\n" + "="*50)
    print("PARKING LOT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Vehicle Entry")
    print("2. Vehicle Exit") 
    print("3. Show Parking Records")
    print("4. Exit")
    print("-" * 50)
    
    try:
        choice = int(input("Enter your choice (1-4): "))
        return choice
    except ValueError:
        print("Error: Please enter a valid number (1-4)!")
        return None


def main():
    """Main function to run the parking lot management system."""
    print("Welcome to Parking Lot Management System!")
    
    # Ensure file exists
    if not create_file_if_not_exists():
        print("Error: Cannot create or access parking records file. Exiting...")
        sys.exit(1)
    
    while True:
        choice = show_menu()
        
        if choice is None:
            continue
        
        if choice == 1:
            record_vehicle_entry()
        elif choice == 2:
            record_vehicle_exit()
        elif choice == 3:
            display_parking_records()
        elif choice == 4:
            print("\nThank you for using Parking Lot Management System!")
            print("Goodbye!")
            break
        else:
            print("Error: Invalid choice! Please enter a number between 1 and 4.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()