import copy

class Test(object):
    def back2origin(self, inputlist):
        for i in range(0,len(inputlist),1):
            if (inputlist[i] >= 0 and inputlist[i] <= 9):
                inputlist[i] = inputlist[i]
            elif(inputlist[i] >= 10 and inputlist[i] <= 17):
                inputlist[i] = chr(inputlist[i] + 55)
            elif (inputlist[i] >= 18 and inputlist[i] <= 22):
                inputlist[i] = chr(inputlist[i] + 56)
            elif (inputlist[i] >= 23 and inputlist[i] <= 25):
                inputlist[i] = chr(inputlist[i] + 57)
            elif (inputlist[i] >= 26 and inputlist[i] <= 27):
                inputlist[i] = chr(inputlist[i] + 58)
            elif (inputlist[i] >= 28 and inputlist[i] <= 30):
                inputlist[i] = chr(inputlist[i] + 59)
        return inputlist

    # inputString is 15 digit, mode 1 is nonZero, mode 2 sets digit 7&8 Zero
    def CheckCode(self, inputString, mode):
        # throw input error if inputString is not 15 digits
        # throw input error if inputString includes non number or capital letter digits

        inputList = list(inputString)
        head = ['9','1']
        merged = head + inputList
        for i in range(0,17,1):
            if (ord(merged[i]) >= 48 and ord(merged[i]) <= 57):
                merged[i] = ord(merged[i]) - 48
            elif (ord(merged[i]) >= 65 and ord(merged[i]) <= 72):
                merged[i] = ord(merged[i]) - 55
            elif (ord(merged[i]) >= 74 and ord(merged[i]) <= 78):
                merged[i] = ord(merged[i]) - 56
            elif (ord(merged[i]) >= 80 and ord(merged[i]) <= 82):
                merged[i] = ord(merged[i]) - 57
            elif (ord(merged[i]) >= 84 and ord(merged[i]) <= 85 ):
                merged[i] = ord(merged[i]) - 58
            elif (ord(merged[i]) >= 87 and ord(merged[i]) <= 89 ):
                merged[i] = ord(merged[i]) - 59
            # elif other letter throw input error
        # print("merged", merged)
        wi = [1,3,9,27,19,26,16,17,20,29,25,13,8,24,10,30,28]

        if mode == 1:
            # CheckCode1: use origin code
            cixwi = list(map(lambda x: x[0] * x[1], zip(wi, merged)))
            sumup = sum(cixwi[0:len(cixwi)])
            rest = 31 - sumup % 31
            merged1 = copy.deepcopy(merged)
            merged1.append(rest)
            # print("merged1", merged1)
            self.back2origin(merged1)
            newmerged1 = ''.join(str(e) for e in merged1)
            # print("newmerged1", newmerged1)
            return newmerged1

        elif mode == 2:
            merged2 = copy.deepcopy(merged)
            # if ZhiXiaShi
            # CheckCode2: make 678 digit 000
            if merged2[2:5] == [1,1,0] or merged2[2:5] == [1,2,0] or merged2[2:5] == [3,1,0] or merged2[2:5] == [5,0,0]:
                merged2[5:8] = [0,0,0]

            # if not ZhiXiaShi
            # CheckCode2: make 78 digit 00
            else:
                merged2[6:8] = [0,0]

            cixwi2 = list(map(lambda x: x[0] * x[1], zip(wi, merged2)))
            sumup2 = sum(cixwi2[0:len(cixwi2)])
            rest2 = 31 - sumup2 % 31
            merged2.append(rest2)
            # print("merged2", merged2)
            self.back2origin(merged2)
            newmerged2 = ''.join(str(e) for e in merged2)
            # print("newmerged2", newmerged2)
            return newmerged2

# if __name__ == '__main__':
#     print (Test().CheckCode("22012266874988X", 1))
#     print (Test().CheckCode("L11010210110532", 1))
#     print (Test().CheckCode("110100625906144",2))
