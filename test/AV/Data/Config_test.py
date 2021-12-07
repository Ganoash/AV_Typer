import unittest
from AV.Data.Config import Config, WeekendConfig, BorrelConfig
from AV.Data.SheetType import SheetType

class MyTestCase(unittest.TestCase):

    def test_config_borrel_instantiation(self):
        """
        instantiating a Config for sheetType Borrel should return a BorrelConfig
        """
        config = Config(SheetType.BORREL)
        self.assertIsInstance(config, BorrelConfig)

    def test_borrel_accessor(self):
        """
        instantiating a Config for sheetType Borrel should return a BorrelConfig
        """
        config = Config(SheetType.BORREL)
        self.assertIsNotNone(config.bp_range)

    def test_config_weekend_instantiation(self):
        """
        instantiating a Config for sheetType Weekend should return a WeekendConfig
        """
        config = Config(SheetType.WEEKEND)
        self.assertIsInstance(config, WeekendConfig)

    def test_weekend_accessor(self):
        """
        instantiating a Config for sheetType Borrel should return a BorrelConfig
        """
        config = Config(SheetType.WEEKEND)
        self.assertIsNotNone(config.voorklim_index)

    def test_config_other_instantiation(self):
        """
        instantiating a Config for sheetType Activiteit, Simpel should return a Config
        """
        config = Config(SheetType.ACTIVITEIT)
        self.assertIsInstance(config, Config)
        self.assertNotIsInstance(config, WeekendConfig)
        self.assertNotIsInstance(config, BorrelConfig)

        config = Config(SheetType.SIMPEL)
        self.assertIsInstance(config, Config)
        self.assertNotIsInstance(config, WeekendConfig)
        self.assertNotIsInstance(config, BorrelConfig)

    def test_other_accessor(self):
        """
        instantiating a Config for sheetType Borrel should return a BorrelConfig
        """
        config = Config(SheetType.SIMPEL)
        try:
            config.voorklim_index
            self.fail("voorklim_index should raise exception")
        except AttributeError:
            try:
                config.bp_range
                self.fail("bp_range should raise exception")
            except AttributeError:
                pass
        config = Config(SheetType.ACTIVITEIT)
        try:
            config.voorklim_index
            self.fail("voorklim_index should raise exception")
        except AttributeError:
            try:
                config.bp_range
                self.fail("bp_range should raise exception")
            except AttributeError:
                pass

    def test_return_values(self):
        conf_a = Config(SheetType.ACTIVITEIT)
        conf_w = Config(SheetType.WEEKEND)
        conf_b = Config(SheetType.BORREL)
        conf_s = Config(SheetType.SIMPEL)

        self.assertTrue(conf_a.column_range == conf_w.column_range == conf_b.column_range != conf_s.column_range)
        self.assertTrue(conf_w.overzicht_range == conf_b.overzicht_range
                        != conf_a.overzicht_range != conf_s.overzicht_range)
        self.assertTrue(conf_w.afronding_range == conf_b.afronding_range
                        != conf_a.afronding_range != conf_s.afronding_range)





if __name__ == '__main__':
    unittest.main()
