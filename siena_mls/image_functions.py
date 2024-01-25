

class MLS_GUI_ImageFunctions:
    
    def showImage(image):
        try:
            from PIL import ImageTk
            from tkinter import Tk,Canvas,NW
            root = Tk()
            canvas = Canvas(root, width = image.PILimg.width, height = image.PILimg.height)
            canvas.pack()
            img = ImageTk.PhotoImage(image.PILimg)
            canvas.create_image(0,0,anchor=NW, image=img)
            root.mainloop()
        except ModuleNotFoundError:
            print("Tkinter is not available on this system.")