# imports
import sys

# error: a method that showcases all the different errors that may occur in the running of this program. 
# *Change for phase 2 = we now get to have 2 arguments (error number, token-name)
def error(number,token):
    if(number == -1):
        print("ERROR (-1): Wrong file types. Files must by of type '.ci' (cimple).")
    elif(number == 0):
        print("ERROR (0): Illegal token detected: '",token,"'")
    elif(number == 1):
        print("ERROR (1): Keyword “program” expected in line 1. All programs should start with the keyword “program”. Instead, '"+token+"' appeared.")
    elif(number == 2):
        print("ERROR (2): The name of the program expected after the keyword “program” in line 1. The illegal program name '"+token+"' appeared.")
    elif(number == 3):
        print("ERROR (3): Every program should end with a fullstop, fullstop at the end is missing.")
    elif(number == 4):
        print("ERROR (4): No characters are allowed after the fullstop indicating the end of the program.")
    elif(number == 5):
        print("ERROR (5): Curly left bracket '{' missing at the start of the block. Instead the token '"+token+"' appeared.")
    elif(number == 6):
        print("ERROR (6): Forgot to close '{' . Instead the token '"+token+"' appeared.")
    elif(number == 7):
        print("ERROR (7): Missing ';' . Instead '"+token+"' appeared.")
    elif(number == 8):
        print("ERROR (8): Missing variable in declaration. Instead '"+token+"' appeared.")
    elif(number == 9):
        print("ERROR (9): The name of the subprogram expected. The illegal subprogram name '"+token+"' appeared.")
    elif(number == 10):
        print("ERROR (10): Round left bracket '(' missing Instead '"+token+"' appeared.")
    elif(number == 11):
        print("ERROR (11): Forgot to close '(' . Instead the token '"+token+"' appeared.")
    #elif(number == 12):
    elif(number == 13):
        print("ERROR (13): Missing relational operator between expressions. Instead '"+token+"' appeared.")
    elif(number == 14):
        print("ERROR (14): Missing argument after 'in' or 'inout' keyword. Instead '"+token+"' appeared.")
    elif(number == 15):
        print("ERROR (15): Missing assignment token ':='. Instead '"+token+"' appeared.")
    elif(number == 16):
        print("ERROR (16): Missing keyword inside a case statement. Instead '"+token+"' appeared.")
    elif(number == 17):
        print("ERROR (17): The name of the call statement expected. The illegal subprogram name '"+token+"' appeared.")
    elif(number == 18):
        print("ERROR (18): Missing identifier inside input expression. Instead '"+token+"' appeared.")
    elif(number == 19):
        print("ERROR (19): Forgot to close '[' . Instead the token '"+token+"' appeared.")
    elif(number == 20):
        print("ERROR (20): There are no more scopes to delete.")
    elif(number == 21):
        print("ERROR (21): The entity you are trying to create is invalid.")
    elif(number == 22):
        print("ERROR (22): No entity with name '"+token+"' was found in the produced symbol table.")
    exit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ File input from terminal

filePath = sys.argv[1]                                          # a global variable that holds our file path or name.
fileNameAndType = filePath.split('.')                           # spliting our filePath into [path,ending/file type]
try:
    if(fileNameAndType[1] != "ci"):                             # if file type belongs to Cimple then accept else we have an error.
        error(-1,None)
