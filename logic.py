from PyQt6.QtWidgets import *
from pay_app import *
import csv


class Logic(QMainWindow, Ui_Pay_App):
    '''
    Sets up the function by linking the buttons to their functions and hiding half of the widgets to make it look more
    clean
    '''
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.Pay_Button.clicked.connect(lambda : self.pay())
        self.Total_Button.clicked.connect(lambda : self.total())
        self.Gross_label.hide()
        self.Medicare_Label.hide()
        self.State_Tax_Label.hide()
        self.Federal_Label.hide()
        self.Net_Label.hide()
        self.Social_Security_label.hide()
        self.Total_Button.hide()
        self.Martial_Status_Label.hide()
        self.Married_Button.hide()
        self.Single_Button.hide()



    def pay(self) -> None:
        '''
        Calculates the pay based off of the hourly rate and the hours worked by multiplying
        Also has exception handling for the case if any symbol, letters, or a negative number was put in
        '''

        try:
            self.hourly = float(self.Hourly_Input.text())
            self.hours = float(self.Hours_Input.text())
            gross_income = 0
            if (self.hourly <= 0) or (self.hours <= 0):
                raise ValueError('Amount must be positive')
                raise ValueError('Amount must be positive')

            gross_income = self.hours * self.hourly
            self.Gross_Input.setText(f'{gross_income:.2f}')
            self.Gross_label.show()
            self.Medicare_Label.show()
            self.State_Tax_Label.show()
            self.Federal_Label.show()
            self.Net_Label.show()
            self.Social_Security_label.show()
            self.Total_Button.show()
            self.Martial_Status_Label.show()
            self.Married_Button.show()
            self.Single_Button.show()


        except (ValueError, TypeError):
            self.feedback.setText('Please enter a valid positive number')





    def total(self) -> None:
        '''
        Calculates the taxes by looking into taxes.csv and federal_tax.csv for the federal tax
        Then adds the values returned to their labels
        Then finally calculates net income by subtracting all taxes by the gross income
        gross_income : Value that holds the calculation from the pay function
        state: Input used for finding the state tax
        social_security_rate : Rate for social security
        social_security_total: Total of social security after multiplying rate and gross
        medicare_rate : Rate for medicare
        medicare_total : Total of medicare after multiplying rate and gross
        state_rate : Rate of tax found from tax.csv and using variable state as its key
        state_total : Total of state tax after multiplying rate and gross
        federal_tax : Rate of tax found by gross income
        federal_total : Total of federal tax after multiplying tax and gross
        married_single_status : Status found off of radio buttons and helps determine federal tax
        state_found : True or False to verify if the state was found or not
        min_income : Minimum income to be in a federal tax bracket
        max_income : Maximum income to be in a federal tax bracket

        '''

        gross_income = float(self.Gross_Input.text())
        state = self.State_Input.text().strip().lower()

        social_security_rate = 0
        social_security_total = 0
        medicare_rate = 0
        medicare_total = 0
        state_rate = 0
        state_total = 0
        net_income = 0
        federal_tax = 0
        federal_total = 0
        married_single_status = ''
        state_found = False

        with open('taxes.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['state'].strip().lower() == state:
                    social_security_rate = float(row['social_security'])
                    medicare_rate = float(row['medicare'])
                    state_rate = float(row['state_rate'])
                    state_found = True

            if state_found == False:
                self.feedback.setText('State not found')

        if self.Single_Button.isChecked():
            married_single_status = 'single'
        elif self.Married_Button.isChecked():
            married_single_status = 'married'
        else:
            self.feedback.setText(f'Please select a martial status')
            return

        with open('federal_tax_yearly.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                min_income = float(row['Minimum'])
                max_income = float(row['Maximum'])
                if (row['Marital_status'].lower() == married_single_status) and (min_income <= gross_income <=
                max_income):
                    federal_tax = float(row['Tax_rate'])
                    federal_total = federal_tax * gross_income



            social_security_total = social_security_rate * gross_income
            medicare_total = medicare_rate * gross_income
            state_total = state_rate * gross_income
            net_income = gross_income - social_security_total - medicare_total - state_total - federal_total

            self.Social_Security_Input.setText(f'${social_security_total:.2f}')
            self.Medicare_Input.setText(f'${medicare_total:.2f}')
            self.State_Tax_Input.setText(f'${state_total:.2f}')
            self.Federal_Input.setText(f'${federal_total:.2f}')
            self.Net_Input.setText(f'${net_income:.2f}')












