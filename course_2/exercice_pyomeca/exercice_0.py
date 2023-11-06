"""
Charger un fichier c3d et regarder les marqueurs

conda install -c conda-forge biosiglive pyomeca

"""
# c3d visualisation
from time import sleep, time
from biosiglive import LivePlot, PlotType
# c3d lecteur
from ezc3d import c3d
# biomecanique toolbox
from pyomeca import Markers
# affichage de graphique classique
import matplotlib.pyplot as plt

def visualiser_le_c3d(c3d_filename: str, numero_marqueur: int = None):
    """ afficher les marqueurs 3D """
    markers_from_c3d = Markers.from_c3d(c3d_filename)
    if numero_marqueur == None:
        markers_from_c3d = markers_from_c3d.values[:3, :, :] * 0.001
    else:
        markers_from_c3d = markers_from_c3d.values[:3, numero_marqueur:(numero_marqueur+1), :] * 0.001
        
    marker_plot = LivePlot(name="markers", plot_type=PlotType.Scatter3D)
    marker_plot.init()
    count = 0
    
    while True:
        marker_plot.update(markers_from_c3d[:, :, count].T, size=0.03)
        count += 1
        sleep(0.01)
        if count == markers_from_c3d.shape[2]:
            count = 0
            
c3d_filename = "2014001_C1_01.c3d"

# Décommenter pour visualiser le c3d
visualiser_le_c3d(c3d_filename)


fichier_c3d = c3d(c3d_filename)

# On affiche le nombre de marqueurs
print("Nombre de marqueurs")
print(fichier_c3d['parameters']['POINT']['USED']['value'][0]);

# On affiche les noms des marqueurs
noms_des_marqueurs = fichier_c3d["parameters"]["POINT"]["LABELS"]['value']
print(fichier_c3d["parameters"]["POINT"]["LABELS"]['value'])

# On veut afficher la trajectoire d'un marqueur
print(fichier_c3d["data"]["points"].shape)  
# dimension (4 x 52 x 387)
# ( XYZ1 x numero du marqueur x time_frame)

# On peut afficher la trajectoire du marqueur 2
numero_marqueur = 2
plt.plot(fichier_c3d["data"]["points"][:3, numero_marqueur, :].T)
plt.title(f"trajectoire du marqueur {noms_des_marqueurs[numero_marqueur]}")
plt.show()

# visualiser_le_c3d(c3d_filename, numero_marqueur)

# EXERCICE 
# afficher la trajectoire en z du marqueur 14 avec matplotlib
# ...