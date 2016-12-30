import prepare
import tkinter
import scraper


class MainWin():
    def __init__(self, master):
        self.master = master
        # set title
        master.title("Naive bayes blog classifier")
        # validate function
        vcmd = master.register(self.validate)
        self.userid = ""
        # entrty for userid
        self.entry = tkinter.Entry(
            master, text="enter a medium userID", validatecommand=(vcmd, "%P"))
        # button to start
        self.start_button = tkinter.Button(
            master, text="start", command=analyze(self.userid))

    def validate(self, new_text):
        if not new_text:
            self.userid = ""
            return False
        try:
            self.userid = new_text
            return True
        except ValueError:
            return False

def analyze(userid):
    return userid


gui_root = tkinter.Tk()
classifier_gui = MainWin(gui_root)
gui_root.mainloop()
