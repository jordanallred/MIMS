from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListView

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

suspended_accounts = []
with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
    user_data = open_file.read()
users = user_data.split('\n')
total_attempts = 0
with open(mims_directory + 'Suspended Accounts.txt', 'r') as open_file:
    suspended_data = open_file.read()
for user in users:
    if user.__contains__(','):
        split = user.split(',')
        if suspended_data.__contains__(split[0]):
            suspended_accounts.append(str(user) + ',suspended')
        else:
            suspended_accounts.append(str(user))
    elif len(user) > 0:
        total_attempts = user
if len(suspended_accounts) == 0:
    suspended_accounts = ['No Accounts to Show']


class CheckSecurity(BoxLayout, Screen):
    total_attempts = ObjectProperty()
    failure_accounts = suspended_accounts
    suspended_accounts = ObjectProperty()

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'systemadmin'

    def reset_total(self):
        with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
            user_data = open_file.read()
        users = user_data.split('\n')
        users[0] = "0"
        write_data = ""
        for user in users:
            write_data += user + '\n'
        with open(mims_directory + 'Failed Login Attempts.txt', 'w') as open_file:
            open_file.write(write_data)
        self.total_attempts.text = self.total_attempts.text[:22] + '0'
        self.update_form()

    def reset(self):
        if self.suspended_accounts.adapter.selection:
            selection = self.suspended_accounts.adapter.selection[0].text
            if selection != 'No Accounts to Show':
                write_data = ""
                with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
                    user_data = open_file.read()
                users = user_data.split('\n')
                for user in users:
                    if user.__contains__(','):
                        split = user.split(',')
                        suspended_accounts.append(user)
                        if split[0] != selection.split(',')[0]:
                            write_data += user
                    else:
                        write_data += user

                with open(mims_directory + 'Failed Login Attempts.txt', 'w') as open_file:
                    open_file.write(write_data)
                self.suspended_accounts.adapter.data.remove(selection)
                self.suspended_accounts._trigger_reset_populate()
                self.update_form()


    def suspend(self):
        if self.suspended_accounts.adapter.selection:
            selection = self.suspended_accounts.adapter.selection[0].text
            if selection != 'No Accounts to Show':
                self.suspended_accounts.adapter.data.remove(selection)
                if str(selection).__contains__('suspended'):
                    selection = str(selection)[:-10]
                    with open(mims_directory + 'Suspended Accounts.txt', 'r') as open_file:
                        user_data = open_file.read()
                    while user_data.__contains__(selection.split(',')[0]):
                        user_data = user_data.replace(selection.split(',')[0], '')
                    while user_data.__contains__('\n\n'):
                        user_data = user_data.replace('\n\n', '\n')
                    with open(mims_directory + 'Suspended Accounts.txt', 'w') as open_file:
                        open_file.write(user_data)
                else:
                    with open(mims_directory + 'Suspended Accounts.txt', 'r') as open_file:
                        user_data = open_file.read()
                    user_data += selection.split(',')[0] + '\n'
                    with open(mims_directory + 'Suspended Accounts.txt', 'w') as open_file:
                        open_file.write(user_data)
                    selection += ',suspended'
                self.suspended_accounts.adapter.data.extend([selection])
                self.suspended_accounts._trigger_reset_populate()

    def update_form(self):
        suspended_accounts = []
        with open(mims_directory + 'Failed Login Attempts.txt', 'r') as open_file:
            user_data = open_file.read()
        users = user_data.split('\n')
        total_attempts = 0
        with open(mims_directory + 'Suspended Accounts.txt', 'r') as open_file:
            suspended_data = open_file.read()
        for user in users:
            if user.__contains__(','):
                split = user.split(',')
                if suspended_data.__contains__(split[0]):
                    suspended_accounts.append(str(user) + ',suspended')
                else:
                    suspended_accounts.append(str(user))
            elif len(user) > 0:
                total_attempts = user
        if len(suspended_accounts) == 0:
            suspended_accounts = ['No Accounts to Show']

        self.total_attempts.text = str(total_attempts)

        items = []
        for entry in self.suspended_accounts.adapter.data:
            items.append(entry)

        if len(items) > 0:
            if suspended_accounts == ['No Accounts to Show'] and items[0] == ['No Accounts to Show']:
                return
            elif suspended_accounts == ['No Accounts to Show'] and items[0] != ['No Accounts to Show']:
                self.suspended_accounts.adapter.data.remove(items[0])
                for account in suspended_accounts:
                    self.suspended_accounts.adapter.data.extend([account])
            elif suspended_accounts != ['No Accounts to Show'] and items[0] != ['No Accounts to Show']:
                for item_to_remove in items:
                    self.suspended_accounts.adapter.data.remove(item_to_remove)
                for account in suspended_accounts:
                    self.suspended_accounts.adapter.data.extend([account])
            else:
                self.suspended_accounts.adapter.data.extend(['No Accounts to Show'])
        else:
            self.suspended_accounts.adapter.data.extend(['No Accounts to Show'])


class CheckSecurityApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    CheckSecurityApp().run()

