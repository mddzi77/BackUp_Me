import json
import os
import time
import PySimpleGUI as sg
import pandas as pd


class Database:

    def __init__(self):

        # Open json file with selected directories
        with open('config.json', encoding='UTF-8') as f:
            self.dirs = json.load(f)['dirs']

        self.temp_df = None
        self.data_to_copy = None
        self.data_at_destination = None

    def check_exist(self, directory):
        """
        Check what files and folders selected directory contains and save it to dataframe
        :param directory: Selected directory
        :return: Pandas dataframe with found files and folders
        """

        if os.path.isdir(directory):
            dirs_list = [directory]
            # resets temp_df in case it's not empty
            self.temp_df = None
            self.temp_df = pd.DataFrame(columns=['path', 'type'])
            self.check_recur(dirs_list)

        return self.temp_df

    def check_recur(self, dirs_list: list):

        start_dirs_list = dirs_list.copy()
        for f in os.listdir(start_dirs_list[0]):
            #
            start_time = time.time()
            #
            f_path = os.path.join(start_dirs_list[0], f)
            row = [
                f_path,
                'file' if os.path.isfile(f_path) else 'folder'
            ]
            self.temp_df.loc[len(self.temp_df)] = row
            if not os.path.isfile(f_path):
                dirs_list.append(f_path)
            #
            end_time = time.time()
            print((end_time - start_time) * 1000, 'ms')
            #

        dirs_list.remove(start_dirs_list[0])
        for row in dirs_list:
            self.check_recur([row])


class Gui:

    def __init__(self):
        self.db = Database()

    def starting_window(self):

        layout = [
            [[sg.T(f'Copy {row[0]} to {row[1]}')] for row in self.db.dirs],
            [sg.Button('More', k='_more_'), sg.Button('Start', k='_start_')]
        ]

        return sg.Window('BackUp Me', layout)

    def new_dir(self):

        col1 = sg.Col([
            [sg.Button('Copy from', k='_c_from_')],
            [sg.Multiline()]
        ])
        col2 = sg.Col([
            [sg.Button('Copy to', k='_c_from_')],
            [sg.Multiline()]
        ])
        layout = [
            [col1, col2]
        ]

        return sg.Window("More", layout)


class App:

    def __init__(self):
        self.db = Database()
        self.gui = Gui()
        self.window = None

    def run(self):

        self.window = self.gui.starting_window()

        while True:

            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                self.window.close()
                break
            elif event == '_start_':
                if not self.db.dirs:
                    sg.Popup('There are no directories selected')


if __name__ == '__main__':
    App().run()
