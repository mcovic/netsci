import marimo

__generated_with = "0.21.1"
app = marimo.App(
    width="medium",
    app_title="Exercise 05 — Gowalla Community Detection",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    ## ① Load Graph
    """)
    return


@app.cell
def _():
    import kagglehub
    import os
    import random
    import pandas as pd
    import networkx as nx

    path = kagglehub.dataset_download("marquis03/gowalla")
    edge_file = os.path.join(path, "Gowalla_edges.txt")
    df_edges = pd.read_csv(edge_file, sep="\t", header=None, names=["user_a", "user_b"])

    G_full = nx.from_pandas_edgelist(df_edges, source="user_a", target="user_b")

    random.seed(42)
    degrees_full = dict(G_full.degree())
    top_node = max(degrees_full, key=lambda n: degrees_full[n])
    bfs_nodes = list(nx.bfs_tree(G_full, top_node).nodes())[:2000]
    G = G_full.subgraph(bfs_nodes).copy()

    print(f"Full graph — Nodes: {G_full.number_of_nodes():,}  |  Edges: {G_full.number_of_edges():,}")
    print(f"Sample     — Nodes: {G.number_of_nodes():,}  |  Edges: {G.number_of_edges():,}")
    print(f"Connected components: {nx.number_connected_components(G)}")
    return G, nx


@app.cell
def _(mo):
    mo.md("""
    ## ② Method 1 — Louvain Community Detection
    """)
    return


@app.cell
def _(G):
    # Install check — community package provides Louvain
    try:
        import community as community_louvain
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "python-louvain", "--break-system-packages", "-q"])
        import community as community_louvain

    louvain_partition = community_louvain.best_partition(G, random_state=42)
    louvain_communities = {}
    for _node, _comm_id in louvain_partition.items():
        louvain_communities.setdefault(_comm_id, []).append(_node)

    n_louvain = len(louvain_communities)
    louvain_sizes = sorted([len(v) for v in louvain_communities.values()], reverse=True)
    louvain_modularity = community_louvain.modularity(louvain_partition, G)

    print(f"Louvain communities found: {n_louvain}")
    print(f"Modularity:                {louvain_modularity:.4f}")
    print(f"Community sizes (top 10):  {louvain_sizes[:10]}")
    print(f"Smallest community:        {louvain_sizes[-1]} node(s)")
    return louvain_modularity, louvain_partition, louvain_sizes, n_louvain


@app.cell
def _(mo):
    mo.md("""
    ## ③ Method 2 — Label Propagation
    """)
    return


@app.cell
def _(G, nx):
    import random as _r
    _r.seed(42)

    lp_communities_raw = nx.community.label_propagation_communities(G)
    lp_communities = [sorted(c) for c in lp_communities_raw]
    lp_communities.sort(key=len, reverse=True)

    n_lp = len(lp_communities)
    lp_sizes = [len(c) for c in lp_communities]

    # Build partition dict for modularity
    lp_partition = {}
    for _cid, _comm in enumerate(lp_communities):
        for _node in _comm:
            lp_partition[_node] = _cid

    lp_modularity = nx.community.modularity(G, lp_communities)

    print(f"Label propagation communities: {n_lp}")
    print(f"Modularity:                    {lp_modularity:.4f}")
    print(f"Community sizes (top 10):      {lp_sizes[:10]}")
    print(f"Smallest community:            {lp_sizes[-1]} node(s)")
    return lp_modularity, lp_sizes, n_lp


@app.cell
def _(mo):
    mo.md("""
    ## ④ Method 3 — Greedy Modularity (Hierarchical Agglomerative)
    """)
    return


@app.cell
def _(G, nx):
    greedy_communities_raw = nx.community.greedy_modularity_communities(G, resolution=1.0)
    greedy_communities = [sorted(c) for c in greedy_communities_raw]
    greedy_communities.sort(key=len, reverse=True)

    n_greedy = len(greedy_communities)
    greedy_sizes = [len(c) for c in greedy_communities]
    greedy_modularity = nx.community.modularity(G, greedy_communities)

    print(f"Greedy modularity communities: {n_greedy}")
    print(f"Modularity:                    {greedy_modularity:.4f}")
    print(f"Community sizes (top 10):      {greedy_sizes[:10]}")
    return greedy_modularity, greedy_sizes, n_greedy


@app.cell
def _(mo):
    mo.md("""
    ## ⑤ Comparison Table
    """)
    return


@app.cell
def _(
    greedy_modularity,
    greedy_sizes,
    louvain_modularity,
    louvain_sizes,
    lp_modularity,
    lp_sizes,
    mo,
    n_greedy,
    n_louvain,
    n_lp,
):
    mo.md(f"""
    ### Community Detection Comparison

    | Method | Communities | Modularity | Largest | 2nd | 3rd | Smallest |
    |---|---|---|---|---|---|---|
    | **Louvain** | {n_louvain} | {louvain_modularity:.4f} | {louvain_sizes[0]} | {louvain_sizes[1] if len(louvain_sizes)>1 else "—"} | {louvain_sizes[2] if len(louvain_sizes)>2 else "—"} | {louvain_sizes[-1]} |
    | **Label Propagation** | {n_lp} | {lp_modularity:.4f} | {lp_sizes[0]} | {lp_sizes[1] if len(lp_sizes)>1 else "—"} | {lp_sizes[2] if len(lp_sizes)>2 else "—"} | {lp_sizes[-1]} |
    | **Greedy Modularity** | {n_greedy} | {greedy_modularity:.4f} | {greedy_sizes[0]} | {greedy_sizes[1] if len(greedy_sizes)>1 else "—"} | {greedy_sizes[2] if len(greedy_sizes)>2 else "—"} | {greedy_sizes[-1]} |

    > **Modularity** ranges from −0.5 to 1.0. Values above 0.3 indicate meaningful community structure.
    > Values above 0.5 indicate strong communities. Values near 0 suggest no more structure than a random graph.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## ⑥ Bridge Nodes Between Communities
    """)
    return


@app.cell
def _(G, louvain_partition):
    # A bridge node has neighbours in more than one community
    bridge_nodes = {}
    for _node in G.nodes():
        _nbr_comms = set(louvain_partition[_nb] for _nb in G.neighbors(_node))
        _own_comm = louvain_partition[_node]
        _external_comms = _nbr_comms - {_own_comm}
        if _external_comms:
            bridge_nodes[_node] = {
                "degree": G.degree(_node),
                "own_community": _own_comm,
                "bridges_to": sorted(_external_comms),
                "n_external_comms": len(_external_comms),
            }

    # Sort by number of communities bridged, then degree
    bridge_sorted = sorted(
        bridge_nodes.items(),
        key=lambda x: (x[1]["n_external_comms"], x[1]["degree"]),
        reverse=True
    )

    print(f"Nodes with cross-community connections: {len(bridge_nodes):,} / {G.number_of_nodes():,}")
    print()
    print(f"{'Node':>8}  {'Degree':>8}  {'Own comm':>10}  {'Bridges to':>25}  {'# ext comms':>12}")
    print("-" * 70)
    for _node, _info in bridge_sorted[:15]:
        print(f"{_node:>8}  {_info['degree']:>8}  {_info['own_community']:>10}  "
              f"{str(_info['bridges_to']):>25}  {_info['n_external_comms']:>12}")
    return bridge_nodes, bridge_sorted


@app.cell
def _(bridge_sorted, mo):
    top_bridges = bridge_sorted[:5]
    mo.md(f"""
    ### Top Bridge Nodes (Louvain partition)

    | Rank | Node | Degree | Own Community | Bridges to | # External Comms |
    |---|---|---|---|---|---|
    """ + "\n".join(
        f"| {i+1} | **{n}** | {info['degree']} | {info['own_community']} | {info['bridges_to']} | {info['n_external_comms']} |"
        for i, (n, info) in enumerate(top_bridges)
    ) + """

    > Bridge nodes are users who have friends in multiple detected communities.
    > High-degree bridge nodes are the social glue connecting otherwise separate friend groups.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## ⑦ Visualization — Louvain Partition
    """)
    return


@app.cell
def _(G, bridge_nodes, louvain_partition, mo, nx):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np
    import random as _r

    _r.seed(42)

    # Sample 400 nodes — top communities by size for readability
    # Keep the top-5 communities by size, sample up to 80 nodes each
    from collections import defaultdict
    comm_to_nodes = defaultdict(list)
    for _node, _cid in louvain_partition.items():
        comm_to_nodes[_cid].append(_node)

    top_comms = sorted(comm_to_nodes.keys(), key=lambda c: len(comm_to_nodes[c]), reverse=True)[:6]
    viz_nodes = []
    for _cid in top_comms:
        _members = comm_to_nodes[_cid]
        _sample = _r.sample(_members, min(70, len(_members)))
        viz_nodes.extend(_sample)
    viz_nodes = list(set(viz_nodes))

    G_viz = G.subgraph(viz_nodes).copy()
    print(f"Visualization subgraph: {G_viz.number_of_nodes()} nodes, {G_viz.number_of_edges()} edges")

    pos = nx.spring_layout(G_viz, seed=42, k=0.5)

    # Color palette — one per community
    palette = [
        "#4f8ef7", "#f76f8e", "#50e3c2", "#f7c948",
        "#c084fc", "#fb923c", "#34d399", "#f472b6"
    ]
    comm_color = {_cid: palette[_i % len(palette)] for _i, _cid in enumerate(top_comms)}

    node_colors = []
    node_sizes = []
    for _n in G_viz.nodes():
        _cid = louvain_partition[_n]
        _is_bridge = _n in bridge_nodes and bridge_nodes[_n]["n_external_comms"] >= 2
        node_colors.append("#ffffff" if _is_bridge else comm_color.get(_cid, "#888888"))
        node_sizes.append(180 if _is_bridge else 40 + G_viz.degree(_n) * 3)

    # Edge colors — cross-community edges in light gray, within-community darker
    edge_cols = []
    for _u, _v in G_viz.edges():
        if louvain_partition[_u] != louvain_partition[_v]:
            edge_cols.append("#aaaaaa")
        else:
            edge_cols.append(comm_color.get(louvain_partition[_u], "#333333"))

    fig, ax = plt.subplots(figsize=(13, 10))
    fig.patch.set_facecolor("#0a0c17")
    ax.set_facecolor("#0a0c17")
    ax.axis("off")

    nx.draw_networkx_edges(G_viz, pos, ax=ax,
                           edge_color=edge_cols, alpha=0.35, width=0.6)
    nx.draw_networkx_nodes(G_viz, pos, ax=ax,
                           node_color=node_colors, node_size=node_sizes, alpha=0.92)

    # Legend patches
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=palette[_i], label=f"Community {_cid} ({len(comm_to_nodes[_cid])} nodes)")
        for _i, _cid in enumerate(top_comms)
    ] + [Patch(facecolor="#ffffff", label="Bridge node (2+ communities)")]

    ax.legend(handles=legend_elements, loc="upper left", framealpha=0.2,
              labelcolor="white", facecolor="#1a1d2e", fontsize=8)

    ax.set_title(
        "Gowalla Sample — Louvain Community Detection\n"
        "Node color = community  |  White nodes = cross-community bridges\n"
        "Gray edges = cross-community  |  Colored edges = within-community",
        color="#dde0f0", fontsize=11, pad=12, linespacing=1.6
    )
    plt.tight_layout()
    mo.mpl.interactive(fig)
    return


@app.cell
def _(mo):
    mo.md("""
    ## ⑧ Interpretation
    """)
    return


@app.cell
def _(
    G,
    bridge_nodes,
    bridge_sorted,
    greedy_modularity,
    louvain_modularity,
    louvain_sizes,
    lp_modularity,
    mo,
    n_greedy,
    n_louvain,
    n_lp,
):
    best_mod = max(louvain_modularity, lp_modularity, greedy_modularity)
    best_method = (
        "Louvain" if louvain_modularity == best_mod
        else "Label Propagation" if lp_modularity == best_mod
        else "Greedy Modularity"
    )
    top_bridge_node = bridge_sorted[0][0] if bridge_sorted else "N/A"
    top_bridge_info = bridge_sorted[0][1] if bridge_sorted else {}
    pct_bridges = len(bridge_nodes) / G.number_of_nodes()

    mo.md(f"""
    ### 📝 Method Note
    **Commands used:** `community.best_partition` (Louvain), `nx.community.label_propagation_communities`,
    `nx.community.greedy_modularity_communities`, `nx.community.modularity`,
    manual bridge-node detection via neighbour community comparison, `nx.spring_layout`

    ---

    ### 📋 Community Detection Summary

    | Method | Communities | Modularity |
    |---|---|---|
    | Louvain | {n_louvain} | {louvain_modularity:.4f} |
    | Label Propagation | {n_lp} | {lp_modularity:.4f} |
    | Greedy Modularity | {n_greedy} | {greedy_modularity:.4f} |

    **Best modularity: {best_mod:.4f} ({best_method})**

    ---

    ### 🧭 What the Communities Represent

    All three methods find between {min(n_louvain, n_lp, n_greedy)} and {max(n_louvain, n_lp, n_greedy)}
    communities in the 2,000-node sample. The best modularity score of **{best_mod:.4f}** indicates
    {"**strong** community structure — well above the 0.3 threshold that distinguishes meaningful communities from noise." if best_mod > 0.5
    else "**moderate** community structure — above 0.3, suggesting genuine but not sharply-separated communities." if best_mod > 0.3
    else "**weak** community structure — near 0.3 or below, suggesting the sample may be too hub-dominated for clean community separation."}

    In the Gowalla geo-social context, these communities most likely correspond to **local friendship
    circles** — groups of users who checked in at similar places and friended each other through
    geographic proximity. The largest community ({louvain_sizes[0]} nodes in Louvain) probably
    represents the dense core around hub node 307, which connects to almost everyone in the sample.
    Smaller communities ({louvain_sizes[-1]}–{louvain_sizes[2] if len(louvain_sizes) > 2 else louvain_sizes[-1]} nodes)
    are likely more cohesive local subgroups — tighter friend circles that share a specific neighbourhood
    or venue cluster.

    **Why the methods disagree on count ({n_louvain} vs {n_lp} vs {n_greedy}):**
    Louvain optimises modularity directly via a greedy hill-climb and tends to find a moderate number
    of well-separated communities. Label propagation is stochastic and can over-split or merge communities
    depending on the propagation order. Greedy modularity merges communities bottom-up and typically
    produces fewer, larger communities. The disagreement in count but agreement in overall modularity
    range means the *total community structure is consistent*, but the exact boundaries between
    smaller communities are ambiguous — a sign of overlapping social circles rather than hard partitions.

    **Bridge nodes:** {len(bridge_nodes):,} of {G.number_of_nodes():,} nodes ({pct_bridges:.1%}) connect
    to at least one other community. The top bridge node is **{top_bridge_node}**
    (degree {top_bridge_info.get('degree', '?')}, spanning {top_bridge_info.get('n_external_comms', '?')} communities).
    In Gowalla terms, these are users whose friendship network crosses geographic or social boundaries —
    people who moved between areas, attended events across different social circles, or acted as
    connectors between otherwise separate local groups. They are the most important users for
    information diffusion and network cohesion despite not necessarily being the most popular.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
