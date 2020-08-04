import csv
import matplotlib.pyplot as plt
import seaborn as sn

import pandas as pd

danceability = []
energy = []
acousticness = []
instrumentalness = []
liveness = []
speechiness = []
valence = []
tempo = []

with open('audio_feat.csv') as data_file:
    dat = csv.reader(data_file, delimiter=',')
    for datum in dat:
        if not datum:
            continue
        danceability.append(float(datum[0]))
        energy.append(float(datum[1]))
        acousticness.append(float(datum[2]))
        instrumentalness.append(float(datum[3]))
        liveness.append(float(datum[4]))
        speechiness.append(float(datum[5]))
        valence.append(float(datum[6]))
        tempo.append(float(datum[7]))

data = {
    'danceability': danceability,
    'energy': energy,
    'acousticness': acousticness,
    'instrumentalness': instrumentalness,
    'liveness': liveness,
    'speechiness': speechiness,
    'valence': valence,
    'tempo': tempo
}


plt.hist(acousticness, bins='auto')
plt.hist(speechiness, bins='auto')
plt.show()