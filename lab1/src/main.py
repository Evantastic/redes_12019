# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, fftfreq, ifft
from scipy.io.wavfile import read, write

# Obtencion de informacion
file = read("../resources/audio/handel.wav")
rate = file[0]
amplitudeTime = file[1]
dataLen = len(amplitudeTime)
delta = 1/rate
time = np.linspace(0, (dataLen - 1) * delta, dataLen)
amplitudeFrequency = fft(amplitudeTime)
frequency = fftfreq(dataLen, delta)
inverseAmplitudeTime = ifft(amplitudeFrequency).real
fakedAmplitudeFrequency = amplitudeFrequency.copy()
for x in range(12504,36557):
    fakedAmplitudeFrequency[x] = 0;
    fakedAmplitudeFrequency[73113 - x] = 0
for x in range(2000):
    fakedAmplitudeFrequency[x] = 0;
    fakedAmplitudeFrequency[73112 - x] = 0
inverseFakedAmplitudeTime = ifft(fakedAmplitudeFrequency).real
write("../resources/audio/handelTruncado.wav",rate,inverseFakedAmplitudeTime)

# Cálculo de errores
firstQuadraticError = np.sqrt(((inverseAmplitudeTime - amplitudeTime) ** 2).mean())
secondQuadraticError = np.sqrt(((inverseFakedAmplitudeTime - amplitudeTime) ** 2).mean())

# # Gráfico de la transformada de fourier
plt.figure(1)
plt.plot(time,amplitudeTime)
plt.title("Señal original")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.figure(2)
plt.plot(time,inverseAmplitudeTime)
plt.title("Señal invertida")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.figure(3)
plt.plot(time,inverseFakedAmplitudeTime)
plt.title("Señal invertida truncada")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.figure(4)
plt.vlines(frequency, 0, np.abs(amplitudeFrequency))
plt.title("Transformada de Fourier")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.figure(5)
plt.vlines(frequency, 0, np.abs(fakedAmplitudeFrequency))
plt.title("Transformada de Fourier truncada")
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.show()