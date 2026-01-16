import time
import os
import networkx as nx
from src.loader import load_dimacs_graph
from src.local_search import iterative_local_search


from src.strategies.independent_set import solve_is_min_degree, solve_is_k_min_degree
from src.strategies.local_score import solve_score_tie_breaking, solve_score_top_k
from src.strategies.vertex_cover import solve_vc_max_degree, solve_vc_matching

# --- GLOBAL CONFIGURATION ---
FILENAME = "p_hat300-1.txt"
DATA_FILE = os.path.join("data", FILENAME) 


NUM_ITER_CONSTRUCTIVE = 1000  
ILS_MAX_ITER = 500            
ILS_PERTURBATION_K = 2        

def verify_clique(G: nx.Graph, clique: set) -> bool:
    """Verifica che l'insieme di nodi sia davvero una cricca."""
    nodes = list(clique)
    # Verifica ogni coppia di nodi
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if not G.has_edge(nodes[i], nodes[j]):
                return False
    return True

def run_experiment(G: nx.Graph, strategy_name: str, strategy_func):
    """
    Esegue un esperimento completo: Costruzione + ILS + Report.
    """
    print(f"\n{'='*60}")
    print(f"ESPERIMENTO: {strategy_name}")
    print(f"{'='*60}")

    # 1. FASE COSTRUTTIVA
    print(f"[*] Avvio fase costruttiva ({NUM_ITER_CONSTRUCTIVE} iterazioni)...")
    start_time = time.time()
    

    initial_solution = strategy_func(G)
    
    heuristic_time = time.time() - start_time
    print(f"    -> Migliore soluzione trovata: {len(initial_solution)} nodi")
    print(f"    -> Tempo impiegato: {heuristic_time:.4f} sec")

    # 2. FASE OTTIMIZZAZIONE (ILS)
    print(f"[*] Avvio Iterated Local Search (Max Iter: {ILS_MAX_ITER}, Perturb: {ILS_PERTURBATION_K})...")
    start_ils = time.time()
    
    final_solution = iterative_local_search(
        G, 
        initial_solution, 
        max_iter=ILS_MAX_ITER, 
        k=ILS_PERTURBATION_K
    )
    
    ils_time = time.time() - start_ils
    print(f"    -> Soluzione finale dopo ILS: {len(final_solution)} nodi")
    print(f"    -> Tempo ILS: {ils_time:.4f} sec")

    # 3. VERIFICA E REPORT
    is_valid = verify_clique(G, final_solution)
    total_time = heuristic_time + ils_time
    
    print("-" * 30)
    print(f"RISULTATO FINALE: {strategy_name}")
    print(f"File:             {FILENAME}")
    print(f"Validità Cricca:  {'OK' if is_valid else 'ERRORE'}")
    print(f"Dimensione:       {len(final_solution)}")
    print(f"Tempo Totale:     {total_time:.4f} sec")
    print("-" * 30)

def main():
    # 1. Caricamento Grafo
    print(f"Caricamento del grafo da: {DATA_FILE}")
    try:
        G = load_dimacs_graph(DATA_FILE)
        print(f"Grafo caricato: {G.number_of_nodes()} nodi, {G.number_of_edges()} archi.")
    except FileNotFoundError:
        print(f"ERRORE CRITICO: Non trovo il file in {DATA_FILE}")
        print(f"Controlla che il file '{FILENAME}' sia dentro la cartella 'data'.")
        return

    # 2. Definizione delle Strategie
    strategies = {
        "1": ("IS - Min Degree (Sez 2.1.1)", 
              lambda g: solve_is_min_degree(g, num_iter=NUM_ITER_CONSTRUCTIVE)),
        
        "2": ("IS - K-Min Degree (Sez 2.1.2)", 
              lambda g: solve_is_k_min_degree(g, k=10, num_iter=NUM_ITER_CONSTRUCTIVE)),
        
        "3": ("Score - Random Tie (Sez 2.2.1)", 
              lambda g: solve_score_tie_breaking(g, num_iter=NUM_ITER_CONSTRUCTIVE)),
        
        "4": ("Score - Top-K (Sez 2.2.2)", 
              lambda g: solve_score_top_k(g, top_k_ratio=0.02, num_iter=NUM_ITER_CONSTRUCTIVE)),
        
        "5": ("VC - Max Degree (Sez 2.3.1)", 
              lambda g: solve_vc_max_degree(g, num_iter=NUM_ITER_CONSTRUCTIVE)),
        
        "6": ("VC - Matching (Sez 2.3.2)", 
              lambda g: solve_vc_matching(g, num_iter=NUM_ITER_CONSTRUCTIVE))
    }

    # 3. Menu Interattivo
    while True:
        print("\nSeleziona l'algoritmo da testare:")
        for key, (name, _) in strategies.items():
            print(f"  {key}. {name}")
        print("  0. Esci")
        
        choice = input("\nScelta (0-6): ")
        
        if choice == "0":
            print("Uscita.")
            break
        elif choice in strategies:
            algo_name, algo_func = strategies[choice]
            run_experiment(G, algo_name, algo_func)
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()