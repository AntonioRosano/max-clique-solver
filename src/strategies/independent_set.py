import networkx as nx
import random
from typing import Set, List

def solve_is_min_degree(G: nx.Graph, num_iter: int = 5000) -> Set[int]:
    """
    [TESI SEZIONE 2.1.1]
    Algoritmo greedy randomizzato con selezione tra vertici a grado minimo.
    Lavora sul grafo complemento per trovare una Clique (equivalente a IS su H).
    """
    # Lavoriamo sul complemento (H) perché cerchiamo una Clique in G
    H = nx.complement(G)
    
    # Precomputazione adiacenze
    adjacency = {u: set(H.neighbors(u)) for u in H.nodes()}
    best_solution = set()

    for _ in range(num_iter):
        remaining_nodes = set(H.nodes())
        independent_set = set()

        while remaining_nodes:
            # 1. Calcola i gradi nel sottografo indotto dai nodi rimanenti
            degrees = {u: len(adjacency[u] & remaining_nodes) for u in remaining_nodes}
            
            if not degrees:
                break
            
            # 2. Trova il grado minimo
            min_deg = min(degrees.values())
            
            # 3. Candidati: TUTTI i nodi che hanno quel grado minimo
            candidates = [u for u, d in degrees.items() if d == min_deg]

            # 4. Scelta casuale (Randomized)
            u = random.choice(candidates)
            independent_set.add(u)

            # 5. Rimozione nodo e vicini (proprietà Independent Set)
            to_remove = {u} | (adjacency[u] & remaining_nodes)
            remaining_nodes -= to_remove

        if len(independent_set) > len(best_solution):
            best_solution = independent_set

    return best_solution


def solve_is_k_min_degree(G: nx.Graph, k: int, num_iter: int = 5000) -> Set[int]:
    """
    [TESI SEZIONE 2.1.2]
    Algoritmo greedy randomizzato con scelta tra i k vertici meno connessi.
    
    Args:
        G (nx.Graph): Il grafo originale.
        k (int): Numero di candidati da considerare (es. 3 o 10).
        num_iter (int): Numero di iterazioni.
    """
    H = nx.complement(G)
    adjacency = {u: set(H.neighbors(u)) for u in H.nodes()}
    best_solution = set()

    for _ in range(num_iter):
        remaining_nodes = set(H.nodes())
        independent_set = set()

        while remaining_nodes:
            # 1. Calcola i gradi dinamici
            degrees = {u: len(adjacency[u] & remaining_nodes) for u in remaining_nodes}
            
            if not degrees:
                break
            
            # 2. Ordina i nodi per grado crescente
            # (Sort è O(N log N), un po' più lento del min() puro, ma necessario qui)
            sorted_nodes = sorted(degrees.keys(), key=lambda x: degrees[x])
            
            # 3. Candidati: I primi k nodi della lista ordinata
            # Se ci sono meno di k nodi, li prendiamo tutti
            slice_idx = min(len(sorted_nodes), k)
            candidates = sorted_nodes[:slice_idx]

            # 4. Scelta casuale tra i top k
            u = random.choice(candidates)
            independent_set.add(u)

            # 5. Rimozione
            to_remove = {u} | (adjacency[u] & remaining_nodes)
            remaining_nodes -= to_remove

        if len(independent_set) > len(best_solution):
            best_solution = independent_set

    return best_solution