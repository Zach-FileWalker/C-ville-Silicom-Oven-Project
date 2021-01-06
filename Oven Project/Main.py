from CSVManager import CSVManager
import matplotlib.pyplot as plt
from CvilleOvenTranslator import CvilleOvenTranslator
import PySimpleGUI as sg
from sys import exit
from time import sleep
from json import (load as jsonload, dump as jsondump)
from os import path


# Time/Temperature calculator for estimates
def ttcalc(dictList: [{}], type: str):
    adam = CvilleOvenTranslator()
    prevtemp = adam.getTemp()       # previous temp
    ttime = 0                       # total time
    datime = []
    datemp = []
    flag = False                    # flag for out-of-bounds ramp rates

    for elem in dictList:
        sshift = abs(float(elem["Temp"]) - prevtemp)    # size of the shift
        targtemp = float(elem["Temp"])                  # target temp
        rrate = float(elem["Ramp Rate"])                # ramp rate

        # convert to negative ramp rate if decrease in temp
        if targtemp - prevtemp < 0:
            rrate = -rrate

        # if ramp rate outside oven limits:
        if type == 'Temp' and (not -10 <= rrate <= 17):
            flag = True

            # display error message
            while True:
                popup_layout_2 = [[sg.Text("Error: Ramp rate outside oven limits")]]
                popup_window_2 = sg.Window('Error Message', popup_layout_2)

                popup_event_2, popup_values_2 = popup_window_2.read()
                if popup_event_2 is None or popup_event_2 == 'Exit':
                    break

        else:
            rrate /= 10
            atemp = 0               # accumulated temp
            ctemp = prevtemp        # current temp

            # ramp
            while atemp < sshift:
                ttime += 0.1
                datime.append(ttime)

                ctemp += rrate
                datemp.append(ctemp)

                atemp += abs(rrate)

            atime = 0       # accumulated time

            # dwell
            while atime < float(elem["Time"]):
                atime += 0.1
                ttime += 0.1
                datime.append(ttime)
                datemp.append(ctemp)

            prevtemp = targtemp     # set prevtemp in preparation for next loop

    if type == 'Time':
        return datime
    elif type == 'Temp' and flag == False:
        return datemp

    # else return error
    return -1


# JSON settings loader upon program startup/update
def load_settings():
    config_file = path.join(path.dirname(__file__), r'config_file.cfg')
    try:
        with open(config_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... Creating a blank one', keep_on_top=True,
                           background_color='red', text_color='white')
        with open(config_file, 'w') as f:
            settings = {'theme': '', 'csv_filepath': '', 'ser_filepath': ''}
            jsondump(settings, f)

    return settings


def update_theme(config_file: str, theme: str):
    settings = load_settings()
    settings["theme"] = theme

    with open(config_file, 'w') as f:
        jsondump(settings, f)


# saves a new CSV filepath to the JSON settings file
def update_csv_filepath(config_file: str, csv_filepath: str):
    settings = load_settings()
    settings["csv_filepath"] = csv_filepath

    with open(config_file, 'w') as f:
        jsondump(settings, f)


# saves a new serial port filepath to the JSON settings file
def update_ser_filepath(config_file: str, ser_filepath: str):
    settings = load_settings()
    settings["ser_filepath"] = ser_filepath

    with open(config_file, 'w') as f:
        jsondump(settings, f)


