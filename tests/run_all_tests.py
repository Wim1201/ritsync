import unittest

# Laad alle testbestanden automatisch in
loader = unittest.TestLoader()
tests = loader.discover(start_dir='tests', pattern='test_*.py')

# Voer alle tests uit
runner = unittest.TextTestRunner(verbosity=2)
runner.run(tests)
