import Tkinter as tk
import tkFont, Tkconstants, tkFileDialog
import Logic as logic
LARGE_FONT = ("Verdana", 16)
MEDIUM_FONT = ("Verdana", 14)


class Project3(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.attFile, self.conFile, self.preFile = "", "", ""
        self.att, self.con, self.pre = False, False, False
        self.verify = []
        self.attributesList = []
        self.constraintsList = []
        self.preferencesList = []
        tk.Tk.__init__(self, *args, **kwargs)
        # self.geometry("800x800+1000+30")
        self.geometry("800x960+1000+30")
        tk.Tk.wm_title(self, "Intelligence-Based Systems")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, UploadFilesPage, EnterManuallyPage):
            # parent, controller
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        # THESE FLAGS ARE FOR BOTH PAGES
        self.att, self.con, self.pre = False, False, False
        # THESE FIELDS ARE FOR FILES
        self.attFile, self.conFile, self.preFile = "", "", ""
        self.verify = []
        # AND THESE FIELDS WILL AIDE WITH MANUALLY ENTERING DATA
        self.attCount = 0
        self.conCount = 0
        self.prefCount = 0
        self.attributesList = []
        self.constraintsList = []
        self.preferencesList = []

        frame = self.frames[cont]
        frame.tkraise()


#############################################################################################


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        top = tk.Frame()
        bottom = tk.Frame()
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Would you like to upload files or enter your input manually?", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, height=2, width=11, text="Upload Files", font=LARGE_FONT,
                            command=lambda: controller.show_frame(UploadFilesPage))
        button2 = tk.Button(self, height=2, width=11, text="Enter Manually", font=LARGE_FONT,
                            command=lambda: controller.show_frame(EnterManuallyPage))
        button1.pack()
        button2.pack()

        quit_button = tk.Button(self, text="Quit", height=2, width=8, command=quit)
        quit_button.pack(side="bottom")


#############################################################################################

