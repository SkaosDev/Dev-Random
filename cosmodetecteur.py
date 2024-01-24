# ---------------------------------------------
# Conversion CSV CosmoDetecteur vers Graphiques 
#                    Skaos
# ---------------------------------------------

import csv
import os
import argparse
from time import *
from datetime import datetime
debug = False

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", type=bool)

args = parser.parse_args()
debug_parameter = args.debug

if debug_parameter == True:
    debug = True


print("\n🔄️ | Vérification des librairies installéés...")
try:
    import matplotlib.pyplot as plt
    print("✅ | Vérification des librairies terminée")
except:
    print("\n⛔ | Librairies requises non installées !")
    print("🔄️ | Début de l'installation des librairies dans 3 secondes...\n\n")
    sleep(3)
    os.system('pip install matplotlib')
    print('\n✅ | Installation des librairies terminée')

import matplotlib.pyplot as plt

filename, intervalle, graph_unity, start_time = "test.csv", 10, 3600, '19/05 10'

if not debug:
    filename = input('\n🔧 | Nom du fichier ou chemin d\'accès : ')
    intervalle = int(input("🔧 | Intervalle entre les captures (en sec) : "))
    graph_unity = int(input("🔧 | Intervalle de temps pour une unité sur le graphique (en sec) : "))
    start_time = input("🔧 | Date de démarrage de l'expérience (Par exemple pour dire le 19 mai à 10h, il faut écrire: '19/05 10' sans les guillemets) : ")

current_year = datetime.now().year
format_str = '%d/%m %H'
dt = datetime.strptime(f"{start_time} {current_year}", f"{format_str} %Y")
timestamp = int(mktime(dt.timetuple()))
values = []

with open(filename, mode='r', encoding='utf-8') as fichier:
    lecteur_csv = csv.reader(fichier)
    
    for ligne in lecteur_csv:
        if ligne:
            values.append(int(ligne[0]))

total_values = len(values)
nbr_per_unity = graph_unity // intervalle
structured_values = []
structured_time = []

last_hour_factor = 1

if total_values % nbr_per_unity == 0:
    last_hour_factor = 2
else:
    print("\n🔒 | La dernière periode de temps n'est pas complète et ne sera pas utilisée !")

for i in range(0, total_values-nbr_per_unity, nbr_per_unity):
    total = 0
    for j in range((i//nbr_per_unity)*nbr_per_unity, (i//nbr_per_unity)*nbr_per_unity+last_hour_factor*nbr_per_unity):
        total += values[j]
    structured_values.append(total)

    dt = datetime.fromtimestamp(timestamp)
    formatted_date = dt.strftime('%d/%m à %Hh')
    structured_time.append(formatted_date)
    timestamp += graph_unity

print("\n🔄️ | Génération du graphique...")

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.bar(structured_time, structured_values)
plt.xticks(rotation=45)

ax.set_ylabel('Nombre de Particule')
ax.set_title('Nombre de particule en fonction du temps')

print("✅ | Génération du graphique terminée\n")
plt.show()