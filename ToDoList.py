#Name: Thomas
#Date: 6/7/2026
#Description: This program manages a simple to-do list with appointment reminders.

from datetime import datetime
import threading
import time

# Global variables
KeepRunning = False  
agenda = []

# Appointment class to hold the details of each appointment
class Appointment:

    def __init__(self, date, time, description):
        self.date = date
        self.time = time
        self.description = description

# Clock function that runs in the background and checks for appointments
def clock():
    global KeepRunning
    print("\nEntering waiting mode. Enter 'exit' to stop waiting.\n")

    while KeepRunning:
        current_dt = datetime.now()
        now_time = current_dt.strftime("%H:%M")
        now_date = current_dt.strftime("%Y-%m-%d")

        # Live clock display (adding seconds here just for visuals)
        live_display = current_dt.strftime("%H:%M:%S")
        print(f"Current Time: {live_display}", end="\r", flush=True)

        # Check for appointments that match the current date and time
        for appt in agenda:
            if (now_time == appt.time) and (now_date == appt.date):
                print(
                    f"\n\n[REMINDER]: {appt.description} is happening NOW!\n"
                )
                agenda.remove(appt)  # Remove the appointment after reminding

        time.sleep(1)

# Main menu function to interact with the user
def main():
    global KeepRunning
    global agenda

    while True:
        print("--- MAIN MENU ---")
        print("1. Add appointment")
        print("2. View appointments")
        print("3. Wait for appointments")
        print("4. Exit program")

        choice = input("Enter your choice: ")
        
        # Add appointment
        if choice == "1":
            #Qol feature 
            print ("Use today's date? (Y/N)")
            use_today = input().upper()
            if use_today == "Y":
                date = datetime.now().strftime("%Y-%m-%d")
            else:
                date = input("Enter date (YYYY-MM-DD): ")
            time_input = input("Enter time (HH:MM): ")
            description = input("Enter description: ")

            appointment = Appointment(date, time_input, description)
            agenda.append(appointment)
            print("Appointment added!\n")

        # View appointments
        elif choice == "2":
            if not agenda:
                print("No appointments scheduled.\n")
            else:
                print("\nYour Agenda:")
                for i, appointment in enumerate(agenda):
                    print(
                        f"{i + 1}. {appointment.date} @ {appointment.time} - {appointment.description}"
                    )
                print()
        
        # The waiting mode starts a background thread that checks for appointments while allowing the user to exit back to the main menu
        elif choice == "3":
            KeepRunning = True
            # Start the clock on a background thread
            clock_thread = threading.Thread(target=clock, daemon=True)
            clock_thread.start()

            # The main thread stays here and watches for the 'exit' command
            while True:
                user_signal = input()
                if user_signal.lower() == "exit":
                    KeepRunning = (
                        False  # Stops the background clock loop safely
                    )
                    print("Returning to Main Menu...\n")
                    break
        #exit program
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()