import threading
from configparser import ConfigParser
from os import path
from AV.Reader.Reader import Reader, Simple_Reader
from AV.Writer.Writer import Writer
from AV.ControllerData import ControllerData


class Controller(object):

    def __init__(self, data: ControllerData):
        config = ConfigParser()
        config.read(path.join(path.dirname(__file__), "./__conf__.ini"))
        self.reader = None
        self.data = data
        self.writer = Writer()
        self.stop_button = config['Typing']['leave_key']

    def set_workbook(self):
        if self.data.sheet_type is None or self.data.file_path is None:
            raise ValueError('sheet_name or file_path not set')
        if self.data.sheet_type == 'simpel':
            self.reader = Simple_Reader(self.data)
            return
        self.reader = Reader(self.data)

    def start_write_baten(self):
        if self.reader is None:
            raise ValueError('Reader is not yet initialized')
        print(self.reader)
        t = threading.Thread(target=self.writer.write, args=[self.reader.get_baten()])
        t.start()

    def start_write_lasten(self):
        if self.reader is None:
            raise ValueError('Reader is not yet initialized')
        t = threading.Thread(target=self.writer.write, args=[self.reader.get_lasten()])
        t.start()

    def set_sheet_type(self, value):
        self.data.sheet_type = value

    def set_file_path(self, value):
        print('called')
        self.data.file_path = value
        print(self.data.file_path)

    def set_sheet_name(self, value):
        self.data.sheet_name = value

