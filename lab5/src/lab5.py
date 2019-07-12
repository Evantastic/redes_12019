import matplotlib.pyplot as plt
import numpy as np
import random
from random import choice

#
# Modulacion de una senal a partir de bits
#
def modulator(bit, frequency, rate, points):
    t = 0
    ts = np.linspace(t, t+rate,points)
    t+=rate
    return 50*bit*np.cos(frequency*ts)

#
# Demodulacion de una senal a partir de los valores del arreglo de modulacion
#
def demodulator(array,points):
    aux = 0
    outputBits = ''
    while (aux < len(array)):
        if(array[aux] == 0.0 or array[aux] == -0.0):
            outputBits += '0'
        else:
            outputBits += '1'
        aux = aux + points + 1
    return outputBits

#
# Agregacion de ruido a una senal dado un determinado SNR
#
def noise(signal,snr):
    noise = np.random.normal(0.0,1.0/snr,len(signal))
    noiseSignal = noise + signal
    return noiseSignal

#
# Identificacion de tasa de error entre senal original y modulada
#
def errorT(demodulated,demodulatedN):
    error = 0
    for i in range(len(demodulated)):
        if demodulated[i] != demodulatedN[i]:
            error += 1
    errorRate = error/len(demodulated)
    return errorRate

#
#Generacion de senal y bits
#
bitQuantity = 5
frequency = 100
#Teorema de muestreo
points = frequency//2
rate = 0.1
bitsLen = int(points*bitQuantity)
bitString = ''.join(choice(['0', '1']) for _ in range(bitQuantity))
bitArray = list(bitString)

#
#Se modula
#
array = []
for c in bitArray:
    array.extend(modulator(int(c), frequency*2*np.pi, rate, points))


# A continuación viene el ploteo de la senal modulada
time = np.linspace(0, bitQuantity*rate, points*bitQuantity)
plt.plot(time, array)
plt.title("Senal original : "+bitString)
plt.show()

# A continuacion vienen los bits obtenidos desde la senal
bitsDemodulated = demodulator(array,points)
print("La senal es "+bitsDemodulated)

#Senal con ruido
snrValue = 4
noisySignal = noise(array,snrValue)

# A continuación viene el ploteo de la senal con ruido
plt.plot(time,noisySignal)
plt.title("Senal con ruido SRN = "+str(snrValue))
plt.show()

# Se consideran los niveles de SNR
SNR = [1,2,4,6,8,10]
errors = []
for snr in SNR:
    sModulated = noise(array,snr)
    sDemodulated = demodulator(sModulated,points)
    error = errorT(bitsDemodulated,sDemodulated)
    errors.append(error)

#Se muestra el grafico BER vs SNR
plt.plot(errors,SNR)
plt.title("BER vs SNR")
plt.show()