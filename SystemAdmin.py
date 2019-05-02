from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from ManageUsers import ManageUsers
from CheckSecurity import CheckSecurity
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import *
from kivy.uix.label import *

mims_directory = "MIMS\\"

patient_jobs = ['Patient']

system_admin_jobs = ['System Administrator']

mpis_jobs = ['Nurse', 'Medical Technician', 'Nurse Practitioner']

nmpis_jobs = ['Clerk', 'Accountant']

medical_professional_jobs = ['Doctor', 'Pharmacist']

management_staff_jobs = ['President', 'Inventory Manager', 'Staff Manager', 'Department Head']

user_files = [
    'Management Staff.txt',
    'Medical Patient Interaction Staff.txt',
    'Medical Professional.txt',
    'Non-Medical Patient Interaction Staff.txt'
]

student_list = []
for file in user_files:
    with open(mims_directory + file, 'r') as open_file:
        user_data = open_file.read()
    users = user_data.split('\n')
    for user in users:
        if len(user) > 0:
            student_list.append(user)


class SystemAdmin(BoxLayout, Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def manage_users(self):
        self.manager.add_widget(ManageUsers(name='manageusers'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'manageusers'

    @staticmethod
    def system_maintenance():
        empty_files = []
        for file in user_files:
            with open(mims_directory + file, 'r') as open_file:
                data = open_file.read()
            if len(data) == 0:
                empty_files.append(file.replace('.txt', ''))
        if len(empty_files) > 0:
            message = 'The following files are empty:'
            for file in empty_files:
                message += '\n' + file
            popup = Popup(title="Empty File Warning",
                          content=Label(text=message),
                          size_hint=(None, None), size=(500, 500))
            popup.open()

        with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
            data = open_file.read()
        while data.__contains__('\n'):
            data = data.replace('\n', '')
        if len(data) == 0:
            with open(mims_directory + 'Failed Login Attempts.txt', 'w') as open_file:
                open_file.write('0\n')
        
    def check_security(self):
        self.manager.add_widget(CheckSecurity(name='checksecurity'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'checksecurity'
        self.manager.get_screen('checksecurity').update_form()


class SystemAdminApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    SystemAdminApp().run()

