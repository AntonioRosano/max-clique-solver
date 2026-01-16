import networkx as nx
import random
from typing import Set, List, Tuple

# =============================================================================
# HELPER FUNCTIONS (Funzioni di supporto interne)
# =============================================================================

def _reduce_to_minimal(G: nx.Graph, cover: Set[int]) -> Set[int]:
    """
    Riduce un Vertex Cover rimuovendo i nodi ridondanti.
    Un nodo è ridondante se, rimuovendolo, tutti gli archi sono ancora coperti
    dagli altri nodi del cover.
    """
    cover = cover.copy()
    edges = list(G.edges())
    
    # Mescoliamo l'ordine di verifica per variare il risultato della riduzione
    nodes_to_check = list(cover)
    random.shuffle(nodes_to_check)
    
    for u in nodes_to_check:
        # Proviamo a rimuovere u
        temp_cover = cover - {u}
        
        # Verifica se temp_cover è ancora un Vertex Cover valido
        # Un cover è valido se per ogni arco (x, y), almeno uno tra x o y è nel cover.
        is_valid = True
        for x, y in edges:
            if x not in temp_cover and y not in temp_cover:
                is_valid = False
                break
        
        if is_valid:
            cover = temp_cover

    return cover

def _heuristic_max_degree(G: nx.Graph) -> Set[int]:
    """Costruisce un VC scegliendo iterativamente i nodi di grado massimo."""
    G_copy = G.copy()
    cover = set()

    while G_copy.number_of_edges() > 0:
        # Dizionario gradi attuali
        degrees = dict(G_copy.degree())
        if not degrees: break
        
        max_deg = max(degrees.values())
        # Tie-breaking casuale tra i nodi con grado massimo
        candidates = [n for n, d in degrees.items() if d == max_deg]
        u = random.choice(candidates)
        
        cover.add(u)
        G_copy.remove_node(u)
        
    return cover

def _heuristic_max_matching(G: nx.Graph) -> Set[int]:
    """
    [TESI 2.3.2] Costruisce un VC basato su Matching Massimale Casuale.
    Tutti i nodi che toccano gli archi del matching formano il cover.
    """
    edges = list(G.edges())
    random.shuffle(edges) # Randomizzazione fondamentale
    
    cover = set()
    covered_nodes = set() # Per tenere traccia rapida di chi è già coperto/usato
    
    for u, v in edges:
        # Se l'arco è "libero" (nessuno dei due estremi è già nel matching)
        if u not in covered_nodes and v not in covered_nodes:
            # Aggiungiamo l'arco al matching -> aggiungiamo i nodi al cover
            cover.add(u)
            cover.add(v)
            covered_nodes.add(u)
            covered_nodes.add(v)
            
    # Nota teorica: I nodi incidenti a un matching massimale sono un Vertex Cover valido
    # (approssimazione fattore 2).
    return cover

# =============================================================================
# PUBLIC FUNCTIONS (Le strategie richiamabili dal main)
# =============================================================================

def solve_vc_max_degree(G: nx.Graph, num_iter: int = 5000) -> Set[int]:
    """
    [TESI SEZIONE 2.3.1]
    Clique via Vertex Cover (approccio Grado Massimo) su Grafo Complementare.
    """
    
    H = nx.complement(G)
    all_nodes = set(G.nodes())
    
    best_vc = set()
    min_vc_size = float('inf')
    
    # 1. Fase Iterativa: Trova diverse cover grezze
    for _ in range(num_iter):
        vc = _heuristic_max_degree(H)
        
        if len(vc) < min_vc_size:
            min_vc_size = len(vc)
            best_vc = vc

    if not best_vc and min_vc_size == float('inf'):
        return set() # Caso grafo vuoto

    # 2. Fase di Riduzione (eseguita solo sulla migliore trovata)
    vc_minimal = _reduce_to_minimal(H, best_vc)
    
    # 3. Conversione: Clique = V - VertexCover(H)
    return all_nodes - vc_minimal


def solve_vc_matching(G: nx.Graph, num_iter: int = 5000) -> Set[int]:
    """
    [TESI SEZIONE 2.3.2]
    Clique via Vertex Cover (approccio Matching Casuale) su Grafo Complementare.
    """
    H = nx.complement(G)
    all_nodes = set(G.nodes())
    
    best_vc = set()
    min_vc_size = float('inf')
    
    # 1. Fase Iterativa
    for _ in range(num_iter):
        # Genera cover tramite matching
        vc = _heuristic_max_matching(H)
        
        if len(vc) < min_vc_size:
            min_vc_size = len(vc)
            best_vc = vc

    if not best_vc and min_vc_size == float('inf'):
        return set()

    # 2. Fase di Riduzione
    vc_minimal = _reduce_to_minimal(H, best_vc)
    
    # 3. Conversione
    return all_nodes - vc_minimal