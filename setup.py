from os import getcwd, listdir, mkdir

working_directory = getcwd()

user_files = [
    'Management Staff.txt',
    'Medical Patient Interaction Staff.txt',
    'Medical Professional.txt',
    'Non-Medical Patient Interaction Staff.txt',
    'System Administrator.txt'
]

empty_files = [
    'Appointments.txt',
    'Payments.txt',
    'Services.txt',
    'Suspended Accounts.txt',
]

if __name__ == '__main__':
    if 'MIMS' not in listdir(working_directory):
        mkdir('MIMS')

    for file in user_files:
        with open('MIMS\\' + file, 'w+') as open_file:
            open_file.write('user,password,role\n')

    with open('MIMS\\Failed Login Attempts.txt', 'w+') as open_file:
        open_file.write('0\n')

    for file in empty_files:
        with open('MIMS\\' + file, 'w+') as open_file:
            open_file.write("")

    mkdir('MIMS\\Patients')
    mkdir('MIMS\\Reports')
