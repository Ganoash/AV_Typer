import datetime
from configparser import ConfigParser
from os import path
from typing import Tuple
import keyboard
import time
import pandas as pd


class Data_Stepper(object):

    def __init__(self, data):
        self.data: pd.DataFrame = data
        self.tabs = {
            'Datum': 1,
            'Deb_NR': 1,
            'GBK': 1,
            'Doc/fac': 1,
            'Omschrijving': 4,
            'Bedrag': -1,
        }

    def __iter__(self):
        for index, row in self.data.iterrows():
            for key in row.keys():
                print(row[key], type(row[key]))
                if type(row[key]) is float:
                    writable = str(round(row[key], 2))
                    print(writable)
                elif type(row[key]) is datetime.datetime:
                    writable = row[key].strftime('%d%m%y')
                else:
                    writable = str(row[key]) if row[key] else ""

                yield writable, self.tabs[key]


class Writer(object):

    def __init__(self):
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "../__conf__.ini"))
        self.key_press_delay = float(config["Typing"]["key_press_delay"])
        self.tab_delay = float(config["Typing"]["tab_delay"])
        self.leave_key = config["Typing"]["leave_key"]
        self.start_key = config["Typing"]["start_key"]

    def write(self, data: Data_Stepper, double_enter: bool = False):
        for writable, tabs in data:
            keyboard.write(writable, delay=self.key_press_delay)
            self.wait()
            if tabs == -1:
                keyboard.press('enter')
                if double_enter:
                    keyboard.press('enter')
                self.wait()
            else:
                for _ in range(tabs):
                    keyboard.press('tab')
                    self.wait()
            if keyboard.is_pressed(self.leave_key):
                print('terminated')
                break

    def write_lasten(self, overzicht: pd.DataFrame, bijdragers: pd.DataFrame):
        overzicht = Data_Stepper(overzicht)
        bijdragers = Data_Stepper(bijdragers)
        self.wait_for_key()
        self.write(overzicht)
        self.write(bijdragers, True)

    def write_baten(self, df: pd.DataFrame):
        data = Data_Stepper(df)
        self.wait_for_key()
        self.write(data)

    def wait(self):
        time.sleep(self.tab_delay)

    def wait_for_key(self):
        keyboard.wait(self.start_key)
