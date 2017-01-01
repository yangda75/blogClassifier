import os
import tkinter

import prepare
import scraper

TAGS = ['teen_f', 'teen_m', 'adult_f', 'adult_m', 'mature_f', 'mature_m']
MINIMAL_PROB={'teen_f':1/26694629,
              'teen_m':1/26829390,
              'adult_f':1/40553782,
              'adult_m':1/39002136,
              'mature_f':1/16526313,
              'mature_m':1/15941756}

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
            master,
            text="start",  # command=self.gen_tag()
        )
        # labels
        instruction = tkinter.Label(
            master,
            text="enter a medium userid, then press start button")
        label1 = tkinter.Label(master, text="userid: ")
        # arrange the UI components
        instruction.grid(row=0, columnspan=3)
        self.entry.grid(row=1, column=1)
        self.start_button.grid(row=1, column=2)
        label1.grid(row=1, column=0)

    def validate(self, new_text):
        if not new_text:
            self.userid = ""
            return False
        try:
            self.userid = new_text
            return True
        except ValueError:
            return False

    def gen_tag(self):
        results = analyze(self.userid)
        print("10 guesses generated from the recent 10 posts of {0}".format(
            self.userid))
        # there may not be ten posts,
        for i in range(len(results)):
            print("post number: {0}, tag generated:{1}".format(i, results[i]))


def analyze(userid):
    # save the recent 10 posts into ./userid/
    scraper.get_rec10(userid)
    # load the saved vocabulary file
    tag_vocab = {}
    for tag in TAGS:
        d = {}
        f = open(tag + '.csv')
        for line in f.readlines():
            word, freq = line.split(',')
            d[word] = float(freq)
        tag_vocab[tag] = d
    # save 10 classifying results in one list, then return it
    results = []
    # process the posts saved, generate hot words list
    for root, dirs, files in os.walk(userid + '/'):
        for f in files:
            # get 30 most used words
            hot_words = prepare.prepare(f)
            # core: calculate likelyhood for every tag
            probability = {}
            for tag in TAGS:
                probability[tag] = 1.0
                for word in hot_words:
                    try:
                        probability[tag] *= tag_vocab[tag][word]
                    except KeyError:
                        probability[tag] *= MINIMAL_PROB[tag]
                        results.append(max(probability, keys=probability.get))
    return results


GUI_ROOT = tkinter.Tk()
CLASSIFIER_GUI = MainWin(GUI_ROOT)
GUI_ROOT.mainloop()
