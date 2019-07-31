import os
import commands

atts = []
conClauses = []
preferences = []
results_List = []

def initialize(a, c, p, r):
    """initializes all the lists"""
    while len(a) > 0:
        a.pop()
    while len(c) > 0:
        c.pop()
    while len(p) > 0:
        p.pop()
    while len(r) > 0:
        r.pop()

def verifyInput(attList, conList, preList):
    """
    This method validates that all 3 lists have valid input.
    The method moves step, by step, checking that all 3 lists have
    data.  Creates dictionaries of attributes and stores in an attribute list.
    Checks constraints to verify that the input is sound.  Also checks preferences.
    If all 3 lists are fine, it converts constraints and preferences into clasp format.
    A this point, if still valid, getFeasibleObjects is called to determine if the
    constraints have feasible objects.  If clasp determines that its satisfiable,
    the program performs penalty logic and finds the optimal objects.  The method
    returns the status of the verification(valid or invalid) and the results obtained
    from the calculations (feasibility, feasible objects, randomly chosen objects and
    their preference relation, and the optimal objects). Error message is displayed
    otherwise, and user is prompted to re-enter input
    """
    initialize(atts, conClauses, preferences, results_List)
    valid = False
    satisfiable = False
    number_of_boolVars = 0
    if len(attList) > 0 and len(conList) > 0 and len(preList) > 0:
        number_of_boolVars, valid = getAttributes(attList)
        if valid:
            valid = checkConstraints(conList)
            if valid:
                valid = checkPreferences(preList)
                if valid:
                    valid = convertConstraints(conList, '0', 'cons')
                    if valid:
                        valid = convertPreferences(preList)
                        if valid:
                            feasibleObjects = []
                            message = ''
                            satisfiable, feasibleObjects, num_feas_objs = getFeasibleObjects(number_of_boolVars, conClauses)
                            if satisfiable:
                                if num_feas_objs == 1:
                                    message = "THERE IS ONE FEASIBLE OBJECT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                else:
                                    message = "THERE ARE " + str(num_feas_objs) + " FEASIBLE OBJECTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                                p = preferences
                                #NEED A WAY TO STORE ALL FEASIBLE OBJECTS AND PUT THEM IN A TEXTBOX IN STRING FORMAT
                                objectTable = performPenaltyLogic(feasibleObjects, number_of_boolVars)
                                randomObjects = generateRandomObjects(objectTable)
                                optimal = findOptimal(objectTable)
                                prepareResults(message, objectTable, randomObjects, optimal)
                                return True, results_List
                            else:
                                message = "NOT SATISFIABLE! NO FEASIBLE OBJECTS (IGNORE ANYTHING UNDER THIS LINE)!!!"
                                results_List.append(message)
                                return False, results_List
                        else:
                            message = 'RE-ENTER YOUR PREFERENCES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                            results_List.append(message)
                            return False, results_List
                    else:
                        message = 'RE-ENTER YOUR CONSTRAINTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                        results_List.append(message)
                        return False, results_List
                else:
                    message = 'RE-ENTER YOUR PREFERENCES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    results_List.append(message)
                    return False, results_List
            else:
                message = 'RE-ENTER YOUR CONSTRAINTS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                results_List.append(message)
                return False, results_List
        else:
            message = 'RE-ENTER YOUR ATTRIBUTES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            results_List.append(message)
            return False, results_List
    else:
        message = 'INVALID INPUT. TRY AGAIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        results_List.append(message)
        return False, results_List


