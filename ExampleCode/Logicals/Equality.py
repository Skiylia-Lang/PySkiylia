#Test the equality operator
print(True == True)         #True
print(True == False)        #False
print(False == True)        #False
print(False == False)       #True

print(True == 1)            #True
print(False == 0)           #True
print(True == "True")       #False
print(False == "False")     #False
print(False == "")          #False

print(True != True)         #False
print(True != False)        #True
print(False != True)        #True
print(False != False)       #False

print(True != 1)            #False
print(False != 0)           #False
print(True != "True")       #True
print(False != "False")     #True
print(False != "")          #True
