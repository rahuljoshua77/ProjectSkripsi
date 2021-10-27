import os
import pandas as pd
import xlsxwriter, re
import numpy as np

#locate your folder excel
files = os.listdir('C:/Users/User/Downloads/INSINAS/DATA/Time Domain/')  

#make array for store the data frame
li = []

#define antenna kuadran
number_data = 1
insert_data = [{'Amplitude (V)': number_data}]
 
#looping file for open one by one
for file in files:
    
    #condition to except this file because raise error
    if "~$" in file:
        pass
    else:
        print(file)
        #find the antenna number from the first name files
        idx = re.findall(r'\b\d+\b', str(file))
        #insert row pandas
        insert_data = [{'Amplitude (V)': int(idx[0])}]

        #read data frame
        df = pd.read_excel(f"E:/INSINAS - Copy/DATA/Time Domain/{file}",engine='openpyxl') 
        print(df)

        #concat the idx to data frame
        df = pd.concat([pd.DataFrame(insert_data), df], ignore_index=True)
        df = df['Amplitude (V)']
    
        print(df)
        
        #store data frame to array li
        li.append(df)
        print(f"Done {file}")

#concat all dataframe with axis 1 = vertikal
frame = pd.concat(li, axis=1, ignore_index=True)
frame = frame.apply(np.roll, shift = 2046)
# print(frame.apply(np.roll, shift = 2046))
#create xlsx file
writer = pd.ExcelWriter('amplitude.xlsx', engine='xlsxwriter')

#write excel
frame.to_excel(writer, sheet_name=f'Sheet1', index=False, header = False)

#save
writer.save()
print("Done Save!")