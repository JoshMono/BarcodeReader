import barcode
from barcode.writer import ImageWriter
import random
from PIL import Image



class BarcodeReader:
    def __init__(self):        
        self.barcode_img = Image.open('barcode_image.png').convert('L')
        self.barcode_img.show()

        self.read_image()
        self.read_barcode()
        

    def read_image(self):
        self.pixels = self.barcode_img.load()
        self.dimensions = self.barcode_img.size
        



    ###
    ### Reads the barcodes lines
    ###


    def read_barcode(self):
        start_pixels = self.get_start()
        starting_index = start_pixels[0][0]
        scale = self.get_scale(start_pixels)

        barcode_lines = []
        current_line_list = []

        line_switch = False
        
        for x in range(starting_index + (scale * 3), self.dimensions[0] - starting_index - (scale * 3)):
            
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if line_switch:
                    current_line_list = []
                    line_switch = False

                current_line_list.append(x)

                if len(current_line_list) == scale:
                    barcode_lines.append(((round(len(current_line_list)/scale)), 0))
                    current_line_list = []
                    line_switch = False



                    

                

            elif self.pixels[x, self.dimensions[1]/2] == 255:
                
                if not line_switch:
                    current_line_list = []
                    line_switch = True


                current_line_list.append(x)
               



                if len(current_line_list) == scale:
                    barcode_lines.append(((round(len(current_line_list)/scale)), 255))
                    current_line_list = []
                    line_switch = True

        self.sort_barcode_list(barcode_lines)







    ###
    ### Gets starting lines
    ###


    def get_start(self):
        
        line_index = 0
        pixel_list = []
        for x in range(self.dimensions[0]):
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if line_index == 0 or line_index == 2:
                    line_index += 1
                pixel_list.append((x, 0))
                
            elif self.pixels[x, self.dimensions[1]/2] == 255 and line_index != 0:
                if line_index == 1:
                    line_index +=1
                elif line_index == 3:
                    break
                pixel_list.append((x, 255))
        return pixel_list






    ###
    ### Calculates the scale for the lines
    ###


    @staticmethod
    def get_scale(pixel_list):
        return (round(len(pixel_list) / 3))
    




    ###
    ### Pattern Search
    ###
    @staticmethod
    def remove_middle_pattern(list):
        mid_index = len(list) // 2

        left = list[:mid_index]
        right = list[mid_index+1:]
        left.reverse()
        for i in range(2):
            del left[0]

        for i in range(2):
            del right[0]
        left.reverse()
        return left, right
    
    @staticmethod
    def remove_pattern(list):
        for i in range(3):
            del list[0]
        return list


    def sort_barcode_list(self, barcode_list):
        left, right = self.remove_middle_pattern(barcode_list)
        self.translate_lines(left, right)

        
    @staticmethod
    def translate_lines(left, right):
        codes_left = {
            ((1,255),(1,255),(1,255),(1,0),(1,0),(1,255),(1,0)) : 0,
            ((1,255),(1,255),(1,0),(1,0),(1,255),(1,255),(1,0)) : 1,
            ((1,255),(1,255),(1,0),(1,255),(1,255),(1,0),(1,0)) : 2,
            ((1,255),(1,0),(1,0),(1,0),(1,0),(1,255),(1,0)) : 3,
            ((1,255),(1,0),(1,255),(1,255),(1,255),(1,0),(1,0)) : 4,
            ((1,255),(1,0),(1,0),(1,255),(1,255),(1,255),(1,0)) : 5,
            ((1,255),(1,0),(1,255),(1,0),(1,0),(1,0),(1,0)) : 6,
            ((1,255),(1,0),(1,0),(1,0),(1,255),(1,0),(1,0)) : 7,
            ((1,255),(1,0),(1,0),(1,255),(1,0),(1,0),(1,0)) : 8,
            ((1,255),(1,255),(1,255),(1,0),(1,255),(1,0),(1,0)) : 9,
            
            
        }


        codes_right = {
            ((1,0),(1,0),(1,0),(1,255),(1,255),(1,0),(1,255)) : 0,
            ((1,0),(1,0),(1,255),(1,255),(1,0),(1,0),(1,255)) : 1,
            ((1,0),(1,0),(1,255),(1,0),(1,0),(1,255),(1,255)) : 2,
            ((1,0),(1,255),(1,255),(1,255),(1,255),(1,0),(1,255)) : 3,
            ((1,0),(1,255),(1,0),(1,0),(1,0),(1,255),(1,255)) : 4,
            ((1,0),(1,255),(1,255),(1,0),(1,0),(1,0),(1,255)) : 5,
            ((1,0),(1,255),(1,0),(1,255),(1,255),(1,255),(1,255)) : 6,
            ((1,0),(1,255),(1,255),(1,255),(1,0),(1,255),(1,255)) : 7,
            ((1,0),(1,255),(1,255),(1,0),(1,255),(1,255),(1,255)) : 8,
            ((1,0),(1,0),(1,0),(1,255),(1,0),(1,255),(1,255)) : 9,
            
            
        }
        i = 0
        current_line = []
        code = ""
        
        for line in left:
            if i == 7:
                
                code += str(codes_left[tuple(current_line)])
                current_line = [line]
                i =+ line[0]
                
            else:
                current_line.append(line)
                i += line[0]
                
        code += str(codes_left[tuple(current_line)])
        current_line= []
        


        i = 0
        current_line = []
        
        for line in right:
            if i == 7:
                current_line
                code += str(codes_right[tuple(current_line)])
                current_line = [line]
                i =+ line[0]
                
            else:
                current_line.append(line)
                i += line[0]
                
        code += str(codes_right[tuple(current_line)])
        current_line= []
        
                

        print(f"{code} is the code")
        
