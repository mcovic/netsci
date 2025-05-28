#!/usr/bin/env python3
"""
Generate supporting visuals for Lecture 11: Character Network Analysis.
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import seaborn as sns

# Create images directory if it doesn't exist
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Set style
plt.style.use('default')
sns.set_palette("husl")


def create_example_character_network():
    """Create an example character network for demonstration."""
    print("Generating example character network...")

    # Create a sample network based on Conclave characters
    G = nx.Graph()

    # Add main characters
    characters = [
        "Thomas Lawrence", "Aldo Bellini", "Joseph Tremblay",
        "Joshua Adeyemi", "Raymond O'Malley", "Vincent Benitez",
        "Sabbadin", "Mandorff", "Goffredo Tedesco", "Agnes"
    ]

    G.add_nodes_from(characters)

    # Add some example relationships with weights
    relationships = [
        ("Thomas Lawrence", "Aldo Bellini", 8),
        ("Thomas Lawrence", "Agnes", 6),
        ("Thomas Lawrence", "Joseph Tremblay", 5),
        ("Aldo Bellini", "Joshua Adeyemi", 4),
        ("Joseph Tremblay", "Raymond O'Malley", 7),
        ("Vincent Benitez", "Sabbadin", 3),
        ("Mandorff", "Goffredo Tedesco", 4),
        ("Thomas Lawrence", "Vincent Benitez", 3),
        ("Aldo Bellini", "Mandorff", 2),
        ("Joshua Adeyemi", "Raymond O'Malley", 3)
    ]

    for char1, char2, weight in relationships:
        G.add_edge(char1, char2, weight=weight)

    # Create visualization
    plt.figure(figsize=(12, 8))

    # Use spring layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Calculate node sizes based on degree
    degrees = dict(G.degree())
    node_sizes = [degrees[node] * 200 + 300 for node in G.nodes()]

    # Draw edges with thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w/2 for w in weights],
                          alpha=0.6, edge_color='gray')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                          node_color='lightblue',
                          alpha=0.8, edgecolors='black', linewidths=1)

    # Draw labels (last names only for readability)
    labels = {node: node.split()[-1] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=12,
                           font_weight='bold')

    plt.title("Example Character Network - Conclave", size=16,
              fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "example_character_network.png"),
                dpi=150, bbox_inches='tight')
    plt.close()

    return G


def create_centrality_comparison():
    """Create a visualization comparing different centrality measures."""
    print("Generating centrality comparison...")

    # Create sample data
    characters = ["Lawrence", "Bellini", "Tremblay", "Adeyemi",
                  "O'Malley", "Benitez"]

    # Sample centrality values
    degree_cent = [0.8, 0.6, 0.5, 0.4, 0.3, 0.2]
    betweenness_cent = [0.7, 0.4, 0.6, 0.2, 0.3, 0.1]
    closeness_cent = [0.9, 0.7, 0.6, 0.5, 0.4, 0.3]
    eigenvector_cent = [0.8, 0.5, 0.4, 0.6, 0.2, 0.1]

    # Create DataFrame
    df = pd.DataFrame({
        'Character': characters,
        'Degree': degree_cent,
        'Betweenness': betweenness_cent,
        'Closeness': closeness_cent,
        'Eigenvector': eigenvector_cent
    })

    # Create comparison plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Degree centrality
    axes[0, 0].bar(df['Character'], df['Degree'], color='skyblue',
                   alpha=0.8)
    axes[0, 0].set_title('Degree Centrality', fontweight='bold')
    axes[0, 0].set_ylabel('Centrality Score')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Betweenness centrality
    axes[0, 1].bar(df['Character'], df['Betweenness'], color='lightcoral',
                   alpha=0.8)
    axes[0, 1].set_title('Betweenness Centrality', fontweight='bold')
    axes[0, 1].set_ylabel('Centrality Score')
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Closeness centrality
    axes[1, 0].bar(df['Character'], df['Closeness'], color='lightgreen',
                   alpha=0.8)
    axes[1, 0].set_title('Closeness Centrality', fontweight='bold')
    axes[1, 0].set_ylabel('Centrality Score')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # Eigenvector centrality
    axes[1, 1].bar(df['Character'], df['Eigenvector'], color='gold',
                   alpha=0.8)
    axes[1, 1].set_title('Eigenvector Centrality', fontweight='bold')
    axes[1, 1].set_ylabel('Centrality Score')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.suptitle('Character Centrality Measures Comparison', size=16,
                 fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "centrality_comparison.png"),
                dpi=150, bbox_inches='tight')
    plt.close()


def create_workflow_diagram():
    """Create a workflow diagram showing the analysis process."""
    print("Generating workflow diagram...")

    fig, ax = plt.subplots(figsize=(14, 10))

    # Define workflow steps
    steps = [
        "1. Load PDF\nScreenplay",
        "2. Extract Text\nwith PyPDF2",
        "3. Named Entity\nRecognition (spaCy)",
        "4. Character\nMapping",
        "5. Proximity-based\nInteraction Extraction",
        "6. Network\nConstruction",
        "7. Centrality\nAnalysis",
        "8. Community\nDetection",
        "9. Visualization\n& Export"
    ]

    # Create a simple 3x3 grid layout that flows naturally
    positions = [
        (2, 8), (5, 8), (8, 8),    # Top row: steps 1-3
        (2, 5), (5, 5), (8, 5),    # Middle row: steps 4-6
        (2, 2), (5, 2), (8, 2)     # Bottom row: steps 7-9
    ]

    # Draw boxes and text
    for i, (step, pos) in enumerate(zip(steps, positions)):
        # Draw box
        box = plt.Rectangle((pos[0]-1.2, pos[1]-0.6), 2.4, 1.2,
                           facecolor='lightblue', edgecolor='black',
                           linewidth=2)
        ax.add_patch(box)

        # Add text
        ax.text(pos[0], pos[1], step, ha='center', va='center',
               fontsize=10, fontweight='bold')

    # Draw simple arrows - all horizontal or vertical, no crosscutting
    arrow_pairs = [
        (0, 1), (1, 2),  # Top row: left to right
        (2, 5),          # Down from step 3 to step 6
        (5, 4), (4, 3),  # Middle row: right to left
        (3, 6),          # Down from step 4 to step 7
        (6, 7), (7, 8)   # Bottom row: left to right
    ]

    for start, end in arrow_pairs:
        start_pos = positions[start]
        end_pos = positions[end]

        if start_pos[1] == end_pos[1]:  # Horizontal arrow
            if start_pos[0] < end_pos[0]:  # Left to right
                ax.annotate('', xy=(end_pos[0]-1.2, end_pos[1]),
                           xytext=(start_pos[0]+1.2, start_pos[1]),
                           arrowprops=dict(arrowstyle='->', lw=2, color='red'))
            else:  # Right to left
                ax.annotate('', xy=(end_pos[0]+1.2, end_pos[1]),
                           xytext=(start_pos[0]-1.2, start_pos[1]),
                           arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        else:  # Vertical arrow
            ax.annotate('', xy=(end_pos[0], end_pos[1]+0.6),
                       xytext=(start_pos[0], start_pos[1]-0.6),
                       arrowprops=dict(arrowstyle='->', lw=2, color='red'))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Character Network Analysis Workflow', size=16,
                 fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "analysis_workflow.png"),
                dpi=150, bbox_inches='tight')
    plt.close()


def create_ner_example():
    """Create an example of Named Entity Recognition output."""
    print("Generating NER example...")

    # Sample text with highlighted entities
    fig, ax = plt.subplots(figsize=(12, 6))

    # Sample screenplay text
    text = """THOMAS LAWRENCE sits across from ALDO BELLINI in the Vatican library.