def main():

    # setup
    owen = CSVManager()
    window = None
    configfile = path.join(path.dirname(__file__), r'config_file.cfg')

    # main
    while True:
        settings = load_settings()

        # load theme if field empty
        if settings['theme'] != '':
            sg.theme(settings['theme'])

        # GUI layout
        layout = [[sg.Text("Theme selector:"), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-'),
                   sg.Button("Preview Themes"), sg.Button("Update Theme")],
                  [sg.Text("   ")],
                  [sg.Text('CSV File:', size=(8, 1)), sg.Input(key="-CSV_NAME-", default_text=settings['csv_filepath']),
                   sg.FileBrowse(), sg.Button("Save as Default CSV File")],
                  [sg.Button("Display Profile as Graph"), sg.Button("Run Profile"),
                   sg.Button("Load Default Oven Settings")]]

        if window is None:
            window = sg.Window('Edge Remote Oven Controller', layout)

        event, values = window.read()
        if event is None or event == 'Exit':
            break

        elif event == "Save Serial Path":
            update_ser_filepath(configfile, values['-SER_PATH-'])

        elif event == "Save as Default CSV File":
            update_csv_filepath(configfile, values['-CSV_NAME-'])

        elif event == "Update Theme":
            window.close()
            window = None
            sg.theme(values['-THEME-'])
            update_theme(configfile, values['-THEME-'])

        elif event == "Preview Themes":
            sg.theme_previewer(scrollable=True)

        elif event == "Load Default Oven Settings":
            adam = CvilleOvenTranslator()
            adam.load_default_settings()

        elif event == "Display Profile as Graph":

            # if csv not in correct format
            format = owen.verifyFormat(values['-CSV_NAME-'])
            if format != True:
                # display error message
                while True:
                    popup_layout = [[sg.Text(format)]]
                    popup_window = sg.Window('Error Message', popup_layout)

                    popup_event, popup_values = popup_window.read()
                    if popup_event is None or popup_event == 'Exit':
                        break

            else:
                adam = CvilleOvenTranslator()

                # weak handshake
                if adam.getTemp() == None:
                    exit("Could not handshake with oven")

                # read profile only if field not empty
                # if values['-CSV_NAME-'] != '':
                #     dictList = owen.readProfile(values['-CSV_NAME-'])

                if values['-CSV_NAME-'].endswith('.csv'):
                    dictList = owen.readProfile(values['-CSV_NAME-'])

                    allTime = ttcalc(dictList, 'Time')
                    allTemp = ttcalc(dictList, 'Temp')

                    if allTime != -1 and allTemp != -1:
                        axzero = plt.subplot()
                        axzero.plot(allTime, allTemp)
                        axzero.set_xlabel("Time (mins)")
                        axzero.set_ylabel("Temp (C)")
                        plt.show()

        elif event == "Run Profile":

            # if csv not in correct format
            format = owen.verifyFormat(values['-CSV_NAME-'])
            if format != True:
                # display error message
                while True:
                    popup_layout = [[sg.Text(format)]]
                    popup_window = sg.Window('Error Message', popup_layout)

                    popup_event, popup_values = popup_window.read()
                    if popup_event is None or popup_event == 'Exit':
                        break

            else:
                dictList = owen.readProfile(values['-CSV_NAME-'])
                adam = CvilleOvenTranslator()

                # weak handshake
                if adam.getTemp() is None:
                    exit("Could not handshake with oven")

                prevTemp = adam.getTemp()
                time = [0]
                # time_run = [0]              # FINISH LATER
                total_time = 0
                # total_time_run = 0          # FINISH LATER
                set_temp = [prevTemp]
                get_temp = [prevTemp]

                allTime = ttcalc(dictList, 'Time')
                allTemp = ttcalc(dictList, 'Temp')

                # fig, (ax0, ax1) = plt.subplots(2)
                ax = plt.subplot()
                ax.set_xlabel("Time (mins)")
                ax.set_ylabel("Temp (C)")
                # ax1.set_xlabel("Time (mins)")
                # ax1.set_ylabel("Temp (C)")
                ax.plot(allTime, allTemp)

                for elem in dictList:
                    size_shift = abs(float(elem["Temp"]) - prevTemp)
                    targetTemp = float(elem["Temp"])
                    rampRate = float(elem["Ramp Rate"])

                    # convert to negative ramp rate if necessary
                    if targetTemp - prevTemp < 0:
                        rampRate = -rampRate

                    rampRate /= 10
                    accum_temp = 0
                    curr_temp = prevTemp

                    # ramp
                    while accum_temp < size_shift:
                        plt.cla()
                        total_time += 0.1
                        # total_time_run += 0.1                   # FINISH LATER
                        time.append(total_time)
                        # time_run.append(total_time_run)         # FINISH LATER

                        curr_temp += rampRate                   # increment current temperature
                        curr_temp = round(curr_temp, 1)
                        adam.setTemp(curr_temp)
                        set_temp.append(curr_temp)
                        get_temp.append(adam.getTemp())

                        ax.plot(allTime, allTemp)
                        ax.plot(time, get_temp)
                        # ax1.plot(time, set_temp)
                        # ax1.plot(time, get_temp)
                        plt.pause(6)
                        # writeTempOven(curr_temp)

                        accum_temp += abs(rampRate)

                    accum_time = 0

                    # dwell
                    while accum_time < float(elem["Time"]):
                        plt.cla()

                        accum_time += 0.1
                        total_time += 0.1
                        time.append(total_time)
                        set_temp.append(curr_temp)
                        get_temp.append(adam.getTemp())

                        ax.plot(allTime, allTemp)
                        ax.plot(time, get_temp)
                        # ax1.plot(time, set_temp)
                        # ax1.plot(time, get_temp)
                        plt.pause(6)

                    prevTemp = targetTemp


if __name__ == "__main__":
    main()