def prepareResults(feas_string, objTab, randomObjects, optimal):
    """
    This method prepares a list to be passed back to the GUI
    Objectt table, random objects, and optimal all need to be converted to string format
    :param feas_string: displays how many feasible objects
    :param objectTable: table of feasible objects. needs to be converted
    :param randomObjects: two randomly chosen objects to compare (only one if 1 feasible object)
    :param optimal: optimal object
    :return: list of results
    """
    results_List.append(feas_string)    #index 0 is feas string

    object_table_strs = []
    for i in range(0, len(objTab)):
        obj_str = convertObject(objTab[i][0])
        penalty = objTab[i][1]
        obj_String = obj_str + ' : ' + str(penalty)
        object_table_strs.append(obj_String)

    results_List.append(object_table_strs) #index 1 is string of objects and their penalties

    rand1 = randomObjects[0]
    rand_str1 = convertObject(rand1[0])
    penalty1 = rand1[1]
    rand_result =''
    if len(randomObjects) == 1:
        rand_result = rand_str1 + ' IS THE ONLY FEASIBLE OBJECT WITH VALUE: ' + str(penalty1)
    else:
        rand2 = randomObjects[1]
        rand_str2 = convertObject(rand2[0])
        penalty2 = rand2[1]

        if penalty1 < penalty2:
            rand_result = rand_str1 + ' : ' + str(penalty1) + '\nSTRICTLY PREFERRED OVER\n' + rand_str2 + ' : ' + str(penalty2)
        elif penalty1 == penalty2:
            rand_result = rand_str1 + ' : ' + str(penalty1) + '\nEQUIVALENT TO\n' + rand_str2 + ' : ' + str(penalty2)
        else:
            rand_result = rand_str2 + ' : ' + str(penalty2) + '\nSTRICTLY PREFERRED OVER\n' + rand_str1 + ' : ' + str(penalty1)
    results_List.append(rand_result) #index 2 is comparison of random objects

    optimal_strs = []

    i = 0
    for i in range(0, len(optimal)):
        obj_str = convertObject(optimal[i][0])
        penalty = optimal[i][1]
        obj_String = obj_str + ' : ' + str(penalty)
        optimal_strs.append(obj_String)



    results_List.append(optimal_strs)  #index 3 has the optimal objects


def generateRandomObjects(objTab):
    import random
    if len(objTab) > 1:
        r1 = random.choice(objTab)
        r2 = random.choice(objTab)
        if r1 == r2:
            r2 = random.choice(objTab)
        randObjs = [r1, r2]
        return randObjs
    else:
        return objTab


def convertObject(objectStr):
    """
    Method takes the list of optimal objects and converts
    its value to it's key label from the attributes dictionary list
    :param optimal: list of optimal objects
    :return: converted optimal objects
    """
    objectList = objectStr.split()
    transObj = []
    for obj in objectList:
        for cur in atts:
            value = cur.values().pop()
            if obj == value:
                key = cur.keys().pop()
                obj = key
                transObj.append(obj)
                break
    i = 1
    while i < len(transObj):
        transObj.insert(i, ' ')
        i += 2
    s = ''
    for i in range(0, len(transObj)):
        s = s + transObj[i]

    return s


def findOptimal(objTab):
    """
    Method sorts the feasible objects with selection sort algorithm
    once the objects are sorted, the minimum (optimal) object is found
    and appended to the list of optimal objects.  The remaining
    feasible objects are searched to determine if any other objects
    have the same penalty value.
    :param objTab:
    :return: optimal (list of optimal objects)
    """
    optVal = 0
    optimal = []

    if len(objTab) == 1:
        return objTab[0]

    for i in range(len(objTab)):

        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i + 1, len(objTab)):
            if objTab[min_idx][1] > objTab[j][1]:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        objTab[i], objTab[min_idx] = objTab[min_idx], objTab[i]


    optVal = objTab[0][1]
    for x in objTab:
        if x[1] == optVal:
            optimal.append(x)

    return optimal



def performPenaltyLogic(feasObjects, boolVars):
    """
    This method performs penalty logic calculations.
    It makes a cnf file containing the preference constraint,
    iterates through the preferences list and for each preference,
    makes a cnf file and searchs for objects in the feasible object list.
    If its not found, penalty is assigned. Process continues until
    all preferences have been checked. Finally, places the obj and its
    penalty value in currentObj, and is appended to the objectTable
    :param feasObjects: objects filtered by the constraints
    :param boolVars: number of attributes
    :return: object table containing objects and their penalty values
    """
    objectTable = []

    for obj in feasObjects:
        penaltyValue = 0
        for pref in preferences:
            satisfiable, feasibleObjects, dummy_num = getFeasibleObjects(boolVars, pref[0])
            if satisfiable:
                found = False
                for i in feasibleObjects:
                    if obj == i:
                        found = True
                        break
                if found == False:
                    num = int(pref[1])
                    penaltyValue += num
            else:
                num = int(pref[1])
                penaltyValue += num
        currentObj = [obj, penaltyValue]
        objectTable.append(currentObj)

    return objectTable


