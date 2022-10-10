from sys import argv
import sys

variable_dict = {}
counter = 0
free_var = 0
list_of_text = []

with open(sys.argv[1], "r") as f:
    if sys.argv[1].endswith(".hay"):
        list_of_lines = [row.strip() for row in f.readlines()]

        for row in list_of_lines:
            if row != "":
                list_of_text.append(row)
    else:
        raise FileNotFoundError("File must have .hay extension")


    
    def Counter(txt, counter):
        """This Function is cheking count of 'if', 'while', 'for' and '!'. They must be equal:"""   

        for line in txt:
            if "if" in line:
                counter += 1
                
            if "while" in line:
                counter += 1
                
            if "for" in line:
                counter += 1

            elif "!" in line:
                counter -= 1

        if counter != 0:
            raise SyntaxError("Number of 'if, while,for' and '!' must be equal:")


    def printing(txt, row, idx):
        if "print" in txt[idx] and free_var <= len(txt):
            row = ' '.join(list(txt[idx]))
            if row[5] != "[" and row[-1] != "]":
                raise SyntaxError("After print you must start with '[' and finish with']'")

            row = (list_of_text[idx].split("print["))[1].split("]")[0].split(" ")

            for ind in range(len(row)):        
                if row[ind] in variable_dict:
                    row[ind] = str(variable_dict[row[ind]])
            try:
                print(eval(' '.join(row))) 
            except:
                print(" ".join(row))       


    def VariableAfterDeclaring(arg, idx):
        arg = list_of_text[idx].split()
        if arg[0] in variable_dict and arg[1] == ":=":
            for i in range(2, len(arg)):
                if arg[i] in variable_dict:
                    arg[i] = str(variable_dict[arg[i]])
            variable_dict[arg[0]] = eval(" ".join(arg[2:]))


    def alreadyDeclared(row, idx):
        "This function is cheking, that declared variables were been declared. "
        
        row = list_of_text[idx].split()
        if row[1] in variable_dict:
            row[1] = variable_dict[row[1]] 


    def CreatingVariable(arg):
        """This function assign value in variable."""

        for i in range(3, len(arg)):
            if arg[i] in variable_dict:
                arg[i] = str(variable_dict[arg[i]])
        variable_dict[arg[1]] = eval(" ".join(arg[3:]))


    def variableName(row):
        """This function is cheking or does it starts with ascii letter?"""

        if not row[1][0].isalpha():
            raise SyntaxError("Variables must start with ascii letter.")


    def variableValue(row):
        for i in range(len(row)):
            if row[i] in variable_dict:
                row[i] = str(variable_dict[row[i]])
        

    def isDeclared(row, idx):
        row = list_of_text[idx].split()
        for i in range(5):
            if row[0] in variable_dict or ["if", "while", "print", "var", "!"][i] in row[0]:
                return True
        
        raise NameError(f"Name ({str(row[0])})' is unrecognizable.")                  


    def untill_if_while_for(ind):
        """This function do file line by line untill will reach a line that starts with 'if'"""

        while ind != len(list_of_text):
            if "if" in list_of_text[ind] or  "while" in list_of_text[ind] or "for" in list_of_text[ind]:
                break

            splitted_row = list_of_text[ind].split()

            if "var" in list_of_text[ind]:
                variableName(splitted_row)
                alreadyDeclared(splitted_row, ind)
                CreatingVariable(splitted_row)

            VariableAfterDeclaring(splitted_row, ind)
            isDeclared(splitted_row, ind)        
            printing(list_of_text, splitted_row, ind)

            ind += 1


    def afterIf(idx):
        """This function is checking, or does it  ends with '!'"""

        if "!" not in list_of_text[idx:]:
            raise SyntaxError("After if you mast end with !") 


    def have_if():
        """This function do file line by line when reach a line that starts 'if'
         and will do untill will reach line that ends with '!''"""

        ind = 0

        while ind != len(list_of_text):
            if "if" in list_of_text[ind]:
                splitted_row = list_of_text[ind].split()
                afterIf(ind)
                variableValue(splitted_row)         
                            
                if eval(' '.join(splitted_row[1:])):
                    while list_of_text[ind] != "!":
                        if "var" in list_of_text[ind]:
                            splitted_row = list_of_text[ind].split()
                            variableName(splitted_row) 
                            alreadyDeclared(splitted_row, ind)
                            CreatingVariable(splitted_row)  

                        VariableAfterDeclaring(splitted_row, ind)
                        isDeclared(splitted_row, ind)     
                        printing(list_of_text, splitted_row, ind)
                    
                        ind += 1

                    if ind != len(list_of_text):
                        untill_if_while_for(ind)   

                else:
                    while "!" not in list_of_text[ind]:
                        ind += 1
                    untill_if_while_for(ind)
            ind += 1
    
     
    def afterwhile(idx):
        """This function is checking, or does While ends with '!'"""

        if "!" not in list_of_text[idx:]:
            raise SyntaxError("After While you mast end with !") 
        

    def have_while():
        """This function do file line by line when reach a line that starts 'while'
         and will do untill will reach line that ends with '!''"""

        ind = 0

        while ind != len(list_of_text):
            if "while" in list_of_text[ind]:
                splitted_row = list_of_text[ind].split()
                afterwhile(ind)
                variableValue(splitted_row) 
                            
                if eval(' '.join(splitted_row[1:])):
                    while list_of_text[ind] != "!":
                            if "var" in list_of_text[ind]:
                                splitted_row = list_of_text[ind].split()
                                variableName(splitted_row) 
                                alreadyDeclared(splitted_row, ind)
                                CreatingVariable(splitted_row)  

                            VariableAfterDeclaring(splitted_row, ind)
                            isDeclared(splitted_row, ind)     
                            printing(list_of_text, splitted_row, ind)
                        
                            ind += 1

                    if ind != len(list_of_text):
                        untill_if_while_for(ind)   

                else:
                    while "!" not in list_of_text[ind]:
                        ind += 1
                    untill_if_while_for(ind)

            ind += 1


    def do_while():
        ind = 0 
        for ind in range(len(list_of_text)):
            if 'while' in list_of_text[ind]:
                splitted_row = list_of_text[ind].split()
                while variable_dict[splitted_row[1]] < int(splitted_row[-1]):
                        have_while()

    
    def Counter_from_to(txt, counter):
        """This Function is cheking count of 'from' and 'to'. They must be equal:"""   
        ind = 0

        while ind != len(txt):
            if "for" in txt[ind]:
                splitted_row = list_of_text[ind].split()
                for line in splitted_row:
                    if "from" in line:
                        counter += 1

                    elif "to" in line:
                        counter -= 1
            ind += 1

        if counter != 0:
            raise SyntaxError("Number of 'from' and 'to' must be equal:")

    
    def CreatingVariable_for(arg):
        """This function assign value in variable."""

        for i in range(3, len(arg)):
            if arg[i] in variable_dict:
                arg[i] = str(variable_dict[arg[i]])
        variable_dict[arg[1]] = eval(" ".join(arg[3]))

    
    def VariableAfterDeclaring_for(arg, idx):
        arg = list_of_text[idx].split()
        if arg[0] in variable_dict and arg[1] == "from":
            for i in range(2, len(arg)):
                if arg[i] in variable_dict:
                    arg[i] = str(variable_dict[arg[i]])
            variable_dict[arg[0]] = eval(" ".join(arg[2:]))
    

    def isDeclared_for(row, idx):
        row = list_of_text[idx].split()
        for i in range(5):
            if row[0] in variable_dict or ["for", "!"][i] in row[0]:
                return True
        
        raise NameError(f"Name ({str(row[0])})' is unrecognizable.") 


    def afterfor(idx):
        """This function is checking, or does FOR ends with '!'"""

        if "!" not in list_of_text[idx:]:
            raise SyntaxError("After FOR you mast end with !") 


    def alreadyDeclared_for(row, idx):
        "This function is cheking, that declared variables were been declared. "
        
        row = list_of_text[idx].split()
        if row[1] in variable_dict:
            variable_dict[row[1]] = variable_dict[row[1]] + 1  


    
    def for_in_dict():
        """This function do file line by line when reach a line that starts 'for'
         and will do untill will reach line that ends with '!' and adds the variable 
         declared in that line to our total dict'"""

        ind = 0

        while ind != len(list_of_text):
            if "for" in list_of_text[ind]:
                splitted_row = list_of_text[ind].split()
                splitted_row_1 = splitted_row[1:]

                if "var" in splitted_row_1:
                    CreatingVariable_for(splitted_row_1)
                    variableName(splitted_row_1)
                    VariableAfterDeclaring_for(splitted_row_1, ind) 
                    alreadyDeclared_for(splitted_row_1, ind)
                    afterfor(ind)
            
            ind += 1


    def have_for():
        ind = 0
        for_in_dict()
        while ind != len(list_of_text):
            
            if "for" in list_of_text[ind]:
                splitted_row = list_of_text[ind].split()
                splitted_row_1 = splitted_row[1:]

                afterwhile(ind)
                variableValue(splitted_row) 
                            
                if int(splitted_row[2]) < int(splitted_row[-1]):
                    while list_of_text[ind] != "!":   
                            printing(list_of_text, splitted_row, ind)
                        
                            ind += 1

                    if ind != len(list_of_text):
                        untill_if_while_for(ind)   

                else:
                    while "!" not in list_of_text[ind]:
                        ind += 1
                    untill_if_while_for(ind)

            ind += 1


    #def do_for():
        #ind = 0
        #for ind in range(len(list_of_text)):
        #while ind != len(list_of_text):
            #if "for" in list_of_text[ind]:
                #splitted_row = list_of_text[ind].split()
                #have_for()
  
            # ind += 1

    
    Counter(list_of_text, counter)
    Counter_from_to(list_of_text, counter)
    untill_if_while_for(free_var)                        
    have_if()
    do_while()
    have_for()
    print(variable_dict)             