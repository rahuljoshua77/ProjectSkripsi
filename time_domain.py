import csv
import numpy as np
import matplotlib.pyplot as plt
import mplcursors
from numpy.fft import ifft, fft
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

Tk().withdraw() # Menghilangkan window utama
filenames = askopenfilenames() # Open files

# Fungsi time domain
def time_domain(path):
    S21_stored = []
    Sfft = []
    label_list = []
    plt.figure(figsize=(10,6), dpi=100)

    for filename in path: # Membaca setiap file didalam list
        try:
            with open(filename, 'r') as csv_file:
                # Membaca file CSV
                csv_reader = csv.reader(csv_file)
                # Looping untuk membaca row data dan indeks
                for index, row in enumerate(csv_reader):
                    if index >= 12 and row != None:
                        # Mengambil row data (real & imajiner) 
                        S21 = complex(float(row[2]), float(row[3]))
                        # Simpan data ke variabel S21_stored <class 'list'>
                        S21_stored.append(S21)
            # assign nilai ke variabel
            Nfft = 2048
            N = len(S21_stored)
            n = 1
            # nilai variabel Sfft indeks ke-0 = 0
            Sfft.insert(0,0)
            # print(Sfft)
            # Memindahkan data Sfft <- S21_stored
            Sfft[n:N] = S21_stored[n:N]
            # print()
            # print(len(Sfft))
            # Nilai variabel Sfft indeks N sampai Nfft-N-n-1 = 0
            for index2 in range(N, Nfft-N-n-1):
                Sfft.insert(index2, 0)
            # print(len(Sfft))
            # Mengubah tipe data list -> numpy.array
            S21_arr = np.array(S21_stored)
            # Memasukkan nilai Konjugasi invers data S21_arr ke variabel Sfft terindeks 
            Sfft[Nfft-N-n+1:Nfft-n] = np.conj(S21_arr[N::-1])
            # print(Sfft)
            # Proses invers fourier transform (IFFT) dan menyimpan bil. real ke variabel St111
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
            
            
            # Proses invers fourier transform (IFFT) dan menyimpan bil. real ke variabel Sr111 => Amplitudo (y-axis)
            sr111 = np.real(ifft(sttr))

            # Membuat range nilai domain waktu (x-axis)
            M = (1/3e8) / 553
            m = np.arange(0, 2047-1) * M

            # Get Filename as a label of line
            count = 0
            for element in filename:
                if element == '/':
                    count += 1
            label = filename.split('/')[count].split('.')[0]
            label_list.append(label)

            # ---PLOT---
            plt.title("Time Domain")
            plt.ylabel('Amplitudo (V)')
            plt.xlabel("Time (ns)")
            plt.plot(m, sr111)
            plt.legend(label_list)
            mplcursors.cursor() # menambah anotasi pada line

            # Menghapus isi dari list/array
            S21_stored.clear() 
            Sfft.clear()
            
        except Exception as err:
            print(f'{err.__class__} = {err}')
    return plt.show()

time_domain(filenames)