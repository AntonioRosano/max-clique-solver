import networkx as nx
import random
from typing import Set, List, Dict, Tuple

def _calculate_scores(G: nx.Graph) -> Dict[int, float]:
    """
    Funzione helper: Calcola lo score per ogni nodo.
    Score(u) = deg(u) / avg_deg(neighbors).
    """
    deg = dict(G.degree())
    score = {}
    
    for u in G.nodes():
        neighbors = list(G.neighbors(u))
        if not neighbors:
            score[u] = 0.0
        else:
            avg_neighbor_deg = sum(deg[v] for v in neighbors) / len(neighbors)
            if avg_neighbor_deg > 0:
                score[u] = deg[u] / avg_neighbor_deg
            else:
                score[u] = 0.0
    return score

def solve_score_tie_breaking(G: nx.Graph, num_iter: int = 5000) -> Set[int]:
    """
    [TESI SEZIONE 2.2.1]
    Greedy score-based con tie-breaking randomizzato.
    I nodi con lo stesso score vengono mescolati tra loro.
    """
    best_solution = set()
    
    # 1. Calcolo score (una volta sola)
    score_map = _calculate_scores(G)
    
    # 2. Raggruppa nodi per score
    # Struttura: { 1.5: [nodo1, nodo3], 1.2: [nodo2], ... }
    nodes_by_score: Dict[float, List[int]] = {}
    for u, s in score_map.items():
        if s not in nodes_by_score:
            nodes_by_score[s] = []
        nodes_by_score[s].append(u)
    
    # Ordina gli score unici dal più alto al più basso
    sorted_scores = sorted(nodes_by_score.keys(), reverse=True)

    for _ in range(num_iter):
        # 3. Costruisci l'ordine di visita per questa iterazione
        current_order = []
        for s in sorted_scores:
            group = nodes_by_score[s][:] # Copia la lista
            random.shuffle(group)        # Mischia il gruppo (Random Tie-Breaking)
            current_order.extend(group)
            
        # 4. Costruzione Greedy Standard
        current_clique = set()
        for u in current_order:
            # Aggiungi se è connesso a TUTTI i nodi già nella clique
            if all(G.has_edge(u, v) for v in current_clique):
                current_clique.add(u)
        
        if len(current_clique) > len(best_solution):
            best_solution = current_clique

    return best_solution


def solve_score_top_k(G: nx.Graph, num_iter: int = 5000, top_k_ratio: float = 0.02) -> Set[int]:
    """
    [TESI SEZIONE 2.2.2]
    Greedy score-based con selezione randomizzata tra i Top-K compatibili.
    """
    best_solution = set()
    
    # 1. Calcolo e Ordinamento Globale
    score_map = _calculate_scores(G)
    # Lista di tutti i nodi ordinati rigidamente per score decrescente
    global_sorted_nodes = sorted(score_map.keys(), key=lambda x: score_map[x], reverse=True)
    
    # Pool size iniziale
    initial_k = max(1, int(len(G) * top_k_ratio))

    for _ in range(num_iter):
        current_clique = set()
        
        # 2. Scelta del primo nodo (random tra i top-k globali)
        start_node = random.choice(global_sorted_nodes[:initial_k])
        current_clique.add(start_node)
        
        # Nodi rimanenti (potenziali candidati)
        remaining = set(G.nodes()) - current_clique
        
        # 3. Espansione della clique
        while True:
            # A. Trova tutti i nodi compatibili con la clique attuale
            # (Devono essere vicini a TUTTI i membri della clique)
            compatible_candidates = []
            for n in remaining:
                if all(G.has_edge(n, member) for member in current_clique):
                    compatible_candidates.append(n)
            
            if not compatible_candidates:
                break
                
            # B. Filtraggio Top-K basato sull'ordine globale
            # Dobbiamo prendere i 'k' migliori candidati secondo lo score originale.
            # L'intersezione tra 'global_sorted_nodes' e 'compatible_candidates' 
            # mantiene l'ordinamento implicito.
            
            valid_pool = []
            pool_limit = max(1, int(len(compatible_candidates) * top_k_ratio))
            
            # Scorrere la lista globale è efficiente per mantenere l'ordine
            count = 0
            for node in global_sorted_nodes:
                if node in compatible_candidates: # Check rapido (se compatible_candidates fosse un set sarebbe O(1))
                    valid_pool.append(node)
                    count += 1
                    if count >= pool_limit:
                        break
            
            # C. Scelta random dal pool ristretto
            next_node = random.choice(valid_pool)
            current_clique.add(next_node)
            
            # Aggiorna rimanenti: Rimuovi nodo scelto e chi non è suo vicino
            # (Ottimizzazione importante per ridurre i check futuri)
            remaining.remove(next_node)
            remaining = {n for n in remaining if G.has_edge(next_node, n)}

        if len(current_clique) > len(best_solution):
            best_solution = current_clique

    return best_solution