from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from logic import BarcodeReader

class GUI:

    @staticmethod
    def resize_image_preserving_aspect_ratio(image, box_width, box_height):
        image_width, image_height = image.size

        aspect_ratio = image_width / image_height

        if image_width > box_width or image_height > box_height:
            if aspect_ratio > 1:
                # Scale based on width
                new_width = box_width
                new_height = int(box_width / aspect_ratio)
            else:
                # Scale based on height
                new_height = box_height
                new_width = int(box_height * aspect_ratio)

            image = image.resize((new_width, new_height), Image.LANCZOS)
        return image

    def load_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png")])

        if self.file_path:
            label_width = self.img_widget.winfo_width()
            label_height = self.img_widget.winfo_height()
            image = Image.open(self.file_path).convert("RGB")
            self.image = self.resize_image_preserving_aspect_ratio(image, label_width, label_height)
            
            
            self.plain_photo = ImageTk.PhotoImage(self.image)

            self.img_widget.config(image=self.plain_photo)
            self.img_widget.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)

    def run_barcode_scan(self):
        if self.img_widget.cget("image") != None and self.image != None:
            barcode_reader = BarcodeReader(self.file_path)
            all_codes_and_images = barcode_reader.run_barcode()

            self.code_label.config(state=NORMAL)  
            self.code_label.delete('1.0', 'end')  
            self.code_label.insert('1.0', "Code:\n")  
            i = 0
            for code in all_codes_and_images:
                self.add_code_with_image(code[0], code[1], i)
                i += 1

            self.code_label.config(state=DISABLED)
            # label_width = self.img_widget.winfo_width()
            # label_height = self.img_widget.winfo_height()
            # image = Image.open(self.file_path).convert("RGB")
            # self.image = self.resize_image_preserving_aspect_ratio(barcode_reader.plain_barcode_img, label_width, label_height)

            # self.photo = ImageTk.PhotoImage(self.image)
            # self.img_widget.config(image=self.photo)
            # self.img_widget.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)

    def add_code_with_image(self, display_text, image_obj, i):
        start_index = self.code_label.index("end-1c") 
        self.code_label.insert("end", display_text + "\n")
        end_index = self.code_label.index("end-1c") 

        tag_name = f"image_link_{display_text}_{i}"

        self.code_label.tag_add(tag_name, start_index, end_index)
        self.code_label.tag_config(tag_name, foreground="blue", underline=True)
        self.code_label.tag_bind(tag_name, "<Button-1>", lambda event, img=image_obj: img.show())

        

    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        self.image = None

        mainFrame = Frame(self.root)
        mainFrame.place(relx=0,rely=0, relwidth=1, relheight=1)

        heading = Label(mainFrame, text="UPC-A Barcode Reader", bg="gray88", font=("Arial", 20))
        self.img_widget = Label(mainFrame, bg="gray88")
        self.code_label = Text(mainFrame, bg="gray88", font=("Arial", 12))
        self.code_label.insert('1.0', "Code: \n")
        select_image_btn = Button(mainFrame, text="Select Image", command=lambda: self.load_image())
        get_code_btn = Button(mainFrame, text="Get Code", command=lambda: self.run_barcode_scan())

        heading.place(relx=0.05, rely=0.05)
        self.img_widget.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.6)
        select_image_btn.place(relx=0.3, rely=0.9, relwidth=0.15, relheight=0.08)
        get_code_btn.place(relx=0.5, rely=0.9, relwidth=0.15, relheight=0.08)
        self.code_label.place(relx=0.05, rely=0.77, relwidth=0.2, relheight=0.15)
        
        self.root.mainloop()
    
