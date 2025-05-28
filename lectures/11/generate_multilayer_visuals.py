#!/usr/bin/env python3
"""
Generate visualization images for Multi-layer Networks lecture.

Required packages:
- networkx>=2.6
- matplotlib>=3.4
- numpy>=1.20
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as mpatches

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)


def save_figure(filename, figsize=(12, 8), dpi=100):
    """Save figure with consistent formatting."""
    plt.tight_layout()
    plt.savefig(f'images/{filename}', dpi=dpi, bbox_inches='tight')
    plt.close()


def generate_monoplex_vs_multiplex():
    """Generate comparison visualization between monoplex and multiplex."""
    print("Generating monoplex vs multiplex comparison...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Create a sample network with 8 nodes
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    # Define different types of connections
    friendship_edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'E'),
                       ('F', 'G')]
    work_edges = [('A', 'C'), ('B', 'D'), ('E', 'F'), ('G', 'H'),
                 ('A', 'F')]
    family_edges = [('B', 'E'), ('C', 'F'), ('D', 'G'), ('A', 'H')]

    # Create monoplex network (aggregated)
    G_mono = nx.Graph()
    G_mono.add_nodes_from(nodes)
    all_edges = friendship_edges + work_edges + family_edges
    G_mono.add_edges_from(all_edges)

    # Position nodes in a circle for consistency
    pos = nx.circular_layout(G_mono)

    # Plot monoplex network
    ax1.set_title('Monoplex Network\n(All relationships aggregated)',
                  fontsize=14, fontweight='bold')
    nx.draw(G_mono, pos, ax=ax1,
            node_color='lightblue',
            node_size=800,
            edge_color='gray',
            width=2,
            with_labels=True,
            font_size=12,
            font_weight='bold')

    # Add legend for monoplex
    legend_elements = [mpatches.Patch(color='gray', label='All relationships')]
    ax1.legend(handles=legend_elements, loc='upper right')

    # Plot multiplex network with layer separation
    ax2.set_title('Multiplex Network\n(Separate relationship layers)',
                  fontsize=14, fontweight='bold')

    # Adjust positions slightly for each layer to show separation
    layer_offsets = {'friendship': (0, 0.1), 'work': (0, 0),
                     'family': (0, -0.1)}
    colors = {'friendship': 'red', 'work': 'blue', 'family': 'green'}

    # Draw nodes once
    nx.draw_networkx_nodes(G_mono, pos, ax=ax2,
                           node_color='lightgray',
                           node_size=800)

    # Draw labels
    nx.draw_networkx_labels(G_mono, pos, ax=ax2,
                            font_size=12,
                            font_weight='bold')

    # Draw edges for each layer with different colors and slight offsets
    for layer, edges in [('friendship', friendship_edges),
                         ('work', work_edges),
                         ('family', family_edges)]:

        # Create temporary graph for this layer
        G_layer = nx.Graph()
        G_layer.add_nodes_from(nodes)
        G_layer.add_edges_from(edges)

        # Adjust positions slightly for visual separation
        offset_pos = {node: (x + layer_offsets[layer][0],
                             y + layer_offsets[layer][1])
                      for node, (x, y) in pos.items()}

        # Draw only edges for this layer
        nx.draw_networkx_edges(G_layer, offset_pos, ax=ax2,
                               edge_color=colors[layer],
                               width=2.5,
                               alpha=0.8)

    # Add legend for multiplex
    legend_elements = [
        mpatches.Patch(color='red', label='Friendship layer'),
        mpatches.Patch(color='blue', label='Work layer'),
        mpatches.Patch(color='green', label='Family layer')
    ]
    ax2.legend(handles=legend_elements, loc='upper right')

    # Remove axes
    ax1.axis('off')
    ax2.axis('off')

    # Add explanatory text
    fig.suptitle('Network Representation Comparison', fontsize=16,
                 fontweight='bold', y=0.95)

    plt.tight_layout()
    save_figure('monoplex_vs_multiplex.png', figsize=(14, 7))


def generate_layer_coupling_types():
    """Generate visualization of different interlayer coupling types."""
    print("Generating layer coupling types...")

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    # Create base positions for 4 nodes
    base_pos = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}

    coupling_types = [
        ('Diagonal (Identity)', 'Each node connects to itself across layers'),
        ('Categorical', 'Nodes grouped by attributes'),
        ('Ordinal', 'Sequential layer connections'),
        ('General', 'Arbitrary cross-layer connections')
    ]

    for idx, (title, description) in enumerate(coupling_types):
        ax = axes[idx]
        ax.set_title(f'{title}\n{description}', fontsize=11,
                     fontweight='bold')

        # Draw two layers
        layer_spacing = 2.5

        # Layer 1 (bottom)
        for node, (x, y) in base_pos.items():
            circle1 = plt.Circle((x, y), 0.15, color='lightblue', alpha=0.7)
            ax.add_patch(circle1)
            ax.text(x, y, str(node), ha='center', va='center',
                    fontweight='bold')

        # Layer 2 (top)
        for node, (x, y) in base_pos.items():
            y_top = y + layer_spacing
            circle2 = plt.Circle((x, y_top), 0.15, color='lightcoral',
                                alpha=0.7)
            ax.add_patch(circle2)
            ax.text(x, y_top, str(node), ha='center', va='center',
                    fontweight='bold')

        # Draw interlayer connections based on type
        if idx == 0:  # Diagonal (Identity)
            for node, (x, y) in base_pos.items():
                ax.plot([x, x], [y + 0.15, y + layer_spacing - 0.15],
                        'k--', linewidth=2, alpha=0.6)

        elif idx == 1:  # Categorical
            # Connect nodes 0,1 to 0,1 and nodes 2,3 to 2,3
            for group in [(0, 1), (2, 3)]:
                for n1 in group:
                    for n2 in group:
                        x1, y1 = base_pos[n1]
                        x2, y2 = base_pos[n2]
                        ax.plot([x1, x2], [y1 + 0.15,
                                          y2 + layer_spacing - 0.15],
                                'k--', linewidth=1.5, alpha=0.4)

        elif idx == 2:  # Ordinal
            # Sequential connections
            connections = [(0, 1), (1, 2), (2, 3), (3, 0)]
            for n1, n2 in connections:
                x1, y1 = base_pos[n1]
                x2, y2 = base_pos[n2]
                ax.plot([x1, x2], [y1 + 0.15, y2 + layer_spacing - 0.15],
                        'k--', linewidth=2, alpha=0.6)

        else:  # General
            # Random connections
            connections = [(0, 2), (1, 3), (2, 0), (3, 1)]
            for n1, n2 in connections:
                x1, y1 = base_pos[n1]
                x2, y2 = base_pos[n2]
                ax.plot([x1, x2], [y1 + 0.15, y2 + layer_spacing - 0.15],
                        'k--', linewidth=2, alpha=0.6)

        # Add layer labels
        ax.text(-0.3, layer_spacing/2 + 0.5, 'Layer 2', rotation=90,
                ha='center', va='center', fontweight='bold', color='red')
        ax.text(-0.3, layer_spacing/2 - 0.5, 'Layer 1', rotation=90,
                ha='center', va='center', fontweight='bold', color='blue')

        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, layer_spacing + 0.5)
        ax.set_aspect('equal')
        ax.axis('off')

    plt.tight_layout()
    save_figure('interlayer_coupling_types.png', figsize=(12, 10))


def generate_multiplex_measures_example():
    """Generate visualization showing different multiplex degree measures."""
    print("Generating multiplex measures example...")

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Create a multiplex network with 3 layers
    nodes = ['A', 'B', 'C', 'D', 'E']

    # Define edges for each layer
    layer1_edges = [('A', 'B'), ('B', 'C'), ('C', 'A')]
    layer2_edges = [('A', 'D'), ('D', 'E'), ('B', 'E')]
    layer3_edges = [('C', 'D'), ('D', 'B'), ('E', 'A')]

    # Position nodes
    pos = nx.circular_layout(nx.Graph(layer1_edges + layer2_edges +
                                     layer3_edges))

    layer_colors = ['red', 'blue', 'green']
    layer_names = ['Social', 'Work', 'Family']
    layer_y_offsets = [1.5, 0, -1.5]

    # Draw each layer separately
    for layer_idx, (edges, color, name, y_offset) in enumerate(zip(
        [layer1_edges, layer2_edges, layer3_edges],
        layer_colors, layer_names, layer_y_offsets
    )):
        # Adjust positions for layer separation
        layer_pos = {node: (x, y + y_offset) for node, (x, y) in pos.items()}

        # Create graph for this layer
        G_layer = nx.Graph()
        G_layer.add_nodes_from(nodes)
        G_layer.add_edges_from(edges)

        # Draw layer
        nx.draw(G_layer, layer_pos, ax=ax,
                node_color=color,
                node_size=1000,
                edge_color=color,
                width=3,
                alpha=0.7,
                with_labels=True,
                font_size=12,
                font_weight='bold',
                font_color='white')

        # Add layer label
        ax.text(-1.8, y_offset, f'{name}\nLayer', ha='center', va='center',
                fontsize=12, fontweight='bold', color=color,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white',
                         alpha=0.8))

    # Draw interlayer connections (diagonal coupling)
    for node in nodes:
        x, y = pos[node]
        # Connect across all three layers
        ax.plot([x, x, x], [y + 1.5, y, y - 1.5], 'k--',
                linewidth=2, alpha=0.5, zorder=0)

    # Add annotations for node A showing different degree measures
    x_a, y_a = pos['A']

    # Intralayer degrees
    ax.annotate('Social degree: 2', xy=(x_a, y_a + 1.5),
                xytext=(x_a + 1, y_a + 2),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, fontweight='bold', color='red')

    ax.annotate('Work degree: 1', xy=(x_a, y_a),
                xytext=(x_a + 1, y_a + 0.5),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2),
                fontsize=10, fontweight='bold', color='blue')

    ax.annotate('Family degree: 1', xy=(x_a, y_a - 1.5),
                xytext=(x_a + 1, y_a - 1),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=10, fontweight='bold', color='green')

    # Total degree annotation
    ax.text(x_a - 1.5, y_a,
            'Node A:\nTotal degree = 4\nOverlapping degree = 3\n' +
            '(active in 3 layers)',
            ha='center', va='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow',
                     alpha=0.8))

    ax.set_title('Multiplex Network Degree Measures', fontsize=16,
                 fontweight='bold')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

    # Add legend
    legend_elements = [
        mpatches.Patch(color='red', label='Social Layer'),
        mpatches.Patch(color='blue', label='Work Layer'),
        mpatches.Patch(color='green', label='Family Layer'),
        mpatches.Patch(color='gray', label='Interlayer connections')
    ]
    ax.legend(handles=legend_elements, loc='upper left')

    save_figure('multiplex_measures_example.png', figsize=(12, 8))


def generate_supra_adjacency_example():
    """Generate visualization of supra-adjacency matrix structure."""
    print("Generating supra-adjacency matrix example...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Create a simple 3-node, 2-layer multiplex network
    nodes = ['A', 'B', 'C']
    n_nodes = len(nodes)
    n_layers = 2

    # Create adjacency matrices for each layer
    A1 = np.array([[0, 1, 0],
                   [1, 0, 1],
                   [0, 1, 0]])  # Layer 1: A-B-C chain

    A2 = np.array([[0, 0, 1],
                   [0, 0, 1],
                   [1, 1, 0]])  # Layer 2: A-C, B-C triangle

    # Create interlayer coupling (identity)
    B12 = np.eye(n_nodes)  # Identity coupling
    B21 = np.eye(n_nodes)

    # Construct supra-adjacency matrix
    supra_adj = np.block([[A1, B12],
                         [B21, A2]])

    # Plot the multiplex network structure
    ax1.set_title('Multiplex Network\n(2 layers, 3 nodes)',
                  fontsize=12, fontweight='bold')

    # Layer positions
    layer1_pos = {i: (i, 0) for i in range(n_nodes)}
    layer2_pos = {i: (i, 1.5) for i in range(n_nodes)}

    # Draw layer 1
    G1 = nx.from_numpy_array(A1)
    nx.draw(G1, layer1_pos, ax=ax1,
            node_color='lightblue',
            node_size=800,
            edge_color='blue',
            width=3,
            with_labels=False)

    # Draw layer 2
    G2 = nx.from_numpy_array(A2)
    nx.draw(G2, layer2_pos, ax=ax1,
            node_color='lightcoral',
            node_size=800,
            edge_color='red',
            width=3,
            with_labels=False)

    # Draw interlayer connections
    for i in range(n_nodes):
        ax1.plot([i, i], [0, 1.5], 'k--', linewidth=2, alpha=0.6)

    # Add node labels
    for i, label in enumerate(nodes):
        ax1.text(i, -0.2, f'{label}₁', ha='center', va='center',
                 fontweight='bold')
        ax1.text(i, 1.7, f'{label}₂', ha='center', va='center',
                 fontweight='bold')

    # Add layer labels
    ax1.text(-0.5, 0, 'Layer 1', rotation=90, ha='center', va='center',
             fontweight='bold', color='blue')
    ax1.text(-0.5, 1.5, 'Layer 2', rotation=90, ha='center', va='center',
             fontweight='bold', color='red')

    ax1.set_xlim(-1, 3)
    ax1.set_ylim(-0.5, 2)
    ax1.axis('off')

    # Plot supra-adjacency matrix
    ax2.set_title('Supra-Adjacency Matrix', fontsize=12, fontweight='bold')
    im = ax2.imshow(supra_adj, cmap='Blues', alpha=0.8)

    # Add matrix values
    for i in range(supra_adj.shape[0]):
        for j in range(supra_adj.shape[1]):
            ax2.text(j, i, str(int(supra_adj[i, j])),
                     ha='center', va='center', fontweight='bold',
                     fontsize=12)

    # Add grid lines to separate blocks
    ax2.axhline(y=2.5, color='red', linewidth=3)
    ax2.axvline(x=2.5, color='red', linewidth=3)

    # Label the blocks
    ax2.text(1, -0.5, 'Layer 1', ha='center', va='center',
             fontweight='bold', color='blue')
    ax2.text(4, -0.5, 'Layer 2', ha='center', va='center',
             fontweight='bold', color='red')
    ax2.text(-0.5, 1, 'Layer 1', rotation=90, ha='center', va='center',
             fontweight='bold', color='blue')
    ax2.text(-0.5, 4, 'Layer 2', rotation=90, ha='center', va='center',
             fontweight='bold', color='red')

    # Add block labels
    ax2.text(1, 1, 'A₁', ha='center', va='center', fontweight='bold',
             fontsize=10, color='white')
    ax2.text(4, 4, 'A₂', ha='center', va='center', fontweight='bold',
             fontsize=10, color='white')
    ax2.text(1, 4, 'B₁₂', ha='center', va='center', fontweight='bold',
             fontsize=10)
    ax2.text(4, 1, 'B₂₁', ha='center', va='center', fontweight='bold',
             fontsize=10)

    # Set node labels
    node_labels = ([f'{node}₁' for node in nodes] +
                   [f'{node}₂' for node in nodes])
    ax2.set_xticks(range(len(node_labels)))
    ax2.set_yticks(range(len(node_labels)))
    ax2.set_xticklabels(node_labels)
    ax2.set_yticklabels(node_labels)

    plt.tight_layout()
    save_figure('supra_adjacency_example.png', figsize=(14, 6))


if __name__ == "__main__":
    print("Generating images for Multi-layer Networks lecture...")

    # Generate all visualizations
    generate_monoplex_vs_multiplex()
    generate_layer_coupling_types()
    generate_multiplex_measures_example()
    generate_supra_adjacency_example()

    print("All images generated successfully!")
    print("Images saved in the 'images' directory:")
    print("- monoplex_vs_multiplex.png")
    print("- interlayer_coupling_types.png")
    print("- multiplex_measures_example.png")
    print("- supra_adjacency_example.png")