from logic import BarcodeReader
from PIL import Image
import unittest


class TestBarcode(unittest.TestCase):
    def test_validate_low_dimensions(self):
        img = Image.open('barcode_image_test_1.png')
        self.assertTrue(BarcodeReader(img))

    def test_validate_medium_dimensions(self):
        img = Image.open('barcode_image_test_2.png')
        self.assertTrue(BarcodeReader(img))

    def test_validate_high_dimensions(self):
        img = Image.open('barcode_image_test_3.png')
        self.assertTrue(BarcodeReader(img))

    def test_validate_transparent_background(self):
        img = Image.open('barcode_image_test_4.png')
        self.assertTrue(BarcodeReader(img))

if __name__ == '__main__':
    
    runner = unittest.TextTestRunner()
    program = unittest.main(testRunner=runner, exit=False)

    result = program.result


    if result.wasSuccessful():
        print("All tests passed!")
        barcode_reader = BarcodeReader()
    else:
        print("Some tests failed.")
        if result.failures:
            print("\nFailed tests:")
            for test_case, traceback in result.failures:
                print(f"- {test_case.id()}")
        
        if result.errors:
            print("\nErrored tests:")
            for test_case, traceback in result.errors:
                print(f"- {test_case.id()}")
