from logic import BarcodeReader
from PIL import Image
import unittest
from gui import GUI


class TestBarcode(unittest.TestCase):
    def test_validate_low_dimensions(self):
        img = Image.open('barcode_image_test_1.png')
        barcode_reader = BarcodeReader(img, True)

        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_medium_dimensions(self):
        img = Image.open('barcode_image_test_2.png')
        barcode_reader = BarcodeReader(img, True)
    
        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_high_dimensions(self):
        img = Image.open('barcode_image_test_3.png')
        barcode_reader = BarcodeReader(img, True)
        
        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_transparent_background(self):
        img = Image.open('barcode_image_test_4.png')
        barcode_reader = BarcodeReader(img, True)
        
        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_different_colours(self):
        img = Image.open('barcode_image_test_5.png')
        barcode_reader = BarcodeReader(img, True)
        print(barcode_reader.read_barcode())
        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_gradient(self):
        img = Image.open('barcode_image_test_6.png')
        barcode_reader = BarcodeReader(img, True)
        
        if barcode_reader.read_barcode() == False:
            self.fail()

    def test_validate_gray(self):
        img = Image.open('barcode_image_test_7.png')
        barcode_reader = BarcodeReader(img, True)
        
        if barcode_reader.read_barcode() == False:
            self.fail()
        
if __name__ == '__main__':
    
    runner = unittest.TextTestRunner()
    program = unittest.main(testRunner=runner, exit=False)

    result = program.result


    if result.wasSuccessful():
        print("All tests passed!")
        gui = GUI()
    
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