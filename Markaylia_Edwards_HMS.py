# Markaylia Edwards 
# Programming Techniques ITT103
# University of the Commonwealth Caribbean
# Summer 2025
# Richard's Memorial Hospital Management System - OOP

import random
import re
import string

# Class to represent doctor specialty
class Doctor:
    doctors_list = {}  # Store all doctors by ID in a dictionary


# Intializes doctors with a name, specialty and unique ID
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty
        self.doctor_id = self.generate_doctor_id()
        Doctor.doctors_list[self.doctor_id] = self

# Generate a random, unique 4-digit doctor ID
    def generate_doctor_id(self):
        while True:
            unique_id = 'D-' + ''.join(random.choices(string.digits, k=4))
            if unique_id not in Doctor.doctors_list:
                return unique_id

# Class method to register and add a doctor.
    @classmethod
    def add_doctor(cls, name, specialty):
        doctor = Doctor(name, specialty)
        print(f"Doctor {name} ({specialty}) added with ID: {doctor.doctor_id}")
        
# List registered doctors and their specialties
    @classmethod
    def list_doctors(cls):
        if not cls.doctors_list:
            print("No Doctors Available.")
            return
        print("\n--- Available doctors ---")
        for doc_id, doc in cls.doctors_list.items():
            print(f"ID: {doc_id}, Name: {doc.name}, Specialty: {doc.specialty}")

    def is_available(self, date, time):
        for appt in Appointment.appointments_list:
            if appt.doctor_id == self.doctor_id and appt.date == date and appt.time == time:
                return False # Doctor already has apointment at this time.
        return True # Doctor is available

# Class to represent patients

class Patient:
    patients_list = {} #Store all patients by ID in a dictionary

# Intializes doctors with a name, specialty and unique ID
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.patient_id = self.generate_patient_id()
        Patient.patients_list[self.patient_id] = self

# Generate a random, unique 4-digit patient ID
    def generate_patient_id(self):
        while True:
            unique_id = 'P-' + ''.join(random.choices(string.digits, k=4))
            if unique_id not in Patient.patients_list:
                return unique_id

# Method to add patient and its validation check
    @classmethod
    def add_patient(cls, name, age, gender):
        if not name.replace(" ", "").isalpha():
            print("Error: Name must contain only alphabetic characters.")
            return None
        if not re.fullmatch(r"[A-Za-z ]+", name):
            print("Invalid name. Only letters and spaces are allowed.")
            return
        
        if not (0 < age <= 120):
            print("Error: Age must be between 1 and 120.")
            return None
        if gender.lower() not in ['male', 'female']:
            print("Error: Gender must be Male or Female.")
            return None

        patient = cls(name, age, gender)
        print(f"Patient {name} added successfully with ID: {patient.patient_id}")
        return patient

# Method to list patients
    @classmethod
    def list_patients(cls):
        if not cls.patients_list:
            print("No patients registered yet.")
            return
        print("\n--- Registered Patients ---")
        for pid, patient in cls.patients_list.items():
            print(f"ID: {pid}, Name: {patient.name}, Age: {patient.age}, Gender: {patient.gender}")

# Class to manage Appointments
class Appointment:
    appointments_list = [] # Appointments stored in a list.

# Initializes an appointment with all the necessary info.
    def __init__(self, patient_id, doctor_id, date, time):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.appointment_id = self.generate_appointment_id()

# Generate appointment info.
    def generate_appointment_id(self):
        return 'A-' + ''.join(random.choices(string.digits, k=5))

# Generate a random apppointment ID and validates that time is entered in 24-hour format.
    @classmethod
    def validate_time(cls, time_str):
        return bool(re.match(r'^([01]\d|2[0-3]):[0-5]\d$', time_str))

    @classmethod
    def book_appointment(cls, patient_id, doctor_id, date, time):
        if patient_id not in Patient.patients_list:
            print("Error: Invalid Patient ID.")
            return
        if doctor_id not in Doctor.doctors_list:
            print("Error: Invalid Doctor ID.")
            return
        if not date.strip():
            print("Error: Date cannot be empty.")
            return
        if not cls.validate_time(time):
            print("Error: Time must be in HH:MM (24-hour) format.")
            return
        
 # Check availiablity before booking
        doctor = Doctor.doctors_list[doctor_id]
        if not doctor.is_available(date, time):
            print(f"\nDr. {doctor.name} is not available on {date} at {time}. Please choose a different time.\n")
            return

        appointment = cls(patient_id, doctor_id, date, time)
        cls.appointments_list.append(appointment)
        print("\nAppointment booked successfully!\n")
        cls.print_bill(appointment)

