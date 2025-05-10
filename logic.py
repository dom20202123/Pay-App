from PyQt6.QtWidgets import *
from pay_app import *
import csv


class Logic(QMainWindow, Ui_Pay_App):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.Pay_Button.clicked.connect(lambda : self.pay())
        self.Total_Button.clicked.connect(lambda : self.total())



    def pay(self):
        self.hourly = float(self.Hourly_Input.text())
        self.hours = float(self.Hours_Input.text())
        gross_income = 0
        try:
            if (self.hourly <= 0) or (self.hours <= 0):
                raise ValueError('Amount must be positive')
                raise ValueError('Amount must be positive')
        except (ValueError, TypeError):
            self.feedback.setText('Please enter a valid positive number')

        gross_income = self.hours * self.hourly
        self.Gross_Input.setText(f'{gross_income:.2f}')


    def total(self):

        gross_income = float(self.Gross_Input.text())
        state = self.State_Input.text().strip().lower()

        social_security_rate = 0
        social_security_total = 0
        medicare_rate = 0
        medicare_total = 0
        state_rate = 0
        state_total = 0
        net_income = 0

        with open('taxes.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['state'] == state.lower():
                    social_security_rate = float(row['social_security'])
                    medicare_rate = float(row['medicare'])
                    state_rate = float(row['state'])

            if social_security_rate == 0:
                self.feedback.setText('State not found')

            social_security_total = social_security_rate * gross_income
            medicare_total = medicare_rate * gross_income
            state_total = state_rate * gross_income
            net_income = gross_income - social_security_total - medicare_total - state_total

            self.Social_Security_Input.setText(f'${social_security_total:.2f}')
            self.Medicare_Input.setText(f'${medicare_total:.2f}')
            self.State_Tax_Input.setText(f'${state_total:.2f}')
            self.Net_Input.setText(f'${net_income:.2f}')












