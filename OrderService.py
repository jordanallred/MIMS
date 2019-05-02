from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager

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

user_list = []
for file in user_files:
    with open(mims_directory + file, 'r') as open_file:
        user_data = open_file.read()
    users = user_data.split('\n')
    for user in users:
        if len(user) > 0:
            user_list.append(user)

class OrderService(BoxLayout, Screen):
    service_text_input = ObjectProperty()
    quantity_text_input = ObjectProperty()

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'mpis'

    def order_service(self):
        if self.service_text_input.text != 'Service':
            if len(self.quantity_text_input.text) > 0:
                try:
                    quantity = int(self.quantity_text_input.text)
                except:
                    popup = Popup(title="Input Error",
                                  content=Label(text="Please enter an integer value for quantity"),
                                  size_hint=(None, None), size=(400, 400))
                    popup.open()
                    return
                if quantity > 0:
                    with open(mims_directory + 'Services.txt', 'r') as open_file:
                        service_data = open_file.read()
                    with open(mims_directory + 'Services.txt', 'w') as open_file:
                        open_file.write(service_data + self.service_text_input.text + ',' + self.quantity_text_input.text + '\n')
                else:
                    popup = Popup(title="Input Error",
                                  content=Label(text="Please enter a value greater than zero"),
                                  size_hint=(None, None), size=(400, 400))
                    popup.open()
                    return
            else:
                popup = Popup(title="Input Error",
                              content=Label(text="Please enter a quantity"),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return
        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please choose a service"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

class OrderServiceApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    OrderServiceApp().run()
