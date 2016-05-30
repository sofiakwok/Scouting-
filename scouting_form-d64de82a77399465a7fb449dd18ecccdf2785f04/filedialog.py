try:
    from Tkinter import *
    from tkFileDialog import *
except ImportError:
    from tkinter import *
    from tkinter.filedialog import *

root = Tk()
root.withdraw()
f = askopenfilename()
root.quit()
print(f.strip())
