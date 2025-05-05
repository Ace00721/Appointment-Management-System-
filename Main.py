"""
Appointment Management System - GUI Application

This module defines the `LoginApp` class, which provides a graphical interface for managing appointments
using the Tkinter library. The application supports user authentication, appointment booking, and role-based
access control (admin and client).
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Authentication import AuthManager
from database import DatabaseManager
import datetime
import calendar

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Management System")
        self.root.geometry("500x650")
        self.root.configure(bg="#f5f5f5")
        self.auth = AuthManager()
        self.db = DatabaseManager()
        self.user_role = None
        self.username = None

        self.login_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.register_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.dashboard_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.calendar_frame = None
        self.time_buttons_frame = None

        self.inactivity_timeout = 5 * 60 * 1000  # 5 minutes in milliseconds
        self.inactivity_job = None

        self.setup_login_frame()

    def clear_frames(self):
        for frame in [self.login_frame, self.register_frame, self.dashboard_frame]:
            frame.pack_forget()

    def clear_frame_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def styled_label(self, frame, text):
        return tk.Label(frame, text=text, font=("Segoe UI", 10), bg="#f5f5f5")

    def styled_entry(self, frame):
        return ttk.Entry(frame, width=30)

    def styled_button(self, frame, text, command, style=None):
        return ttk.Button(frame, text=text, command=command, style=style)

    def setup_login_frame(self):
        self.clear_frames()
        self.clear_frame_widgets(self.login_frame)
        self.login_frame.pack(padx=10, pady=10)

        self.styled_label(self.login_frame, "Username:").pack(pady=(5, 0))
        self.login_username = self.styled_entry(self.login_frame)
        self.login_username.pack()

        self.styled_label(self.login_frame, "Password:").pack(pady=(5, 0))
        self.login_password = self.styled_entry(self.login_frame)
        self.login_password.config(show="*")
        self.login_password.pack()

        self.styled_button(self.login_frame, "Login", self.login).pack(pady=10)
        self.styled_button(self.login_frame, "Go to Register", self.setup_register_frame).pack()

    def reset_inactivity_timer(self, event=None):
        if self.inactivity_job:
            self.root.after_cancel(self.inactivity_job)
        self.inactivity_job = self.root.after(self.inactivity_timeout, self.auto_logout)

    def auto_logout(self):
        messagebox.showinfo("Logged Out", "You have been logged out due to inactivity.")
        self.logout()

    def setup_register_frame(self):
        self.clear_frames()
        self.clear_frame_widgets(self.register_frame)
        self.register_frame.pack(padx=10, pady=10)

        self.styled_label(self.register_frame, "Username:").pack(pady=(5, 0))
        self.register_username = self.styled_entry(self.register_frame)
        self.register_username.pack()

        self.styled_label(self.register_frame, "Password:").pack(pady=(5, 0))
        self.register_password = self.styled_entry(self.register_frame)
        self.register_password.config(show="*")
        self.register_password.pack()

        self.styled_label(self.register_frame, "Role (admin/client):").pack(pady=(5, 0))
        self.register_role = self.styled_entry(self.register_frame)
        self.register_role.pack()

        self.styled_button(self.register_frame, "Register", self.register).pack(pady=10)
        self.styled_button(self.register_frame, "Go to Login", self.setup_login_frame).pack()

    def show_dashboard(self):
        self.clear_frames()
        self.clear_frame_widgets(self.dashboard_frame)
        self.dashboard_frame.pack(padx=10, pady=10)

        self.root.bind_all("<Any-KeyPress>", self.reset_inactivity_timer)
        self.root.bind_all("<Any-Button>", self.reset_inactivity_timer)
        self.root.bind_all("<Motion>", self.reset_inactivity_timer)
        self.reset_inactivity_timer()  # Start the timer

        self.styled_button(self.dashboard_frame, "Log Out", self.logout, style="Danger.TButton").pack(pady=(0, 10))
        self.styled_label(self.dashboard_frame, f"Welcome {self.username}! ({self.user_role})").pack(pady=(0, 10))

        if self.user_role == "client":
            self.styled_button(self.dashboard_frame, "My Appointments", self.view_my_appointments).pack(pady=5)
        elif self.user_role == "admin":
            self.styled_button(self.dashboard_frame, "View All Appointments", self.view_all_appointments).pack(pady=5)

        self.styled_label(self.dashboard_frame, "Book an Appointment").pack(pady=(10, 0))
        self.show_calendar()

    def logout(self):
        if self.inactivity_job:
            self.root.after_cancel(self.inactivity_job)
            self.inactivity_job = None
        self.root.unbind_all("<Any-KeyPress>")
        self.root.unbind_all("<Any-Button>")
        self.root.unbind_all("<Motion>")
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.username = None
            self.user_role = None
            self.setup_login_frame()

    def show_calendar(self):
        if self.calendar_frame:
            self.calendar_frame.destroy()
        self.calendar_frame = tk.Frame(self.dashboard_frame, bg="#f5f5f5")
        self.calendar_frame.pack()

        now = datetime.datetime.now()
        year = now.year
        month = now.month

        month_days = calendar.monthcalendar(year, month)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, bg="#f5f5f5", font=("Segoe UI", 9, "bold")).grid(row=0, column=i)

        for row_idx, week in enumerate(month_days):
            for col_idx, day in enumerate(week):
                if day != 0:
                    btn = tk.Button(self.calendar_frame, text=str(day), width=4,
                                    command=lambda d=day: self.show_time_slots(year, month, d))
                    btn.grid(row=row_idx + 1, column=col_idx, padx=2, pady=2)

    def show_time_slots(self, year, month, day):
        if self.time_buttons_frame:
            self.time_buttons_frame.destroy()
        self.time_buttons_frame = tk.Frame(self.dashboard_frame, bg="#f5f5f5")
        self.time_buttons_frame.pack(pady=10)

        self.selected_date = f"{month:02d}-{day:02d}"
        self.styled_label(self.time_buttons_frame, f"Available Time Slots for {self.selected_date}:").pack()

        appointments = self.db.get_appointments()
        booked_times = [appt[3] for appt in appointments if appt[2] == self.selected_date]

        for hour in range(9, 17):
            time_str = f"{hour}:00 AM" if hour < 12 else f"{hour - 12 if hour > 12 else 12}:00 PM"
            state = tk.NORMAL if time_str not in booked_times else tk.DISABLED
            ttk.Button(self.time_buttons_frame, text=time_str,
                       command=lambda t=time_str: self.select_service_and_provider(t), state=state).pack(pady=2)

    def select_service_and_provider(self, selected_time):
        top = tk.Toplevel(self.root)
        top.title("Select Service and Provider")

        services = {
            "Haircut": {"provider": "Alice", "price": 30},
            "Massage": {"provider": "Bob", "price": 60},
            "Manicure": {"provider": "Clara", "price": 25}
        }

        tk.Label(top, text="Select Service:").pack(pady=5)
        service_var = tk.StringVar()
        service_dropdown = ttk.Combobox(top, textvariable=service_var, values=list(services.keys()), state="readonly")
        service_dropdown.pack(pady=5)

        details_label = tk.Label(top, text="")
        details_label.pack(pady=5)

        def update_details(event):
            service = service_var.get()
            if service:
                provider = services[service]["provider"]
                price = services[service]["price"]
                details_label.config(text=f"Provider: {provider}\nPrice: ${price}")

        service_dropdown.bind("<<ComboboxSelected>>", update_details)

        def confirm_service():
            selected_service = service_var.get()
            if not selected_service:
                messagebox.showerror("Error", "Please select a service.")
                return
            provider = services[selected_service]["provider"]
            price = services[selected_service]["price"]
            top.destroy()
            self.confirm_booking(self.selected_date, selected_time, selected_service, provider, price)

        ttk.Button(top, text="Confirm", command=confirm_service).pack(pady=10)

    def confirm_booking(self, date, time, service, provider, price):
        appointments = self.db.get_appointments()
        for appt in appointments:
            if appt[2] == date and appt[3] == time:
                messagebox.showerror("Conflict", f"Appointment already exists on {date} at {time}.")
                return

        if self.user_role == "client":
            clients = self.db.get_clients()
            client_ids = [c[0] for c in clients if c[1] == self.username]
            if client_ids:
                client_id = client_ids[0]
            else:
                self.db.add_client(self.username, "")
                client_id = self.db.get_clients()[-1][0]
            self.db.add_appointment(client_id, date, time)
            messagebox.showinfo("Success",
                                f"Appointment booked for {date} at {time}.\nService: {service}\nProvider: {provider}\nPrice: ${price}")
            self.show_time_slots(datetime.datetime.now().year, datetime.datetime.now().month, int(date.split('-')[1]))

        elif self.user_role == "admin":
            top = tk.Toplevel(self.root)
            top.title("Client Info")

            tk.Label(top, text="Client Name:").pack()
            name_entry = ttk.Entry(top)
            name_entry.pack()

            tk.Label(top, text="Client Contact Info:").pack()
            contact_entry = ttk.Entry(top)
            contact_entry.pack()

            def submit_info():
                client_name = name_entry.get()
                client_contact = contact_entry.get()
                self.db.add_client(client_name, client_contact)
                client_id = self.db.get_clients()[-1][0]
                self.db.add_appointment(client_id, date, time)
                messagebox.showinfo("Success",
                                    f"Appointment booked for {client_name} on {date} at {time}.\nService: {service}\nProvider: {provider}\nPrice: ${price}")
                top.destroy()
                self.show_time_slots(datetime.datetime.now().year, datetime.datetime.now().month, int(date.split('-')[1]))

            ttk.Button(top, text="Confirm", command=submit_info).pack(pady=5)

    def view_my_appointments(self):
        top = tk.Toplevel(self.root)
        top.title("My Appointments")

        clients = self.db.get_clients()
        client_ids = [c[0] for c in clients if c[1] == self.username]
        if client_ids:
            client_id = client_ids[0]
            appointments = self.db.get_client_appointments(client_id)

            now = datetime.datetime.now()
            appointments.sort(
                key=lambda appt: datetime.datetime.strptime(f"{now.year}-{appt[2]} {appt[3]}", "%Y-%m-%d %I:%M %p"))

            for appt in appointments:
                date_obj = datetime.datetime.strptime(f"{now.year}-{appt[2]}", "%Y-%m-%d")
                date_str = date_obj.strftime("%B %d")
                appt_text = f"{date_str} at {appt[3]}"
                frame = tk.Frame(top)
                frame.pack(fill='x', pady=2)
                tk.Label(frame, text=appt_text, width=30, anchor='w').pack(side='left')
                ttk.Button(frame, text="Cancel", command=lambda a_id=appt[0]: self.confirm_cancel(a_id, top)).pack(side='right')
        else:
            tk.Label(top, text="No appointments found.").pack()

    def view_all_appointments(self):
        top = tk.Toplevel(self.root)
        top.title("All Appointments")

        appointments = self.db.get_appointments()

        now = datetime.datetime.now()
        appointments.sort(
            key=lambda appt: datetime.datetime.strptime(f"{now.year}-{appt[2]} {appt[3]}", "%Y-%m-%d %I:%M %p"))

        for appt in appointments:
            date_obj = datetime.datetime.strptime(f"{now.year}-{appt[2]}", "%Y-%m-%d")
            date_str = date_obj.strftime("%B %d")
            appt_text = f"ClientID {appt[1]}: {date_str} at {appt[3]}"
            frame = tk.Frame(top)
            frame.pack(fill='x', pady=2)
            tk.Label(frame, text=appt_text, width=40, anchor='w').pack(side='left')
            ttk.Button(frame, text="Delete", command=lambda a_id=appt[0]: self.confirm_delete(a_id, top)).pack(side='right')

    def confirm_cancel(self, appointment_id, top_window):
        if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this appointment?"):
            self.db.delete_appointment(appointment_id)
            messagebox.showinfo("Cancelled", "Appointment cancelled successfully.")
            top_window.destroy()
            self.view_my_appointments()

    def confirm_delete(self, appointment_id, top_window):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?"):
            self.db.delete_appointment(appointment_id)
            messagebox.showinfo("Deleted", "Appointment deleted successfully.")
            top_window.destroy()
            self.view_all_appointments()

    def register(self):
        username = self.register_username.get()
        password = self.register_password.get()
        role = self.register_role.get().lower()
        if role not in ["admin", "client"]:
            messagebox.showerror("Error", "Role must be 'admin' or 'client'")
            return
        self.auth.register(username, password, role)
        self.setup_login_frame()

    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        role = self.auth.login(username, password)
        if role:
            self.user_role = role
            self.username = username
            self.show_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Danger.TButton", foreground="white", background="#d9534f")
    app = LoginApp(root)
    root.mainloop()
