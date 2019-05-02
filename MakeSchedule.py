from KivyCalendar.calendar_ui import DatePicker
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from os import listdir
from ManageUsers import ManageUsers
from CheckSecurity import CheckSecurity
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import *
from kivy.uix.label import *


user_files = [
    'Management Staff.txt',
    'Medical Patient Interaction Staff.txt',
    'Medical Professional.txt',
    'Non-Medical Patient Interaction Staff.txt'
]

mims_directory = "MIMS\\"

patient_names = []
for patient in listdir(mims_directory + 'Patients'):
    patient_names.append(patient)

class CustomDatePicker(DatePicker):
    def update_value(self, inst):
        self.text = "%s.%s.%s" % tuple(self.cal.active_date)
        self.focus = False


class MakeSchedule(BoxLayout, Screen):
    name_text_input = ObjectProperty()
    datePicker = CustomDatePicker()

    def show_calendar(self):
        self.datePicker.show_popup(1, .5)
        self.name_text_input.text = self.datePicker.text

    def update_appointment(self):
        self.name_text_input.text = self.datePicker.text

    def submit_appointment(self):
        if len(self.name_text_input.text) > 0:
            pass


class MakeScheduleApp(App):
    def build(self):
        return MakeSchedule()