def getFeasibleObjects(boolVars, clauseList):
    """This method writes to a CNF file.  The file contains
    all the clauses to be checked by clasp.  The method runs
    clasp and collects all feasible objects filtered by the
    constraints.  If satisfiable, the method returns a list
    of all the feasible objects
    param: number of attributes
    param: clauseList
    return: feasibleObjects list
    """
    satisfiable = False
    feasibleObjects = []
    vars = str(boolVars)
    num_clauses = str(len(clauseList))
    firstLine = 'p cnf ' + vars + ' ' + num_clauses + '\n'
    file_name = 'temp.cnf'
    save = open(file_name, 'w')
    clause_text =''
    for current in clauseList:
        for item in current:
            clause_text += item
        clause_text += '\n'

    clasp_text = firstLine + clause_text

    save.write(clasp_text)
    save.close()

    output = commands.getoutput("clasp " + file_name + ' -n 0')
    results = []

    results = output.splitlines()

    if results.__contains__('s SATISFIABLE'):
        satisfiable = True

    if satisfiable:
        for line in results:
            if line[0] == 'v':
                # not sure if i should keep the 0 at the end
                feasibleObj = line[2:-2]  #this gets rid of the 0
                # feasibleObj = line[2:]  #this does not
                feasibleObjects.append(feasibleObj)
    return satisfiable, feasibleObjects, len(feasibleObjects)


def convertPreferences(prefList):
    """
    Parses the list of preferences into a format suitable
    for the convertConstraints method.  Removes the comments
    from the last value before the penalty value.
    Extracts the penalty value from each preference string.
    Converts all preferences to CLASP formatted clauses
    and groups the clauses with the appropriate penalty value.
    :param prefList: list of preferences
    :return: validity
    """
    valid = True
    prefList_phase2 = []
    for line in prefList:
        # I NEED TO GET RID OF THE COMMA AND ALSO PUT THE CONSTRAINT IN A LIST
        pref_cons = line.split()
        penaltyVal = pref_cons.pop()
        commaRemove = pref_cons[-1].replace(',', '')
        pref_cons[-1] = commaRemove
        i = 1
        while i < len(pref_cons):
            pref_cons.insert(i, ' ')
            i += 2
        s = ''
        for i in range(0, len( pref_cons)):
            s = s +  pref_cons[i]
        prefStrList = [s]
        prefList_phase1 = []
        prefList_phase1 = [prefStrList, penaltyVal]
        prefList_phase2.append(prefList_phase1)

    for i in range(0, len(prefList_phase2), 1):
        # I NEED TO PASS A LIST OF STRING OBJECTS IN THE FIRST PARAMETER
        listOfPrefs = prefList_phase2[i][0]
        penVal = prefList_phase2[i][1]
        valid = convertConstraints(listOfPrefs, penVal, 'prefs')
        if valid == False:
            break

    return valid

def getValues(item):
    """searches attributes list and returns numeric value
        returns validity
    """
    valid = False
    for cur in atts:
        keyname = cur.keys().pop()
        if item == 'NOT' or item == 'AND' or item == 'OR':
            valid = True
            break
        if item == keyname:
            item = cur.values().pop()
    return valid

