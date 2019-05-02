from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager
from os import listdir

mims_directory = "MIMS\\"

patient = ['Patient']

system_admin = ['System Administrator']

mpis = ['Nurse', 'Medical Technician', 'Nurse Practitioner']

nmpis = ['Clerk', 'Accountant']

medical_professional = ['Doctor', 'Pharmacist']

management_staff = ['President', 'Inventory Manager', 'Staff Manager', 'Department Head']

user_files = [
    'Management Staff.txt',
    'Medical Patient Interaction Staff.txt',
    'Medical Professional.txt',
    'Non-Medical Patient Interaction Staff.txt'
]

patient_names = []
for patient in listdir(mims_directory + 'Patients'):
    patient_names.append(patient)

class CollectPayment(BoxLayout, Screen):
    service_text_input = ObjectProperty()
    quantity_text_input = ObjectProperty()

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'nmpis'

    def submit_payment(self):
        if self.service_text_input.text != 'Choose a Patient':
            if len(self.quantity_text_input.text) > 0:
                try:
                    quantity = int(self.quantity_text_input.text)
                except:
                    popup = Popup(title="Input Error",
                                  content=Label(text="Please enter an integer value for payment"),
                                  size_hint=(None, None), size=(400, 400))
                    popup.open()
                    return
                with open(mims_directory + 'Payments.txt', 'r') as open_file:
                    service_data = open_file.read()
                with open(mims_directory + 'Payments.txt', 'w') as open_file:
                    open_file.write(
                        service_data + self.service_text_input.text + ',' + self.quantity_text_input.text + '\n')
                self.service_text_input.text = 'Choose a Patient'
                self.quantity_text_input.text = ""
            else:
                popup = Popup(title="Input Error",
                              content=Label(text="Please enter a payment"),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return
        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please choose a patient"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

class CollectPaymentApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    CollectPaymentApp().run()
