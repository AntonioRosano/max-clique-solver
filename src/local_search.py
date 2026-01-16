import networkx as nx
import random
from typing import Set

# =============================================================================
# HELPER: Euristica per trovare una cricca nei candidati
# =============================================================================
def _greedy_clique_on_candidates(G: nx.Graph, candidates: Set[int]) -> Set[int]:
    if not candidates:
        return set()
    
    subgraph = G.subgraph(candidates)
    sorted_nodes = sorted(list(subgraph.nodes()), key=lambda n: subgraph.degree(n), reverse=True)
    
    new_clique = set()
    for node in sorted_nodes:
        if all(G.has_edge(node, existing) for existing in new_clique):
            new_clique.add(node)
            
    return new_clique

# =============================================================================
# SEZIONE 3.1: PERTURBAZIONE
# =============================================================================
def perturbation(clique: Set[int], k: int) -> Set[int]:
    C = clique.copy()
    if k >= len(C):
        if not C:
            return set()
        return {random.choice(list(C))}

    nodes_to_remove = random.sample(list(C), k)
    for node in nodes_to_remove:
        C.remove(node)
    return C

# =============================================================================
# SEZIONE 3.2: LOCAL SEARCH (1,k)-swap
# =============================================================================
def local_search(initial_clique: Set[int], G: nx.Graph) -> Set[int]:
    C = initial_clique.copy()
    improved = True

    while improved:
        improved = False
        nodes_to_check = list(C)
        
        for u in nodes_to_check:
            C_prime = C - {u}
            
            if not C_prime:
                candidates = set(G.nodes()) - {u}
            else:
                iterator = iter(C_prime)
                first_node = next(iterator)
                candidates = set(G.neighbors(first_node))
                for member in iterator:
                    candidates.intersection_update(G.neighbors(member))
                candidates -= C

            K = _greedy_clique_on_candidates(G, candidates)
            
            if len(K) > 1:
                C = C_prime.union(K)
                improved = True
                break 

    return C

# =============================================================================
# SEZIONE 3.3: ITERATIVE LOCAL SEARCH
# =============================================================================
def iterative_local_search(G: nx.Graph, initial_solution: Set[int], max_iter: int, k: int) -> Set[int]:
    print(f"--- Avvio ILS (Max Iter: {max_iter}, k={k}) ---")

    C_best = local_search(initial_solution, G)
    C_ref = C_best
    
    print(f"Start ILS -> Ottimo locale iniziale: {len(C_best)}")

    for i in range(max_iter):
        C_prime = perturbation(C_ref, k)
        C_double_prime = local_search(C_prime, G)
        
        if len(C_double_prime) > len(C_best):
            print(f"[Iter {i+1}] Nuovo record globale trovato: {len(C_double_prime)}")
            C_best = C_double_prime
            C_ref = C_double_prime
            
    return C_best