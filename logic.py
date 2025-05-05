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
        

    # def generate_barcode(self):
        # upc = barcode.get('upca', '03600029145', writer=ImageWriter())
        # print(upc.save("upc_barcode"))

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

        
        for x in range(starting_index, self.dimensions[0]):
            
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if len(current_line_list) == scale:
                    barcode_lines.append(((round(len(current_line_list)/scale)), 255))
                    current_line_list = []
                    
                current_line_list.append(x)

                

            elif self.pixels[x, self.dimensions[1]/2] == 255:
               
                if len(current_line_list) == scale:
                    barcode_lines.append(((round(len(current_line_list)/scale)), 0))
                    current_line_list = []
                    
                current_line_list.append(x)

        # print(barcode_lines)
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
                # print("here")
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
        pattern = [(1, 255),(1, 0),(1, 255),(1, 0),(1, 255)]
        pattern_len = len(pattern)
        i = 0
        while i <= len(list) - pattern_len:
            if list[i:i+pattern_len] == pattern:
                # Split the list at the pattern
                return list[:i], list[i+pattern_len:]
            i += 1
        return list, []
    
    @staticmethod
    def remove_pattern(list):
        for i in range(3):
            del list[0]

        return list


    def sort_barcode_list(self, barcode_list):
        # print(barcode_list)
        left, right = self.remove_middle_pattern(barcode_list)

        print(f"{left} \n\n\n {right} \n\n\n")

        left = self.remove_pattern(left)
        right = self.remove_pattern(list(reversed(right)))
        
        self.translate_lines(left, list(reversed(right)))

        
    @staticmethod
    def translate_lines(left, right):
        codes = {
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
        i = 0
        current_line = []
        code = ""
        
        for line in left:
            if i == 7:
                
                code += str(codes[tuple(current_line)])
                current_line = [line]
                i =+ line[0]
                
            else:
                current_line.append(line)
                i += line[0]
                
        code += str(codes[tuple(current_line)])
        current_line= []
        print(current_line)


        # i = 0
        # current_line = []
        # for line in right:
            
        #     if i == 7:

                
        #         code += str(codes[tuple(current_line)])
        #         current_line = [line]
        #         i = line[0]
                
        #     else:
                
        #         current_line.append(line)
        #         i += line[0]

        # code += str(codes[tuple(current_line)])
                

        print(f"{code} is the code")
        
