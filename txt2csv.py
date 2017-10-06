import pandas as pd

df = pd.DataFrame([],columns = ["taxPersonCode","companyName","unifiedCreditCodeZero","unifiedCreditCodeNotZero"])

with open("/Users/xuyujie/Desktop/taxdata.txt","r",encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    # print("read done")
    data = ''.join(lines).replace("/n"," ")
    # print("join done")
    splitdata = data.splitlines()
    # print("split done")
    for i in range(len(splitdata)//4):
        df.loc[i] = {"taxPersonCode":splitdata[4*i+0], "companyName":splitdata[4*i+1], "unifiedCreditCodeZero":splitdata[4*i+2],"unifiedCreditCodeNotZero":splitdata[4*i+3]}
        print(i)
    print("to csv done")
    df.to_csv("ori2.csv")
