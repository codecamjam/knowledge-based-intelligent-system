import Tkinter as tk
import tkFont, Tkconstants, tkFileDialog
import Logic as logic
LARGE_FONT = ("Verdana", 16)
MEDIUM_FONT = ("Verdana", 14)
SHMEDIUM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)
class Project3(tk.Tk):
    """This class will aide in organizing the 3 pages within the GUI application.
       The 3 pages are as follows: Start page, manual entry page, and file upload page
       All attributes are there for ease of resetting when user changes page.
       A set of frame objects aides in providing the user the ability to change pages.
    """
    def __init__(self, *args, **kwargs):
        """Provides the user 3 different pages to navigate to.
        The attributes have been included for ease of initializing
        when switching between pages"""
        self.attFile, self.conFile, self.preFile = "", "", ""
        self.att, self.con, self.pre = False, False, False
        self.verify = []
        self.attributesList = []
        self.constraintsList = []
        self.preferencesList = []
        self.results = []
        tk.Tk.__init__(self, *args, **kwargs)
        # self.geometry("800x800+1000+30")
        self.geometry("800x960+500+0")
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
        """This method aides in switching between the 3 different pages contained
        in the gui.  attributes are reset each time a user changes the page"""
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
        self.results = []

        frame = self.frames[cont]
        frame.tkraise()


#############################################################################################

