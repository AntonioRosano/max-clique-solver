import networkx as nx
from pathlib import Path


def load_dimacs_graph(path: str | Path) -> nx.Graph:
    """
    Load an undirected graph from a DIMACS-like edge list file.

    Expected format:
        Lines starting with 'e u v' define an edge between nodes u and v.

    Parameters
    ----------
    path : str or Path
        Path to the DIMACS graph file.

    Returns
    -------
    nx.Graph
        The loaded undirected graph.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Graph file not found: {path}")

    G = nx.Graph()

    with path.open("r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("c"):
                # Skip empty lines and comments
                continue

            if line.startswith("e"):
                _, u, v = line.split()
                G.add_edge(int(u), int(v))

    return G