# Method to view doctor schedule
    @classmethod
    def view_schedule(cls, doctor_id):
        if doctor_id not in Doctor.doctors_list:
            print("\nInvalid Doctor ID.\n")
            return

        doctor = Doctor.doctors_list[doctor_id]
        print(f"\n--- Schedule for Dr. {doctor.name} ({doctor.specialty}) ---")
        appointments_found = False

        sorted_appts = sorted(
            [a for a in cls.appointments_list if a.doctor_id == doctor_id],
            key=lambda x: (x.date, x.time)
        )

        for appt in sorted_appts:
            patient = Patient.patients_list[appt.patient_id]
            print(f"- {appt.date} at {appt.time} | Patient: {patient.name} | Appointment ID: {appt.appointment_id}")
            appointments_found = True

        if not appointments_found:
            print("No appointments scheduled for this doctor.\n")

# If valid, appointment is created and stored.
    @classmethod
    def list_appointments(cls):
        if not cls.appointments_list:
            print("No appointments booked yet.")
            return
        print("\n--- All Appointments ---")
        for appt in cls.appointments_list:
            patient = Patient.patients_list[appt.patient_id]
            doctor = Doctor.doctors_list[appt.doctor_id]
            print(f"Appointment ID: {appt.appointment_id} | Date: {appt.date} | Time: {appt.time} | "
                  f"Patient: {patient.name} | Doctor: {doctor.name} ({doctor.specialty})")

# Info for bill with appointment info
    @classmethod
    def print_bill(cls, appointment):
        hospital_name = "Richard's Memorial"
        address = "24 Cargill Avenue"
        phone = "(876) 743-4021"
        tagline = "Where care is constant"

        patient = Patient.patients_list[appointment.patient_id]
        doctor = Doctor.doctors_list[appointment.doctor_id]


# Hospital details with layout details

        print("\n" + "="*50)
        print(f"{hospital_name:^50}")
        print(f"{address:^50}")
        print(f"Tel: {phone:^39}")
        print(f"'{tagline}'".center(50))
        print("="*50)
        print(f"Bill No.: {appointment.appointment_id}")
        print(f"Patient Name : {patient.name}")
        print(f"Doctor Name  : {doctor.name} ({doctor.specialty})")
        print(f"Date         : {appointment.date}")
        print(f"Time         : {appointment.time}")
        print("="*50)
        print(f"Consultation Fee: {'$3000' :>32}")
        print("="*50)
        print("Thank you for choosing Richard's Memorial Hospital!".center(50))
        print("="*50 + "\n")

# To cancel appointments previously made
    @classmethod
    def cancel_appointment(cls, appointment_id):
        for appt in cls.appointments_list:
            if appt.appointment_id == appointment_id:
                cls.appointments_list.remove(appt)
                print(f"\nAppointment ID {appointment_id} has been cancelled successfully.\n")
                return
        print("\nNo Appointment found with that ID.\n")

# Menu to interact with the hospital's system

def hospital_menu():
    while True:
        print("\n--- Richard's Memorial Management System ---")
        print("1. Register Patient")
        print("2. Add Doctor")
        print("3. Book Appointment")
        print("4. View All Patients")
        print("5. View All Doctors")
        print("6. View All Appointments")
        print("7. Cancel Appointment")
        print("8. View Schedule")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            name = input("Enter patient name: ")
            try:
                age = int(input("Enter patient age: "))
            except ValueError:
                print("Error: Age must be a number.")
                continue
            gender = input("Enter patient gender (Male/Female): ")
            Patient.add_patient(name, age, gender)

        elif choice == '2':
            name = input("Enter Doctor name: ")
            specialty = input("Enter doctor specialty: ")
            Doctor.add_doctor(name, specialty)

        elif choice == '3':
            Patient.list_patients()
            patient_id = input("Enter Patient ID: ").upper()

            Doctor.list_doctors()
            doctor_id = input("Enter Doctor ID: ").upper()

            date = input("Enter appointment date (e.g., 2025-04-26): ")
            time = input("Enter appointment time (HH:MM in 24-hour format): ")

            Appointment.book_appointment(patient_id, doctor_id, date, time)

        elif choice == '4':
            Patient.list_patients()

        elif choice == '5':
            Doctor.list_doctors()

        elif choice == '6':
            Appointment.list_appointments()

        elif choice == '7':
            appointment_id = input("Enter Appointment ID to cancel: ").strip()
            Appointment.cancel_appointment(appointment_id)

        elif choice == '8':
            doctor_id = input("Enter Doctor ID to view schedule: ").strip()
            Appointment.view_schedule(doctor_id)

        elif choice == '9':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

hospital_menu()