class EnterManuallyPage(tk.Frame):
    def __init__(self, parent, controller):
        # these will be used to display the count of each
        controller.attCount, controller.conCount, controller.prefCount = 0, 0, 0
        controller.att, controller.con, controller.pre = False, False, False
        controller.attributesList, controller.constraintsList, controller.preferencesList = [], [], []
        medium_font = ('Verdana', 11)
        small_font = ('Verdana', 10)
        tk.Frame.__init__(self, parent)
        top_label = tk.Label(self, text="Enter your attributes, constraints, and preferences below (one at a time)", font=LARGE_FONT)
        top_label.pack(pady=5, padx=0)

        def initializeLists():
            controller.attributesList = []
            controller.constraintsList = []
            controller.preferencesList = []

        def runProgram():
            programReady = logic.verifyInput(controller.attributesList,
                              controller.constraintsList, controller.preferencesList)
            initializeLists()
            if programReady:
                run_button.config(text="CLICK TO RUN THE PROGRAM!")
                print "ok"
            else:
                run_button.config(text="ERROR FOUND! RE-ENTER INPUT")

        def insertAttribute(obj):
            controller.attCount += 1
            controller.attributesList.append(obj.get().upper())
            att_listbox.insert("end", str(controller.attCount) + ". " + obj.get())
            obj.__del__()
            entry_1.delete(0, 'end')

        def insertConstraint(obj):
            controller.conCount += 1
            controller.constraintsList.append(obj.get().upper())
            con_listbox.insert("end", str(controller.conCount) + ". " + obj.get())
            obj.__del__()
            entry_2.delete(0, 'end')

        def insertPreference(obj):
            controller.prefCount += 1
            controller.preferencesList.append(obj.get().upper())
            pre_listbox.insert("end", str(controller.prefCount) + ". " + obj.get())
            obj.__del__()
            entry_3.delete(0, 'end')

        def resetAttributes():
            while len(controller.attributesList) > 0:
                controller.attributesList.pop()
            controller.attCount = 0
            att_listbox.delete(0, "end")

        def resetConstraints():
            while len(controller.constraintsList) > 0:
                controller.constraintsList.pop()
            controller.conCount = 0
            con_listbox.delete(0, "end")

        def resetPreferences():
            while len(controller.preferencesList) > 0:
                controller.preferencesList.pop()
            controller.prefCount = 0
            pre_listbox.delete(0, "end")



        field_label = tk.Label(self, text='      Attributes (attribute:  X, Y)         ' + \
                               ' Constraints (NOT X OR NOT Y)       ' + \
                               'Preferences (X AND Y, number)', font=medium_font)
        field_label.place(x=12, y=44)

        instruct_label = tk.Label(self, text='    Attributes List (Reset if typo)       ' + \
                                          ' Constraints List (Reset if typo)       ' + \
                                          'Preferences List (Reset if typo)', font=medium_font)
        instruct_label.place(x=12, y=138)


        # attVar_label.pack(pady=5, padx=0)
        userAttr = tk.StringVar()
        entry_1 = tk.Entry(self, width=30, textvariable=userAttr, font=small_font)
        entry_1.place(x=12, y=70)

        button_1 = tk.Button(self, text="Click to enter your attribute",\
                             command=lambda: insertAttribute(userAttr))
        button_1.place(x=34, y=100)

        att_scroll = tk.Scrollbar(self)
        att_listbox = tk.Listbox(self, width=30, height=5, yscrollcommand=att_scroll.set)
        att_listbox.place(x=12, y=158)

        reset_att_button = tk.Button(self, text="Reset Attributes", command=resetAttributes)
        reset_att_button.place(x=65, y=250)

        userConst = tk.StringVar()
        entry_2 = tk.Entry(self, width=30, textvariable=userConst, font=small_font)
        entry_2.place(x=280, y=70)
        button_2 = tk.Button(self, text="Click to enter your constraint", \
                             command=lambda: insertConstraint(userConst))
        button_2.place(x=300, y=100)

        con_scroll = tk.Scrollbar(self)
        con_listbox = tk.Listbox(self, width=30, height=5, yscrollcommand=con_scroll.set)
        con_listbox.place(x=280, y=158)

        reset_con_button = tk.Button(self, text="Reset Constraints", command=resetConstraints)
        reset_con_button.place(x=334, y=250)


        userPref = tk.StringVar()
        entry_3 = tk.Entry(self, width=30, textvariable=userPref, font=small_font)
        entry_3.place(x=550, y=70)
        button_3 = tk.Button(self, text="Click to enter your preference", \
                             command=lambda: insertPreference(userPref))
        button_3.place(x=572, y=100)

        pre_scroll = tk.Scrollbar(self)
        pre_listbox = tk.Listbox(self, width=30, height=5, yscrollcommand=pre_scroll.set)
        pre_listbox.place(x=550, y=158)

        reset_pre_button = tk.Button(self, text="Reset Preferences", command=resetPreferences)
        reset_pre_button.place(x=606, y=250)

        attVar_label = tk.Label(self, text="      BEFORE YOU RUN THE PROGRAM, MAKE SURE YOUR LISTS DO NOT CONTAIN ANY ERRORS!", font=medium_font)
        attVar_label.place(x=24, y= 290)

        attVar_label = tk.Label(self, text="       (To double check your lists, you can scroll through with arrow keys or your mousewheel)",font=medium_font)
        attVar_label.place(x=24, y=310)

        run_button = tk.Button(self, height=2, width=23, text="CLICK TO RUN THE PROGRAM!",
                                font=medium_font, command=runProgram)
        run_button.place(x=276, y=340)

        home_button = tk.Button(self, text="Front Page", height=2, width=8, \
                    command=lambda: controller.show_frame(StartPage)).place(x=300, y=900)
        # home_button.pack(side="bottom")
        quit_button = tk.Button(self, text="Quit", height=2, width=8, command=quit).place(x=400, y=900)
        # quit_button.pack(side="bottom")


