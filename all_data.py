import os
import pandas as pd
import xlsxwriter, re
import numpy as np

#locate your folder excel
files = os.listdir('C:/Users/User/Downloads/INSINAS/DATA/Time Domain/')  

#make array for store the data frame


#define antenna kuadran
number_data = 1
insert_data = [{'Amplitude (V)': number_data}]
#location = ['x=-8,y=-7,z=4.83','x=0,y=-7,z=4.83','x=0,y=2,z=4.83','x=-8,y=1,z=4.83']
loc_x= ['8','0','0','8']
loc_y= ['7','7','2','1']
loc_z= ['4.83','4.83','4.83','4.83']
validator = []
#looping file for open one by one


data = [loc_x, loc_y, loc_z]
  
for idx_data in range(0,len(data)):
    idx_loc = 0
    li = []
    for i in range(0,len(files)):
        
        #condition to except this file because raise error
        if "~$" in files[i]:
            pass
        else:
            print(files[i])
            #find the antenna number from the first name files
            idx = re.findall(r'\b\d+\b', str(files[i]))
            
            if i % 5 == 0:
                idx_loc = idx_loc + 1
            
            # minus 1 because 0 % 5 = 5
            try:
                insert_data_loc = [{'Amplitude (V)': int(data[idx_data][idx_loc-1])}]
            except:
                insert_data_loc = [{'Amplitude (V)': float(data[idx_data][idx_loc-1])}]
            print(data[idx_data][idx_loc-1])
            
            #insert row pandas
            insert_data_kuadran = [{'Amplitude (V)': " "}]
            
            #read data frame
            df = pd.read_excel(f"E:/INSINAS - Copy/DATA/Time Domain/{files[i]}",engine='openpyxl') 
            print(df)

            #concat the idx to data frame
            df = pd.concat([pd.DataFrame(insert_data_kuadran), pd.DataFrame(insert_data_loc), df], ignore_index=True)
            df = df['Amplitude (V)']
        
            print(df)
            
            #store data frame to array li
            li.append(df)
            print(f"Done {files[i]}")

    #concat all dataframe with axis 1 = vertikal
    frame = pd.concat(li, axis=1, ignore_index=True)
    data_fix = frame.apply(np.roll, shift = 2046)
    print(data_fix.apply(np.roll, shift = 2046))
    #create xlsx file
    # writer = pd.ExcelWriter(f'amplitude_{data[idx_data]}.xlsx', engine='xlsxwriter')

    # #write excel
    # data_fix.to_excel(writer, sheet_name=f'Sheet1', index=False, header = False)

    # #save
    # writer.save()

    print("Done Save!")