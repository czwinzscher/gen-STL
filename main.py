#!/usr/bin/env python3

from copy import deepcopy
from math import pi, sin, cos


def get_circle(num_facets, radius):
    angle = (2 * pi) / num_facets
    circle = [[] for _ in range(num_facets)]
    for i in range(num_facets):
        circle[i].append([0.0, 0.0, 0.0])
        circle[i].append(
            [cos(i * angle) * radius, sin(i * angle) * radius, 0.0])
        circle[i].append([cos((i + 1) * angle) * radius,
                          sin((i + 1) * angle) * radius, 0.0])

    return circle


def get_cylinder(num_facets_circle, height, radius):
    bottom = get_circle(num_facets_circle, radius)
    top = deepcopy(bottom)
    rect = [[] for _ in range(2 * num_facets_circle)]

    for t in top:
        for v in t:
            v[2] += height

    for i in range(num_facets_circle):
        rect[2 * i].append(top[i][1])
        rect[2 * i].append(bottom[i][1])
        rect[2 * i].append(bottom[i][2])
        rect[2 * i + 1].append(bottom[i][2])
        rect[2 * i + 1].append(top[i][1])
        rect[2 * i + 1].append(top[i][2])

    top.extend(bottom)
    top.extend(rect)

    return top


def get_cuboid(x, y, z):
    x /= 2
    y /= 2

    c = [[] for _ in range(12)]
    c[0] = [[x, -y, 0], [-x, y, 0], [-x, -y, 0]]
    c[1] = [[x, -y, 0], [-x, y, 0], [x, y, 0]]
    c[2] = [[x, -y, z], [-x, y, z], [-x, -y, z]]
    c[3] = [[x, -y, z], [-x, y, z], [x, y, z]]
    c[4] = [[x, -y, 0], [-x, -y, 0], [x, -y, z]]
    c[5] = [[-x, -y, 0], [x, -y, z], [-x, -y, z]]
    c[6] = [[x, y, 0], [-x, y, 0], [x, y, z]]
    c[7] = [[-x, y, 0], [x, y, z], [-x, y, z]]
    c[8] = [[x, y, 0], [x, -y, 0], [x, y, z]]
    c[9] = [[x, -y, 0], [x, -y, z], [x, y, z]]
    c[10] = [[-x, y, 0], [-x, -y, 0], [-x, y, z]]
    c[11] = [[-x, -y, 0], [-x, -y, z], [-x, y, z]]

    return c


def write_stl(data):
    filename = input("in which file do you want to write? ")
    with open(filename, "w") as f:
        f.write("solid k\n")
        for e in data:
            f.write("facet normal 0.0 0.0 0.0\nouter loop\n")
            for vertex in e:
                f.write("vertex {:8f} {:8f} {:8f}\n".format(*vertex))
            f.write("endloop\nendfacet\n")
        f.write("endsolid k\n")


def main():
    ans = input("Do you want to generate a (cy)linder or a (cu)boid?"
                + " Other inputs will end the program.\n")
    if ans == "cy":
        num_facets = input("Number of triangles per circle: ")
        radius = input("radius of the cylinder: ")
        height = input("height of the cylinder: ")

        c = get_cylinder(int(num_facets), float(height), float(radius))
        write_stl(c)

    elif ans == "cu":
        x = input("edge length x: ")
        y = input("edge length y: ")
        z = input("edge length z: ")

        c = get_cuboid(float(x), float(y), float(z))
        write_stl(c)


if __name__ == "__main__":
    main()