except IndexError:
    error(-1,None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Lexical Analyser

# a global counter that will help us return to where we left off at reading the file.
characterCounter = 0

# an array of possible (and acceptable) encounters except from letters and numbers.
possibleEncounters = ['+','-','*','/','{','}','(',')','[',']',',',';','.',':','<','>','=','#']

# an array of possible (and acceptable) preoccupied words.
keywords = ["program","declare","if","else","while","switchcase","forcase","incase","case","default","not","and","or","function","procedure",
            "call","return","in","inout","input","print"]

# the states of our Lexical Analyser's state machine.
states = {
    "stateSTART" : ["stateSTART","stateDIG","stateIDK","addTOKEN","subTOKEN","mulTOKEN","divTOKEN","leftCurlyBracketTOKEN",
                    "rightCurlyBracketTOKEN","leftRoundBracketTOKEN","rightRoundBracketTOKEN","leftBoxBracketTOKEN","rightBoxBracketTOKEN",
                    "commaTOKEN","semicolonTOKEN","periodTOKEN","stateASGN","stateSMALLER","stateLARGER","equalTOKEN","stateREM","EOF","illegalTOKEN"],
    "stateDIG" : ["endDIG","stateDIG","illegalTOKEN","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG",
                  "endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG","endDIG"],
    "stateIDK" : ["endIDK","stateIDK","stateIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK",
                  "endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK","endIDK"],
    "stateASGN" : ["illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN",
                   "illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN",
                   "illegalTOKEN","illegalTOKEN","assignmentTOKEN","illegalTOKEN","illegalTOKEN","illegalTOKEN"],
    "stateSMALLER" : ["smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN",
                      "smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN",
                      "differentTOKEN","smallerEqualTOKEN","smallerTOKEN","smallerTOKEN","smallerTOKEN"],
    "stateLARGER" : ["largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN",
                     "largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","largerTOKEN","differentTOKEN","largerTOKEN",
                     "largerEqualTOKEN","largerTOKEN","largerTOKEN","largerTOKEN"],
    "stateREM" : ["stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM",
                  "stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateREM","stateSTART","illegalTOKEN","stateREM"]  
}

# Lexical Analyser
def lexicalAnalyser():
    global filePath,characterCounter                            # the global variables we will be using.

    file = open(filePath, "r")                                  # open the file.
    file.read(characterCounter)                                 # reading up to the point we last left off.

    token = ""                                                  # this variable will be the word we will be reading each time.
    currentState = "stateSTART"                                 # starting state of the state machine.
    result = 0                                                  # starting result (next state) of the state machine.

    # the state machine.
    while(currentState != "illegalTOKEN") or (currentState not in states.keys()):
        
        # read character by character.
        currentCharacter = file.read(1)                         # current character.
        characterCounter = characterCounter + 1                 # adding to the counter. (next character)

        # state machine.
        if(currentCharacter.isspace()):                         # if we have empty char.
            result = 0
        elif(currentCharacter.isdigit()):                       # if we have number char.
            result = 1
        elif(currentCharacter.isalpha()):                       # if we have letter char.
            result = 2
        elif(currentCharacter in possibleEncounters):           # if we have a symbol char.
            result = 3 + possibleEncounters.index(currentCharacter)
            if(currentCharacter == '#') and (currentState == "stateREM"):   # for comments.
                token = ""
        elif(currentCharacter == ""):                           # if we have EOF.
            result = 21
        else:                                                   # if we have illegal char.
            result = 22
        currentState = states[currentState][result]             # calculation of the next state.

        # if we stay in stateSTART, we have whitespace and we don't want to save that.
        if(currentState != "stateSTART"): 
            token = token + currentCharacter
        
        # if we have a state that is a finishing state then we get out of the state machine.
        if(currentState not in states.keys()): break

    # states that need the pointer to go back 1 position.
    if(currentState == "endDIG" or currentState == "endIDK" or currentState == "smallerTOKEN" or currentState == "largerTOKEN"):
        
        token = token[:-1]
        characterCounter = characterCounter - 1

    # for number token.
    if(currentState == "endDIG"):
        currentState = "numberTOKEN"
    
    # figuring out if tokens of endIDK are identifiers or keywords.
    if(currentState == "endIDK"):
        if(token in keywords):
            str = token + "TOKEN"
            currentState = str
        else:
            currentState = "identifierTOKEN"

    # in case of error, the program ends while informing the user of the error that was made.
    if(currentState == "illegalTOKEN"): error(0,token)

    # *Change for middleware* now instead of only having the currentState as a result, we will get the tokens also. (all in a form of a list)
    finalResult = [currentState,token] 
    return finalResult

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Methods and global variables for Middleware

# *Change for middleware* global variables.
quadList = []                                                   # a global list.
quadCounter = -1                                                # a global counter (that will act as a label for each item in quadList)
tempCounter = 0                                                 # a global counter (that will count temporary variables)

# *Change for middleware* methods.
def genQuad(operator, operand1, operand2, operand3):
    global quadList,quadCounter
    quadCounter = quadCounter + 1                               # finding the new label of the new entry.
    newQuad = [quadCounter,[operator,operand1,operand2,operand3]] # making a new quad entry.
    quadList.append(newQuad)                                    # adding the entry to the global list.

def nextQuad():
    global quadCounter
    temporary = quadCounter + 1                                 # finding the next label.
    return temporary                                            # returning that label.

def newTemp():
    global tempCounter
    temporary = "temp_" + str(tempCounter)                      # new name for the next temporary variable.
    tempCounter = tempCounter + 1
    return temporary                                            # returning the temporary variable.

def emptyList():
    emptyList = []                                              # making an empty list.
    return emptyList                                            # returning that list.

def makeList(label):                                
    newList = [label]                                           # making a list with only label inside.
    return newList                                              # returning that list.

def mergeList(list1,list2):
    newList = list1 + list2                                     # merging the lists into a new list.
    return newList                                              # returning that list.

def backpatch(list,label):
    for i in list:                                              # for each item (i) in the list that was given,
        quadList[i][1][3] = label                               # replace with label the last element of the quads with label i.

def printList(list):                                            # printing the results in .init and .c files.
    try:                                                        # if files .init and .c don't exist -> create them.
        f_init = open("endiamesos.init", "w")
        f_c = open("endiamesos.c", "w")
    except FileExistsError:                                     # if files .init and .c exist -> overwrite them.
        f_init = open("endiamesos.init", "x")
        f_c = open("endiamesos.c", "x")

    # print to the .init file.
    f_init.write("The Middleware results are:\n")
    for i in range(0,len(list)):
        f_init.write(str(i)+" : "+str(list[i][1][0])+","+str(list[i][1][1])+","+str(list[i][1][2])+","+str(list[i][1][3])+"\n")
    f_init.close()

    # print to the .c file.
    variables = []
    f_c.write("//The Middleware results are:\n\n")
    f_c.write("#include <stdio.h>\n\nint main(){\n")
    for i in range(0,len(list)):
        
        one = list[i][1][0]
        two = list[i][1][1]
        three = list[i][1][2]
        four = list[i][1][3]

        if("main_" in str(two)) and (one == "begin_block"):
            f_c.write("\tLine_"+str(i)+": goto Line_"+str(i+1)+";")
            f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
        elif("main_" in str(two)) and (one == "end_block"):
            f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            f_c.write("}\n")
        elif("main_" not in str(two)) and (one in ["begin_block","end_block"]):
            f_c.write("\tLine_"+str(i)+": goto Line_"+str(i+1)+";")
            f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
        else:
            if(one == "halt"):
                f_c.write("\tLine_"+str(i)+": return 0;")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "jump"):
                f_c.write("\tLine_"+str(i)+": goto Line_"+str(four)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "out"):
                f_c.write("\tLine_"+str(i)+": printf(\"%d\","+str(two)+");")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "in"):
                f_c.write("\tLine_"+str(i)+": scanf(\"%d\", &"+two+");")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "ret"):
                f_c.write("\tLine_"+str(i)+": goto Line_"+str(i+1)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")                   
            elif(one in ["+","-","*","/"]):
                f_c.write("\tLine_"+str(i)+": ")
                if(four not in variables):
                    f_c.write("int "+str(four)+" = "+str(two)+" "+str(one)+" "+str(three)+";")
                    variables.append(four)
                else:
                    f_c.write(str(four)+" = "+str(two)+" "+str(one)+" "+str(three)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one in [">","<","<=",">="]):
                f_c.write("\tLine_"+str(i)+": if("+str(two)+" "+str(one)+" "+str(three)+") goto Line_"+str(four)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "="):
                f_c.write("\tLine_"+str(i)+": if("+str(two)+" == "+str(three)+") goto Line_"+str(four)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "<>"):
                f_c.write("\tLine_"+str(i)+": if("+str(two)+" != "+str(three)+") goto Line_"+str(four)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == ":="):
                f_c.write("\tLine_"+str(i)+": ")
                if(four not in variables):
                    f_c.write("int "+str(four)+" = "+str(two)+";")
                    variables.append(four)
                else:
                    f_c.write(str(four)+" = "+str(two)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(one == "par"):
                if(three == "cv"):
                    f_c.write("\tLine_"+str(i)+": goto Line_"+str(i+1)+";")
                elif(three == "ret"):
                    if(two not in variables):
                        f_c.write("\tLine_"+str(i)+": int "+str(two)+";")
                        variables.append(four)
                else:
                    f_c.write("\tLine_"+str(i)+": "+str(two)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")
            elif(list[i][1][0] == "call"):
                f_c.write("\tLine_"+str(i)+": goto Line_"+str(i+1)+";")
                f_c.write("\t//"+str(i)+" : "+str(one)+","+str(two)+","+str(three)+","+str(four)+"\n")     
            
            else: 
                f_c.write("\n")
    f_c.close()
            
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~ Classes, methods and global variables for Symbol Table

# *Change for symbol table* global variables.
currentScope = None                                             # our current Scope
symbolTable = deepCopySymbolTable = None                        # *Change for final code* our tables. (we need the deepcopy for the production of our final code) 
table_file = None                                               # our file in which we will print the symbol table's contents. 

# *Change for symbol table* classes.
class Entity:                                                   # class for entity.
    def __init__(self,name):                                    # initialiser.
        self.name = name
    
class Variable(Entity):                                         # class for variables that implement class entity.
    def __init__(self,name,dataType,offset):                    # initialiser.
        Entity.__init__(self,name)                              # calling entity in order not to overwrite it.
        self.dataType = dataType
        self.offset = offset
    
    def printFields(self):                                      # method for printing the object
        return "|| name = "+str(self.name)+"|| data type = "+str(self.dataType)+"|| offset = "+str(self.offset)

class TemporaryVariable(Variable): pass                         # class for temporary variables that implements class variable as is without any change.

class FormalParameter(Entity):                                  # class for formal parameters that implement class entity.
    def __init__(self,name,dataType,mode,offset):               # initialiser.
        Entity.__init__(self,name)
        self.dataType = dataType
        self.mode = mode
        self.offset = offset

    def printFields(self):                                      # method for printing the object.
        return "|| name = "+str(self.name)+"|| data type = "+str(self.dataType)+"|| mode = "+str(self.mode)+"|| offset = "+str(self.offset)

class Parameter(FormalParameter,Variable):                      # class for parameters that implement the classes entity and formalparameters. 
    def __init__(self,name,dataType,mode,offset):               # initialiser.
        FormalParameter.__init__(self,name,dataType,mode)
        Variable.__init__(self,name,dataType,offset)

class Procedure(Entity):                                        # class for procedures that implement the class entity.
    def __init__(self,name,formalParameters,startingQuad,frameLength): # initialiser.
        Entity.__init__(self,name)
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters = formalParameters
    
    def printFields(self):                                      # method for printing the object.
        return "|| name = "+str(self.name)+"|| frame length = "+str(self.frameLength)+"|| starting quad = "+str(self.startingQuad)+"|| formal parameters ="+str(self.formalParameters)

    def addFormalParameters(self,update):                       # method to add formal parameters in the list.
        self.formalParameters.append(update)
    
    def updateStartingQuad(self,update):                        # method to update the startingQuad value.
        self.startingQuad = update
    
    def updateFrameLength(self,update):                         # method to update the frameLength value.
        self.frameLength = update

class Function(Procedure):                                      # class for functions that implement the class procedure.
    def __init__(self,name,formalParameters,startingQuad,frameLength,dataType): # initialiser.
        Procedure.__init__(self,name,formalParameters,startingQuad,frameLength)
        self.dataType = dataType

    def printFields(self):                                      # method for printing the object.
        return "|| name = "+str(self.name)+"|| data type = "+str(self.dataType)+"|| frame length = "+str(self.frameLength)+"|| starting quad = "+str(self.startingQuad)+"|| formal parameters ="+str(self.formalParameters)

class Scope:                                                    # class for the scopes.
    def __init__(self,name,entityList,nextScope):               # initialiser.
        self.name = name
        self.entityList = entityList
        self.nextScope = nextScope
    
    def getOffset(self):                                        # method that finds the next offset.
        if(self.entityList == None) or (self.entityList == []):
            newOffset = 12
        else:
            count = -1
            for i in range(0,len(self.entityList)):
                offset = 0
                if(isinstance (self.entityList[count],Variable)) or (isinstance (self.entityList[count],FormalParameter)) or (isinstance (self.entityList[count],TemporaryVariable)) or (isinstance (self.entityList[count],Parameter)):
                    offset = self.entityList[count].offset
                    break
                else:
                    count = count - 1
            newOffset = offset + 4
        return newOffset

    def searchEntity(self,name):                                # method that searches for an entity.
        entity = None
        for i in self.entityList:
            if (i.name == name):
                entity = i
                break
        return entity

class Table():                                                  # class for the symbol table.
    def __init__(self,scopeList):
        self.scopeList = scopeList
    
    def printTable(self,f):                                     # method for printing the object's scope list.
        f.write("----------- NEW ENTRY IN THIS FILE -----------\n")
        for i in self.scopeList:
            f.write("Scope: "+i.name+"\n")
            for j in i.entityList:
                temp = j.printFields()
                f.write("\t"+temp+"\n")
        f.write("\n")

# *Change for symbol table* methods.
def createScope(name):
    global currentScope,symbolTable,deepCopySymbolTable
    if(symbolTable == None):                                    # if we dont have a table yet.
        symbolTable = Table([])
        deepCopySymbolTable = Table([])                         # *Change for final code* we initiallise here the symbol table deep copy.
    if(currentScope == None):                                   # if we have our first scope creation.
        currentScope = Scope(name,[],None)                      # the new scope.
        symbolTable.scopeList.append(currentScope)              # adding it to the scope list of our table.
    else:
        newScope = Scope(name,[],currentScope)
        symbolTable.scopeList.append(newScope)
        currentScope = newScope

def removeScope():
    global currentScope,symbolTable,deepCopySymbolTable
    if(currentScope == None):                                   # if we don't have any more scopes to remove.
        error(20,None)
    else:
        deepCopySymbolTable.scopeList.append(symbolTable.scopeList[-1]) # *Change for final code* we want to save the completed scopes in our symbol table deep copy.
        symbolTable.scopeList.remove(symbolTable.scopeList[-1]) # removing it from the table.
        currentScope = currentScope.nextScope                   # moving on to the next scope.

def insertEntity(entityType,name,mode):
    global currentScope
    newOffset = currentScope.getOffset()
    if(entityType == "variable"):                               # if we want to create a variable.
        newEntity = Variable(name,"VAR",newOffset)
    elif(entityType == "temporary"):                            # if we want to create a temporary variable.
        newEntity = TemporaryVariable(name,"TEMP",newOffset)
    elif(entityType == "parameter"):                            # if we want to create a parameter.
        newEntity = Parameter(name,"PARAM",mode,newOffset)
    elif(entityType == "formal"):                               # if we want to create a formal parameter.
        newEntity = FormalParameter(name,"FORMAL",mode,newOffset)
    elif(entityType == "procedure"):                            # if we want to create a procedure.
        newEntity = Procedure(name,[],None,None)
    elif(entityType == "function"):                             # if we want to create a function.
        newEntity = Function(name,[],None,None,"FUNC")
    else:
        error(21,None)
    currentScope.entityList.append(newEntity)                   # inserting the new Entity to the scope

def searchEntity(name):
    global symbolTable
    entity = None
    for i in symbolTable.scopeList:                             # searching the scopes for the entity.
        entity = i.searchEntity(name)
        if(entity != None):
            break                                               # if we find it -> stop.
    return entity

def updateEntity(name,fieldName,updateValue):
    global currentScope,symbolTable
    entity = searchEntity(name)                                 # find the entity.
    if(fieldName == "startingQuad"):                            # if we want to update the starting quad.
        entity.updateStartingQuad(updateValue)
    elif(fieldName == "frameLength"):                           # if we want to update the frame length.
        entity.updateFrameLength(updateValue)
    else: 
        error(22,name)                                          # if we want to update a field that isn't updatable or doesn't exist.

def addFormalParameter(name,formalParameter):
    global currentScope
    entity = searchEntity(name)                                 # find the entity.
    entity.addFormalParameters(formalParameter)                 # add to its formal parameters list.

def printTable(f):
    global symbolTable
    symbolTable.printTable(f)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Methods and global variables for Final Code

# *Change for final code* global variables.
lineCounter = 0                                             # a line counter for the file we will write.
final_file = None                                           # the file we will write our final code in.

# *Change for final code* methods.
def searchEntityInDeepCopy(name, currentScope):             # searching the deep copy table for entities.
    global deepCopySymbolTable
    entity = foundScope = None
    currentScopeIndex = deepCopySymbolTable.scopeList.index(currentScope)   # getting the index of the scope we are currently in.
    for i in deepCopySymbolTable.scopeList:                 # find the entity
        entity = i.searchEntity(name)
        if(entity != None) and (currentScopeIndex <= deepCopySymbolTable.scopeList.index(i)): # if we find a similarly named entity and we are in a scope that still exists at this time, in the table.
            foundScope = i
            break
    if(entity == None):                                     # if we don't find the entity -> error
        error(22,name)
    return [entity,foundScope]                              # return the entity and the scope it was found in.

def gnlvcode(variable, currentScope):
    global deepCopySymbolTable,final_file,lineCounter
    search = searchEntityInDeepCopy(variable,currentScope)  # search the entity.
    entity = search[0]
    targetScope = search[1]
    targetScopeIndex = deepCopySymbolTable.scopeList.index(targetScope) # index of the target scope in our scope list.
    currentScopeIndex = deepCopySymbolTable.scopeList.index(currentScope) # index of the current scope in our scope list.
    layersToClimb = targetScopeIndex - currentScopeIndex    # layers to climb up until we find the target scope from our current scope.
    if(layersToClimb > 0): 
        final_file.write("\tlw t0,-8(sp)\n")
        for i in range(0,layersToClimb-1):
            final_file.write("\tlw t0,-8(t0)\n")
        final_file.write("\taddi t0,t0,-"+str(entity.offset)+"\n")
    return layersToClimb

def loadvr(sourceVariable, targetRegister, currentScope):
    global deepCopySymbolTable,final_file,lineCounter    
    # digit
    if(sourceVariable.isnumeric()):
        final_file.write("\tli "+targetRegister+","+sourceVariable+"\n")
    else: 
        search = searchEntityInDeepCopy(sourceVariable,currentScope)
        entity = search[0]
        foundScope = search[1]
        foundScopeIndex = deepCopySymbolTable.scopeList.index(foundScope)
        currentScopeIndex = deepCopySymbolTable.scopeList.index(currentScope)
        # local variable
        if(foundScopeIndex == currentScopeIndex and entity.dataType == "VAR"):
            layers = gnlvcode(sourceVariable,currentScope)
            if (layers <= 0):
                final_file.write("\tlw "+targetRegister+",-"+str(entity.offset)+"(sp)\n")
            else:
                final_file.write("\tlw "+targetRegister+",(t0)\n")
        # global variable
        elif(foundScopeIndex == len(deepCopySymbolTable.scopeList)-1 and entity.dataType == "VAR"):
            final_file.write("\tlw "+targetRegister+",-"+str(entity.offset)+"(gp)\n")
        # temporary variable
        elif (entity.dataType in "TEMP"):
            final_file.write("\tlw "+targetRegister+",-"+str(entity.offset)+"(sp)\n")
        # parameter that was set with "in"
        elif(entity.dataType == "FORMAL" and entity.mode == "CV"):
            layers = gnlvcode(sourceVariable,currentScope)
            if (layers <= 0):
                final_file.write("\tlw "+targetRegister+",-"+str(entity.offset)+"(sp)\n")
            else:
                final_file.write("\tlw "+targetRegister+",(t0)\n")
        # parameter that was set with "inout"
        elif(entity.dataType == "FORMAL" and entity.mode == "REF"):
            layers = gnlvcode(sourceVariable,currentScope)
            if (layers <= 0):
                final_file.write("\tlw t0,-"+str(entity.offset)+"(sp)\n")
                final_file.write("\tlw "+targetRegister+",(t0)\n")
            else:
                final_file.write("\tlw t0,(t0)\n")
                final_file.write("\tlw "+targetRegister+",(t0)\n")

def storevr(sourceRegister, targetVariable, currentScope):
    global deepCopySymbolTable,final_file,lineCounter
    search = searchEntityInDeepCopy(targetVariable,currentScope)
    entity = search[0]
    foundScope = search[1]
    foundScopeIndex = deepCopySymbolTable.scopeList.index(foundScope)
    currentScopeIndex = deepCopySymbolTable.scopeList.index(currentScope)
    # local variable
    if(foundScopeIndex == currentScopeIndex and entity.dataType == "VAR"):
        layers = gnlvcode(targetVariable,currentScope)
        if (layers <= 0):
            final_file.write("\tsw "+sourceRegister+",-"+str(entity.offset)+"(sp)\n")
        else:
            final_file.write("\tsw "+sourceRegister+",(t0)\n")
    # global variable
    elif(foundScopeIndex == len(deepCopySymbolTable.scopeList)-1 and entity.dataType == "VAR"):
        final_file.write("\tsw "+sourceRegister+",-"+str(entity.offset)+"(gp)\n")
    # temporary variable
    elif (entity.dataType in "TEMP"):
        final_file.write("\tsw "+sourceRegister+",-"+str(entity.offset)+"(sp)\n")
    # parameter that was set with "in"
    elif(entity.dataType == "FORMAL" and entity.mode == "CV"):
        layers = gnlvcode(targetVariable,currentScope)
        if (layers <= 0):
            final_file.write("\tsw "+sourceRegister+",-"+str(entity.offset)+"(sp)\n")
        else:
            final_file.write("\tsw "+sourceRegister+",(t0)\n")
    # parameter that was set with "inout"
    elif(entity.dataType == "FORMAL" and entity.mode == "REF"):
        layers = gnlvcode(targetVariable,currentScope)
        if (layers <= 0):
            final_file.write("\tlw t0,-"+str(entity.offset)+"(sp)\n")
            final_file.write("\tsw "+sourceRegister+",(t0)\n")
        else:
            final_file.write("\tlw t0,(t0)\n")
            final_file.write("\tsw "+sourceRegister+",(t0)\n")


# This is a method that produces the final code.
def produceFinalCode():
    global quadList,final_file,lineCounter,deepCopySymbolTable
    currentScope = deepCopySymbolTable.scopeList[0]
    parCounter = 0
    for i in range(0,len(quadList)):
        
        one = str(quadList[i][1][0])
        two = str(quadList[i][1][1])
        three = str(quadList[i][1][2])
        four = str(quadList[i][1][3])
        
        if(i == 0):                                         # start of the program               
            final_file.write("L"+str(lineCounter)+":\n\tj main\n")
            lineCounter = lineCounter + 1
        if(one == "begin_block"):                           # start of function or procedure (including our main)
            if("main_" in two):
                final_file.write("\nmain:\n")
                final_file.write("L"+str(lineCounter)+":\n\taddi sp,sp,"+str(currentScope.getOffset())+"\n\tmv gp,sp\n")
                lineCounter = lineCounter + 1   
            else:
                final_file.write("\n"+two+":\n")
                final_file.write("L"+str(lineCounter)+":\n\tsw ra,-0(sp)\n") 
                lineCounter = lineCounter + 1
        elif(one == "end_block"):                           # end of function or procedure (including our main)
            currentScope = currentScope.nextScope           # moving to the nextScope since we end the current function/procedure.
            if("main_" not in two):
                final_file.write("L"+str(lineCounter)+":\n\tlw ra,-0(sp)\n\tjr ra")
                lineCounter = lineCounter + 1
        elif(one == "halt"):                                # end of program
            final_file.write("L"+str(lineCounter)+":\n\tli a0,0\n\tli a7,93\n\tecall")
            lineCounter = lineCounter + 1
        elif(one in ["+","-","/","*",":="]):                # math and assignments
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            if(three == "_"):                               # if we have assignment with 2 variables
                loadvr(two,"t1",currentScope)
                storevr("t1",four,currentScope)
            else:                                           # if we have assignment or operation with 3 variables
                loadvr(two,"t1",currentScope)
                loadvr(three,"t2",currentScope)
                if("+" in one):                             # addition.
                    final_file.write("\tadd t1,t1,t2\n")
                elif("-" in one):                           # subtraction.
                    final_file.write("\tsub t1,t1,t2\n")
                elif("/" in one):                           # division.
                    final_file.write("\tdiv t1,t1,t2\n")
                elif("*" in one):                           # multiplication.
                    final_file.write("\tmul t1,t1,t2\n")
                storevr("t1",four,currentScope)
        elif(one == "jump"):                                # for jump.
            final_file.write("L"+str(lineCounter)+":\n\tj L"+four)
            lineCounter = lineCounter + 1
        elif(one in [">",">=","<","<=","<>","="]):          # logical operations
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            loadvr(two,"t5",currentScope)
            loadvr(three,"t6",currentScope)
            if(one == ">"):
                final_file.write("\tbgt t5,t6,L"+four+"\n") # bgt
            elif(one == ">="):
                final_file.write("\tbge t5,t6,L"+four+"\n") # bge
            elif(one == "<"):
                final_file.write("\tblt t5,t6,L"+four+"\n") # blt
            elif(one == "<="):  
                final_file.write("\tble t5,t6,L"+four+"\n") # ble
            elif(one == "<>"):
                final_file.write("\tbne t5,t6,L"+four+"\n") # bne
            elif(one == "="):
                final_file.write("\tbeq t5,t6,L"+four+"\n") # beq
        elif(one == "out"):                                 # printing
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            loadvr(two,"a0",currentScope)
            final_file.write("\tli a7,1\n\tecall\n")
        elif(one == "in"):                                  # inputs
            final_file("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            loadvr(two,"t1",currentScope)
            final_file("\tli a7,5\n\tecall\n")
        elif(one == "ret"):                                 # returns
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            loadvr(two,"t1",currentScope)
            final_file.write("\tlw t0,-8(sp)\n\tsw t1,(t0)\n")
        elif(one == "par"):                                 # parameters
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            if(parCounter == 0):
                final_file.write("\taddi fp,sp,"+str(currentScope.getOffset())+"\n")
            parCounter = parCounter + 1
            d = 12 + (parCounter - 1) * 4
            if(three == "cv"): #in
                loadvr(two,"t1",currentScope)
                final_file.write("\tsw t1,-"+str(d)+"(fp)\n")
            elif(three == "ret"): #return
                search = searchEntityInDeepCopy(two,currentScope)
                entity = search[0]
                targetScope = search[1]
                if(currentScope.nextScope == targetScope.nextScope):
                    if(entity.dataType == "VAR") or (entity.dataType == "FORMAL" and entity.mode == "CV"):
                        final_file.write("\tadd t0,sp,-"+str(entity.offset)+"\n")
                        final_file.write("\tadd t0,sp,-"+str(d)+"(fp)\n")
                    elif(entity.dataType == "FORMAL" and entity.mode == "REF"):
                        final_file.write("\tlw t0,-("+str(entity.offset)+"(sp)\n")
                        final_file.write("\tsw t0,-"+str(d)+"(fp)\n")
                else:
                    if(entity.dataType == "VAR") or (entity.dataType == "FORMAL" and entity.mode == "CV"):
                        gnlvcode(two,currentScope)
                        final_file("\tsw t0,-"+str(d)+"(fp)\n")
                    elif(entity.dataType == "FORMAL" and entity.mode == "REF"):
                        gnlvcode(two,currentScope)
                        final_file("\tlw t0,(t0)\n")
                        final_file("\tsw t0,-"+str(d)+"(fp)\n")
            elif(three == "ref"): #inout
                search = searchEntityInDeepCopy(two,currentScope)
                entity = search[0]
                targetScope = search[1]
                final_file.write("\taddi t0,sp,-"+str(entity.offset)+"\n")
                final_file.write("\tsw t0,-"+str(entity.offset)+"(fp)\n")
        elif(one == "call"):                            # function or procedure calls.
            final_file.write("L"+str(lineCounter)+":\n")
            lineCounter = lineCounter + 1
            search = searchEntityInDeepCopy(two,currentScope)
            entity = search[0]
            targetScopeIndex = deepCopySymbolTable.scopeList.index(search[1])-1
            targetScope = deepCopySymbolTable.scopeList[targetScopeIndex]
            if(len(entity.formalParameters) == 0):
                final_file.write("\taddi fp,sp,"+str(entity.frameLength)+"\n")
            if(currentScope.nextScope == targetScope.nextScope):
                final_file.write("\tlw t0,-4(sp)\n\tsw t0,-4(fp)\n")
            else:
                final_file.write("\tsw sp,-4(fp)\n")
            final_file.write("\taddi sp,sp,"+str(entity.frameLength)+"\n")
            final_file.write("\tjal "+two+"\n")
            final_file.write("\taddi sp,sp,-"+str(entity.frameLength)+"\n")  

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Syntax Analyser

# a global variable for the token we are currently in.
currentToken = []

# Syntax Analyser
def syntaxAnalyser(): 
    global currentToken,table_file,final_file,deepCopySymbolTable
    currentToken = lexicalAnalyser()                            # getting the first token of the file.
    try:                                                        # *Change for final code* opening the .symb AND .asm file for writing
        table_file = open("pinakas.symb","w")
        final_file = open("final.asm","w")
    except FileExistsError:
        table_file = open("pinakas.symb","x")
        final_file = open("final.asm","x")
    program()                                                   # starting the syntax recognition.
    printList(quadList)                                         # *Change for middleware* print the middleware.
    table_file.close()                                          # *Change for symbol table* closing the .symb file.
    produceFinalCode()                                          # *Change for final code* writing our final code .asm file.
    final_file.close()                                          # *Change for final code* closing the .asm file.
    print("\n\tCompilation successfully completed.Yay.\n")      # if all goes well, print out the success message.

def program():
    global currentToken,currentScope,file
    if(currentToken[0] == "programTOKEN"):                      # if the file starts with "program".
        currentToken = lexicalAnalyser()                        # move on to the next token.
        if(currentToken[0] == "identifierTOKEN"):
            ID = "main_" + currentToken[1]                      # *Change for middleware* getting the identifier token in order to call the programBlock (we add "main_" in order to know that we are talking about our main programBlock)
            currentToken = lexicalAnalyser()
            createScope(ID)                                     # *Change for symbol table* creating the first scope with name as the main_ID.
            programBlock(ID)                                    # *Change for middleware* now programBlocks have a unique ID-name.
            printTable(table_file)                              # *Change for symbol table* printing for results.
            removeScope()                                       # *Change for symbol table* now that we finished with this scope, we remove it.
            if(currentToken[0] == "periodTOKEN"):               # if the program ends correctly with '.'
                currentToken = lexicalAnalyser()
                if(currentToken[0] == "EOF"):                   # if we have the end of file, we read the next token but that is not really needed.
                    currentToken = lexicalAnalyser()
                else:
                    error(4,currentToken[1])
            else:
                error(3,currentToken[1])
        else:
            error(2,currentToken[1])
    else:
        error(1,currentToken[1])

# *Change from phase 1 = we call the programStatementBlock from on for the statements.
def programBlock(name):                                         # *Change for middleware* the programBlock now will have an argument -name- that will specify the unique ID of each block.
    global currentToken
    if(currentToken[0] == "leftCurlyBracketTOKEN"):             # if the next token is '{'
        currentToken = lexicalAnalyser()
        programDeclarations()
        programSubprograms()
        genQuad("begin_block",name,"_","_")                     # *Change for middleware* begining of program-block quad.             
        startingQuad = nextQuad()                               # *Change for symbol table* getting the nextQuad number in order to update the starting quad in our functions/procedures.
        programStatementBlock()
        if(currentToken[0] == "rightCurlyBracketTOKEN"):
            currentToken = lexicalAnalyser()
            if("main_" in name):                                # *Change for middleware* if we have the main program-block closing then add the halt quad.
                genQuad("halt","_","_","_")                     # *Change for middleware* end of program quad.
            genQuad("end_block",name,"_","_")                   # *Change for middelware* ending of program-block quad.
        else:
            error(6,currentToken[1])
    else:
        error(5,currentToken[1])
    return startingQuad                                         # *Change for symbol table* making a return here in order to get the starting quad's number for the updating of it in our functions/procedures.

def programDeclarations():
    global currentToken
    if(currentToken[0] == "declareTOKEN"):                      # if we have "declare".
        currentToken = lexicalAnalyser()
        variableList()
        if(currentToken[0] == "semicolonTOKEN"):                # if we have ; at the end.
            currentToken = lexicalAnalyser()
            programDeclarations()                               # recursion (in case we have more declarations)
        else:
            error(7,currentToken[1])
           
def variableList():
    global currentToken
    if(currentToken[0] == "identifierTOKEN"):                   # if we have an ID (identifier)
        insertEntity("variable",currentToken[1],None)           # *Change for symbol table* we insert a variable entity.
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "commaTOKEN"):                    # if we have a comma after the first variable.
            currentToken = lexicalAnalyser()       
            variableList()                                      # recursion
    else:
        error(8,currentToken[1])

def programSubprograms():
    global currentToken,currentScope,file
    # if we have a function or a procedure:
    if(currentToken[0] in ["functionTOKEN","procedureTOKEN"]):
        if(currentToken[0] == "functionTOKEN"):                 # *Change for symbol table* if we have function.
            type = "function"
        else:                                                   # *Change for symbol table* if we have procedure.
            type = "procedure"
        currentToken = lexicalAnalyser()        
        if(currentToken[0] == "identifierTOKEN"):               # if the next token is an identifier (ID)
            ID = currentToken[1]                                # *Change for middleware* getting the identifier token in order to call the programBlock.
            insertEntity(type,ID,None)                          # *Change for the symbol table* we insert the entity of function/procedure
            currentToken = lexicalAnalyser()
            if(currentToken[0] == "leftRoundBracketTOKEN"):     # if the next token is '('
                currentToken = lexicalAnalyser()
                createScope(ID)                                 # *Change for the symbol table* we create the function or procedure scope.
                formalParameterList(ID)                         # *Change for the symbol table* formal parameters need an argument now.
                if(currentToken[0] == "rightRoundBracketTOKEN"):    # if the next token is ')'
                    currentToken = lexicalAnalyser()
                    temp = programBlock(ID)                     # *Change for middleware* block with ID.
                    updateEntity(ID,"startingQuad",temp)        # *Change for the symbol table* we get the starting Quad of the function/procedure block. -> We do that here since the nextQuad will certainly be inside our function.
                    updateEntity(ID,"frameLength",currentScope.getOffset())    # *Change for symbol table* we update the frame length (adding to the last offset 4)
                    printTable(table_file)                      # *Change for symbol table* printing for results.
                    removeScope()                               # *Change for the symbol table* once we finish with the scope we remove it.
                    programSubprograms()                        # recursion in case we have multiple subprograms.
                else:
                    error(11,currentToken[1])
            else:
                error(10,currentToken[1])
        else:
            error(9,currentToken[1])

# *Change from phase 1 = fixed the function that used to print error for >2 
# args) using a while loop - we had forgotten to put recursion of some sort.
# *Change for symbol table* we added a name argument into formalParameterList
# in order to pass it through the items. This name is the function or procedure
# ID. We need it in order to seach for them and update them.
def formalParameterList(name):
    global currentToken
    formalParameterItem(name)                                   # *Change for symbol table* we added an argument in the method.
    while(currentToken[0] == "commaTOKEN"):
        currentToken = lexicalAnalyser()
        formalParameterItem(name)

# *Change for symbol table* we added a name argument. This name is the function 
# or procedure ID. We need it in order to seach for them and update them.
def formalParameterItem(name):
    global currentToken
    if(currentToken[0] in ["inTOKEN","inoutTOKEN"]):            # *Change for middleware* if we have in token.
        in_inout = currentToken[1]
        addFormalParameter(name,in_inout)                       # *Change for symbol table* add a formal parameter.
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "identifierTOKEN"):
            if(in_inout == "in"):
                insertEntity("formal",currentToken[1],"CV")     # *Change for symbol table* add entity if we have "in".
            else:
                insertEntity("formal",currentToken[1],"REF")    # *Change for symbol table* add entity if we have "inout"
            currentToken = lexicalAnalyser()
        else:
            error(14,currentToken[1])

def programStatementBlock():
    global currentToken
    statement()
    if(currentToken[0] == "semicolonTOKEN"):
        currentToken = lexicalAnalyser()
        programStatementBlock()

def statements():
    global currentToken
    if(currentToken[0] == "leftCurlyBracketTOKEN"):             # if we have '{' -> multiple statements.
        currentToken = lexicalAnalyser()
        statement()
        while(currentToken[0] == "semicolonTOKEN") or (currentToken[1] in keywords):
            if(currentToken[0]=="semicolonTOKEN"):    
                currentToken = lexicalAnalyser()
            statement()
        if(currentToken[0] == "rightCurlyBracketTOKEN"):        # if we have '}' -> end of statement block.
            currentToken = lexicalAnalyser()
        else:
            error(6,currentToken[1])
    else:                                                       # else if we only have 1 statement.
        statement() 
        if(currentToken[0] == "semicolonTOKEN"):
            currentToken = lexicalAnalyser()

def statement():
    global currentToken
        
    if(currentToken[0] == "identifierTOKEN"):                   # if we have ID token we can only go to assignment from here.
        previousToken = currentToken                            # *Change for middleware* we need to have the token before the := in order to make the assign quad.
        currentToken = lexicalAnalyser()
        assignStatement(previousToken)                          # *Change for middleware* we made assignStatement need an argument.
    elif(currentToken[0] == "ifTOKEN"):
        currentToken = lexicalAnalyser()
        ifStatement()
    elif(currentToken[0] == "whileTOKEN"):
        currentToken = lexicalAnalyser()
        whileStatement()
    elif(currentToken[0] == "switchcaseTOKEN"):
        currentToken = lexicalAnalyser()
        switchcaseStatement()
    elif(currentToken[0] == "forcaseTOKEN"):
        currentToken = lexicalAnalyser()
        forcaseStatement()
    elif(currentToken[0] == "incaseTOKEN"):
        currentToken = lexicalAnalyser()
        incaseStatement()
    elif(currentToken[0] == "callTOKEN"):
        currentToken = lexicalAnalyser()
        callStatement()
    elif(currentToken[0] == "returnTOKEN"):
        tokenDivider = currentToken[0]                          # *Change for middleware* we get the return token.
        currentToken = lexicalAnalyser()
        returnPrintStatement(tokenDivider)                      # *Change for middleware* we call returnPrintStatement with args.
    elif(currentToken[0] == "inputTOKEN"):
        currentToken = lexicalAnalyser()
        inputStatement()
    elif(currentToken[0] == "printTOKEN"):
        tokenDivider = currentToken[0]                          # *Change for middleware* we get the print token.
        currentToken = lexicalAnalyser()
        returnPrintStatement(tokenDivider)                      # *Change for middleware* we call returnPrintStatement with args.

# *Change for middleware* We made assignStatement have the previousToken 
# as an argument, in order to use it for the assignment quad.
def assignStatement(previousToken):                 
    global currentToken
    if(currentToken[0] == "assignmentTOKEN"):
        currentToken = lexicalAnalyser()
        expr = expression()  
        found = searchEntity(previousToken[1])                  # *Change for symbol table* searching to see if we need to insert the entity that is being assigned here.
        if(found == None):                                      # *Change for symbol table* if the entity is not found in our search - then we need to add it to the symbol table.
            insertEntity("variable",previousToken[1],None)      # *Change for symbol table* inserting the entity we were missing.
        genQuad(":=",expr,"_",previousToken[1])                 # *Change for middleware* assignment quad generation.
    else:
        error(15,currentToken[1])

def ifStatement():
    global currentToken
    cond = [[],[]]                                              # *Change for middleware* we define the condition variable as [[list for condition.true][list for condition.false]]
    if(currentToken[0] == "leftRoundBracketTOKEN"):
        currentToken = lexicalAnalyser()
        condition(cond)
        if(currentToken[0] == "rightRoundBracketTOKEN"):
            currentToken = lexicalAnalyser()
            backpatch(cond[0],nextQuad())                       # *Change for middleware* we backpatch for condition.true
            statements()
            ifList = makeList(nextQuad())                       # *Change for middleware* making a list for the else part. (condition.false)
            genQuad("jump","_","_","_")                         # *Change for middleware* generating the jumps.
            backpatch(cond[1],nextQuad())                       # *Change for middleware* we backpatch for condition.false
            elsePart()
            backpatch(ifList,nextQuad())                        # *Change for middleware* we backpatch for else part.
        else:
            error(11,currentToken[1])
    else:
        error(10,currentToken[1])

def elsePart():             
    global currentToken
    if(currentToken[0] == "elseTOKEN"):
        currentToken = lexicalAnalyser()
        statements()        

def whileStatement():
    global currentToken
    cond = [[],[]]                                              # *Change for middleware* we define the condition variable as [[list for condition.true][list for condition.false]]    
    conditionQuad = nextQuad()
    if(currentToken[0] == "leftRoundBracketTOKEN"):
        currentToken = lexicalAnalyser()
        condition(cond)
        if(currentToken[0] == "rightRoundBracketTOKEN"):
            currentToken = lexicalAnalyser()
            backpatch(cond[0],nextQuad())                       # *Change for middleware* we backpatch for condition.true
            statements()
            genQuad("jump","_","_",conditionQuad)               # *Change for middleware* generating the jumps.
            backpatch(cond[1],nextQuad())                       # *Change for middleware* we backpatch for condition.false        
        else:
            error(11,currentToken[1])
    else:
        error(10,currentToken[1])

# *Change for middleware* We had to separate the caseStatement into 
# forcaseStatement and switchcaseStatement due to differences of code in 
# the middleware phase (phase2).
def forcaseStatement():
    global currentToken
    cond = [[],[]]                                              # *Change for middleware* we define the condition variable as [[list for condition.true][list for condition.false]]
    if(currentToken[0] == "caseTOKEN"):
        currentToken = lexicalAnalyser()
        firstCondQuad = nextQuad()
        if(currentToken[0] == "leftRoundBracketTOKEN"): 
            currentToken = lexicalAnalyser()   
            condition(cond)
            if(currentToken[0] == "rightRoundBracketTOKEN"):
                currentToken = lexicalAnalyser()
                backpatch(cond[0],nextQuad())                   # *Change for middleware* we backpatch for condition.true
                statements()
                genQuad("jump","_","_",firstCondQuad)           # *Change for middleware* generating the jumps.
                backpatch(cond[1],nextQuad())                   # *Change for middleware* we backpatch for condition.false
                if(currentToken[0] in ["caseTOKEN","defaultTOKEN"]):
                    forcaseStatement()
            else:
                error(11,currentToken[1])
        else:
            error(10,currentToken[1])
    elif(currentToken[0] == "defaultTOKEN"):
        currentToken = lexicalAnalyser()
        statements()
    else:
        error(16,currentToken[1])

exitList = emptyList()                                          # *Change for middleware* we made exit list a global variable.
def switchcaseStatement():
    global currentToken,exitList
    cond = [[],[]]                                              # *Change for middleware* we define the condition variable as [[list for condition.true][list for condition.false]]
    if(currentToken[0] == "caseTOKEN"):
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "leftRoundBracketTOKEN"): 
            currentToken = lexicalAnalyser()
            condition(cond)
            if(currentToken[0] == "rightRoundBracketTOKEN"):
                currentToken = lexicalAnalyser()
                backpatch(cond[0],nextQuad())                   # *Change for middleware* we backpatch for condition.true
                statements()
                temp = makeList(nextQuad())                     # *Change for middleware* making a temporary list.
                genQuad("jump","_","_","_")                     # *Change for middleware* generating the jumps.
                exitList = mergeList(exitList,temp)             # *Change for middleware* exit list merge with temporary list.
                backpatch(cond[1],nextQuad())                   # *Change for middleware* we backpatch for condition.false
                if(currentToken[0] in ["caseTOKEN","defaultTOKEN"]):
                    switchcaseStatement()
            else:
                error(11,currentToken[1])
        else:
            error(10,currentToken[1])
    elif(currentToken[0] == "defaultTOKEN"):
        currentToken = lexicalAnalyser()
        statements()
        backpatch(exitList,nextQuad())                          # *Change for middleware* backpatching for the exit list.
        exitList = emptyList()                                  # *Change for middleware* emptying the exit list each time since its a global variable.
    else:
        error(16,currentToken[1])

def incaseStatement():
    global currentToken
    cond = [[],[]]                                              # *Change for middleware* we define the condition variable as [[list for condition.true][list for condition.false]]
    defaultDetector = 0                                         # *Change for middleware* this is a variable that detects if we have a default statement.
    flag = newTemp()                                            # *Change for middleware* our flag.
    firstCondQuad = nextQuad()                                  # *Change for middleware* our first condition quad number.
    while(currentToken[0] in ["caseTOKEN","defaultTOKEN"]):
        insertEntity("temporary",flag,None)
        genQuad(":=",0,"_",flag)                                # *Change for middleware* generating the quad for flag.
        if(currentToken[0] == "caseTOKEN"):
            currentToken = lexicalAnalyser()
            if(currentToken[0] == "leftRoundBracketTOKEN"):   
                currentToken = lexicalAnalyser() 
                condition(cond)
                if(currentToken[0] == "rightRoundBracketTOKEN"):
                    currentToken = lexicalAnalyser()
                    backpatch(cond[0],nextQuad())               # *Change for middleware* we backpatch for condition.true
                    statements()
                    backpatch(cond[1],nextQuad()+1)             # *Change for middleware* we backpatch for condition.false
                else:
                    error(11,currentToken[1])
            else:
                error(10,currentToken[1])
        elif(currentToken[0] == "defaultTOKEN"):
            defaultDetector = 1                                 # *Change for middleware* detector detects (1) the default-statement.
            genQuad(":=",1,flag,firstCondQuad)                  # *Change for middleware* generating the quad for flag for the default statement.
            currentToken = lexicalAnalyser()
            statements()
            flag = ""                                           # *Change for middleware* reseting the flag.
        else:
            error(16,currentToken[1])
    if(defaultDetector == 0):                                   # *Change for middleware* if we did not detect a default-statement.
        genQuad(":=",1,flag,firstCondQuad)                      # *Change for middleware* generating the quad for flag if we don't have a default statement.

def returnPrintStatement(tokenDivider):
    global currentToken
    if(currentToken[0] == "leftRoundBracketTOKEN"):
        currentToken = lexicalAnalyser()    
        expr = expression()
        if(currentToken[0] == "rightRoundBracketTOKEN"):
            if(tokenDivider == "returnTOKEN"):                  # *Change for middleware* if we have return.
                genQuad("ret",expr,"_","_")                     # *Change for middleware* generate the return quad.
            if(tokenDivider == "printTOKEN"):                   # *Change for middleware* if we have print.
                genQuad("out",expr,"_","_")                     # *Change for middleware* generate the print quad.
            currentToken = lexicalAnalyser()
        else:
            error(11,currentToken[1])
    else:
        error(10,currentToken[1])

def callStatement():
    global currentToken
    if(currentToken[0] == "identifierTOKEN"):
        ID = currentToken[1]                                    # *Change for middleware* getting the name of the function/procedure we want to call.
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "leftRoundBracketTOKEN"):  
            currentToken = lexicalAnalyser()
            actualParameterList()
            if(currentToken[0] == "rightRoundBracketTOKEN"):
                currentToken = lexicalAnalyser()
                genQuad("call",ID,"_","_")                      # *Change for middleware* generating call quad.
            else:
                error(11,currentToken[1])
        else:
            error(10,currentToken[1])
    else:
        error(17,currentToken[1])

