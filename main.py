from gui import *
from tkinter import Tk


def main():
    """
    Main function to initialize the Tkinter window and start the application.
    """
    window = Tk()
    window.title('E-PACERR Statistical Analysis')

    # Get the screen's width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the center position
    x = (screen_width - window.winfo_reqwidth()) / 2
    y = (screen_height - window.winfo_reqheight()) / 2

    # Set the window position at the center of the screen
    window.geometry(f"+{int(x)}+{int(y)}")

    # Set the window width and height (WxH)
    window.geometry('300x120')

    window.resizable(False, False)

    widgets = GUI(window)

    window.mainloop()


if __name__ == '__main__':
    main()
