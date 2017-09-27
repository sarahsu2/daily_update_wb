import copy

class Test(object):
    def CheckCode(self, inputString):
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
        wi = [1,3,9,27,19,26,16,17,20,29,25,13,8,24,10,30,28]
        cixwi = list(map(lambda x: x[0] * x[1], zip(wi, merged)))
        sumup = sum(cixwi[0:len(cixwi)])
        rest = 31 - sumup % 31
        if (rest >= 0 and rest <= 9):
            rest = rest
        elif(rest >= 10 and rest <= 17):
            rest = chr(rest+ 55)
        elif (rest >= 18 and rest <= 22):
            rest = chr(rest + 56)
        elif (rest >= 23 and rest <= 25):
            rest = chr(rest + 57)
        elif (rest >= 26 and rest <= 27):
            rest = chr(rest + 58)
        elif (rest >= 28 and rest <= 30):
            rest = chr(rest + 59)
        merged1 = copy.deepcopy(merged)
        merged1.append(rest)
        newmerged1 = ''.join(str(e) for e in merged1)

        print(newmerged1)

        # CheckCode2: make 7&8 digit 0&0
        merged2 = copy.deepcopy(merged)
        merged2[6:8] = [0,0]
        cixwi2 = list(map(lambda x: x[0] * x[1], zip(wi, merged2)))
        sumup2 = sum(cixwi2[0:len(cixwi2)])
        rest2 = 31 - sumup2 % 31
        if (rest2 >= 0 and rest2 <= 9):
            rest2 = rest2
        elif(rest2 >= 10 and rest2 <= 17):
            rest2 = chr(rest2 + 55)
        elif (rest2 >= 18 and rest2 <= 22):
            rest2 = chr(rest2 + 56)
        elif (rest2 >= 23 and rest2 <= 25):
            rest2 = chr(rest2 + 57)
        elif (rest2 >= 26 and rest2 <= 27):
            rest2 = chr(rest2 + 58)
        elif (rest2 >= 28 and rest2 <= 30):
            rest2 = chr(rest2 + 59)
        merged2.append(rest2)
        newmerged2 = ''.join(str(e) for e in merged2)

        print(newmerged2)

        return 0

if __name__ == '__main__':
    print (Test().CheckCode("140110051961485"))