def inputStatement():
    global currentToken
    if(currentToken[0] == "leftRoundBracketTOKEN"):    
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "identifierTOKEN"):
            ID = currentToken[1]                                # *Change for middleware* getting the ID we want to input.
            currentToken = lexicalAnalyser()
            if(currentToken[0] == "rightRoundBracketTOKEN"):
                genQuad("in",ID,"_","_")                        # *Change for middleware* generating the input quad.
                currentToken = lexicalAnalyser()
            else:
                error(11,currentToken[1])
        else:
            error(18,currentToken[1])
    else:
        error(10,currentToken[1])

# *Change from phase 1 = fixed the function that used to print error for >2 
# args) using a while loop - we had forgotten to put recursion of some sort.
def actualParameterList():
    global currentToken
    actualParameterItem()
    while(currentToken[0] == "commaTOKEN"):
        currentToken = lexicalAnalyser()
        actualParameterItem()

def actualParameterItem():
    global currentToken
    if(currentToken[0] == "inoutTOKEN"):
        currentToken = lexicalAnalyser()
        if(currentToken[0] == "identifierTOKEN"):
            genQuad("par",currentToken[1],"ref","_")            # *Change for middleware* generating the parameters' quads for inout.
            currentToken = lexicalAnalyser()
        else:
            error(14,currentToken[1])
    elif(currentToken[0] == "inTOKEN"):
        currentToken = lexicalAnalyser()
        expr = expression()
        genQuad("par",expr,"cv","_")                            # *Change for middleware* generating the parameters' quads for in.

