import math
import copy


def norm(V):
    sum = 0
    for i in V:
        sum += (pow(i, 2))
    sum = math.sqrt(sum)
    return sum


def createMatrix(n, m, value):
    new_matrix = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(value)
        new_matrix.append(row)

    return new_matrix


def createTriangularMatrix(matrix, upper):
    # if parameter upper is equal True then the Matrix is UpperTriangular else LowerTriangular
    new_matrix = createMatrix(len(matrix), len(matrix[0]), 0)
    for i in range(len(new_matrix)):
        for j in range(i):
            x = [i, j][upper == True]
            y = [j, i][upper == True]
            new_matrix[x][y] = matrix[x][y]

    return new_matrix


def getLUfromMatrix(A):
    new_matrix = copy.deepcopy(A)
    for i in range(len(new_matrix)):
        new_matrix[i][i] = 0
    return new_matrix


def createDiagonalMatrix(matrix):
    new_matrix = createMatrix(len(matrix), len(matrix[0]), 0)
    for i in range(len(new_matrix)):
        new_matrix[i][i] = matrix[i][i]

    return new_matrix


def printMatrix(matrix):
    for row in matrix:
        print(row)


def diagMatrix(a1, a2, a3, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                matrix[i][j] = a1
            elif ((i + 1) == j) or ((i - 1) == j):
                matrix[i][j] = a2
            elif ((i + 2) == j) or ((i - 2) == j):
                matrix[i][j] = a3


def createVector(n, f):
    new_vector = []
    for i in range(n):
        new_vector.append(math.sin(i * (f + 1)))
    return new_vector


def addTwoMatrix(A, B):
    # adding two matrixes, working ONLY when they have same size
    product = copy.deepcopy(A)
    for i in range(len(B)):
        for j in range(len(B[0])):
            product[i][j] += B[i][j]
    return product


def inverseDiagMatrix(A):
    new_matrix = createMatrix(len(A), len(A[0]), 0)
    for i in range(len(new_matrix)):
        new_matrix[i][i] = 1 / A[i][i]
    return new_matrix


def deternminantMatrix(A):
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]

    determinant = 0
    for j in range(len(A)):
        determinant += ((-1) ** j) * A[0][j] * deternminantMatrix(minorMatrix(A, 0, j))
    return determinant


def minorMatrix(A, i, j):
    return [row[:j] + row[j + 1:] for row in (A[:i] + A[i + 1:])]


def transposeMatrix(A):
    transposed = []
    for j in range(len(A[0])):
        row = []
        for i in range(len(A)):
            row.append(A[i][j])
        transposed.append(row)

    return transposed


def multiplyMatrixByScalar(A, s):
    new_matrix = copy.deepcopy(A)
    for i in range(len(new_matrix)):
        for j in range(len(new_matrix[0])):
            new_matrix[i][j] *= s
    return new_matrix


def multiplyVectorByScalar(V, s):
    new_matrix = copy.deepcopy(V)
    for i in range(len(new_matrix)):
        if new_matrix[i] != 0:
            new_matrix[i] = new_matrix[i] * s

    return new_matrix


def multiplyMatrices(A, B):
    product = createMatrix(len(A), len(A[0]), 0)
    for i in range(len(A)):
        for j in range(len(B[0])):
            total = 0
            for k in range(len(A[0])):
                total += A[i][k] * B[k][j]
            product[i][j] = total

    return product


def multiplyMatrixVector(A, v):
    product = []
    for i in range(len(A[0])):
        total = 0
        for j in range(len(v)):
            total += A[i][j] * v[j]
        product.append(total)

    return product


def subVector(A, B):
    # adding two vectors, working ONLY when they have same size
    total = []
    for i in range(len(A)):
        total.append(A[i] - B[i])

    return total


def addVector(A, B):
    # adding two vectors, working ONLY when they have same size
    total = []
    for i in range(len(A)):
        total.append(A[i] + B[i])

    return total


def forwardSub(A, b):
    n = len(A)
    x = createMatrix(len(b), 1, 0)
    x = x[0]
    for i in range(n):
        sum = 0
        for j in range(i):
            sum += A[i][j] * x[j]
        x[i] = (b[i] - sum) / A[i][i]
    return x


def backwardSub(A, b):
    n = len(A)
    x = createMatrix(len(b), 1, 0)
    x = x[0]
    for i in range(n):
        sum = 0
        for j in range(i):
            sum +=  x[n-j-1] * A[n - i - 1][n - j - 1]
        x[n - i - 1]=(b[n - i - 1]- sum) / A[n - i - 1][n - i - 1]

    return x
