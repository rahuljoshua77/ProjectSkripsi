# FEATURES:
# 1. open files
# 2. plot many files in a figure 
# 3. on/off pick line
# 4. Saving time domain data

import csv
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from numpy.fft import ifft, fft
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

Tk().withdraw() # removing main window
filenames = askopenfilenames() # Open files

# time domain function
def time_domain(path):
    S21_stored = []
    Sfft = []
    lines = []
    header = ['Time (ns)', 'Amplitude (V)']
    # plt.figure(figsize=(10,6), dpi=100)
    fig, ax = plt.subplots()

    for filename in path: # read every file on the list
        try:
            with open(filename, 'r') as csv_file:
                # read CSV file
                csv_reader = csv.reader(csv_file, dialect='excel', delimiter=",", quoting=csv.QUOTE_MINIMAL)
                # read the row data and index
                for index, row in enumerate(csv_reader):
                    if index >= 12 and row != None:
                        # fetch row data (real & imajiner) 
                        S21 = complex(float(row[2]), float(row[3]))
                        # save data to variabel S21_stored <class 'list'>
                        S21_stored.append(S21)
            # assign value to variable
            Nfft = 2048
            N = len(S21_stored)
            n = 1
            # value of variabel Sfft indeks ke-0 = 0
            Sfft.insert(0,0)
            # print(Sfft)
            # move data Sfft <- S21_stored
            Sfft[n:N] = S21_stored[n:N]
            # print()
            # print(len(Sfft))
            # Nilai variabel Sfft indeks N sampai Nfft-N-n-1 = 0
            for index2 in range(N, Nfft-N-n-1):
                Sfft.insert(index2, 0)
            # print(len(Sfft))
            # change the data type (list -> numpy.array)
            S21_arr = np.array(S21_stored)
            # assign conjugate value of the invers data S21_arr to sfft variable indexed 
            Sfft[Nfft-N-n+1:Nfft-n] = np.conj(S21_arr[N::-1])
            # print(Sfft)
            # IFFT process and saving real number to St111 variable
            # St111 = np.real(ifft(Sfft))

            # ---FILTER----
            fmin = 1000
            fmax = 10000
            deltaf = (fmax-fmin)/Nfft
            fm = N*deltaf/2
            fs = 2*fm*1e6
            t = np.arange(0, (1/fs)*Nfft, 1/fs)
            t = t - 68.5*1e-09 * np.ones(len(t))
            tt = t*t
            a = 18.*1e-09
            x = (-1/(a*np.sqrt(2*np.pi)))*(1/a**2)*t*np.exp(-tt/(2*a**2))
            x = x / np.max(x)

            # Fast fourier transform (FFT)
            xf = fft(x)
            # list to numpy.array
            Sfft_arr = np.array(Sfft)
            sttr = Sfft_arr * xf[0:Nfft-2]
            # print(np.shape(Sfft_arr))
            # print(np.shape(xf[0:Nfft-2]))
            
            # IFFT process and saving the real number to Sr111 variable => Amplitude (y-axis)
            sr111 = np.real(ifft(sttr))

            # create value range of time domain (x-axis)
            M = (1/3e8) / 553
            m = np.arange(0, 2047-1) * M

            # Get Filename as a label of line
            count = 0
            for element in filename:
                if element == '/':
                    count += 1
            label = filename.split('/')[count].split('.')[0]

            # SAVING DATA
            # csv_data = zip(m, sr111)
            # csv_list = list(csv_data)
            # csv_filename = label + '_extracted.csv'
            # with open(csv_filename, 'w') as csv_save:
            #     csv_writer = csv.writer(csv_save)
            #     csv_writer.writerow(header)
            #     csv_writer.writerows(csv_list)

            # ---PLOT---
            plt.title("Time Domain")
            plt.ylabel('Amplitudo (V)')
            plt.xlabel("Time (ns)")

            # hide and appear line 
            line, = ax.plot(m, sr111, label=label)
            lines.append(line)
            leg = ax.legend(loc='upper right')
            leg.get_frame().set_alpha(0.4)
            lined = dict()
            for legline, origline in zip(leg.get_lines(), lines):
                legline.set_picker(5)  # 5 pts tolerance
                lined[legline] = origline
            mplcursors.cursor() # add anotation of the line

            # remove content 
            S21_stored.clear() 
            Sfft.clear()
            
        except Exception as err:
            print(f'{err.__class__} = {err}')

    def onpick(event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        legline = event.artist
        origline = lined[legline]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            legline.set_alpha(1.0)
        else:
            legline.set_alpha(0.2)
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', onpick)

    return plt.show()

time_domain(filenames)