import re

class tokenization():
    def __init__(self,sourcecode):
        self.sourcecode = sourcecode
        self.tokens = self.maketokens()

    
    
    def maketokens(self):
        # all tokens will be kept here
        tokens = []
        self.lines= self.sourcecode.splitlines()
        for line in self.lines:
            tokens.append(self.breakline(line))
        return tokens
    def breakline(self, line):
        return line.split()
       

class parser(tokenization):
    def __init__(self,sourcecode):
        tokenization.__init__(self,sourcecode)
        self.initial = False
        self.run = False
        self.first_run =True
        self.redeclare = False
        self.id=False ##just to know if we have to check variable id or something else
        self.variable = False
        self.nopoint =False
        self.point= False #to keep track that variable is point or no point
        self.variables={}
        self.operators = ['==','<=','>=','<','>','!=']
        self.main()
                        
     
    def main(self):
        flag = True
        for self.line in range(len(self.tokens)):
            for token_num in range(len(self.tokens[self.line])):
                token = self.tokens[self.line][token_num]
                if(token_num == 0 and not self.run):
                    if(self.checkfirsttoken(token)):#first token is correct
                        continue
                    else:
                        self.raiseerror("expected a keyword [point,nopoint or run] or declared variable name")
                        flag = False
                        break
                if(self.id):
                # id is true means that the last keyword was a Datatype and the user is declaring variable
                    if(self.variabledeclaration(token)):
                        if(token_num==len(self.tokens[self.line])-1):
                            continue
                        else:
                            self.raiseerror("unexpected statement after the delimineter '!'")
                            flag=False
                            break
                    else:
                        # variable name not perfect
                        if(self.varnameerror):
                            flag=False
                            break
                        #this function return false in case of missing ! to check next token 
                        if(token_num==len(self.tokens[self.line])-1):
                            self.raiseerror("Missing delimeter '!' ") 
                            flag = False
                            break
                        else:
                            if(self.check_assignment_operator(self.tokens[self.line][token_num+1])):
                                self.initial = True
                                self.id = False
                                continue
                            elif(self.tokens[self.line][token_num+1]!="="):
                                self.raiseerror("Invalid Syntax") 
                                flag = False
                                break

                            else:

                                self.raiseerror("Invalid Syntax")
                                flag = False
                                break
                if(self.initial):
                    if(token=="="):
                        continue
                    else:
                        if(self.variableinitialization(token)):
                            self.initial=False
                            self.point = False
                            self.nopoint = False
                            if(token_num==len(self.tokens[self.line])-1):
                                continue
                            else:
                                self.raiseerror("unexpected statement after the delimineter '!'")
                                flag = False
                                break
                             
                        else:
                            flag = False
                            break

                if(self.run):
                    if(self.first_run):
                        if (self.run_first_line(self.tokens[self.line])):
                            self.first_run=False
                            break

                        else:
                            flag = False
                            break
                    else:
                        if (len(self.tokens[self.line])!=1):
                            self.first_run = True
                            self.run= False
                            self.raiseerror("Expected a closing paranthesis }")
                            flag = False
                            break
                        else:
                            if(self.tokens[self.line][0]=='}'):
                                self.first = True
                                self.run= False
                                continue
                            else:
                                self.run= False
                                self.first = True
                                self.raiseerror("Expected a closing paranthesis }")
                                flag = False
                                break

            if(flag):
                print("Line ",self.line+1,"is valid")
                
    
    def checkfirsttoken(self,token):
        if(self.run):
           pass
        else:
            if(self.alreadyvar(token)):
                self.initial=True
                if(self.variables[token]=="point"):
                    self.point=True
                else:
                    self.nopoint=True
                return True

            elif(token=='point'):
                self.id=True    
                self.point=True
                return True
            elif(token=='nopoint'):
                self.id=True
                self.nopoint=True
                return True
            elif(token=='run'):
                self.run = True
                return True
        return False
    
    def keywordcheck(self,token):
        if(token=='point'):
           return True
        elif(token=='nopoint'):
            return True
        elif(token=='run'):
            return True
        else:
            return False

    def alreadyvar(self,token):
        if token in self.variables:
            return True
        else:
            return False
        

    def variabledeclaration(self,token):
        self.varnameerror= False
        # now we are excepting a variable id token like *abd*! but *abd* is also valid in the case of = together 
        if(self.checkvariableid(token)):
                if(self.checkdeliminter(token)):
                    self.updatevarlist(token[:-1])
                    self.id=False
                    self.point=False
                    self.nopoint=False
                    return True
                else:
                    # no delimeter at the end means there are two cases 
                    # 1 syntax error, user forget the !
                    # 2 user is initializer and declarating variable together
                    return False
        else:
            # returning false beacuase the varibale name is not a perfect name, not following rule or maybe a keyword or redeclaration
            self.varnameerror=True
            return False

    def updatevarlist(self,varname):
        if(self.point):
           self.variables[varname]="point"
        elif(self.nopoint):
           self.variables[varname]="nopoint"

    def check_assignment_operator(self,token):
           if(token=="="):
               return True
           return False
    
    def checkdeliminter(self,token):
        if(token[-1]=='!'):
            return True
        return False
 
    def variableinitialization(self,token):
        if(self.point):
            pattren = r"[+-]?[0-9]+\.[0-9]+"
        elif(self.nopoint):
            pattren = r"^[-+]?[0-9]+$"
        newtoken = token
        if(token[-1]=="!"):
            newtoken = token[:-1]
        if(re.match(pattren,newtoken)):
            if(self.checkdeliminter(token)):
                return True
            else:
                self.raiseerror("Missing delimeter '!'")
                return False
        else:
            if(self.point):
                self.raiseerror("Invalid number! Type point expected a floating number")
            elif(self.nopoint):
                self.raiseerror("Invalid number! Type nopoint expected a integer number")
            return False
    
    def checkvariableid(self,token):
        if(token[-1]=='!'):
            token = token[:-1] 
        id = r"[*][\w\d]+[*]"
        if(re.match(id,token)):
            if(self.keywordcheck(token[1:len(token)-1])):
                self.raiseerror("varible name cannot be a keyword")
                return False
            else:
                if(self.alreadyvar(token)):
                    self.redeclare= True
                    self.raiseerror("Redeclaration of variable is not allowed")
                    return False
                else:
                    return True   
        else:
            self.raiseerror("varible name rules are not followed")
            return False
        

    def raiseerror(self,errormessage):
       print("Error at line ",self.line+1,self.lines[self.line],'\n',errormessage)
 
                        
    def integer(self,number):
        if(re.match(r"^[-+]?[0-9]+$",number)):
            return True 
        else:
            return False
        

    def run_first_line(self,line):
            
            for i in range(len(line)):
        
                if(len(line)>13):
                    self.raiseerror("Invalid syntax")
                    return False
                
                if(i==0) :
                    continue

                if(i==1) :
                        if(line[i]=='[('):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Maybe imbalance paranthesis")
                            return False
                elif(i==2) :
                        if(self.checkvariableid(line[i])):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Wrong variable name is used")
                            return False
                elif(i==3) :
                        if(line[i]=='='):
                            continue
                        else:
                            self.raiseerror("Invalid syntax! may be expected a assignment operator ")
                            return False
                elif(i==4)  :
                        if(self.integer(line[i])):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Expexted an integer number")
                            return False

                elif(i==5) :
                        if(line[i]==')('):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Maybe imbalance paranthesis")
                            return False
                    
                elif(i==6) :
                        if(line[i]==line[2]):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Maybe wrong variable is refrenced")
                            return False
                    
                elif(i==7):
                        flag=False
                        for op in self.operators:    
                            if(line[i]==op):
                                flag= True
                                break
                        if(flag):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! may be expected a conditional operator")
                            return False 
                    
                elif(i==8):
                        if(self.integer(line[i])):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Expexted an integer number")
                            return False 
                    
                    
                elif(i==9): 
                        if(line[i]==')('):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Maybe imbalance paranthesis")
                            return False 
                    
                elif(i==10) :
                        if(line[i][:-2]==line[2]) and (line[i][-2:]=="++" or line[i][-2:]=="--" ):
                            continue
                        
                        else:
                            self.raiseerror("Invalid sytax! Increment operator was expected")
                            return False 
                

                elif(i==11) :
                        if(line[i]==')]'):
                            continue
                        else:
                            self.raiseerror("Invalid sytax! Maybe imbalance paranthesis")
                            return False 
                elif(i==12) :
                        if(line[i]=='{'):
                            return True
                        else:
                            self.raiseerror("Invalid sytax! Maybe expecting opening paranthesis {")
                            return False 
