import prepare
import tkinter
import scraper

class MainWin():
    def __init__(self, master):
        self.master = master
        master.title("Naive bayes blog classifier")
        vcmd = master.register(self.validate)
        self.userid = ""
        self.entry = tkinter.Entry(
            master, text="enter a medium userID", validatecommand=(vcmd, "%P"))
        self.start_button = tkinter.Button(
            master, text="start", command=self.analyze(self.userid))

    def validate(self, new_text):
        if not new_text:
            self.userid = ""
            return False
        try:
            self.userid = new_text
            return True
        except ValueError:
            return False

    def analyze(self, userid):
        pass

def getParam():
    pass


gui_root = tkinter.Tk()
classifier_gui = MainWin(gui_root)
gui_root.mainloop()