# *Change for middleware* condition had to get an argument (conditionCondition), that will modify for later use.
def condition(conditionCondition):
    global currentToken
    cond1 = cond2 = [[],[]]                                     # *Change for middleware* cond1 and cond2 are of type conditionCondition.
    boolTerm(cond1)                                             # *Change for middleware* getting cond1 (boolTerm will change it accordingly)
    conditionCondition[0] = cond1[0]                            # *Change for middleware* condition.true = cond1.true
    conditionCondition[1] = cond1[1]                            # *Change for middleware* condition.false = cond1.false
    while(currentToken[0] == "orTOKEN"):
        currentToken = lexicalAnalyser()
        backpatch(conditionCondition[1],nextQuad())             # *Change for middleware* backpatching for condition.false
        boolTerm(cond2)                                         # *Change for middleware* getting cond2 (boolTerm will change it accordigly)
        conditionCondition[0] = mergeList(conditionCondition[0],cond2[0])   # *Change for middleware* condition.true = condition.true + cond2.true
        conditionCondition[1] = cond2[1]                        # *Change for middleware* condition.false = cond2.false

# *Change for middleware* condition had to get an argument (boolTermCondition), that it will modify for later use.
def boolTerm(boolTermCondition):
    global currentToken
    cond1 = cond2 = [[],[]]                                     # *Change for middleware* cond1 and cond2 are of type conditionCondition.
    boolFactor(cond1)                                           # *Change for middleware* getting cond1 (boolFactor will change it accordingly)
    boolTermCondition[0] = cond1[0]                             # *Change for middleware* condition.true = cond1.true
    boolTermCondition[1] = cond1[1]                             # *Change for middleware* condition.false = cond1.false
    while(currentToken[0] == "andTOKEN"):                       # -- and token will be the opposite of the or token.
        currentToken = lexicalAnalyser()
        backpatch(boolTermCondition[0],nextQuad())              # *Change for middleware* backpatching for condition.true
        boolFactor(cond2)                                       # *Change for middleware* getting cond2 (boolFactor will change it accordingly)
        boolTermCondition[0] = cond2[0]                         # *Change for middleware* condition.true = cond2.true
        boolTermCondition[1] = mergeList(boolTermCondition[1],cond2[1]) # *Change for middleware* condition.false = condition.false + cond2.false

