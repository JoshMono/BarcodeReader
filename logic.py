import barcode
from barcode.writer import ImageWriter
from random import randint
from PIL import Image, ImageDraw, ImageEnhance



class BarcodeReader:
    def __init__(self ,img=None, test=False):        

        self.test = test
    
        if img == None:
            self.plain_barcode_img = Image.open('barcode_image_test_2.png').convert('RGB')
            self.barcode_img = Image.open('barcode_image_test_2.png').convert('L')
        else:
            self.plain_barcode_img = img.convert('RGB')
            self.barcode_img = img.convert('L')

        threshold = 200
        self.barcode_img = self.barcode_img.point(lambda x: 255 if x > threshold else 0, 'L')

        self.read_image()

        

    def read_image(self):
        self.pixels = self.barcode_img.load()
        self.dimensions = self.barcode_img.size
        



    ###
    ### Reads the barcodes lines
    ###


    def read_barcode(self):
        start_pixels = self.get_start()
        end_pixels = self.get_end()

       
        starting_index = start_pixels[0][0]
        ending_index = end_pixels[0][0]
        scale = self.get_scale(start_pixels)
    
        barcode_lines = []
        current_line_list = []
        current_line_positions = []

        line_switch = False
        
        # while len(barcode_lines) != 89:
        draw = ImageDraw.Draw(self.plain_barcode_img)
   
        for x in range(starting_index + (scale * 3), self.dimensions[0] - ending_index - (scale * 3)):
            
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if line_switch:
                    if len(current_line_list) > round(scale * .75):
                        barcode_lines.append(((round(len(current_line_list)/round(scale * .75))), 255))
                        draw.line((current_line_list[0], self.dimensions[1]/2, current_line_list[len(current_line_list) - 1], self.dimensions[1]/2), fill="blue", width=3)
                    current_line_list = []
                    line_switch = False

                current_line_list.append(x)
                

                if len(current_line_list) == scale:
                    barcode_lines.append(((round(len(current_line_list)/scale)), 0))
                    draw.line((current_line_list[0], self.dimensions[1]/2, current_line_list[len(current_line_list) - 1], self.dimensions[1]/2), fill="red", width=3)
                    
                    current_line_list = []
                    line_switch = False

            elif self.pixels[x, self.dimensions[1]/2] == 255:
                
                if not line_switch:
                    if len(current_line_list) > round(scale * .75):
                        barcode_lines.append(((round(len(current_line_list)/round(scale * .75))), 0))
                        draw.line((current_line_list[0], self.dimensions[1]/2, current_line_list[len(current_line_list) - 1], self.dimensions[1]/2), fill="red", width=3)
                    current_line_list = []
                    line_switch = True


                current_line_list.append(x)
                
                if len(current_line_list) == scale:
                    draw.line((current_line_list[0], self.dimensions[1]/2, current_line_list[len(current_line_list) - 1], self.dimensions[1]/2), fill="blue", width=3)
                    
                    barcode_lines.append(((round(len(current_line_list)/scale)), 255))
                    current_line_list = []
                    line_switch = True
       
        if not self.test:
            self.plain_barcode_img.show()
        return self.sort_barcode_list(barcode_lines)







    ###
    ### Gets starting lines
    ###




    def get_start(self):
        
        line_index = 0
        pixel_list = []
        black_line = []
        white_line = []

        if self.dimensions[0] > 4000:
            accuarcy_error = 15
        elif self.dimensions[0] > 2000:
            accuarcy_error = 10
        elif self.dimensions[0] > 1500:
            accuarcy_error = 7
        elif self.dimensions[0] > 1000:
            accuarcy_error = 4
        elif self.dimensions[0] > 700:
            accuarcy_error = 3
        else:
            accuarcy_error = 2


        for x in range(self.dimensions[0]):
            
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if self.pixels[x, self.dimensions[1]/2 + 1 ] == 0 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 0:
                    black_line.append(x)
                    white_line = []
                elif self.pixels[x, self.dimensions[1]/2 + 1 ] == 255 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 255:
                    white_line.append(x)
                    black_line = []
                else:
                    black_line.append(x)
                    white_line = []
            else:
                if self.pixels[x, self.dimensions[1]/2 + 1 ] == 255 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 255:
                    white_line.append(x)
                    black_line = []
                elif self.pixels[x, self.dimensions[1]/2 + 1 ] == 0 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 0:
                    black_line.append(x)
                    white_line = []
                else:
                    white_line.append(x)
                    black_line = []


            if self.pixels[x, self.dimensions[1]/2 ] == 0 and len(black_line) >= accuarcy_error:
                
                if line_index == 0 or line_index == 2:
                    line_index += 1
                    for line in black_line:
                        pixel_list.append((line, 0))
                else:
                    pixel_list.append((x, 0))
                
            elif self.pixels[x, self.dimensions[1]/2] == 255 and line_index != 0 and len(white_line) >= accuarcy_error:
                
                if line_index == 1:
                    line_index +=1
                    for line in white_line:
                        pixel_list.append((line, 255))
                elif line_index == 3:
                    break
                else:
                    pixel_list.append((x, 255))
        return pixel_list


    def get_end(self):
        self.barcode_img.transpose(Image.FLIP_LEFT_RIGHT)
        line_index = 0
        pixel_list = []
        black_line = []
        white_line = []

        if self.dimensions[0] > 4000:
            accuarcy_error = 15
        elif self.dimensions[0] > 2000:
            accuarcy_error = 10
        elif self.dimensions[0] > 1500:
            accuarcy_error = 7
        elif self.dimensions[0] > 1000:
            accuarcy_error = 4
        elif self.dimensions[0] > 700:
            accuarcy_error = 3
        else:
            accuarcy_error = 2

        for x in range(self.dimensions[0]):
           
            if self.pixels[x, self.dimensions[1]/2 ] == 0:
                if self.pixels[x, self.dimensions[1]/2 + 1 ] == 0 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 0:
                    black_line.append(x)
                    white_line = []
                elif self.pixels[x, self.dimensions[1]/2 + 1 ] == 255 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 255:
                    white_line.append(x)
                    black_line = []
                else:
                    black_line.append(x)
                    white_line = []
            else:
                if self.pixels[x, self.dimensions[1]/2 + 1 ] == 255 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 255:
                    white_line.append(x)
                    black_line = []
                elif self.pixels[x, self.dimensions[1]/2 + 1 ] == 0 and self.pixels[x, self.dimensions[1]/2 - 1 ] == 0:
                    black_line.append(x)
                    white_line = []
                else:
                    white_line.append(x)
                    black_line = []


            if self.pixels[x, self.dimensions[1]/2 ] == 0 and len(black_line) >= accuarcy_error:
                
                if line_index == 0 or line_index == 2:
                    line_index += 1
                    for line in black_line:
                        pixel_list.append((line, 0))
                else:
                    pixel_list.append((x, 0))
                
            elif self.pixels[x, self.dimensions[1]/2] == 255 and line_index != 0 and len(white_line) >= accuarcy_error:
                
                if line_index == 1:
                    line_index +=1
                    for line in white_line:
                        pixel_list.append((line, 255))
                elif line_index == 3:
                    break
                else:
                    pixel_list.append((x, 255))
        self.barcode_img.transpose(Image.FLIP_LEFT_RIGHT)
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
        code = self.translate_lines(left, right)
        if self.check_sum(code):
            return code
        return False

    @staticmethod
    def check_sum(code):
        sum_odd = int(code[0]) + int(code[2]) + int(code[4]) + int(code[6]) + int(code[8]) + int(code[10])

        sum_even = int(code[1]) + int(code[3]) + int(code[5]) + int(code[7]) + int(code[9])

        result1 = sum_odd * 3

        total = result1 + sum_even
        modulo = total % 10

        if modulo != 0:
            check_digit = 10 - modulo
        else:
            check_digit = 0
        
        check_digit = (10 - (modulo)) % 10

        if str(check_digit) == code[11]:
            return True
        
        return False

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

        
        
                
        return code
        
   
