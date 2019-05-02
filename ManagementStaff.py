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

ManagementStaff_jobs = ['Clerk', 'Accountant']

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


class ManagementStaff(BoxLayout, Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def manage_payments(self):
        from ManagePayments import ManagePayments
        self.manager.add_widget(ManagePayments(name='managepayments'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'managepayments'

    def manage_reports(self):
        from ManageReportsManagement import ManageReportsManagement
        self.manager.add_widget(ManageReportsManagement(name='managereports'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'managereports'

    def make_schedule(self):
        from MakeSchedule import MakeSchedule
        self.manager.add_widget(MakeSchedule(name='makeschedule'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'makeschedule'

    def order_item(self):
        from OrderItem import OrderItem
        self.manager.add_widget(OrderItem(name='orderitem'))
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'orderitem'


class ManagementStaffApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    ManagementStaffApp().run()

