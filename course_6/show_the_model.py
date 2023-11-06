"""
This file is to display the human model into bioviz
"""
import os
import bioviz

model = "gait2354.bioMod"
export_model = False
background_color = (1, 1, 1) if export_model else (0.5, 0.5, 0.5)
show_gravity_vector = False if export_model else True
show_floor = False if export_model else True
show_local_ref_frame = False if export_model else True
show_global_ref_frame = False if export_model else True
show_markers = False if export_model else True
show_mass_center = False if export_model else True
show_global_center_of_mass = False if export_model else True
show_segments_center_of_mass = False if export_model else True


biorbd_viz = bioviz.Viz(model,
    show_gravity_vector=False,
    show_floor=False,
    show_local_ref_frame=False,
    show_global_ref_frame=show_global_ref_frame,
    show_markers=show_markers,
    show_mass_center=show_mass_center,
    show_global_center_of_mass=False,
    show_segments_center_of_mass=True,
    mesh_opacity=1,
    background_color=(1, 1, 1),
    show_muscles=False,
    )

biorbd_viz.exec()

print("Done")
