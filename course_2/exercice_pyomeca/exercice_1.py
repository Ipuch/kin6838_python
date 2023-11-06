"""
Charger un fichier c3d et regarder les marqueurs v2

conda install -c conda-forge biosiglive pyomeca

"""
# biomecanique toolbox
from pyomeca import Markers
            
c3d_filename = "2014001_C1_01.c3d"

# OUBLIONS EZC3D, c'était bien trop compliqué, allons plus vite avec pyomeca
markers = Markers.from_c3d(c3d_filename)
print(markers)

# On affiche le nombre de marqueurs
print("Nombre de marqueurs")
print(markers.shape);
# dimension (4 x 52 x 387)


# On affiche les noms des marqueurs
noms_des_marqueurs = markers.channel
print(noms_des_marqueurs)

# seulement le marqueur numero 2
marker_2 = Markers.from_c3d(c3d_filename, usecols=["R_IPS"])
marker_2[1,0,:].plot(label="brut")

# Filtrer les données
marker_2.meca.low_pass(order=4, cutoff=5, freq=marker_2.rate)
marker_2[1,0,:].plot(label="filtree")


# Filtrer les données
marker_2.meca.time_normalize(norm_time=True)  # ou specifier n_frames
marker_2[1,0,:].plot(label="normalise")

# On se concentre sur la lecture de la documentation c'est plus facile

# EXERCICE - Visualiser la composante en z du marqueur SXS 
# et normaliser sur 100 frames