"""
This script is exercice.
The goal is to transform this three function into a class. To make it easier to use function as methods and store values as arguments.
"""

import ezc3d
import matplotlib.pyplot as plt


def load_c3d(path):
    """
    Load a c3d file and return the data
    :param path: path of the c3d file
    :return: data of the c3d file
    """
    return ezc3d.c3d(path)


def display_c3d(c3d, time_index=0):
    """
    Display the data of a c3d file
    :param data: data of the c3d file
    :param marker_index: index of the frame to display
    :return: None
    """

    data = c3d['data']['points']

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    for marker_index in range(data.shape[1]-1):
        ax.scatter(data[0, marker_index, time_index], data[1, marker_index, time_index], data[2, marker_index, time_index], 'o')

    ax.set_title(f"All markers at time {time_index} in 3D")

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    # set all axis equal
    ax.set_aspect('equal')

    plt.show()


def print_all_marker_names(c3d):
    """
    Print all the marker names
    :param data: data of the c3d file
    :return: None
    """
    for i in c3d["parameters"]["POINT"]["LABELS"]["value"]:
        print(i)


if __name__ == '__main__':
    c3d = load_c3d('static.c3d')
    display_c3d(c3d, 0)
    print_all_marker_names(c3d)
