"""
Main file of program.
Checking the triangulation of the polygon.
Usage:
    main.py (--input PATH)
    main.py (--help)
Options:
    -i --input PATH     Path to the file with input arguments
    -h --help           Show help
"""

import os
import docopt
import math

from typing import Tuple, List


def parse_input_arguments(file_path: str) -> List[Tuple[int, int]]:
    if not os.path.exists(file_path):
        raise IOError(f"File '{file_path}' doesn't exist.")

    with open(file_path, "r") as f:
        file_lines = f.read().split('\n')
    num_of_points = int(file_lines[0].strip())
    points = []
    for line in file_lines[1:num_of_points + 1]:
        coords = line.split(' ')
        points.append((int(coords[0]), int(coords[1])))

    return points


def get_points_dist(p1: Tuple[int, int], p2: Tuple[int, int]):
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))


def vec_by_points(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]


def get_diameter(points: List[Tuple[int, int]]):
    # Find extreme points
    min_point_index = None
    max_point_index = None
    for i, p in enumerate(points):
        if min_point_index is None or p[1] < points[min_point_index][1]:
            min_point_index = i
        if max_point_index is None or p[1] > points[max_point_index][1]:
            max_point_index = i

    # Initialization
    diameter = 0
    ind1 = max_point_index
    l1 = (1, 0)

    ind2 = min_point_index
    l2 = (-1, 0)

    while not (ind1 == min_point_index and ind2 == max_point_index):
        diameter = max(diameter, get_points_dist(points[ind1], points[ind2]))

        prev_ind_1 = (ind1 - 1) % len(points)
        prev_ind_2 = (ind2 - 1) % len(points)
        vec1 = vec_by_points(points[ind1], points[prev_ind_1])
        vec2 = vec_by_points(points[ind2], points[prev_ind_2])

        angle1 = angle(l1, vec1)
        angle2 = angle(l2, vec2)
        if angle1 <= angle2:
            l1 = vec1
            ind1 = prev_ind_1
            l2 = (-vec1[0], -vec1[1])
        else:
            l2 = vec2
            ind2 = prev_ind_2
            l1 = (-vec2[0], -vec2[1])

    return diameter


def run(opts):
    points = parse_input_arguments(opts['--input'])
    diameter = get_diameter(points)

    print(f"Diameter of polygon = {diameter}")


if __name__ == "__main__":
    run(docopt.docopt(__doc__))
