import csv
import matplotlib.pyplot as plt
import matrix

plt.rcParams["figure.figsize"] = [12, 8]
#plt.rcParams["figure.autolayout"] = True

filename = 'source/MountEverest.csv'

points = [[], []]


def S(a, b, c, d, h, deriative):
    if (deriative == 0):
        return a + b * (h) + c * (h) ** 2 + d * (h) ** 3
    elif (deriative == 1):
        return b + 2 * c * (h) + 3 * d * (h) ** 2
    else:
        return 2 * c + 6 * d * (h)


with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        for j in range(2):
            points[j].append(float(row[j]))

steps = [2, 5, 10, 15, 30, 50, 100, 200]
for step in steps:
    nr_points = int(len(points[0]) / step)
    selected_points = [[], []]
    for i in range(nr_points):
        for j in range(2):
            selected_points[j] = points[j][::step]
    n = len(selected_points[0])
    A = matrix.createMatrix(4 * (n - 1), 4 * (n - 1), 0)
    b = matrix.createMatrix(4 * (n - 1), 1, 0.0)
    b = b[0]
    # step 1: Si(xj) = f(xj)
    # S0(x0)    a0 = f(x0) +
    # S1(x1)    a1 = f(x1) +
    # S0(x0)    a0 + 2*b0 + 4*c0 + 8*d0 = f(x1) +
    # S1(x2)    a1 + 2*b1 + 4*c1 + 8*d1= f(x2) +
    # S0'(x1)   b0 + 4*c0 + 12*d0 -b1 = 0 +
    # S0''(x1)  2*c0 + 12*d0 - 2c1 = 0 +
    # S0''(x0)  c0=0
    # S1''(x2)  2*c1+12*d1=0

    # S0(x0)    a0 = f(x0)
    # S1(x1)    a1 = f(x1)
    # S0(x0)    a0 + b0*h + c0*h**2 + d0*h**3 = f(x1)
    # S1(x2)    a1 + b1*h + c1*h**2 + d1*h**3 = f(x2)
    # S0'(x1)   b0 + 2*c0*h + 3*d0*h**2 -b1 = 0
    # S0''(x1)  2*c0 + 6*d0*h - 2c1 = 0
    # S0''(x0)  c0=0
    # S1''(x2)  2*c1+6*d1*h=0
    for i in range(n - 1):
        x1 = selected_points[0][i + 1]
        y1 = selected_points[1][i + 1]
        x0 = selected_points[0][i]
        y0 = selected_points[1][i]
        row = matrix.createMatrix(4 * (n - 1), 1, 0)
        row = row[0]
        row[4 * i + 3] = 1
        A[4 * i + 3] = row
        b[4 * i + 3] = y0
        h = x1 - x0
        row = matrix.createMatrix(4 * (n - 1), 1, 0)
        row = row[0]
        row[4 * i] = h ** 3
        row[4 * i + 1] = h ** 2
        row[4 * i + 2] = h ** 1
        row[4 * i + 3] = 1
        A[4 * i + 2] = row
        b[4 * i + 2] = y1
        if i < (n - 2):
            row = matrix.createMatrix(4 * (n - 1), 1, 0)
            row = row[0]
            row[4 * i] = 3 * (h ** 2)
            row[4 * i + 1] = 2 * h
            row[4 * i + 2] = 1
            row[4 * (i + 1) + 2] = -1
            A[4 * i] = row
            b[4 * i] = 0.0
            h = x1 - x0
            row = matrix.createMatrix(4 * (n - 1), 1, 0)
            row = row[0]
            row[4 * i] = 6 * h
            row[4 * i + 1] = 2
            row[4 * (i + 1) + 1] = -2
            A[4 * (i + 1) + 1] = row
            b[4 * (i + 1) + 1] = 0.0

    row = matrix.createMatrix(4 * (n - 1), 1, 0)
    row = row[0]
    row[1] = 2
    A[1] = row
    b[1] = 0.0
    row = matrix.createMatrix(4 * (n - 1), 1, 0)
    row = row[0]
    x1 = selected_points[0][-1]
    y1 = selected_points[1][-1]
    x0 = selected_points[0][-2]
    y0 = selected_points[1][-2]
    h = x1 - x0
    row[1] = 2
    row[-4] = 6 * h
    A[-4] = row
    b[-4] = 0.0

    # parametry x = [a0,b0,c0,d0,a1,b1,c1,d1.....]
    x = matrix.FactorLU(A, b)

    param_array = []
    row = []
    for param in x:
        row.append(param)
        if len(row) == 4:
            param_array.append(row.copy())
            row.clear()

    newy = []

    for i in range(len(points[0])):
        for j in range(1, len(selected_points[0])):
            xi = selected_points[0][j - 1]
            xj = selected_points[0][j]
            if float(xi) <= points[0][i] <= float(xj):
                a, b, c, d = param_array[j - 1]
                h = points[0][i] - float(xi)
                tmp = S(d, c, b, a, h, 0)
                newy.append(tmp)
                break

    name = filename.split("/")
    tmp = name[1]
    tmp = tmp.split(".")
    tmp = tmp[0]
    name = tmp + " method Spline for " + str(nr_points) + " points"
    plt.title(name)
    plt.plot(points[0], points[1], 'b-', label='all points')
    plt.plot(selected_points[0], selected_points[1], 'ro', label='selected points')
    plt.plot(points[0][0:len(newy)], newy, 'g', label='Spline function')
    plt.grid()
    plt.xlabel("Distance (m)")
    plt.ylabel("Altitude (m)")
    plt.legend()
    # plt.show()
    name = name.replace(" ", "_")

    name = "figures/" + tmp + "/" + name + '.png'
    print(name)
    plt.savefig(name)
    plt.figure().clear()
