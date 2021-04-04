import PySimpleGUI as sg

# All the stuff inside your window.
layout = [  [sg.Text('Routeur VGF'), sg.InputText()],
            [sg.Text('Nom du site principale'), sg.InputText()],
            [sg.Text('Adresse réseau site principale'), sg.InputText()],
            [sg.Text('Netmask site principale'), sg.InputText()],
            [sg.Text('Serveur principale'), sg.InputText()],
            [sg.Text('Nom du site'), sg.InputText()],
            [sg.Text('Adresse réseau site'), sg.InputText()],
            [sg.Text('Netmask site'), sg.InputText()],
            [sg.Text('Nom de l\'équiepemnt'), sg.InputText()],
            [sg.Text('Suffixe DNS propre au site'), sg.InputText()],
            [sg.Text('Netbios'), sg.InputText()],
            [sg.Text('ADMIN PASS'), sg.InputText(password_char="*")],
            [sg.Text('Box internet IP'), sg.InputText()],
            [sg.Text('Wifi invite pass'), sg.InputText()],
            [sg.Checkbox('Atelier sur site ?')],
            [sg.Checkbox('Est-ce un site principale ?')],
            [sg.Text('Adresse réseau wifi INVITE : 172.16.'), sg.InputText(default_text="190")],
            [sg.Text('Adresse réseau wifi AGENT : 172.16.'), sg.InputText(default_text="200")],
            [sg.Text('Adresse réseau wifi DIGITAL : 172.16.'), sg.InputText(default_text="210")],
            [sg.Text('Adresse réseau wifi ATELIER : 172.16.'), sg.InputText(default_text="220")],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Fortigate Config Generator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print(values)
    print(type(layout))
    print(type(values))

window.close()