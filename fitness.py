# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QFormLayout, QComboBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import requests


class PersonalTrainerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Personal Trainer Assistant')
        self.setGeometry(100, 100, 400, 500)
        self.setWindowIcon(QIcon('fitness_icon.png'))

        # Set fonts
        font = QFont('Arial', 12)
        title_font = QFont('Arial', 16, QFont.Bold)

        # Title
        self.title_label = QLabel('Fitness Management System', self)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)

        # Gender selection
        self.gender_label = QLabel('Gender:', self)
        self.gender_label.setFont(font)
        self.gender_input = QComboBox(self)
        self.gender_input.addItems(["Male", "Female"])
        self.gender_input.setFont(font)

        # Height and weight input
        self.height_label = QLabel('Height (cm):', self)
        self.height_label.setFont(font)
        self.height_input = QLineEdit(self)
        self.height_input.setFont(font)

        self.weight_label = QLabel('Weight (kg):', self)
        self.weight_label.setFont(font)
        self.weight_input = QLineEdit(self)
        self.weight_input.setFont(font)

        # Calculate BMI button
        self.calc_button = QPushButton('Calculate BMI', self)
        self.calc_button.setFont(font)
        self.calc_button.setStyleSheet("background-color: lightblue;")
        self.calc_button.clicked.connect(self.calculate_bmi)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow(self.gender_label, self.gender_input)
        form_layout.addRow(self.height_label, self.height_input)
        form_layout.addRow(self.weight_label, self.weight_input)

        # Vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.calc_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.show()

    def calculate_bmi(self):
        gender = self.gender_input.currentText()
        height = self.height_input.text()
        weight = self.weight_input.text()

        if not height or not weight:
            QMessageBox.warning(self, 'Input Error', 'Please enter height and weight')
            return

        try:
            height = int(height)
            weight = int(weight)
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Please enter valid height and weight')
            return

        url = "https://www.apii.cn/api/huaiyun/te/"
        params = {
            "weight": weight,
            "height": height
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            result = response.json()
            bmi = result.get("bmi", "BMI not found in API response")
            advice = self.get_advice(gender, height, bmi)
            QMessageBox.information(self, 'BMI Calculation Result', f'Your BMI is: {bmi}\n\n{advice}')
        else:
            QMessageBox.warning(self, 'API Error', f'API request failed, status code: {response.status_code}')

    def get_advice(self, gender, height, bmi):
        bmi = float(bmi)
        advice = ""

        if gender == "Male":
            if height > 180:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods daily (e.g., chicken breast, fish, protein powder).\nIncrease carbohydrate intake (e.g., whole grains, rice, pasta).\nConsume healthy fats daily (e.g., nuts, avocados, olive oil).\nIncrease meal frequency and include snacks.\nExercise:\nFocus on strength training: squats, deadlifts, bench press, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking, jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after each strength training session."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet, consume enough protein, carbohydrates, and healthy fats daily.\nEat multiple meals a day to maintain blood sugar levels.\nExercise:\nCombine strength training and cardio: e.g., HIIT.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
            elif 170 <= height <= 180:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods (e.g., beef, chicken, fish, protein powder).\nIncrease carbohydrate intake (e.g., rice, pasta, potatoes).\nConsume healthy fats (e.g., olive oil, avocados, nuts).\nIncrease meal frequency and calorie intake.\nExercise:\nStrength training: squats, bench press, deadlifts, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking or jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after strength training."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet daily, increase protein intake.\nEat multiple small meals a day.\nExercise:\nCombine strength training and cardio.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
            else:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods (e.g., fish, chicken breast, protein powder).\nIncrease carbohydrate intake (e.g., brown rice, pasta, potatoes).\nConsume healthy fats (e.g., nuts, avocados, olive oil).\nIncrease meal frequency and calorie intake.\nExercise:\nStrength training: squats, bench press, deadlifts, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking or jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after strength training."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet daily, increase protein intake.\nEat multiple small meals a day.\nExercise:\nCombine strength training and cardio.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
        else:  # Female
            if height > 170:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods daily (e.g., chicken breast, fish, protein powder).\nIncrease carbohydrate intake (e.g., whole grains, rice, pasta).\nConsume healthy fats daily (e.g., nuts, avocados, olive oil).\nIncrease meal frequency and include snacks.\nExercise:\nFocus on strength training: squats, deadlifts, bench press, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking, jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after each strength training session."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet, consume enough protein, carbohydrates, and healthy fats daily.\nEat multiple meals a day to maintain blood sugar levels.\nExercise:\nCombine strength training and cardio: e.g., HIIT.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
            elif 160 <= height <= 170:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods daily (e.g., chicken breast, fish, protein powder).\nIncrease carbohydrate intake (e.g., whole grains, rice, pasta).\nConsume healthy fats daily (e.g., nuts, avocados, olive oil).\nIncrease meal frequency and include snacks.\nExercise:\nFocus on strength training: squats, deadlifts, bench press, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking, jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after each strength training session."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet, consume enough protein, carbohydrates, and healthy fats daily.\nEat multiple meals a day to maintain blood sugar levels.\nExercise:\nCombine strength training and cardio: e.g., HIIT.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
            else:
                if bmi < 18.5:
                    advice = "Goal: Gain muscle and weight\nAdvice: Diet, exercise, rest\nDiet:\nEat high-protein foods daily (e.g., chicken breast, fish, protein powder).\nIncrease carbohydrate intake (e.g., whole grains, rice, pasta).\nConsume healthy fats daily (e.g., nuts, avocados, olive oil).\nIncrease meal frequency and include snacks.\nExercise:\nFocus on strength training: squats, deadlifts, bench press, rowing.\n3-4 times a week, 1 hour each session.\nInclude a small amount of cardio (e.g., walking, jogging), 1-2 times a week, 30 minutes each.\nRest:\nEnsure 8 hours of sleep each night.\nRest for 48 hours after each strength training session."
                elif 18.5 <= bmi < 24.9:
                    advice = "Goal: Maintain physique and increase muscle strength\nAdvice: Diet, exercise, rest\nDiet:\nBalanced diet, consume enough protein, carbohydrates, and healthy fats daily.\nEat multiple meals a day to maintain blood sugar levels.\nExercise:\nCombine strength training and cardio: e.g., HIIT.\n3-4 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."
                else:
                    advice = "Goal: Lose fat and gain muscle\nAdvice: Diet, exercise, rest\nDiet:\nLow-carb diet, increase protein and fiber intake.\nControl daily calorie intake, avoid high-sugar and high-fat foods.\nExercise:\nCombine HIIT, strength training, and cardio.\n4-5 times a week, 45-60 minutes each session.\nRest:\nEnsure 7-8 hours of sleep each night.\nRest for at least 24 hours after training."

        return advice


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PersonalTrainerApp()
    sys.exit(app.exec_())