class StartPage(tk.Frame):
    """
    The start page aides in providing the user with 2 options: enter input manually or upload files.
    The user also can quit at any time by pressing the quit button
    """
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
    """
    This page gives the users 3 entries: one for attributes, one for constraints, one for preferences.
    The user can enter each entry, but only one at a time.  Each entry is stored in the appropriate list.
    If the user makes a mistake with their input, there are reset buttons that clear the list and the
    listbox containing the stored entries.  User will see informative information displayed to verify
    that their input is sound.  The program assumes that the user typed constraints/preferences in CNF
    form.
    """
    def __init__(self, parent, controller):
        """Inherets the parent and controller objects from the start page and project 3 classes
           All attributes inhereted from the controller aide in clearing all data when the user changes
           from page to page.
        """
        # these will be used to display the count of each
        controller.attCount, controller.conCount, controller.prefCount = 0, 0, 0
        controller.att, controller.con, controller.pre = False, False, False
        controller.attributesList, controller.constraintsList, controller.preferencesList = [], [], []
        controller.results = []
        medium_font = ('Verdana', 11)
        small_font = ('Verdana', 10)
        tk.Frame.__init__(self, parent)
        top_label = tk.Label(self, text="Enter your attributes, constraints, and preferences below (one at a time)", font=LARGE_FONT)
        top_label.pack(pady=5, padx=0)

        def initializeLists():
            """clears all lists"""
            controller.attributesList = []
            controller.constraintsList = []
            controller.preferencesList = []
            controller.results = []

        def runProgram():
            """
            This method calls the verifyInput() method from Logic.py
            Essentially, this method performs the backend logic to perform all
            necessary calculations as well as verifying that input was sound.
            """
            programReady, results = logic.verifyInput(controller.attributesList,
                              controller.constraintsList, controller.preferencesList)
            initializeLists()
            if programReady:
                run_button.config(text="CLICK TO RUN THE PROGRAM!")
                if programReady:

                    run_button.config(text="RUN PROGRAM")
                    # index 0 is feas string
                    feasible = '1) ' + results[0] + '!'
                    feasibleLabel = tk.Label(self, text=feasible, font=MEDIUM_FONT)
                    feasibleLabel.place(x=10, y=400)

                    # index 1 is string of objects and their penalties

                    objTabLabel = tk.Label(self, text='2) LIST OF FEASIBLE OBJECTS', font=MEDIUM_FONT)
                    objTabLabel.place(x=10, y=430)
                    feasObj_scroll = tk.Scrollbar(self)
                    feasObj_listbox = tk.Listbox(self, width=94, height=8, yscrollcommand=feasObj_scroll.set)
                    feasObj_listbox.place(x=10, y=456)
                    for objects in results[1]:
                        feasObj_listbox.insert("end", objects)

                    # index 2 is comparison of random objects
                    random = '3) RANDOM OBJECTS:'
                    randomLabel = tk.Label(self, text=random, font=MEDIUM_FONT)
                    randomLabel.place(x=10, y=587)

                    random_res =  results[2]
                    randomLabel = tk.Label(self, text=random_res, font=SMALL_FONT)
                    randomLabel.place(x=25, y=630)

                    # index 3 has the optimal objects
                    optimalLabel = tk.Label(self, text='4) OPTIMAL OBJECTS:', font=MEDIUM_FONT)
                    optimalLabel.place(x=10, y=710)
                    optimal_scroll = tk.Scrollbar(self)
                    optimal_listbox = tk.Listbox(self, width=94, height=8, yscrollcommand=optimal_scroll.set)
                    optimal_listbox.place(x=10, y=740)
                    for opt in results[3]:
                        optimal_listbox.insert("end", opt)

                    t1Label = tk.Label(self, text='After you push reset, the output from', font=SMALL_FONT)
                    t1Label.place(x=10, y=880)
                    t2Label = tk.Label(self, text='previous session will display until you', font=SMALL_FONT)
                    t2Label.place(x=10, y=900)
                    t3Label = tk.Label(self, text='run the program with new input', font=SMALL_FONT)
                    t3Label.place(x=10, y=920)
                else:
                    feasible = results[0]
                    feasibleLabel = tk.Label(self, text=feasible, font=MEDIUM_FONT)
                    feasibleLabel.place(x=10, y=400)

            else:
                run_button.config(text="RESET ALL FIELDS & PUSH RESET!\nCLICK HERE AFTER YOU RE-ENTER INPUT")

        def insertAttribute(obj):
            """Takes user entry and stores in list and listbox"""
            controller.attCount += 1
            controller.attributesList.append(obj.get().upper())
            att_listbox.insert("end", str(controller.attCount) + ". " + obj.get())
            obj.__del__()
            entry_1.delete(0, 'end')

        def insertConstraint(obj):
            """Takes user entry and stores in list and listbox"""
            controller.conCount += 1
            controller.constraintsList.append(obj.get().upper())
            con_listbox.insert("end", str(controller.conCount) + ". " + obj.get())
            obj.__del__()
            entry_2.delete(0, 'end')

        def insertPreference(obj):
            """Takes user entry and stores in list and listbox"""
            controller.prefCount += 1
            controller.preferencesList.append(obj.get().upper())
            pre_listbox.insert("end", str(controller.prefCount) + ". " + obj.get())
            obj.__del__()
            entry_3.delete(0, 'end')

        def resetAttributes():
            """Clears listbox containing attributes"""
            while len(controller.attributesList) > 0:
                controller.attributesList.pop()
            controller.attCount = 0
            att_listbox.delete(0, "end")

        def resetConstraints():
            """Clears listbox containing constraints"""
            while len(controller.constraintsList) > 0:
                controller.constraintsList.pop()
            controller.conCount = 0
            con_listbox.delete(0, "end")

        def resetPreferences():
            """Clears listbox containing preferences"""
            while len(controller.preferencesList) > 0:
                controller.preferencesList.pop()
            controller.prefCount = 0
            pre_listbox.delete(0, "end")

        # the following lines correspond to button and label placement
        field_label = tk.Label(self, text='      Attributes (attribute:  X, Y)       ' + \
                               ' Constraints (NOT X OR NOT Y)       ' + \
                               'Preferences (X AND Y, number)', font=medium_font)
        field_label.place(x=8, y=44)

        instruct_label = tk.Label(self, text='    Attributes List (Reset if typo)       ' + \
                                          ' Constraints List (Reset if typo)       ' + \
                                          'Preferences List (Reset if typo)', font=medium_font)
        instruct_label.place(x=9, y=138)
        userAttr = tk.StringVar()
        entry_1 = tk.Entry(self, width=32, textvariable=userAttr, font=small_font)
        entry_1.place(x=2, y=70)
        button_1 = tk.Button(self, text="Click to enter your attribute",\
                             command=lambda: insertAttribute(userAttr))
        button_1.place(x=34, y=100)
        att_scroll = tk.Scrollbar(self)
        att_listbox = tk.Listbox(self, width=32, height=5, yscrollcommand=att_scroll.set)
        att_listbox.place(x=5, y=158)
        reset_att_button = tk.Button(self, text="Reset Attributes", command=resetAttributes)
        reset_att_button.place(x=65, y=250)
        userConst = tk.StringVar()
        entry_2 = tk.Entry(self, width=32, textvariable=userConst, font=small_font)
        entry_2.place(x=267, y=70)
        button_2 = tk.Button(self, text="Click to enter your constraint", \
                             command=lambda: insertConstraint(userConst))
        button_2.place(x=300, y=100)
        con_scroll = tk.Scrollbar(self)
        con_listbox = tk.Listbox(self, width=32, height=5, yscrollcommand=con_scroll.set)
        con_listbox.place(x=271, y=158)
        reset_con_button = tk.Button(self, text="Reset Constraints", command=resetConstraints)
        reset_con_button.place(x=334, y=250)
        userPref = tk.StringVar()
        entry_3 = tk.Entry(self, width=32, textvariable=userPref, font=small_font)
        entry_3.place(x=535, y=70)
        button_3 = tk.Button(self, text="Click to enter your preference", \
                             command=lambda: insertPreference(userPref))
        button_3.place(x=572, y=100)
        pre_scroll = tk.Scrollbar(self)
        pre_listbox = tk.Listbox(self, width=32, height=5, yscrollcommand=pre_scroll.set)
        pre_listbox.place(x=536, y=158)
        reset_pre_button = tk.Button(self, text="Reset Preferences", command=resetPreferences)
        reset_pre_button.place(x=606, y=250)
        attVar_label = tk.Label(self, text="      BEFORE YOU RUN THE PROGRAM, MAKE SURE YOUR LISTS DO NOT CONTAIN ANY ERRORS!", font=medium_font)
        attVar_label.place(x=24, y= 290)
        attVar_label = tk.Label(self, text="       (To double check your lists, you can scroll through with arrow keys or your mousewheel)",font=medium_font)
        attVar_label.place(x=24, y=310)
        run_button = tk.Button(self, height=2, width=30, text="CLICK TO RUN THE PROGRAM!",
                                font=medium_font, command=runProgram)
        run_button.place(x=226, y=340)
        home_button = tk.Button(self, text="Reset", height=2, width=8, \
                    command=lambda: controller.show_frame(StartPage)).place(x=300, y=900)
        quit_button = tk.Button(self, text="Quit", height=2, width=8, command=quit).place(x=400, y=900)