def convertConstraints(conList, penVal, type):
    """Parses constraint list, checks for errors,
       removes NOTS, converts attributes into
       their binary numeric values.
       If the type is 'cons', that means
       this is a hard constraint, and
       generatesConstraintClause method will be called.
       Otherwise, a list of preference clauses will be
       generated along with its penalty value.
       param: conList (list of constraints)
       param: penVal (only applicable for preferences)
       param: type (determines if hard constraint or preference)
       returns validity
    """
    valid = True
    for line in conList:
        buildCons = []
        cur = line.split()
        if cur[0] == 'AND' or cur[0] == 'OR' or \
                cur[-1] == 'AND' or cur[-1] == 'OR' or cur[-1] == 'NOT':
            valid = False
            break
        for item in cur:
            if item == 'NOT' or item == 'AND' or item == 'OR':
                buildCons.append(item)
            else:
                for curStr in atts:
                    keyname = curStr.keys().pop()
                    if item == keyname:
                        item = curStr.values().pop()
                        buildCons.append(item)
                        break
        valid = checkErrors(buildCons)
        if valid:
            cons_phase_1 = removeNots(buildCons)
            if type == 'cons':
                generateConstraintClauses(cons_phase_1)
            else:
                generatePreferenceClauses(cons_phase_1, penVal)
            buildCons = []
        else:
            valid = False
            break
    return valid

def removeNots(tempCon):
    """Detects if NOT's are found in the constraint.
    If NOT is detected, method removes the NOT and negates
    the binary value associated with the NOT placement.
    Returns a constraint without NOTS.  For easier
    conversion of clauses into CLASP format.
    """
    no_nots_con = []
    getLast = True
    # maybe do a check to see if the last two items in list are NOT , number
    if(len(tempCon) >= 2 and tempCon[-2] == 'NOT'):
        getLast = False
    j = 0
    for i in range(0, len(tempCon) - 1, 1):
        i = j
        if i >= len(tempCon):
            break
        if tempCon[i] == 'NOT' and is_int(tempCon[i+1]):
            num = int(tempCon[i+1])
            res = num * -1
            no_nots_con.append(str(res))
            j = i + 2
        elif tempCon[i] == 'NOT' and tempCon[i+1] == 'NOT':
            j = i + 2
        else:
            if i == len(tempCon) - 1:
                getLast = False
            no_nots_con.append(tempCon[i])
            j = i + 1

    if getLast and len(tempCon) >= 2:
        no_nots_con.append(tempCon[-1])
    return no_nots_con

def generatePreferenceClauses(tempCon, penVal):
    """Parses the preference constraints, converts
    the constraints into CLASP FORMAT, includes
    the list of clauses with the appropriate penalty value.
    Stores the grouping of preference clauses with penalty values
    into a global list of preferences.
    """
    prefClauses = []
    pref_and_penalty = []
    clause = []
    j = 0
    for i in range(0, len(tempCon) - 1, 1):
        i = j
        if j >= len(tempCon):
            break
        if is_int(tempCon[i]):
            val1 = tempCon[i]
            clause.append(val1)
            j = i + 1
        elif tempCon[i] == 'OR' and is_int(tempCon[i+1]):
            val2 = tempCon[i + 1]
            checkLastIndex = i+1
            if checkLastIndex == len(tempCon) - 1:
                clause.append(' ')
                clause.append(val2)
                clause.append(' ')
                clause.append('0')
                prefClauses.append(clause)
                clause = []
                j = i + 2
            elif tempCon[i+2] == 'OR':
                clause.append(' ')
                clause.append(val2)
                j = i + 2
            elif tempCon[i+2] == 'AND':
                clause.append(' ')
                clause.append(val2)
                j = i + 2
        elif tempCon[i] == 'AND':
            checkLastIndex = i + 1
            if checkLastIndex == len(tempCon) - 1:
                clause.append(' ')
                clause.append('0')
                prefClauses.append(clause)
                clause = []
                val1 = tempCon[i+1]
                clause.append(val1)
                clause.append(' ')
                clause.append('0')
                prefClauses.append(clause)
                clause = []
                j = i + 2
            else:
                clause.append(' ')
                clause.append('0')
                prefClauses.append(clause)
                clause = []
                j = i + 1

    pref_and_penalty = [prefClauses, penVal]
    preferences.append(pref_and_penalty)

