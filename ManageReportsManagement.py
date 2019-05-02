from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager
from os import listdir, rename, remove
from shutil import copy

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

report_names = []
report_list = []
for file in listdir(mims_directory + 'Reports'):
    report_names.append(file[:-4])
    with open(mims_directory + 'Reports\\' + file, 'r') as open_file:
        report_data = open_file.read()
        if len(report_data) > 0:
            report_list.append(report_data)

patient_list = []
for patient in listdir(mims_directory + 'Patients'):
    if patient.__contains__('('):
        new_patient = patient[:patient.index('(')]
        patient_list.append(new_patient)
    else:
        patient_list.append(patient)


class ManageReportsManagement(BoxLayout, Screen):
    name_text_input = ObjectProperty()
    date_text_input = ObjectProperty()
    reason_text_input = ObjectProperty()
    symptoms_text_input = ObjectProperty()

    def logout(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'managementstaff'

    def submit_report(self):
        report_name = self.name_text_input.text + '_' + self.date_text_input.text
        report = self.reason_text_input.text + '\n' + self.symptoms_text_input.text

        while report_name.__contains__('/') or report_name.__contains__('-') or report_name.__contains__(' '):
            report_name = report_name.replace('/', '.')
            report_name = report_name.replace('-', '.')
            report_name = report_name.replace(' ', '_')

        if len(self.name_text_input.text) > 0 and len(self.date_text_input.text) > 0 and len(self.reason_text_input.text) > 0 and len(self.symptoms_text_input.text) > 0:
            patient_name = report_name.split('_')[0] + '_' + report_name.split('_')[1]
            if patient_name not in patient_list:
                print(patient_name)
                print(patient_list)
                popup = Popup(title="Patient Error",
                              content=Label(text="Patient is not in system. \nPlease create user and try again."),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return
            with open(mims_directory + 'Reports\\' + report_name + '.txt', 'w+') as open_file:
                open_file.write(report)

        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please enter all fields"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        report_list.append(report)
        report_names.append(report_name)

        self.report_names.adapter.data.extend([report_name])
        self.report_names._trigger_reset_populate()
        self.synchronize_folders()
        self.reset_fields()

    def delete_report(self, *args):
        if self.report_names.adapter.selection:
            selection = self.report_names.adapter.selection[0].text
            if not selection.__contains__('pending'):
                remove(mims_directory + 'Reports\\' + selection + '.txt')
                self.report_names.adapter.data.remove(selection)
                self.report_names._trigger_reset_populate()
                self.synchronize_folders()
                self.reset_fields()

    def replace_report(self, *args):
        if self.report_names.adapter.selection:
            selection = self.report_names.adapter.selection[0].text
            if not selection.__contains__('pending'):
                report_name = self.name_text_input.text + '_' + self.date_text_input.text
                report = self.reason_text_input.text + '\n' + self.symptoms_text_input.text

                while report_name.__contains__('/') or report_name.__contains__('-') or report_name.__contains__(' '):
                    report_name = report_name.replace('/', '.')
                    report_name = report_name.replace('-', '.')
                    report_name = report_name.replace(' ', '_')

                if len(self.name_text_input.text) > 0 and len(self.date_text_input.text) > 0 and len(
                        self.reason_text_input.text) > 0 and len(self.symptoms_text_input.text) > 0:
                    patient_name = report_name.split('_')[0] + '_' + report_name.split('_')[1]
                    if patient_name not in patient_list:
                        popup = Popup(title="Patient Error",
                                      content=Label(text="Patient is not in system. \nPlease create user and try again."),
                                      size_hint=(None, None), size=(400, 400))
                        popup.open()
                        return
                    with open(mims_directory + 'Reports\\' + report_name + '.txt', 'w+') as open_file:
                        open_file.write(report)
                    report_list[report_names.index(selection)] = report
                else:
                    self.name_text_input.text = selection.split('_')[0] + '_' + selection.split('_')[1]
                    self.date_text_input.text = selection.split('_')[2]
                    self.reason_text_input.text = report_list[report_names.index(selection)].split('\n')[0]
                    self.symptoms_text_input.text = report_list[report_names.index(selection)].split('\n')[1]
                    return

                self.report_names.adapter.data.remove(selection)
                if selection != report_name:
                    rename(mims_directory + 'Reports\\' + selection + '.txt',
                           mims_directory + 'Reports\\' + report_name + '.txt')
                    self.report_names.adapter.data.extend([report_name])

                self.report_names._trigger_reset_populate()
                self.synchronize_folders()
                self.reset_fields()

    def reset_fields(self):
        self.name_text_input.text = ""
        self.date_text_input.text = ""
        self.reason_text_input.text = ""
        self.symptoms_text_input.text = ""

    @staticmethod
    def synchronize_folders():
        for report_file in listdir(mims_directory + 'Reports'):
            name = report_file.split('_')[0] + '_' + report_file.split('_')[1]
            date = report_file.split('_')[2][:-4]
            for patient_file in listdir(mims_directory + 'Patients\\'):
                if patient_file.__contains__(name):
                    file_found = False
                    pending_found = False
                    if date.__contains__('('):
                        new_date = date[:date.index('(')]
                    else:
                        new_date = ""
                    for patient_report in listdir(mims_directory + 'Patients\\' + patient_file):
                        if patient_report[:-4] == date:
                            file_found = True
                        if patient_report[:-4] == new_date:
                            pending_found = True
                    if not file_found and not pending_found:
                        copy(mims_directory + 'Reports\\' + report_file, mims_directory + 'Patients\\' + patient_file + '\\' + date + '.txt')
                    elif not file_found and pending_found:
                        rename(mims_directory + 'Patients\\' + patient_file + '\\' + new_date + '.txt', mims_directory + 'Patients\\' + patient_file + '\\' + date + '.txt')

    def approve(self):
        if self.report_names.adapter.selection:
            selection = self.report_names.adapter.selection[0].text
            if selection.__contains__('pending'):
                if selection.__contains__('pending submission'):
                    self.report_names.adapter.data.remove(selection)
                    self.report_names.adapter.data.extend([selection[:selection.index('(')]])
                    rename(mims_directory + 'Reports\\' + selection + '.txt', mims_directory + 'Reports\\' + selection[:selection.index('(')] + '.txt')
                elif selection.__contains__('pending deletion'):
                    self.report_names.adapter.data.remove(selection)
                    remove(mims_directory + 'Reports\\' + selection + '.txt')
                elif selection.__contains__('pending replacement'):
                    self.report_names.adapter.data.remove(selection)
                    self.report_names.adapter.data.extend([selection[:selection.index('(')]])
                    remove(mims_directory + 'Reports\\' + selection + '.txt')
                    rename(mims_directory + 'Reports\\' + selection + '.txt', mims_directory + 'Reports\\' + selection[:selection.index('(')] + '.txt')

    def deny(self):
        if self.report_names.adapter.selection:
            selection = self.report_names.adapter.selection[0].text
            if selection.__contains__('pending'):
                if selection.__contains__('pending submission'):
                    self.report_names.adapter.data.remove(selection)
                    remove(mims_directory + 'Reports\\' + selection + '.txt')
                elif selection.__contains__('pending deletion'):
                    self.report_names.adapter.data.remove(selection)
                    self.report_names.adapter.data.extend([selection[:selection.index('(')]])
                    rename(mims_directory + 'Reports\\' + selection + '.txt', mims_directory + 'Reports\\' + selection[:selection.index('(')] + '.txt')
                elif selection.__contains__('pending replacement'):
                    self.report_names.adapter.data.remove(selection)
                    self.report_names.adapter.data.extend([selection[:selection.index('(')]])
                    remove(mims_directory + 'Reports\\' + selection[:selection.index('(')] + '.txt')
                    rename(mims_directory + 'Reports\\' + selection + '.txt', mims_directory + 'Reports\\' + selection[:selection.index('(') + '.txt'])


class ManageReportsManagementApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    ManageReportsManagementApp().run()
