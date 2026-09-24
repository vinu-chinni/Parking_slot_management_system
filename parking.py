# PARKING SLOT MANAGEMENT SYSTEM
# 1. Park Vehicle
# 2. Display Parking Slots
# 3. Release Vehicle
# 4. Parking History
# 5. Exit

import csv
import os
import sys
from datetime import datetime

FILE = "parking.csv"

TWO_WHEELER_SLOTS = ["A01", "A02", "A03"]
FOUR_WHEELER_SLOTS = ["B01", "B02", "B03"]


def get_input(message):
    sys.stdout.write(message)
    sys.stdout.flush()
    return sys.stdin.readline().strip()


class ParkingSystem:

    def __init__(self):
        self.create_file()

    def create_file(self):
        if not os.path.exists(FILE):
            with open(FILE, "w") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "vehicle_no",
                    "owner",
                    "vehicle_type",
                    "slot",
                    "time",
                    "status"
                ])

    def park_vehicle(self):

        print("\n--- PARK VEHICLE ---")

        vehicle_no = get_input("Enter Vehicle Number: ").upper()
        owner = get_input("Enter Owner Name: ")

        print("\n1. Two Wheeler")
        print("2. Four Wheeler")

        vehicle_choice = get_input("Enter Vehicle Type: ")

        if vehicle_choice == "1":
            vehicle_type = "Two Wheeler"
            slots = TWO_WHEELER_SLOTS

        elif vehicle_choice == "2":
            vehicle_type = "Four Wheeler"
            slots = FOUR_WHEELER_SLOTS

        else:
            print("Invalid vehicle type")
            return

        print("Available Slots:", slots)

        slot = get_input("Enter Parking Slot: ").upper()

        if slot not in slots:
            print("Invalid slot for this vehicle type")
            return

        with open(FILE, "r") as file:
            records = list(csv.DictReader(file))

        for row in records:

            if row["slot"].upper() == slot and row["status"] == "Parked":
                print("Slot already occupied")
                return

            if row["vehicle_no"].upper() == vehicle_no and row["status"] == "Parked":
                print("Vehicle already parked")
                return

        with open(FILE, "a") as file:

            writer = csv.writer(file)

            writer.writerow([
                vehicle_no,
                owner,
                vehicle_type,
                slot,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Parked"
            ])

        print("Vehicle parked successfully")


    def display_slots(self):

        occupied = []

        with open(FILE, "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["status"] == "Parked":
                    occupied.append(row["slot"].upper())

        print("\n--- TWO WHEELER SLOTS ---")

        for slot in TWO_WHEELER_SLOTS:

            if slot in occupied:
                print(slot, "- Occupied")
            else:
                print(slot, "- Available")

        print("\n--- FOUR WHEELER SLOTS ---")

        for slot in FOUR_WHEELER_SLOTS:

            if slot in occupied:
                print(slot, "- Occupied")
            else:
                print(slot, "- Available")


    def release_vehicle(self):

        print("\n--- RELEASE VEHICLE ---")

        vehicle_no = get_input("Enter Vehicle Number: ").upper()

        with open(FILE, "r") as file:
            records = list(csv.DictReader(file))

        found = False

        for row in records:

            if (
                row["vehicle_no"].upper() == vehicle_no
                and row["status"] == "Parked"
            ):

                row["status"] = "Released"
                found = True
                break

        if found:

            with open(FILE, "w") as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "vehicle_no",
                        "owner",
                        "vehicle_type",
                        "slot",
                        "time",
                        "status"
                    ]
                )

                writer.writeheader()
                writer.writerows(records)

            print("Vehicle released successfully")

        else:

            print("Vehicle not found")


    def parking_history(self):

        print("\n--- PARKING HISTORY ---")

        with open(FILE, "r") as file:

            records = list(csv.DictReader(file))

        if not records:

            print("No parking history found")
            return

        for row in records:

            print(
                row["vehicle_no"],
                "-",
                row["owner"],
                "-",
                row["vehicle_type"],
                "-",
                row["slot"],
                "-",
                row["time"],
                "-",
                row["status"]
            )


parking = ParkingSystem()


while True:

    print("\n===== PARKING SLOT MANAGEMENT =====")
    print("1. Park Vehicle")
    print("2. Display Parking Slots")
    print("3. Release Vehicle")
    print("4. Parking History")
    print("5. Exit")

    choice = get_input("Enter your choice: ")

    if choice == "1":

        parking.park_vehicle()

    elif choice == "2":

        parking.display_slots()

    elif choice == "3":

        parking.release_vehicle()

    elif choice == "4":

        parking.parking_history()

    elif choice == "5":

        print("Thank you")
        break

    else:

        print("Invalid choice")