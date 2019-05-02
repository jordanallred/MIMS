from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager
from os import listdir, mkdir, rename, removedirs
from shutil import rmtree

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


class ManagePatientsAdmin(BoxLayout, Screen):
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
        self.manager.current = 'medicalprofessional'

    def submit_patient(self):
        patient_name = self.name_text_input.text

        while patient_name.__contains__(' '):
            patient_name = patient_name.replace(' ', '_')

        if len(self.name_text_input.text) > 0:
            if patient_name in patient_names:
                popup = Popup(title="Patient Error",
                              content=Label(text="Patient is already in system."),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return
            mkdir(mims_directory + 'Patients\\' + patient_name)
        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please enter all fields"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        patient_names.append(patient_name)

        self.patient_names.adapter.data.extend([patient_name])
        self.patient_names._trigger_reset_populate()

    def delete_patient(self, *args):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if not selection.__contains__('pending'):
                rmtree(mims_directory + 'Patients\\' + selection)
                self.patient_names.adapter.data.remove(selection)
                self.patient_names._trigger_reset_populate()

    def replace_patient(self, *args):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if not selection.__contains__('pending'):
                patient_name = self.name_text_input.text
                if len(self.name_text_input.text) > 0:
                    while patient_name.__contains__(' '):
                        patient_name = patient_name.replace(' ', '_')

                    if patient_name in patient_names:
                        popup = Popup(title="Patient Error",
                                      content=Label(text="Patient is already in system."),
                                      size_hint=(None, None), size=(400, 400))
                        popup.open()
                        return
                    patient_names[patient_names.index(selection)] = patient_name
                else:
                    self.name_text_input.text = selection
                    return

                if selection != patient_name:
                    rename(mims_directory + 'Patients\\' + selection,
                           mims_directory + 'Patients\\' + patient_name)
                    self.patient_names.adapter.data.remove(selection)
                    self.report_names.adapter.data.extend([patient_name])

                self.patient_names._trigger_reset_populate()

    def approve(self):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if selection.__contains__('pending'):
                if selection.__contains__('pending submission'):
                    self.patient_names.adapter.data.remove(selection)
                    self.patient_names.adapter.data.extend([selection[:selection.index('(')]])
                    rename(mims_directory + 'Patients\\' + selection, mims_directory + 'Patients\\' + selection[:selection.index('(')])
                elif selection.__contains__('pending deletion'):
                    self.patient_names.adapter.data.remove(selection)
                    rmtree(mims_directory + 'Patients\\' + selection)

    def deny(self):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if selection.__contains__('pending'):
                if selection.__contains__('pending submission'):
                    self.patient_names.adapter.data.remove(selection)
                    rmtree(mims_directory + 'Patients\\' + selection)
                elif selection.__contains__('pending deletion'):
                    self.patient_names.adapter.data.remove(selection)
                    self.patient_names.adapter.data.extend([selection[:selection.index('(')]])
                    rename(mims_directory + 'Patients\\' + selection, mims_directory + 'Patients\\' + selection[:selection.index('(')])


class ManagePatientsAdminApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    ManagePatientsAdminApp().run()