# *Change for middleware* condition had to get an argument (boolFactorCondition), that it will modify for later use.
def boolFactor(boolFactorCondition):
    global currentToken
    cond = [[],[]]                                              # *Change for middleware* cond1 and cond2 are of type conditionCondition
    notDetector = 0                                             # *Change for middleware* this variable will detect if we have "not"
    # not detection
    if(currentToken[0] == "notTOKEN"):
        currentToken = lexicalAnalyser()
        notDetector = 1                                         # *Change for middleware* if we have "not" then detector variable = 1
    # box brackets
    if(currentToken[0] == "leftBoxBracketTOKEN"):
        currentToken = lexicalAnalyser()
        condition(cond)
        if(currentToken[0] == "rightBoxBracketTOKEN"):
            currentToken = lexicalAnalyser()
            if(notDetector == 0):                               # *Change for middleware* if we didn't have "not" (detector = 0)
                boolFactorCondition[0] = cond[0]                # *Change for middleware* condition.true = cond.true
                boolFactorCondition[1] = cond[1]                # *Change for middleware* condition.false = cond.false
            else:                                               # *Change for middleware* if we do have "not" (detector = 1) do the opposite.
                boolFactorCondition[0] = cond[1]                # *Change for middleware* condition.true = cond.false
                boolFactorCondition[1] = cond[0]                # *Change for middleware* condition.false = cond.true
        else:
            error(19,currentToken[1])
    else:
        expr1 = expression()
        if(currentToken[0] in ["equalTOKEN","smallerEqualTOKEN","largerEqualTOKEN","smallerTOKEN","largerTOKEN","differentTOKEN"]):
            relationalOperator = currentToken[1]                # *Change for middleware* getting the relational operator for the quad generation.
            currentToken = lexicalAnalyser()
            expr2 = expression()
            boolFactorCondition[0] = makeList(nextQuad())       # *Change for middleware* condition.true = [nextQuad]
            genQuad(relationalOperator,expr1,expr2,"_")         # *Change for middleware* generating the expressiong quad.
            boolFactorCondition[1] = makeList(nextQuad())       # *Change for middleware* condition.false = [nextQuad]
            genQuad("jump","_","_","_")                         # *Change for middleware* generating the jumps.
        else:
            error(13,currentToken[1])

