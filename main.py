from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

MAX = 20
A = [[0] * MAX] * MAX
B = [[0] * MAX] * MAX
C = [[0] * MAX] * MAX
E = [[0] * MAX] * MAX
n = 0
u = 0
hasCycle = False
dd = [0]*MAX
dem = 1

def check_hamiltonian_path(adj, N):
    dp = [[False for i in range(1 << N)]
          for j in range(N)]
    for i in range(N):
        dp[i][1 << i] = True
    for i in range(1 << N):
        for j in range(N):
            if ((i & (1 << j)) != 0):
                for k in range(N):
                    if ((i & (1 << k)) != 0 and
                        adj[k][j] == 1 and
                            dp[k][i ^ (1 << j)]):
                        dp[j][i] = True
                        break
    for i in range(N):
        if (dp[i][(1 << N) - 1]):
            return True
    return False

class Graph_for_Hamiltonian:
    def __init__(self, C, n):
        self.adjList = [[] for _ in range(n+1)]
        for i in range(n):
            for j in range(n):
                if (C[i][j] == 1): # Nếu i và j liền kề
                    if ((j+1) not in self.adjList[i+1]):
                        self.adjList[i+1].append(j+1)
                    if ((i+1) not in self.adjList[j+1]):
                        self.adjList[j+1].append(i+1)

def hamiltonianPaths(graph, v, visited, path, n):
    if len(path) == n:
        for x in path:
            print(x, end=' ')
        print()
        return
    for w in graph.adjList[v]:
        if not visited[w]:
            visited[w] = True
            path.append(w)
            hamiltonianPaths(graph, w, visited, path, n)
            visited[w] = False
            path.pop()

def print_hamiltonian_path(graph, n):
    for start in range(1, n+1):
        path = [start]
        visited = [False] * (n+1)
        visited[start] = True
        hamiltonianPaths(graph, start, visited, path, n)

def check_hamilton_graph():
    if (n < 3):
        return False
    deg = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += C[i][j]
        deg.append(s)
    for i in range(n):
        for j in range(n):
            if (j == i or C[i][j] == 1):
                continue
            else:
                if (deg[j] + deg[i] < n):
                    return False
    return True

class Graph_2():
    def __init__(self, vertices):
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        self.V = vertices
    def isSafe(self, v, pos, path):
        if self.graph[path[pos-1]][v] == 0:
            return False
        # Ktra dinh hien tai co trong duong dan chua
        for vertex in path:
            if vertex == v:
                return False
        return True
    def hamCycleUtil(self, path, pos):
        if pos == self.V:
            if self.graph[path[pos-1]][path[0]] == 1:
                return True
            else:
                return False
        for v in range(1, self.V):
            if self.isSafe(v, pos, path) == True:
                path[pos] = v
                if self.hamCycleUtil(path, pos+1) == True:
                    return True
                path[pos] = -1
        return False

    def hamCycle(self):
        path = [-1] * self.V
        path[0] = 0
        if self.hamCycleUtil(path, 1) == False:
            return False
        return True
    def printSolution(self):
        path = [-1] * self.V
        path[0] = 0
        self.hamCycleUtil(path, 1)
        path.append(path[0])
        for vertex in path:
            print(vertex + 1, end=" ")
        print()
        G = nx.DiGraph()
        for i in range(len(path)-1):
            s1 = str(chr(path[i]+1 + 48))
            s2 = str(chr(path[i+1]+1 + 48))
            G.add_edge(s1, s2)
        pos = nx.spring_layout(G)
        val_map = {'1': 0.9}
        values = [val_map.get(node, 0.5) for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                               node_color=values, node_size=500)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_weight="bold")
        plt.title("Chu trình Hamilton")
        plt.show()

#################################################################################

def BFS(A, n, x):
    global dd
    dd[0] = -1
    dd[x] = 1
    for j in range(1, n + 1):
        if A[x][j] != 0 and dd[j] == 0:
            global dem
            dem += 1
            BFS(A, n, j)

def check_euler_path_udg():
    global u
    d = 0
    for i in range(1, n+1):
        s = 0
        for j in range(1, n+1):
            s += A[i][j]
        if s % 2 != 0:
            d += 1
            u = i
    if d != 2 and d!= 0:
        return False
    return True

def check_euler_path_dg():
    global u
    d1 = 0
    dr = 0
    dv = 0
    for i in range(1, n+1):
        rowsum = 0
        colsum = 0
        for j in range(1, n + 1):
            rowsum += A[i][j]
            colsum += A[j][i]
        if rowsum != colsum:
            d1 += 1
        if rowsum - colsum == 1:
            u = i
            dr += 1
        if colsum - rowsum == 1:
            dv += 1
    if (d1 != 2) or (dr != 1) or (dv != 1):
        return False
    return True

def print_euler_path():
    # v, x = 0, 0
    stack = [0] * MAX
    CE = [0] * MAX
    top = 1
    stack[top] = u
    dCE = 0
    while True:
        v = stack[top]
        x = 1
        while x <= n and A[v][x] == 0:
            x += 1
        if (x > n):
            dCE += 1
            CE[dCE] = v
            top -= 1
        else:
            top += 1
            stack[top] = x
            A[v][x] = 0
            A[x][v] = 0
        if (top == 0):
            break
    for x in range(dCE, 0, -1):
        print(chr(CE[x] + 48), end=" ")
    print()

