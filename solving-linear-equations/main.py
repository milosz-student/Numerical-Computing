
from matrix import *
from data import *
import time

file = open("wyniki.txt", "w")
#N_table = [100, 500,1000, 2000, 3000]

N_table = [1000]
for N in N_table:
    file.write(f"N = {N}")
    #print(N)
    A = createMatrix(N, N, 0)
    b = createVector(N, f)
    r = createMatrix(N ,1 ,1)
    r = r[0]
    # Zadanie A
    #diagMatrix(a1, a2, a3, A)
    # printMatrix(A)
    # Zadanie C
    diagMatrix(3, (-1), (-1), A)

    #printMatrix(A)
    L = createTriangularMatrix(A, False)
    U = createTriangularMatrix(A, True)
    D = createDiagonalMatrix(A)

    # Zadanie D
    # metoda LU


    #start = time.time()
    lu_U = copy.deepcopy(A)
    lu_L = createMatrix(len(A),len(A[0]),0)
    diagMatrix(1, 0, 0, lu_L)
    n = len(A)
    start = time.time()
    for k in range(n - 1):
        for j in range(k + 1, n):
            lu_L[j][k] = lu_U[j][k] / lu_U[k][k]
            for m in range(k, n):
                lu_U[j][m] -= lu_L[j][k] * lu_U[k][m]
    end = time.time()

    print(f"Runtime of creating L i U {round(end - start, 2)}")

    start = time.time()
    y = forwardSub(lu_L, b)
    end = time.time()
    print(f"Runtime of forwardSub {round(end - start, 2)}")
    start = time.time()
    x = backwardSub(lu_U, y)
    end = time.time()
    print(f"Runtime of backwardSub {round(end - start, 2)}")

    #print("L:")
    #printMatrix(lu_L)
    #print("U:")

    #printMatrix(lu_U)
    start = time.time()
    M_r = multiplyMatrixVector(A,x)
    Mr_b = subVector(M_r,b)
    end = time.time()
    #file.write(f"Lu Norm: {norm(Mr_b)} Runtime of the program is {round(end - start,2)}")
    print("x:",x)
    print(x[100],x[250],x[499])
    print("Norm: ",norm(Mr_b))
    print(f"Runtime of the program is {round(end - start,2)}")
    print("LU")




    A = createMatrix(N, N, 0)
    b = createVector(N, f)
    r = createMatrix(N, 1, 1)
    r = r[0]
    diagMatrix(a1, a2, a3, A)
    L = createTriangularMatrix(A, False)
    U = createTriangularMatrix(A, True)
    D = createDiagonalMatrix(A)
    #Zadanie B
    #metoda jacobiego
    #print("Jacob Method for N = ",N)

    rCopy = copy.deepcopy(r)
    D_minus1 = inverseDiagMatrix(D)
    minusD_minus1 = multiplyMatrixByScalar(D_minus1, (-1))
    L_sum_U = getLUfromMatrix(A)
    X = multiplyMatrices(minusD_minus1,L_sum_U) #−D^(−1) * (L + U)
    Y = multiplyMatrixVector(D_minus1,b) #D^(−1) * b
    #                 X                     Y
    # r^(k+1) = −D^(−1) * (L + U)*r^(k) + D^(−1) * b
    k = 0
    M_r = multiplyMatrixVector(A,r)
    Mr_b = subVector(M_r,b)
    start = time.time()
    while(norm(Mr_b)>10e-9):
        temp = multiplyMatrixVector(X,rCopy)
        r = addVector(temp,Y)
        rCopy = copy.deepcopy(r)
        M_r = multiplyMatrixVector(A,r)
        Mr_b = subVector(M_r,b)
        k+=1
    end = time.time()
    print(r)
    #file.write(f"Jacob Method: Norm- {norm(Mr_b)}  Iterations- {k} Runtime of the program is {round(end - start, 2)}")
    print("Iterations: ",k)
    print(f"Runtime of the program is {round(end - start,2)}")
    print("Jacob")
    A = createMatrix(N, N, 0)
    b = createVector(N, f)
    r = createMatrix(N, 1, 1)
    r = r[0]
    diagMatrix(a1, a2, a3, A)
    L = createTriangularMatrix(A, False)
    U = createTriangularMatrix(A, True)
    D = createDiagonalMatrix(A)
    #print("Gaussa-Seidla Method for N = ",N)
    r = createMatrix(N,1,1)
    r = r[0]
    rCopy = copy.deepcopy(r)
    #metody Gaussa-Seidla: r^(k+1) = −(D + L)^(−1)*(U*r^(k)) + (D + L)^(−1) * b
    DplusL = addTwoMatrix(D,L)
    DL_minus1b = forwardSub(DplusL,b) #(D + L)^(−1) * b
    Ur = multiplyMatrixVector(U,r) #(U*r^(k))
    DL_minus1Ur = forwardSub(DplusL,Ur)
    minusDL_minus1Ur = multiplyVectorByScalar(DL_minus1Ur,(-1))
    k = 0
    M_r = multiplyMatrixVector(A,r)
    Mr_b = subVector(M_r,b)
    rCopy = copy.deepcopy(r)
    start = time.time()
    while((norm(Mr_b)>10e-9)and(k<1000)):
        Ur = multiplyMatrixVector(U, rCopy)  # (U*r^(k))
        DL_minus1Ur = forwardSub(DplusL, Ur)
        minusDL_minus1Ur = multiplyVectorByScalar(DL_minus1Ur, (-1))
        r = addVector(minusDL_minus1Ur, DL_minus1b)
        rCopy = copy.deepcopy(r)
        M_r = multiplyMatrixVector(A,r)
        Mr_b = subVector(M_r,b)
        k+=1
    end = time.time()
    #file.write(f"Gaussa-Seidla: Norm- {norm(Mr_b)}  Iterations- {k} Runtime of the program is {round(end - start, 2)}")
    print(r)
    print("Gauss")
    print("Iterations: ",k)
    print(f"Runtime of the program is {round(end - start,2)}")
file.close()