LAWRENCE speaks quietly about the upcoming conclave. BELLINI nods,
understanding the gravity of the situation. AGNES enters the room,
carrying important documents for the CARDINAL."""

    # Entities to highlight
    entities = [
        ("THOMAS LAWRENCE", "PERSON", (0, 14)),
        ("ALDO BELLINI", "PERSON", (35, 46)),
        ("Vatican", "ORG", (54, 61)),
        ("LAWRENCE", "PERSON", (72, 80)),
        ("BELLINI", "PERSON", (118, 125)),
        ("AGNES", "PERSON", (175, 180)),
        ("CARDINAL", "PERSON", (230, 238))
    ]

    # Create text visualization
    ax.text(0.05, 0.7, "Original Text:", fontsize=14, fontweight='bold',
            transform=ax.transAxes)
    ax.text(0.05, 0.6, text, fontsize=11, transform=ax.transAxes,
            wrap=True)

    ax.text(0.05, 0.4, "Identified Entities:", fontsize=14,
            fontweight='bold', transform=ax.transAxes)

    # List entities
    entity_text = ""
    for entity, label, span in entities:
        entity_text += f"• {entity} ({label})\n"

    ax.text(0.05, 0.1, entity_text, fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Named Entity Recognition Example', size=16,
                 fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "ner_example.png"),
                dpi=150, bbox_inches='tight')
    plt.close()


def create_community_detection_example():
    """Create an example of community detection in the character network."""
    print("Generating community detection example...")

    # Create a network with clear communities
    G = nx.Graph()

    # Vatican Cardinals community
    cardinals = ["Lawrence", "Bellini", "Tremblay", "Adeyemi"]
    # Vatican Staff community
    staff = ["Agnes", "Sabbadin", "Mandorff"]
    # External/Other community
    others = ["Tedesco", "O'Malley", "Benitez"]

    # Add nodes
    all_chars = cardinals + staff + others
    G.add_nodes_from(all_chars)

    # Add intra-community edges (stronger connections)
    for i in range(len(cardinals)):
        for j in range(i+1, len(cardinals)):
            G.add_edge(cardinals[i], cardinals[j],
                      weight=np.random.randint(3, 8))

    for i in range(len(staff)):
        for j in range(i+1, len(staff)):
            G.add_edge(staff[i], staff[j], weight=np.random.randint(2, 6))

    for i in range(len(others)):
        for j in range(i+1, len(others)):
            G.add_edge(others[i], others[j], weight=np.random.randint(2, 5))

    # Add inter-community edges (weaker connections)
    G.add_edge("Lawrence", "Agnes", weight=4)
    G.add_edge("Bellini", "Sabbadin", weight=2)
    G.add_edge("Tremblay", "Tedesco", weight=3)
    G.add_edge("Agnes", "O'Malley", weight=2)

    # Create visualization
    plt.figure(figsize=(12, 8))

    # Use spring layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Define community colors
    community_colors = {
        'Cardinals': 'red',
        'Staff': 'blue',
        'Others': 'green'
    }

    node_colors = []
    for node in G.nodes():
        if node in cardinals:
            node_colors.append(community_colors['Cardinals'])
        elif node in staff:
            node_colors.append(community_colors['Staff'])
        else:
            node_colors.append(community_colors['Others'])

    # Draw edges
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w/3 for w in weights],
                          alpha=0.6, edge_color='gray')

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800,
                          alpha=0.8, edgecolors='black', linewidths=2)

    # Draw labels with better readability
    # First draw white outline
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold',
                           font_color='white', bbox=dict(boxstyle="round,pad=0.1",
                           facecolor='white', alpha=0.8, edgecolor='none'))
    # Then draw black text on top
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold',
                           font_color='black')

    # Add legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                 markerfacecolor=color,
                                 markersize=15, label=community)
                      for community, color in community_colors.items()]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=12)

    plt.title("Community Detection in Character Network", size=16,
              fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "community_detection.png"),
                dpi=150, bbox_inches='tight')
    plt.close()


def create_text_processing_steps():
    """Create a clear visualization of the text processing pipeline."""
    print("Generating text processing pipeline...")

    fig, ax = plt.subplots(figsize=(16, 10))

    # Define the pipeline steps with more detail
    steps = [
        {
            'title': '1. PDF Input',
            'subtitle': 'Conclave Screenplay',
            'content': 'Raw PDF Document\nwith screenplay text',
            'icon': 'PDF',
            'color': '#FFE6E6',
            'pos': (2, 8)
        },
        {
            'title': '2. Text Extraction',
            'subtitle': 'PyPDF2 Processing',
            'content': 'Extract plain text\nfrom PDF pages',
            'icon': 'TXT',
            'color': '#E6F3FF',
            'pos': (6, 8)
        },
        {
            'title': '3. Text Cleaning',
            'subtitle': 'Preprocessing',
            'content': 'Remove formatting\nNormalize text',
            'icon': 'CLN',
            'color': '#F0E6FF',
            'pos': (10, 8)
        },
        {
            'title': '4. Named Entity Recognition',
            'subtitle': 'spaCy NER',
            'content': 'Identify character names\nand organizations',
            'icon': 'NER',
            'color': '#E6FFE6',
            'pos': (14, 8)
        },
        {
            'title': '5. Character Mapping',
            'subtitle': 'Name Variations',
            'content': 'Map "LAWRENCE" to\n"Thomas Lawrence"',
            'icon': 'MAP',
            'color': '#FFFFE6',
            'pos': (14, 4)
        },
        {
            'title': '6. Interaction Extraction',
            'subtitle': 'Proximity Analysis',
            'content': 'Find characters appearing\nwithin text windows',
            'icon': 'INT',
            'color': '#FFE6F3',
            'pos': (10, 4)
        },
        {
            'title': '7. Network Construction',
            'subtitle': 'NetworkX Graph',
            'content': 'Nodes: Characters\nEdges: Interactions',
            'icon': 'NET',
            'color': '#E6FFF0',
            'pos': (6, 4)
        },
        {
            'title': '8. Network Analysis',
            'subtitle': 'Centrality & Communities',
            'content': 'Calculate importance\nDetect groups',
            'icon': 'ANA',
            'color': '#F0F0FF',
            'pos': (2, 4)
        }
    ]

    # Draw steps
    for i, step in enumerate(steps):
        x, y = step['pos']

        # Draw main box
        box = plt.Rectangle((x-1.4, y-1), 2.8, 2,
                           facecolor=step['color'],
                           edgecolor='black',
                           linewidth=2)
        ax.add_patch(box)

        # Add icon
        ax.text(x, y+0.6, step['icon'], ha='center', va='center',
               fontsize=14, fontweight='bold', color='darkblue',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white',
                        alpha=0.9, edgecolor='darkblue'))

        # Add title
        ax.text(x, y+0.2, step['title'], ha='center', va='center',
               fontsize=12, fontweight='bold')

        # Add subtitle
        ax.text(x, y-0.1, step['subtitle'], ha='center', va='center',
               fontsize=10, style='italic', color='gray')

        # Add content
        ax.text(x, y-0.5, step['content'], ha='center', va='center',
               fontsize=9)

    # Draw arrows between steps
    arrow_paths = [
        (0, 1), (1, 2), (2, 3),  # Top row: 1→2→3→4 (left to right)
        (3, 4),                   # Down: 4→5 (NER to Character Mapping)
        (4, 5), (5, 6), (6, 7)   # Bottom row: 5→6→7→8 (right to left)
    ]

    for start_idx, end_idx in arrow_paths:
        start_pos = steps[start_idx]['pos']
        end_pos = steps[end_idx]['pos']

        if start_pos[1] == end_pos[1]:  # Horizontal arrow
            if start_pos[0] < end_pos[0]:  # Left to right
                ax.annotate('', xy=(end_pos[0]-1.4, end_pos[1]),
                           xytext=(start_pos[0]+1.4, start_pos[1]),
                           arrowprops=dict(arrowstyle='->', lw=3,
                                         color='#2E8B57'))
            else:  # Right to left
                ax.annotate('', xy=(end_pos[0]+1.4, end_pos[1]),
                           xytext=(start_pos[0]-1.4, start_pos[1]),
                           arrowprops=dict(arrowstyle='->', lw=3,
                                         color='#2E8B57'))
        else:  # Vertical arrow
            ax.annotate('', xy=(end_pos[0], end_pos[1]+1),
                       xytext=(start_pos[0], start_pos[1]-1),
                       arrowprops=dict(arrowstyle='->', lw=3,
                                     color='#2E8B57'))

    # Add example data boxes
    example_box_y = 1.5

    # Example input text
    ax.text(4, example_box_y,
           'Example Input:\n"THOMAS LAWRENCE sits with ALDO BELLINI..."',
           ha='center', va='center', fontsize=9,
           bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                    edgecolor="gray", alpha=0.8))

    # Example output
    ax.text(12, example_box_y,
           'Example Output:\nNetwork with 14 characters,\n19 relationships',
           ha='center', va='center', fontsize=9,
           bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                    edgecolor="gray", alpha=0.8))

    # Set title and layout
    ax.set_title('Character Network Analysis: Text Processing Pipeline',
                size=18, fontweight='bold', pad=20)

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "text_processing_steps.png"),
                dpi=150, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    print("Generating visuals for Lecture 11: Character Network Analysis")

    # Generate all visualizations
    create_example_character_network()
    create_centrality_comparison()
    create_workflow_diagram()
    create_ner_example()
    create_community_detection_example()
    create_text_processing_steps()

    print(f"\nAll visuals generated and saved to '{output_dir}/' directory:")
    print("- example_character_network.png")
    print("- centrality_comparison.png")
    print("- analysis_workflow.png")
    print("- ner_example.png")
    print("- community_detection.png")
    print("- text_processing_steps.png")
    print("\nLecture 11 visuals complete!")