from datetime import ((datetime, timedelta))


class AppointmentCalendar:
    def __init__(self):
        #stores appointments as {date_string: [time_slots]}
        self.calendar = {}

    def add_appointment(self, date_str, time_str, client_name):
        #adds an appointment for a given date and time.
        #date_str: 'YYYY-MM-DD'
        #time_str: 'HH:MM' (24-hour format)
        
        key = date_str
        time_slot = f"{time_str} - {client_name}"

        if key not in self.calendar:
            self.calendar[key] = []

        if any(time_str in slot for slot in self.calendar[key]):
            print("Time slot unavailable.")
            return

        self.calendar[key].append(time_slot)
        print(f" Appointment booked for {date_str} at {time_str} for {client_name}")

    def remove_appointment(self, date_str, time_str):
        #removes an appointment based on date and time.
        
        key = date_str
        if key in self.calendar:
            for i, slot in enumerate(self.calendar[key]):
                if slot.startswith(time_str):
                    removed = self.calendar[key].pop(i)
                    print(f" Appointment removed: {removed}")
                    return
            print("No appointment found at that time.")
        else:
            print("No appointments found on that date.")

    def view_appointments(self, date_str):
        #shows all appointments for a given date.
        
        if date_str in self.calendar:
            print(f"Appointments on {date_str}:")
            for slot in sorted(self.calendar[date_str]):
                print(f" - {slot}")
        else:
            print(f"No appointments found on {date_str}.")



