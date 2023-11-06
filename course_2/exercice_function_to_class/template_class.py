"""
This script is exercice.
The goal is to transform this three function into a class. To make it easier to use function as methods and store values as arguments.
"""

import ezc3d
import matplotlib.pyplot as plt

class C3D:
    def __init__(self, path):
            # self.path
            # self.c3d = ezc3d.c3d(path)
            print("you have to complete this section")

    def display_c3d(self, time_index=0):
        # reuse self to access the c3d data
        print("you have to complete this section")

    def print_all_marker_names(self):
        # reuse self to access the c3d data
        print("you have to complete this section")


if __name__ == '__main__':
    # Here it is how it should look now
    c3d = C3D('static.c3d')
    c3d.display_c3d()
    c3d.print_all_marker_names()
