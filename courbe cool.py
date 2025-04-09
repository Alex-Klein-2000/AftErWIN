import numpy as np
import matplotlib.pyplot as plt
from collections import deque
plt.rc('text', usetex=True)

def fenetre_glissante(sequence, k):
    """Calcule une moyenne sur des fenêtres glissantes.
    k est la taille de la fenêtre glissante
 
    >>> fenetre_glissante([40, 30, 50, 46, 39, 44], 3)
    [40.0, 42.0, 45.0, 43.0]
    """
    d = deque(sequence[:k])  # on initialise avec les k premiers élements
    avg, s = [], sum(d)
    avg.append(s / k)  # la moyenne sur la fenêtre
 
    for elt in sequence[k:]:
        s += elt - d.popleft()  # on enlève la 1re valeur, on ajoute la nouvelle
        d.append(elt)
        avg.append(s / k)
 
    return avg

# Fonction pour lire les données à partir des fichiers texte et isoler le deuxième nombre de chaque ligne
def lire_fichier(fichier):
    with open(fichier, 'r') as f:
        donnees = [float(ligne.strip().split()[1]) for ligne in f]
    return donnees
def lire_fichier2(fichier):
    with open(fichier, 'r') as f:
        donnees = [float(ligne.strip().split()[2]) for ligne in f]
    return donnees



# Listes pour stocker les signaux des différents fichiers
signaux = []
phases = []

# Lire les données à partir des 5 fichiers texte
with open('test_200_0', 'r') as g:
    frequence = [float(ligne.strip().split()[0]) for ligne in g]
    
for j in range(100,2000,300):
    fichier = 'test_'+str(j)+'_0'
    courbe = lire_fichier(fichier)
    signaux.append(courbe)

fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
for i in range(0,len(signaux)):
    momo = fenetre_glissante(signaux[i], 5)
    newfreq = []
    count = 0
    while count < len(momo):
        newfreq.append(frequence[count])
        count+=1
    ax.plot(newfreq, momo, label=f'Signal à {(i+1)*50+50}mV')
        
ax.set_xlabel('Fréquence')
ax.grid(True, alpha=0.4, color='indigo')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#888888')
ax.spines['left'].set_color('#888888')
ax.set_ylabel('Amplitude')
plt.legend(loc='best', shadow=True)



plt.show()

for j in range(100,2000,200):
    fichier = 'test_'+str(j)+'_0'
    courbe = lire_fichier2(fichier)
    phases.append(courbe)

fig, ax = plt.subplots(figsize=(8, 5), dpi=200)
for i in range(0,len(phases)):
    momo = fenetre_glissante(phases[i], 5)
    newfreq = []
    count = 0
    while count < len(momo):
        newfreq.append(frequence[count])
        count+=1
    ax.plot(newfreq, momo, label=f'Signal à {(i+1)*50+50}mV')
        
ax.set_xlabel('Fréquence')
ax.grid(True, alpha=0.4, color='indigo')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#888888')
ax.spines['left'].set_color('#888888')
ax.set_ylabel('phase')
plt.legend(loc='best', shadow=True)

plt.show()