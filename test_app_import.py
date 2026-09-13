import unittest


class AppImportTest(unittest.TestCase):
    def test_app_imports(self):
        import app
        self.assertTrue(hasattr(app, 'app'))


if __name__ == '__main__':
    unittest.main()
