from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.screenmanager import ScreenManager
from os import listdir, mkdir, rename, removedirs
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

patient_names = []
for patient in listdir(mims_directory + 'Patients'):
    patient_names.append(patient)


class ManagePatients(BoxLayout, Screen):
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
        self.manager.current = 'mpis'

    def submit_patient(self):
        patient_name = self.name_text_input.text

        if patient_name.count(' ') == 0:
            popup = Popup(title="Patient Error",
                          content=Label(text="Patient name must include first and last names."),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

        elif patient_name.count(' ') > 1:
            popup = Popup(title="Patient Error",
                          content=Label(text="Please enter first and last names only."),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return

        else:
            patient_name = patient_name.replace(' ', '_')

        if len(self.name_text_input.text) > 0:
            if patient_name in patient_names:
                popup = Popup(title="Patient Error",
                              content=Label(text="Patient is already in system."),
                              size_hint=(None, None), size=(400, 400))
                popup.open()
                return
            mkdir(mims_directory + 'Patients\\' + patient_name + '(pending submission)')
        else:
            popup = Popup(title="Input Error",
                          content=Label(text="Please enter all fields"),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
            return
        patient_names.append(patient_name)

        self.patient_names.adapter.data.extend([patient_name + '(pending submission)'])
        self.patient_names._trigger_reset_populate()

    def delete_patient(self, *args):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if not selection.__contains__('pending'):
                rename(mims_directory + 'Patients\\' + selection, mims_directory + 'Patients\\' + selection + '(pending deletion)')
                self.patient_names.adapter.data.remove(selection)
                self.patient_names.adapter.data.extend([selection + '(pending deletion)'])
                self.patient_names._trigger_reset_populate()

    def replace_patient(self, *args):
        if self.patient_names.adapter.selection:
            selection = self.patient_names.adapter.selection[0].text
            if not selection.__contains__('pending'):

                patient_name = self.name_text_input.text

                if len(self.name_text_input.text) > 0:
                    if not patient_name.__contains__(' '):
                        popup = Popup(title="Patient Error",
                                      content=Label(text="Patient name must include first and last names."),
                                      size_hint=(None, None), size=(400, 400))
                        popup.open()
                        return

                    patient_name = patient_name.replace(' ', '_')

                    if patient_name.__contains__(' '):
                        popup = Popup(title="Patient Error",
                                      content=Label(text="Please enter first and last names only."),
                                      size_hint=(None, None), size=(400, 400))
                        popup.open()
                        return

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

                self.patient_names.adapter.data.remove(selection)

                if selection != patient_name:
                    copy(mims_directory + 'Patients\\' + selection,
                         mims_directory + 'Patients\\' + patient_name + '(pending submission)')
                    rename(mims_directory + 'Patients\\' + selection,
                           mims_directory + 'Patients\\' + selection + '(pending deletion)')
                    self.report_names.adapter.data.extend([selection + '(pending deletion)'])
                    self.report_names.adapter.data.extend([patient_name + '(pending submission)'])
                else:
                    copy(mims_directory + 'Patients\\' + selection,
                         mims_directory + 'Patients\\' + patient_name + '(pending replacement)')
                    self.report_names.adapter.data.extend([selection + '(pending replacement)'])

                self.patient_names._trigger_reset_populate()


class ManagePatientsApp(App):
    def build(self):
        manager = ScreenManager.current_screen
        return manager


if __name__ == '__main__':
    ManagePatientsApp().run()
