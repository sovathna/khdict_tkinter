import tkinter as tk
from tkinter import ttk
from splash_frame import SplashFrame

if __name__ == '__main__':
    window = tk.Tk()
    window.title('Test')
    window.configure(bg='green')
    window.minsize(640,480)

    window.columnconfigure(0,weight=1)
    window.rowconfigure(0,weight=1)

    sp = SplashFrame(window)

    window.mainloop()