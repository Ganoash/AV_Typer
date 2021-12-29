import unittest
from os import path

from src.Controller import Controller
from src.UI.Scene import SelectScene, TypeScene
from src.Data.File import FileBuilder, SheetType
from src.Reader.Reader import Reader, File, BorrelReader, SimpleReader, WeekendReader
from src.Data.Config import Config, WeekendConfig, BorrelConfig

class ControllerTest(unittest.TestCase):

    def test_instantiation(self):
        controller = Controller(test=True)
        self.assertIsInstance(controller.scene, SelectScene)
        self.assertEqual(controller.reader, None)
        self.assertIsInstance(controller.builder, FileBuilder)

    def test_reader_instantiation(self):
        controller = Controller(test=True)
        self.assertIsNone(controller.reader)
        self.assertIsNone(controller.file)

        controller.set_path(path.join(path.dirname(__file__), "../../test_data/Activiteitensheet 21.xlsx"))
        controller.set_type(SheetType.ACTIVITEIT)
        controller.build_file()

        self.assertIsInstance(controller.reader, Reader)
        self.assertIsInstance(controller.file, File)

    def test_scene_switch(self):
        controller = Controller(test=True)
        self.assertIsInstance(controller.scene, SelectScene)
        controller.set_path(path.join(path.dirname(__file__), "../../test_data/Activiteitensheet 21.xlsx"))
        controller.set_type(SheetType.ACTIVITEIT)
        controller.transition_to_type()

        self.assertIsInstance(controller.scene, TypeScene)

        controller.transition_to_select()
        self.assertIsInstance(controller.scene, SelectScene)

    def test_scene_switch_data(self):
        controller = Controller(test=True)
        self.assertIsInstance(controller.scene, SelectScene)
        controller.set_path(path.join(path.dirname(__file__), "../../test_data/Activiteitensheet 21.xlsx"))
        controller.set_type(SheetType.WEEKEND)
        controller.transition_to_type()

        self.assertIsInstance(controller.scene, TypeScene)

        controller.transition_to_select()
        self.assertEqual(controller.builder.path, path.join(path.dirname(__file__), "../../test_data/Activiteitensheet 21.xlsx"))
        self.assertEqual(controller.builder.type, SheetType.WEEKEND)

    def test_file_state(self):
        self.file_state(SheetType.WEEKEND)
        self.file_state(SheetType.BORREL)
        self.file_state(SheetType.ACTIVITEIT)
        self.file_state(SheetType.SIMPEL)

    def file_state(self, sheet_type):
        controller = Controller(test=True)
        controller.set_path(path.join(path.dirname(__file__), "../../test_data/Activiteitensheet 21.xlsx"))
        controller.set_type(sheet_type)
        controller.transition_to_type()

        self.assertEqual(controller.file.type, sheet_type)
        self.assertTrue(controller.file is controller.reader.file)
        if sheet_type is SheetType.WEEKEND:
            self.assertIsInstance(controller.file.config, WeekendConfig)
            self.assertIsInstance(controller.reader, WeekendReader)
        elif sheet_type is SheetType.BORREL:
            self.assertIsInstance(controller.file.config, BorrelConfig)
            self.assertIsInstance(controller.reader, BorrelReader)
        elif sheet_type is SheetType.SIMPEL:
            self.assertIsInstance(controller.file.config, Config)
            self.assertIsInstance(controller.reader, SimpleReader)
        else:
            self.assertIsInstance(controller.file.config, Config)
            self.assertIsInstance(controller.reader, Reader)




if __name__ == '__main__':
    unittest.main()
