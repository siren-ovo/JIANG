Overview
Personal Trainer Assistant is a simple personal fitness management system that uses PyQt5 to create a graphical user interface. It helps users calculate their BMI (Body Mass Index) based on gender, height, and weight, and provides dietary and exercise advice based on the BMI value.

Features
1.Input user gender, height, and weight
2.Calculate BMI value
3.Provide personalized dietary and exercise advice based on the user's gender, height, and BMI value

Dependencies
1.Python 3.x
2.PyQt5
3.requests

Installation
1.Clone or download this repository to your local machine.
2.Install the required dependencies using pip:
pip install PyQt5 requests

Running the Application
1.Ensure that all dependencies are installed.
2.Navigate to the project directory in your command line and run the following command to start the application:
python personal_trainer.py

3.Usage
1.After launching the application, you will see a window titled "Fitness Management System".
2.Enter your gender, height (cm), and weight (kg).
3.Click the "Calculate BMI" button. The program will calculate your BMI and display the corresponding dietary and exercise advice.

Code Structure
personal_trainer.py: The main program file containing the PersonalTrainerApp class and the core application logic.

Example
Assume you are a male with a height of 180cm and a weight of 75kg. After entering this information and clicking the "Calculate BMI" button, you will see your BMI value along with the corresponding dietary and exercise advice.