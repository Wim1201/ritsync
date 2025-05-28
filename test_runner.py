import unittest

if __name__ == '__main__':
    print("🧪 Test gestart...")
    loader = unittest.TestLoader()
    suite = loader.discover('tests')  # Zorg dat ./tests/ bestaat
    runner = unittest.TextTestRunner()
    runner.run(suite)

