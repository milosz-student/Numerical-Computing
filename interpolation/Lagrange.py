import csv
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [12, 8]
plt.rcParams["figure.autolayout"] = True

filename = 'source/WielkiKanionKolorado.csv'

points = [[], []]

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        for j in range(2):
            points[j].append(float(row[j]))


def Lagrange(value):
    length = len(selected_points[0])
    sum = 0
    for i in range(length):
        tmp = 1.0
        for j in range(length):
            if i != j:
                tmp *= ((value - selected_points[0][j]) / (selected_points[0][i] - selected_points[0][j]))
        sum += selected_points[1][i] * tmp
    return sum


steps = [2, 5, 10, 15, 30, 50, 100, 200]
for step in steps:
    nr_points = int(len(points[0]) / step)
    selected_points = [[], []]

    for i in range(nr_points):
        for j in range(2):
            selected_points[j] = points[j][::step]

    newy = []
    for i in range(len(points[0])):
        newy.append(Lagrange(points[0][i]))
    name = filename.split("/")
    tmp = name[1]
    tmp = tmp.split(".")
    tmp = tmp[0]
    name = tmp + " method Lagrange for " + str(len(selected_points[0])) + " points"
    plt.title(name)
    plt.plot(points[0], points[1], 'b-', label='all points')
    plt.plot(selected_points[0], selected_points[1], 'ro', label='selected points')
    plt.plot(points[0], newy, 'g', label='lagrange function')
    plt.grid()
    plt.xlabel("Distance (m)")
    plt.ylabel("Altitude (m)")
    plt.legend()
    #plt.show()
    name = name.replace(" ", "_")
    name = "figures/" + tmp + "/" + name + '.png'
    print(name)
    plt.savefig(name)
    plt.figure().clear()
