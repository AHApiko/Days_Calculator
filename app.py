import tkinter as tk
from datetime import datetime, timedelta

class AddDaysApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Add Days to Date")

        # Define bank holidays dictionaries for Barcelona and Madrid
        self.bank_holidays_barcelona = {
            "01-01-2024": "Año Nuevo",
            "06-01-2024": "Epifania del Señor",
            "29-03-2024": "Viernes Santo",
            "01-05-2024": "Fiesta del trabajo",
            "15-08-2024": "Asunción de la Virgen",
            "12-10-2024": "Fiesta Nacional de España",
            "01-11-2024": "Todos los Santos",
            "06-12-2024": "Día de la Constitución Española",
            "25-12-2024": "Natividad del Señor",
            "01-04-2024": "Lunes de Pascua",
            "24-06-2024": "San Juan",
            "11-09-2024": "Fiesta Nacional de Cataluña",
            "26-12-2024": "San Esteban",
            "20-05-2024": "Fiesta Local"
        }

        self.bank_holidays_madrid = {
            "01-01-2024": "Año Nuevo",
            "06-01-2024": "Epifania del Señor",
            "29-03-2024": "Viernes Santo",
            "01-05-2024": "Fiesta del trabajo",
            "15-08-2024": "Asunción de la Virgen",
            "12-10-2024": "Fiesta Nacional de España",
            "01-11-2024": "Todos los Santos",
            "06-12-2024": "Día de la Constitución Española",
            "25-12-2024": "Natividad del Señor",
            "28-03-2024": "Jueves Santo",
            "02-05-2024": "Fiesta de la Comunidad de Madrid",
            "25-07-2024": "Santiago Apóstol"
        }

        # Create labels and entry fields
        self.date_label = tk.Label(master, text="Enter first day of absence (DD-MM-YYYY):")
        self.date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        self.days_label = tk.Label(master, text="Enter the total number of days/weeks of absence:")
        self.days_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.days_entry = tk.Entry(master)
        self.days_entry.grid(row=1, column=1, padx=5, pady=5)

        # Add options for the user to select the type of days to add
        self.days_type_label = tk.Label(master, text="Select type:")
        self.days_type_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.days_type_var = tk.StringVar()
        self.days_type_var.set("Natural Days")
        self.days_type_option = tk.OptionMenu(master, self.days_type_var, "Natural Days", "Natural Weeks", "Working Days")
        self.days_type_option.grid(row=2, column=1, padx=5, pady=5)

        # Create option menu for selecting location
        self.location_var = tk.StringVar()
        self.location_var.set("Madrid")  # Default location
        self.location_label = tk.Label(master, text="Select Location:")
        self.location_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.location_option = tk.OptionMenu(master, self.location_var, "Madrid", "Barcelona", command=self.update_bank_holidays)
        self.location_option.grid(row=3, column=1, padx=5, pady=5)

        # Create button to add days
        self.add_days_button = tk.Button(master, text="Add", command=self.add_days)
        self.add_days_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Create reset button
        self.reset_button = tk.Button(master, text="Reset", command=self.reset_data)
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Create label to display result
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

        # Create label to display bank holidays
        self.bank_holidays_label = tk.Label(master, text="")
        self.bank_holidays_label.grid(row=7, column=0, columnspan=2, pady=5)

        # Update bank holidays based on the default location
        self.update_bank_holidays()

    def update_bank_holidays(self, *args):
        # Update bank holidays based on the selected location
        location = self.location_var.get()
        if location == "Madrid":
            self.bank_holidays = self.bank_holidays_madrid
        elif location == "Barcelona":
            self.bank_holidays = self.bank_holidays_barcelona

    def add_days(self):
        # Get user input
        user_date = self.date_entry.get()
        days_to_add = int(self.days_entry.get())
        days_type = self.days_type_var.get()

        try:
            # Convert user input to datetime object
            date_object = datetime.strptime(user_date, '%d-%m-%Y')

            # Check if the year is 2024
            if date_object.year != 2024:
                raise ValueError("Please select a date in the year 2024.")
            
            # Calculate the new date based on the selected option
            new_date = self.calculate_new_date(date_object, days_to_add, days_type)

            # Display the result
            self.result_label.config(text=f"First day back at work: {new_date.strftime('%d-%m-%Y')}")

           # Display bank holidays between initial date and result date
            bank_holidays_between = self.get_bank_holidays_between(date_object, new_date)
            if bank_holidays_between:
                self.bank_holidays_label.config(text=f"Bank Holidays in between:\n{bank_holidays_between}")
            else:
                self.bank_holidays_label.config(text="No bank holidays between the dates.")

        except ValueError as e:
            # Handle invalid date format
            if "year" in str(e):
                self.result_label.config(text=str(e))
            else:    
                self.result_label
                
    def calculate_new_date(self, date_object, days_to_add, days_type):
        if days_type == "Natural Days":
            return date_object + timedelta(days=days_to_add)
        elif days_type == "Natural Weeks":
            return date_object + timedelta(weeks=days_to_add)
        elif days_type == "Working Days":
            new_date = date_object
            while days_to_add > 0:
                new_date += timedelta(days=1)
                if new_date.weekday() in [5, 6] or new_date.strftime("%d-%m-%Y") in self.bank_holidays:
                    continue
                days_to_add -= 1  # Decrement days_to_add when a working day is added
            return new_date

    def get_bank_holidays_between(self, start_date, end_date):
        bank_holidays_between = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.strftime("%d-%m-%Y") in self.bank_holidays:
                bank_holidays_between.append(f"{current_date.strftime('%d-%m-%Y')}: {self.bank_holidays[current_date.strftime('%d-%m-%Y')]}")
            current_date += timedelta(days=1)
        return bank_holidays_between
    
    def reset_data(self):
        # Reset entry fields and labels
        self.date_entry.delete(0, tk.END)
        self.days_entry.delete(0, tk.END)
        self.days_type_var.set("Natural Days")
        self.result_label.config(text="")
        self.bank_holidays_label.config(text="")    

root = tk.Tk()
app = AddDaysApp(root)
root.mainloop()