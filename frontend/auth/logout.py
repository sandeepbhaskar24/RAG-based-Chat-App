import subprocess
from termcolor import colored

class LogOutService:
    def __init__(self, window):
        self.window = window

    def update_ui(self):     
        username = self.window.ui.username_label.text()
        self.window.ui.login_button.setText("Log In")
        self.window.ui.login_button.setStyleSheet('''QPushButton{
                                                color: rgba(255, 255, 255, 200);
                                                font-family: 'Roboto';       /* font family */
                                                font-size: 10pt;            /* font size */
                                                background-color: rgb(48, 53, 65);
                                                border-radius:10px;
                                            }
                                            QPushButton:hover{
                                                color:rgb(85, 170, 255);
                                                background-color:rgb(52, 57, 70)
                                            }''')
        self.window.ui.login_button.setEnabled(True)
        self.window.ui.login_button.setToolTip("")
        
        self.window.ui.logged_in_label.setText('Not Logged In')
        self.window.ui.logged_in_label.setStyleSheet('''color: rgba(255, 0, 0, 200);
                                                font-family: 'Roboto';       /* font family */
                                                font-size: 10pt;            /* font size */
                                                ''')
        
        self.window.ui.username_label.setText("Username: ")
        self.window.ui.email_label.setText("Email: ")
        self.window.ui.button_logout.setText('Log In')
        self.window.ui.button_logout.setStyleSheet("""
                                                QPushButton{
                                                    color: rgba(1, 190, 118, 200); 
                                                    border: 2px solid rgba(1, 190, 118, 200);
                                                    background-color: rgba(0, 170, 127, 20);
                                                    border-radius : 10px;
                                                }

                                                QPushButton:hover{
                                                    background-color: rgba(0, 170, 127, 10);
                                                    border: 2px solid rgba(1, 190, 118, 170);
}""")

        print(colored(f"LOGGED OUT User: {username.split()[1]}", 'green'))
        
    def LogOut(self):
        # subprocess.run(
        #     ["icacls", "auth_token.x", "/remove:d", "Everyone"],
        #     check=True
        # )
        with open("auth_token.x", "w"):
            pass

        # subprocess.run(
        #     ["icacls", "auth_token.x", "/deny", "Everyone:(R)"],
        #     check=True
        # )
        self.update_ui()