def expression():
    global currentToken,currentScope
    optionalSign()
    term1 = term()
    while(currentToken[0] in ["addTOKEN","subTOKEN"]):
        relationalOperator = currentToken[1]                    # *Change for middleware* getting the relational operator.
        currentToken = lexicalAnalyser()
        term2 = term()
        temp = newTemp()                                        # *Change for middleware* generating a new temporary variable.
        found = searchEntity(temp)                              # *Change for symbol table* if the temporary variable we generated is found for the first time (found = None)
        if(found == None):
            insertEntity("temporary",temp,None)                 # *Change for symbole table* then insert it to the entity list. 
        genQuad(relationalOperator,term1,term2,temp)            # *Change for middleware* generating the expression quad.
        term1 = temp                                            # *Change for middleware* term1 = Eplace
    expressionPlace = term1                                     # *Change for middleware* Eplace = term1
    return expressionPlace                                      # *Change for middleware* now expression will return Eplace (expressionPlace).

def term():
    global currentToken
    factor1 = factor()                                          # *Change for middleware* we get the return valur of factor()
    while(currentToken[0] in ["mulTOKEN","divTOKEN"]):
        relationalOperator = currentToken[1]                    # *Change for middleware* we get the relational operator.
        currentToken = lexicalAnalyser()
        factor2 = factor()                                      # *Change for middlware* we get the return value of factor()
        temp = newTemp()                                        # *Change for middleware* generate new temporary variable.
        found = searchEntity(temp)                              # *Change for symbol table* if the temporary variable we generated is found for the first time (found = None)
        if(found == None):
            insertEntity("temporary",temp,None)                 # *Change for symbole table* then insert it to the entity list. 
        genQuad(relationalOperator,factor1,factor2,temp)        # *Change for middleware* generate quad with temporary variable.
        factor1 = temp                                          # *Change for middleware* factor1 = Fplace
    termPlace = factor1                                         # *Change for middleware* Fplace = factor1
    return termPlace                                            # *Change for middleware* now our function returns the T.place (termPlace)

