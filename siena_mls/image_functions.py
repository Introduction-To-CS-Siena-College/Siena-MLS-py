

class MLS_GUI_ImageFunctions:
    
    def show(image):
        try:
            from PIL import ImageTk
            from tkinter import Tk, Canvas, NW
            
            root = Tk()
            canvas = Canvas(root, width=image.PILimg.width, height=image.PILimg.height)
            canvas.pack()
            img = ImageTk.PhotoImage(image.PILimg)
            canvas.create_image(0, 0, anchor=NW, image=img)
            root.mainloop()
            return
        except ModuleNotFoundError:
            pass  # Fall back to matplotlib
        
        # Fallback to matplotlib if tkinter is not available
        try:
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots()
            ax.imshow(image.PILimg)
            
            # # Set the title to the filename
            # if hasattr(image, 'filename') and image.filename:
            #     ax.set_title(image.filename)
            
            # Move x-axis to the top
            ax.xaxis.set_ticks_position('top')
            ax.xaxis.set_label_position('top')
            
            plt.show()
        except ModuleNotFoundError:
            print("Neither tkinter nor matplotlib is available on this system.")