# conList = ['NOT X OR NOT Y', 'X OR Y OR X AND X']
# -1 1 0     1 -1 1 0
def generateConstraintClauses(tempCon):
    """Parses the data contained in the constraints list,
       after list has been stripped of NOTS.
       Converts constraints into clauses
       in correct CLASP format
    """
    clause = []
    j = 0
    for i in range(0, len(tempCon) - 1, 1):
        i = j
        if i >= len(tempCon):
            break
        if is_int(tempCon[i]):
            val1 = tempCon[i]
            clause.append(val1)
            j = i + 1
        elif tempCon[i] == 'OR' and is_int(tempCon[i+1]):
            val2 = tempCon[i + 1]
            checkLastIndex = i+1
            if checkLastIndex == len(tempCon) - 1:
                clause.append(' ')
                clause.append(val2)
                clause.append(' ')
                clause.append('0')
                conClauses.append(clause)
                clause = []
                j = i + 2
            elif tempCon[i+2] == 'OR':
                clause.append(' ')
                clause.append(val2)
                j = i + 2
            elif tempCon[i+2] == 'AND':
                clause.append(' ')
                clause.append(val2)
                j = i + 2
        elif tempCon[i] == 'AND':
            checkLastIndex = i + 1
            if checkLastIndex == len(tempCon) - 1:
                clause.append(' ')
                clause.append('0')
                conClauses.append(clause)
                clause = []

                val1 = tempCon[i+1]
                clause.append(val1)
                clause.append(' ')
                clause.append('0')
                conClauses.append(clause)
                clause = []
                j = i + 2
            else:
                clause.append(' ')
                clause.append('0')
                conClauses.append(clause)
                clause = []
                j = i + 1

def checkErrors(tempCon):
    """Checks if there are errors (AND AND, AND OR, digit digit, OR AND)"""
    res = True
    # len might take into account the last index
    for i in range(0, len(tempCon)-1, 1):
        if tempCon[i] == 'AND' and (tempCon[i+1] == 'AND' or tempCon[i+1] == 'OR'):
            res = False
            break
        elif tempCon[i] == 'OR' and (tempCon[i+1] == 'AND' or tempCon[i+1] == 'OR'):
            res = False
            break
        elif is_int(tempCon[i]) and is_int(tempCon[i+1]):
            res = False
            break
    return res

def checkPreferences(preList):
    """Verifies that the preferences contain correct values
        that match attributes list and checks if last
        item in each string contains a number.
        Returns if valid or invalid
    """
    valid = True
    for line in preList:
        cur = line.split()
        last = cur[-1]
        if is_int(last) == False:
            valid = False
            break
        for item in cur[:-1]:
            x = item.replace(",", "")
            valid = searchAttributes(x)
            if valid:
                continue
            else:
                valid = False
                break
    return valid

def is_int(input):
    """checks if the input can be parsed into an integer value"""
    try:
        num = int(input)
    except ValueError:
        return False
    return True

def searchAttributes(item):
    """Searches the list of attributes to verify that the item was found.
       Ignores NOT AND OR
       returns if item is valid
    """
    valid = False
    for cur in atts:
        keyname = cur.keys().pop()
        if item == 'NOT' or item == 'AND' or item == 'OR' or item == keyname:
            valid = True
            break
    return valid

def checkConstraints(conList):
    """Verifies that the values in the constraints list
       are located in the list of attributes. Returns true
       if constraints are sound.
    """
    valid = True
    for line in conList:
        cur = line.split()
        for item in cur:
            valid = searchAttributes(item)
            if valid:
                continue
            else:
                valid = False
                break
    return valid

def getAttributes(attList):
    """Takes each binary value, and stores it in a dictionary along
        with a numeric value.  Checks if the input is in correct format.
        Returns true if input valid.  Stores all dictionaries into a list.
        Returns the number of attributes
    """
    count = 1
    valid = False
    for line in attList:
        cur = line.split()
        if len(cur) == 3 and cur[0][-1].endswith(':') and cur[1][-1].endswith(','):
            binPos = {cur[1][:-1]: str(count)}
            binNeg = {cur[2]: str(-count)}
            atts.append(binPos)
            atts.append(binNeg)
            count += 1
            valid = True
        else:
            valid = False
            break
    count -= 1
    return count, valid

