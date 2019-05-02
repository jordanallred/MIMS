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

class ManageUsers(BoxLayout, Screen):

    id_text_input = ObjectProperty()
    password_text_input = ObjectProperty()
    name_text_input = ObjectProperty()
    role_text_input = ObjectProperty()

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'systemadmin'

    def submit_student(self):
        student_name = self.id_text_input.text + "," + self.password_text_input.text + "," + self.name_text_input.text + "," + self.role_text_input.text

        if self.role_text_input.text in patient:
            role = 'patient'

        elif self.role_text_input.text in system_admin:
            role = 'System Administrator'

        elif self.role_text_input.text in mpis:
            role = 'Medical Patient Interaction Staff'

        elif self.role_text_input.text in nmpis:
            role = 'Non-Medical Patient Interaction Staff'

        elif self.role_text_input.text in medical_professional:
            role = 'Medical Professional'

        elif self.role_text_input.text in management_staff:
            role = 'Management Staff'

        else:
            popup = Popup(title="Role Error",
                          content=Label(text="Please choose a role"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

        if len(self.id_text_input.text) > 0 and len(self.password_text_input.text) > 0 and len(self.name_text_input.text) > 0:
            with open(mims_directory + role + '.txt', 'r') as open_file:
                user_data = open_file.read()
            with open(mims_directory + role + '.txt', 'w') as open_file:
                open_file.write(user_data + str(student_name) + '\n')
        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please enter all fields"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

        self.user_list.adapter.data.extend([student_name])

        self.user_list._trigger_reset_populate()

    def delete_student(self, *args):
        if self.user_list.adapter.selection:
            selection = self.user_list.adapter.selection[0].text
            self.user_list.adapter.data.remove(selection)

            self.user_list._trigger_reset_populate()

    def replace_student(self, *args):
        if self.user_list.adapter.selection:
            selection = self.user_list.adapter.selection[0].text
            student_name = self.id_text_input.text + "," + self.password_text_input.text + "," + self.name_text_input.text + "," + self.role_text_input.text
            if self.role_text_input.text in patient:
                role = 'patient'

            elif self.role_text_input.text in system_admin:
                role = 'System Administrator'

            elif self.role_text_input.text in mpis:
                role = 'Medical Patient Interaction Staff'

            elif self.role_text_input.text in nmpis:
                role = 'Non-Medical Patient Interaction Staff'

            elif self.role_text_input.text in medical_professional:
                role = 'Medical Professional'

            elif self.role_text_input.text in management_staff:
                role = 'Management Staff'

            else:
                popup = Popup(title="Role Error",
                              content=Label(text="Please choose a role"),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return

            if len(self.id_text_input.text) > 0 and len(self.password_text_input.text) > 0 and len(
                    self.name_text_input.text) > 0:
                if selection.split(',')[0] != self.id_text_input.text:
                    for file in user_files:
                        with open(mims_directory + file) as open_file:
                            user_data = open_file.read()
                        users = user_data.split('\n')
                        for user in users:
                            if user.split(',')[0] == self.id_text_input.text:
                                popup = Popup(title="Input Error",
                                              content=Label(text="This ID is already in use"),
                                              size_hint=(None, None), size=(400, 400))
                                popup.open()
                                return

                if selection.split(',')[3] != self.role_text_input.text:
                    for file in user_files:
                        write_data = ""
                        found_user = False
                        with open(mims_directory + file) as open_file:
                            user_data = open_file.read()
                        users = user_data.split('\n')
                        for user in users:
                            if user.split(',')[0] == self.id_text_input.text:
                                found_user = True
                            else:
                                write_data += str(user) + '\n'
                        if found_user:
                            with open(mims_directory + file, 'w') as open_file:
                                open_file.write(write_data)

                with open(mims_directory + role + '.txt', 'r') as open_file:
                    user_data = open_file.read()
                    user_data += str(student_name) + '\n'
                with open(mims_directory + role + '.txt', 'w') as open_file:
                    open_file.write(user_data)
            else:
                popup = Popup(title="Input Error",
                              content=Label(text="Please enter all fields"),
                              size_hint=(None, None), size=(500, 500))
                popup.open()
                return

            self.user_list.adapter.data.remove(selection)

            self.user_list.adapter.data.extend([student_name])

            self.user_list._trigger_reset_populate()


class ManageUsersApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    ManageUsersApp().run()