def factor():
    global currentToken
    if(currentToken[0] == "numberTOKEN"):
        factorPlace = currentToken[1]                           # *Change for middleware* factor = number
        currentToken = lexicalAnalyser()  
    elif(currentToken[0] == "leftRoundBracketTOKEN"):
        currentToken = lexicalAnalyser()
        expr = expression()
        if(currentToken[0] == "rightRoundBracketTOKEN"):
            factorPlace = expr                                  # *Change for middleware* factor = expression
            currentToken = lexicalAnalyser()
        else:
            error(11,currentToken[1])
    elif(currentToken[0] == "identifierTOKEN"):
        ID = currentToken[1]
        currentToken = lexicalAnalyser()
        factorPlace = idTail(ID)                                # *Change for middleware* factor = idTail
    return factorPlace                                          # *Change for middleware* now our function returns the F.place (factorPlace)

# *Change for middleware* we added an argument in order to pass the ID through.
def idTail(name):
    global currentToken
    if(currentToken[0] == "leftRoundBracketTOKEN"):
        currentToken = lexicalAnalyser()
        actualParameterList()
        if(currentToken[0] == "rightRoundBracketTOKEN"):
            currentToken = lexicalAnalyser()
            temp = newTemp()                                    # *Change for middleware* generate a new temporary variable.
            insertEntity("temporary",temp,None)                 # *Change for symbol table* insert new temporary variable entity.
            genQuad("par",temp,"ret","_")                       # *Change for middleware* generate quad.
            genQuad("call",name,"_","_")                        # *Change for middleware* generate quad.
            return temp                                         # *Change for middleware* returning the temporary variable.
        else:
            error(11,currentToken[1])
    return name                                                 # *Change for middleware* we return the ID that we got, (it is of no actual use but we do it for comfort)

def optionalSign():
    global currentToken
    if(currentToken[0] == "addTOKEN") or (currentToken[0] == "subTOKEN"):
        currentToken = lexicalAnalyser()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Program Run

syntaxAnalyser()                                                # syntax analyser start.