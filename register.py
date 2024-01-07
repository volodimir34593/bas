import sys
import json
import os
import hashlib
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog

class RegisterWindow(QDialog):
    def __init__(self, user_database, parent=None):
        super().__init__(parent)
        self.user_database = user_database
        self.setWindowTitle('Registration Window')
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register_clicked)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def register_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if os.path.exists('user_database.json'):
                with open('user_database.json', 'r') as file:
                    user_data = json.load(file)
            else:
                user_data = {}

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            user_data[username.upper()] = {'password': hashed_password}

            with open('user_database.json', 'w') as file:
                json.dump(user_data, file)

            print(f'Registration successful - Username: {username}')
            self.accept()
        else:
            print("Please enter a username and password.")

class LoginWindow(QWidget):
    def __init__(self, user_database):
        super().__init__()
        self.user_database = user_database
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login Window')
        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login_clicked)
        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.show_register_window)
        self.error_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.error_label)
        self.setLayout(layout)
        self.show()

    def login_clicked(self):
        self.error_label.clear()

        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            with open('user_database.json', 'r') as file:
                user_data = json.load(file)

            if username.upper() in user_data:
                hashed_input_password = hashlib.sha256(password.encode()).hexdigest()
                stored_password = user_data[username.upper()]['password']
                if stored_password == hashed_input_password:
                    print(f'Login successful - Username: {username}')
                else:
                    self.show_error_message("Incorrect password")
            else:
                self.show_error_message("Username not found")
        else:
            self.show_error_message("Please provide a username and password")

    def show_error_message(self, message):
        self.error_label.setText(f'<font color="red"><b>{message}</b></font>')

    def show_register_window(self):
        register_window = RegisterWindow(self.user_database, self)
        result = register_window.exec_()

        if result == QDialog.Accepted:
            print("Registration successful")

if __name__ == '__main__':
    try:
        with open('user_database.json', 'r') as file:
            user_database = json.load(file)
    except FileNotFoundError:
        user_database = {}

    app = QApplication(sys.argv)
    window = LoginWindow(user_database)
    sys.exit(app.exec_())
