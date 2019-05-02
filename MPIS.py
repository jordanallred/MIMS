from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
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


class MPIS(BoxLayout, Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def manage_patients(self):
        from ManagePatients import ManagePatients
        self.manager.add_widget(ManagePatients(name='managepatients'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'managepatients'

    def manage_reports(self):
        from ManageReports import ManageReports
        self.manager.add_widget(ManageReports(name='managereports'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'managereports'

    def order_service(self):
        from OrderService import OrderService
        self.manager.add_widget(OrderService(name='orderservice'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'orderservice'


class MPISApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    MPISApp().run()

