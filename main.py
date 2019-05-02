from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

mims_directory = "MIMS\\"

system_admin = ['System Administrator']

mpis = ['Nurse', 'Medical Technician', 'Nurse Practitioner']

nmpis = ['Clerk', 'Accountant']

medical_professional = ['Doctor', 'Pharmacist']

management_staff = ['President', 'Inventory Manager', 'Staff Manager', 'Department Head']

with open(mims_directory + 'Suspended Accounts.txt', 'r') as open_file:
    suspended_data = open_file.read()


class Login(Screen):
    def do_login(self, username, password, role):
        app = App.get_running_app()

        app.username = username
        app.password = password

        if role in system_admin:
            role = 'System Administrator'

        elif role in mpis:
            role = 'Medical Patient Interaction Staff'

        elif role in nmpis:
            role = 'Non-Medical Patient Interaction Staff'

        elif role in medical_professional:
            role = 'Medical Professional'

        elif role in management_staff:
            role = 'Management Staff'

        else:
            popup = Popup(title="Role Error",
                          content=Label(text="Please choose a role"),
                          size_hint=(None, None), size=(500, 500))
            popup.open()
            return

        with open(mims_directory + role + ".txt", 'r') as login_file:
            login_data = login_file.read()

        user_data = login_data.split('\n')
        if suspended_data.__contains__(username):
            popup = Popup(title="Account Error",
                          content=Label(text="Account has been suspended. Contact system administrator."),
                          size_hint=(None, None), size=(500, 500))
            popup.open()
        else:
            user_in = False
            verified = False
            for user in user_data:
                if len(user) > 0:
                    user_id = user.split(',')[0]
                    user_password = user.split(',')[1]
                    if username == user_id:
                        user_in = True
                        if password == user_password:
                            verified = True
                            break
            if verified and role == 'System Administrator':
                from SystemAdmin import SystemAdmin
                self.manager.add_widget(SystemAdmin(name='systemadmin'))
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'systemadmin'
            elif verified and role == 'Medical Patient Interaction Staff':
                from MPIS import MPIS
                self.manager.add_widget(MPIS(name='mpis'))
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'mpis'
            elif verified and role == 'Non-Medical Patient Interaction Staff':
                from NMPIS import NMPIS
                self.manager.add_widget(NMPIS(name='nmpis'))
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'nmpis'
            elif verified and role == 'Medical Professional':
                from MedicalProfessional import MedicalProfessional
                self.manager.add_widget(MedicalProfessional(name='medicalprofessional'))
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'medicalprofessional'
            elif verified and role == 'Management Staff':
                from ManagementStaff import ManagementStaff
                self.manager.add_widget(ManagementStaff(name='managementstaff'))
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'managementstaff'
            else:
                if user_in:
                    with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
                        user_data = open_file.read()
                    users = user_data.split('\n')
                    write_data = ""
                    existing_user = False
                    for user in users:
                        if user.__contains__(','):
                            split = user.split(',')
                            if split[0] == username:
                                existing_user = True
                                split[1] = str(int(split[1]) + 1)
                                write_data += split[0] + ',' + split[1] + '\n'
                            else:
                                write_data += user + '\n'
                        elif len(user) > 0:
                            write_data += user + '\n'
                    if not existing_user:
                        write_data += username + ',1\n'
                    with open(mims_directory + 'Failed Login Attempts.txt', 'w') as open_file:
                        open_file.write(write_data)

                with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
                    user_data = open_file.read()
                users = user_data.split('\n')
                write_data = ""
                users[0] = str(int(users[0]) + 1)
                for user in users:
                    write_data += user + '\n'
                with open(mims_directory + 'Failed Login Attempts.txt', 'w') as open_file:
                    open_file.write(write_data)

        app.config.read(app.get_application_config())
        app.config.write()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""
        self.ids['role_spinner'].text = "Role"


class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        return manager

    def get_application_config(self):
        if not self.username:
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if(not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )


if __name__ == '__main__':
    LoginApp().run()
