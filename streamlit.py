import streamlit as st
import time
from collections import deque
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

def count_borders(matrix):
    borders = 0
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(m):
            if i > 0 and matrix[i][j] != matrix[i - 1][j]:
                borders += 1
            if j > 0 and matrix[i][j] != matrix[i][j - 1]:
                borders += 1

    return borders

def bfs(matrix, max_borders):
    start_time = time.time()

    n = len(matrix)
    m = len(matrix[0])

    visited = set()
    queue = deque([(matrix, [])])

    generations = 0
    expansions = 0

    while queue:
        generations += 1
        current_matrix, actions = queue.popleft()
        current_borders = count_borders(current_matrix)

        if current_borders <= max_borders:
            processing_time = time.time() - start_time
            return current_matrix, actions, current_borders, generations, expansions, processing_time

        for i in range(n):
            for j in range(m):
                for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                    if 0 <= x < n and 0 <= y < m:
                        expansions += 1
                        new_matrix = deepcopy(current_matrix)
                        new_matrix[i][j], new_matrix[x][y] = new_matrix[x][y], new_matrix[i][j]

                        if tuple(map(tuple, new_matrix)) not in visited:
                            new_actions = actions + [((i, j), (x, y))]
                            queue.append((new_matrix, new_actions))
                            visited.add(tuple(map(tuple, new_matrix)))

        if time.time() - start_time > 60:
            break

    processing_time = time.time() - start_time
    return None, [], -1, generations, expansions, processing_time

instances = [
  [
        [1, 2, 3],
        [1, 2, 2],
        [3, 3, 1]
    ],
    [
        [1, 2, 2, 2],
        [1, 2, 1, 1]
    ],
    [
        [1, 2, 2, 2],
        [1, 3, 3, 3],
        [1, 2, 1, 1],
        [1, 1, 3, 2]
    ],
    [
        [1, 1, 2, 1, 1],
        [2, 2, 1, 2, 1],
        [1, 1, 2, 1, 2],
        [2, 1, 1, 2, 1]
    ],
    [
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2],
        [1, 3, 3, 3, 4, 1, 3, 3, 3, 4],
        [1, 2, 1, 4, 3, 1, 2, 1, 4, 3],
        [1, 4, 4, 4, 3, 1, 4, 4, 4, 3]
    ],
    [
        [1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
        [2, 2, 1, 2, 1, 2, 2, 1, 2, 1],
        [1, 1, 2, 1, 2, 1, 1, 2, 1, 2],
        [2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 1, 2, 1, 1, 1, 1, 2, 1, 1],
        [2, 2, 1, 2, 1, 2, 2, 1, 2, 1],
        [1, 1, 2, 1, 2, 1, 1, 2, 1, 2],
        [2, 1, 1, 2, 1, 2, 1, 1, 2, 1]
    ],
    [
        [1, 1, 2, 8, 8, 1, 4, 3, 1, 4],
        [2, 2, 1, 8, 3, 8, 4, 3, 2, 1],
        [1, 1, 8, 8, 3, 1, 6, 2, 1, 4],
        [2, 1, 1, 3, 1, 2, 1, 1, 4, 4],
        [1, 7, 7, 3, 1, 1, 5, 6, 4, 4],
        [2, 2, 1, 3, 1, 2, 2, 1, 6, 6],
        [1, 7, 2, 7, 5, 5, 5, 5, 1, 6],
        [2, 7, 7, 7, 1, 5, 5, 1, 6, 6]
]
    
]
W1 = [6, 4, 10, 10, 30, 41, 70]
W2 = [5, 2, 9, 9, 25, 35, 62]

def apply_action(matrix, action):
    new_matrix = deepcopy(matrix)
    (i, j), (x, y) = action
    new_matrix[i][j], new_matrix[x][y] = new_matrix[x][y], new_matrix[i][j]
    return new_matrix

def plot_matrix(matrix):
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix, cmap='viridis')
    fig.colorbar(cax)
    
    for (i, j), value in np.ndenumerate(matrix):
        ax.text(j, i, f'{value}', ha='center', va='center', color='white')
    
    return fig


if __name__ == "__main__":
    st.title("Simulador de Busca em Largura para Redução de Fronteiras")
    
    option = st.selectbox("Selecione W1 ou W2:", ("W1", "W2"))
    selected_W = W1 if option == "W1" else W2

    start_button = st.button("Iniciar gráficos")

    if start_button:
        for idx, instance in enumerate(instances):
            result_matrix, actions, final_borders, generations, expansions, processing_time = bfs(instance, selected_W[idx])
            st.header(f"Instância {idx + 1}:")
            st.write(f"Fronteiras iniciais: {count_borders(instance)}")
            st.write(f"Número de gerações: {generations}")
            st.write(f"Número de expansões: {expansions}")
            st.write(f"Tempo de processamento: {processing_time:.2f} seconds")
            
            current_matrix = instance
            st.subheader("Estado Inicial:")
            fig = plot_matrix(current_matrix)
            st.pyplot(fig)
            
            for idx, action in enumerate(actions):
                current_matrix = apply_action(current_matrix, action)
                st.subheader(f"Alteração {idx + 1}: {action}")
                fig = plot_matrix(current_matrix)
                st.pyplot(fig)

            st.write(f"\nFronteiras finais: {final_borders}")
            if result_matrix is not None:
                fig = plot_matrix(result_matrix)
                st.pyplot(fig)
            else:
                st.write("Não foi possível encontrar uma solução.")
            st.write("\n")