##################################################################################################

class UploadFilesPage(tk.Frame):
    """
    This class provides the logic and GUI components necessary for the user to upload
    text files that will be parsed to perform the penalty logic. User is informed if their
    input is correctly entered.  Displays the results returned from the Logic.verifyInput()
    method.
    """

    def __init__(self, parent, controller):
        """
        This method inherets the parent and controller attributes in order to provide
        ease of use when the user changes the page (in order to clear all data in the lists,
        in the event that the user switches back to the front page).
        Contains the buttons, logic necessary to upload files.
        """
        tk.Frame.__init__(self, parent)
        top_label = tk.Label(self, text="Upload 3 files. Once your files are selected, you can run the program!",
                             font=LARGE_FONT)
        top_label.pack(pady=10, padx=10)
        controller.attFile, controller.conFile, controller.preFile = "", "", ""
        controller.att, controller.con, controller.pre = False, False, False
        controller.results = []
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

        home_button = tk.Button(self, text="Reset", height=2, width=8, \
                                command=lambda: controller.show_frame(StartPage)).place(x=300, y= 900)
        quit_button = tk.Button(self, text="Quit", height=2, width=8, command=quit).place(x=400, y= 900)




        def initializeLists():
            """clears all strings contained in the lists"""
            controller.attributesList = []
            controller.constraintsList = []
            controller.preferencesList = []
            controller.results = []

        def runProgram(controller):
            """
            Prepares all data parsed from the files.
            Verifies that all files were uploaded. If user
            uploads 3 files, logic.verifyInput() is called
            to: a)verify that the input is error-free and
            b) perform the penalty logic and capture results
            to be displayed. Displays error message if problem detected.
            """


            filesReady = False
            if count3Files(controller):
                filesReady, fileList = tryOpeningFiles(controller)
                if filesReady:
                    prepareList(fileList[0], controller.attributesList)
                    prepareList(fileList[1], controller.constraintsList)
                    prepareList(fileList[2], controller.preferencesList)

                    programReady, results = logic.verifyInput(controller.attributesList, \
                            controller.constraintsList, controller.preferencesList)
                    initializeLists()
                    if programReady:
                        # index 0 is feas string
                        feasible = '1) ' + results[0] + '!'
                        feasibleLabel = tk.Label(self, text=feasible, font=MEDIUM_FONT)
                        feasibleLabel.place(x=10, y=200)

                        # index 1 is string of objects and their penalties

                        objTabLabel = tk.Label(self, text='2) LIST OF FEASIBLE OBJECTS', font=MEDIUM_FONT)
                        objTabLabel.place(x=10, y=240)
                        feasObj_scroll = tk.Scrollbar(self)
                        feasObj_listbox = tk.Listbox(self, width=94, height=10, yscrollcommand=feasObj_scroll.set)
                        feasObj_listbox.place(x=10, y=266)
                        for objects in results[1]:
                            feasObj_listbox.insert("end", objects)



                        # index 2 is comparison of random objects
                        random = '3) RANDOM OBJECTS:'
                        randomLabel = tk.Label(self, text=random, font=MEDIUM_FONT)
                        randomLabel.place(x=10, y=440)

                        random_res = results[2]
                        randomLabel = tk.Label(self, text=random_res, font=SMALL_FONT)
                        randomLabel.place(x=25, y=470)




                        # index 3 has the optimal objects
                        optimalLabel = tk.Label(self, text='4) OPTIMAL OBJECTS:', font=MEDIUM_FONT)
                        optimalLabel.place(x=10, y=550)
                        optimal_scroll = tk.Scrollbar(self)
                        optimal_listbox = tk.Listbox(self, width=94, height=10, yscrollcommand=optimal_scroll.set)
                        optimal_listbox.place(x=10, y=580)
                        for opt in results[3]:
                            optimal_listbox.insert("end", opt)

                        t1Label = tk.Label(self, text='After you push reset, the output from', font=MEDIUM_FONT)
                        t1Label.place(x=240, y=810)
                        t2Label = tk.Label(self, text='previous session will display until you', font=MEDIUM_FONT)
                        t2Label.place(x=240, y=840)
                        t3Label = tk.Label(self, text='run the program with new input', font=MEDIUM_FONT)
                        t3Label.place(x=254, y=870)

                    else:
                        feasible = results[0]
                        feasibleLabel = tk.Label(self, text=feasible, font=MEDIUM_FONT)
                        feasibleLabel.place(x=10, y=200)

                        t1Label = tk.Label(self, text='After you push reset, the output from', font=MEDIUM_FONT)
                        t1Label.place(x=240, y=810)
                        t2Label = tk.Label(self, text='previous session will display until you', font=MEDIUM_FONT)
                        t2Label.place(x=240, y=840)
                        t3Label = tk.Label(self, text='run the program with new input', font=MEDIUM_FONT)
                        t3Label.place(x=254, y=870)

                else:
                    mid_label.config(text="Push Reset and try again (must be .txt")
            else:
                mid_label.config(text="Push Reset & try again (must be .txt)")



        def count3Files(controller):
            """Verifies that all 3 files were uploaded"""
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
            """error message"""
            mid_label.config(text="Cannot open " + fileName + " try again")

        def tryOpeningFiles(controller):
            """Verifies that all files can be opened
            returns whether all 3 files were uploaded.
            If true, it returns a list of files
            If not, an empty list is returned."""
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
            """removes and tabs in case file contains them"""
            for line in file:
                x = line.upper().strip()
                x = x.replace("\t", " ")
                curList.append(x)


        def getAtt(controller):
            """For uploading the attributes file. Also checks if all 3 files
            have been uploaded and displays that program is ready to run"""
            # NEED TO CHANGE THE DIRECTORY BEFORE I TURN IT IN!!!
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/home/jam/Project3/test_files", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.attFile = controller.filename
            if controller.attFile != "":
                controller.att = True
                controller.verify.append(controller.att)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")

        def getCon(controller):
            """For uploading the constraints file. Also checks if all 3 files
            have been uploaded and displays that program is ready to run"""
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/home/jam/Project3/test_files", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.conFile = controller.filename
            if controller.conFile != "":
                controller.con = True
                controller.verify.append(controller.con)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")

        def getPref(controller):
            """For uploading the preferences file. Also checks if all 3 files
            have been uploaded and displays that program is ready to run"""
            controller.filename = tkFileDialog.askopenfilename( \
                initialdir="/home/jam/Project3/test_files", title="Select file", \
                filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            controller.preFile = controller.filename
            if controller.preFile != "":
                controller.pre = True
                controller.verify.append(controller.pre)
            if count3Files(controller):
                mid_label.config(text="Program is ready to run!")


#############################################################################################
# this is where the program begins!
app = Project3()
app.mainloop()
