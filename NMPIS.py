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


class NMPIS(BoxLayout, Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def collect_payment(self):
        from CollectPayment import CollectPayment
        self.manager.add_widget(CollectPayment(name='collectpayment'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'collectpayment'

    def make_appointment(self):
        from MakeAppointment import MakeAppointment
        self.manager.add_widget(MakeAppointment(name='makeappointment'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'makeappointment'


class NMPISApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    NMPISApp().run()

