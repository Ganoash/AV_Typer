# standard library imports
import threading
from os import path
# dependency import
from configparser import ConfigParser
# package imports
from src.Reader.Reader import Reader
from src.Writer.Writer import Writer
from src.Data.File import FileBuilder
from src.UI.Scene import Scene, SceneType
from src.Utility import resource_path


class Controller(object):
    """Controller handling interaction between UI and the rest of the code
    """

    def __init__(self, test=False):
        config = ConfigParser()
        config.read(resource_path("__conf__.ini"))
        self.writer = Writer()
        self.stop_button = config['Typing']['leave_key']
        self.reader = None
        self.file = None

        self.builder = FileBuilder()
        self.scene = Scene(SceneType.SELECT, self)
        self.test = test
        if not self.test:
            self.scene.render()

    def start_write_baten(self):
        t = threading.Thread(target=self.writer.write_baten, args=[self.reader.get_baten()])
        t.start()

    def start_write_lasten(self):
        t = threading.Thread(target=self.writer.write_lasten, args=[*self.reader.get_lasten()])
        t.start()

    def transition_to_type(self):
        if self.build_file():
            scene = Scene(SceneType.TYPE, self)
            if not self.test:
                self.scene.switch(scene)
            self.scene = scene

    def transition_to_select(self):
        self.file = None
        scene = Scene(SceneType.SELECT, self)
        if not self.test:
            self.scene.switch(scene)
        self.scene = scene

    def build_file(self):
        self.file = self.builder.build()
        if self.file:
            self.reader = Reader(self.file)
        print(self.file)
        return bool(self.file)

    def set_path(self, path):
        self.builder.set_path(path)

    def set_type(self, type):
        print("called")
        self.builder.set_type(type)
        print(self.builder.type)

    def set_active(self, name):
        self.file.set_active(name)

    def get_path(self):
        if self.file:
            return self.file.path
        return self.builder.path

    def get_type(self):
        if self.file:
            return self.file.type
        return self.builder.type