def check_euler_cycle_udg():
    s, d = 0, 0
    for i in range(1, n+1):
        s = 0
        for j in range(1, n+1):
            s += B[i][j]
        if s % 2 != 0:
            d += 1
    if d > 0:
        return False
    return True

def check_euler_cycle_dg():
    d = 0
    for i in range(1, n+1):
        rowsum = 0
        colsum = 0
        for j in range(1, n + 1):
            rowsum += B[i][j]
            colsum += B[j][i]
        if rowsum != colsum:
            d += 1
    if d != 0:
        return False
    return True

def print_euler_cycle():
    stack = [0] * MAX
    CE = [0] * MAX
    top = 1
    u = 1
    stack[top] = u
    dCE = 0
    while True:
        v = stack[top]
        x = 1
        while x <= n and B[v][x] == 0:
            x += 1
        if x > n:
            dCE += 1
            CE[dCE] = v
            top -= 1
        else:
            top += 1
            stack[top] = x
            B[v][x] = 0
            B[x][v] = 0
        if (top == 0):
            break
    for x in range(dCE, 0, -1):
        print(chr(CE[x] + 48), end=" ")
    print()
    if check_euler_cycle_dg() or check_euler_cycle_udg():
        graph_euler(CE, dCE)

def graph_euler(A, n):
    G = nx.DiGraph()
    for x in range(n, 1, -1):
        s1 = str(chr(A[x] + 48))
        s2 = str(chr(A[x - 1] + 48))
        G.add_edge(s1, s2)
    pos = nx.spring_layout(G)
    val_map = {'1': 0.9}
    values = [val_map.get(node, 0.5) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color=values, node_size=500)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_weight= "bold")
    plt.title("Chu trình Euler")
    plt.show()

def menu1():
    print("1. Nhap vao ma tran ke")
    print("2. Doc ma tran ke tu file")
    print("0. Thoat")

def menu2():
    print("A. Tìm chu trình, đường đi Haminton")
    print("B. Tìm chu trình, đường đi Euler")
    print("C. Thoát")

if __name__ == "__main__":
    while True:
        menu1()
        choice1 = int(input("Lua chon: "))
        print()
        if choice1 == 1:
            n = int(input("Nhap so dinh: "))
            print("Nhap ma tran ke: ")
            for i in range(1, n + 1):
                A[i] = [-1] + [int(x) for x in input().split()]
            B = deepcopy(A)
            menu2()
            choice2 = input("Lua chon: ")
            if choice2 == 'A' or choice2 == 'a':
                C = [[A[i][j] for i in range(1, n + 1)] for j in range(1, n + 1)]
                ham = Graph_for_Hamiltonian(C, n)
                ham_2 = Graph_2(n)
                ham_2.graph = C
                print("\tHAMILTON")
                if check_hamiltonian_path(C, n):
                    print("Đường đi Hamilton: ")
                    print_hamiltonian_path(ham, n)
                    if ham_2.hamCycle() == True:
                        print("Chu trình Hamilton: ")
                        ham_2.printSolution()
                        continue
                    else:
                        print("Không có chu trình Hamilton!")
                        continue
                else:
                    print("Không có đường đi và chu trình Hamilton!")
                    continue
                print("-------------------------------")
            if choice2 == 'B' or choice2 =='b':
                    print("ELUER")
                    BFS(A, n, 1)
                    if dem == n and (check_euler_cycle_udg() or check_euler_cycle_dg()):
                        print("Chu trình Euler: ")
                        print_euler_cycle()
                    elif dem == n and (check_euler_cycle_udg() or check_euler_cycle_dg()):
                        print("Không có chu trình Euler!")
                        print("Đường đi Euler:")
                        print_euler_path()
                        continue
                    else:
                        print("Không có đường đi Euler và chu trình Euler!")
                        continue
                    print("---------------------------------------")
            elif choice2 == 'C':
                break
            else:
                print("Error")
        elif choice1 == 2:
            filename = input("Nhap ten file: ")
            f = open(filename, 'r').readlines()
            # Đọc toàn bộ các dòng trong file
            n = int(f[0])
            adj = []
            adj.append([-1] * n)
            for line in f[1:]:
                adj.append([-1] + list(map(int, line.split())))
            A = deepcopy(adj)
            B = deepcopy(adj)
            C = [[adj[i][j] for i in range(1, n+1)] for j in range(1, n+1)]
            ham = Graph_for_Hamiltonian(C, n)
            ham_2 = Graph_2(n)
            ham_2.graph = C
            print("-------------------------------")
            print("\tHAMILTON")
            if check_hamiltonian_path(C, n):
                print("Đường đi Hamilton: ")
                print_hamiltonian_path(ham, n)
                if ham_2.hamCycle() == True:
                    print("Chu trình Hamilton: ")
                    ham_2.printSolution()
                else:
                    print("Không có chu trình Hamilton !")
            else:
                print("Không có đường đi và chu trình Hamilton !")
            print("-------------------------------------------")
            print("\tEULER")
            BFS(A, n, 1)
            if dem == n and (check_euler_cycle_dg() or check_euler_cycle_udg()):
                print("Chu trình Euler: ")
                print_euler_cycle()
            elif dem == n and (check_euler_path_dg() or check_euler_path_udg()):
                print("Không có chu trình Euler")
                print("Đường đi Euler: ")
                print_euler_path()
            else:
                print("Không có chu trình và đường đi Euler")
            print("------------------------------------")
        elif (choice1 == 0):
            break
        else:
            print("Error")
        print()