# #################################################################################################3
class UploadFilesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        top_label = tk.Label(self, text="Upload 3 files. Once your files are selected, you can run the program!",
                             font=LARGE_FONT)
        top_label.pack(pady=10, padx=10)
        controller.attFile, controller.conFile, controller.preFile = "", "", ""
        controller.att, controller.con, controller.pre = False, False, False
        controller.verify = []

        button_1 = tk.Button(self, height=2, width=15, text="Select Attributes File", \
                             command=lambda: getAtt(controller)).place(x=140, y=50)

        button_2 = tk.Button(self, height=2, width=15, text="Select Constraints File", \
                             command=lambda: getCon(controller)).place(x=320, y=50)

        button_3 = tk.Button(self, height=2, width=15, text="Select Preferences File", \
                             command=lambda: getPref(controller)).place(x=500, y=50)


        mid_label = tk.Label(self, text="Click here when ready", font=MEDIUM_FONT)
        mid_label.place(x=286, y=106)
        button_4 = tk.Button(self, height=2, width=15, text="Run The Program!", \
                             command=lambda: runProgram(controller)).place(x=320, y=144)


        home_button = tk.Button(self, text="Front Page", height=2, width=8, \
                                command=lambda: controller.show_frame(StartPage)).place(x=300, y= 900)

        quit_button = tk.Button(self, text="Quit", height=2, width=8, command=quit).place(x=400, y= 900)


        def initializeLists():
            controller.attributesList = []
            controller.constraintsList = []
            controller.preferencesList = []

        def runProgram(controller):
            filesReady = False
            if count3Files(controller):
                filesReady, fileList = tryOpeningFiles(controller)
                if filesReady:
                    prepareList(fileList[0], controller.attributesList)
                    prepareList(fileList[1], controller.constraintsList)
                    prepareList(fileList[2], controller.preferencesList)
                    # print controller.attributesList
                    # print controller.constraintsList
                    # print controller.preferencesList
                    programReady = logic.verifyInput(controller.attributesList, \
                            controller.constraintsList, controller.preferencesList)
                    initializeLists()
                    if programReady:
                        print "ok"

                else:
                    mid_label.config(text="There was a problem with one of your files. Re-enter")
            else:
                mid_label.config(text="Files missing. Select 3")



        def count3Files(controller):
            start = False
            count = 0
            if len(controller.verify) == 3:
                for i in controller.verify:
                    if i == True:
                        count += 1
            if count == 3:
                start = True
            return start

        def displayError(fileName):
            mid_label.config(text="Cannot open " + fileName + " try again")

        def tryOpeningFiles(controller):
            fileList = []
            good = [True, True, True]
            try:
                file1 = open(controller.attFile, 'r')
                good[0] = True
                fileList.append(file1)
            except IOError:
                # print 'Cannot open', controller.attFile
                good[0] = False
                displayError(controller.attFile)
            try:
                file2 = open(controller.conFile, 'r')
                good[1] = True
                fileList.append(file2)
            except IOError:
                # print 'Cannot open', controller.conFile
                good[1] = False
                displayError(controller.conFile)

            try:
                file3 = open(controller.preFile, 'r')
                good[2] = True
                fileList.append((file3))
            except IOError:
                # print 'Cannot open', controller.preFile
                good[2] = False
                displayError(controller.preFile)

            if good[0] and good[1] and good[2]:
                return True, fileList
            else:
                return False, fileList


        def prepareList(file, curList):
            for line in file:
                x = line.upper().strip()
                x = x.replace("\t", " ")
                curList.append(x)


        def getAtt(controller):
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.attFile = controller.filename
            if controller.attFile != "":
                controller.att = True
                controller.verify.append(controller.att)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")

        def getCon(controller):
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.conFile = controller.filename
            if controller.conFile != "":
                controller.con = True
                controller.verify.append(controller.con)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")

        def getPref(controller):
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.preFile = controller.filename
            if controller.preFile != "":
                controller.pre = True
                controller.verify.append(controller.pre)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")


#############################################################################################

app = Project3()
app.mainloop()
