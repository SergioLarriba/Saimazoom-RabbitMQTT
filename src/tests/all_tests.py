import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
if __name__ == "__main__":
    # Encuentra todos los tests en el directorio test/classes_tests
    test_suite = unittest.TestLoader().discover('classes_tests')

    # Ejecuta todos los tests encontrados
    unittest.TextTestRunner().run(test_suite)