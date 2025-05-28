#!/usr/bin/env python3
"""
Complete Character Network Analysis Script for Conclave (2024)
This script follows the step-by-step tutorial from Lecture 11.

Students can run this in Google Colab to perform the complete analysis.
"""

# Step 1: Install and Import Required Libraries
print("=== Step 1: Installing Required Libraries ===")
print("Run these commands in Google Colab:")
print("!pip install networkx matplotlib spacy anthropic plotly")
print("!pip install PyPDF2 python-docx")
print("!python -m spacy download en_core_web_sm")
print()

# Import libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy
import re
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px

# For PDF processing (when available)
try:
    import PyPDF2
    from io import BytesIO
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("PyPDF2 not available. Using sample text instead.")

# For Claude API (optional)
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Anthropic library not available. Skipping AI analysis.")

print("=== Step 2: Character Names and Sample Data ===")

# Define full character names from the screenplay
full_character_names = [
    "Thomas Lawrence", "Aldo Bellini", "Joseph Tremblay",
    "Joshua Adeyemi", "Raymond O'Malley", "Vincent Benitez",
    "Sabbadin", "Mandorff", "Goffredo Tedesco", "Agnes",
    "Janusz Woźniak", "Villanueva", "Lombardi", "Shanumi"
]

# Sample screenplay text for demonstration
sample_screenplay_text = """
THOMAS LAWRENCE sits in the Vatican library, reviewing documents.
ALDO BELLINI enters the room, his face grave with concern.

LAWRENCE
The conclave must proceed according to tradition.

BELLINI
But the circumstances are unprecedented, Thomas.

AGNES appears in the doorway, carrying a sealed envelope.

AGNES
Cardinal Lawrence, this arrived for you.

LAWRENCE takes the envelope from AGNES. BELLINI watches intently.

JOSEPH TREMBLAY approaches from the corridor.

TREMBLAY
Lawrence, we need to discuss the voting procedures.

JOSHUA ADEYEMI joins the group, followed by RAYMOND O'MALLEY.

ADEYEMI
The African cardinals have concerns about the process.

O'MALLEY
As do the Americans. We must ensure transparency.

VINCENT BENITEZ enters, speaking quietly with SABBADIN.

BENITEZ
The Latin American delegation is unified in our position.

SABBADIN nods in agreement. MANDORFF appears, looking troubled.

MANDORFF
There are rumors circulating about irregularities.

GOFFREDO TEDESCO approaches LAWRENCE directly.

TEDESCO
Cardinal, we must speak privately about the situation.

LAWRENCE
Very well. Agnes, please ensure we're not disturbed.

AGNES
Of course, Your Eminence.

The cardinals gather in small groups, discussing in hushed tones.
BELLINI speaks with TREMBLAY while ADEYEMI confers with O'MALLEY.
BENITEZ and SABBADIN continue their conversation as MANDORFF
approaches TEDESCO. LAWRENCE observes the dynamics carefully.

JANUSZ WOŹNIAK enters the library, followed by VILLANUEVA.

WOŹNIAK
The Polish delegation supports traditional procedures.

VILLANUEVA
Spain agrees with Poland on this matter.

LOMBARDI appears, carrying additional documents.

LOMBARDI
The documentation is complete, Cardinal Lawrence.

SHANUMI joins the gathering, representing the Asian cardinals.

SHANUMI
We must consider all perspectives in this decision.

The tension in the room is palpable as the cardinals continue
their discussions. LAWRENCE exchanges glances with BELLINI,
while AGNES maintains her position by the door.
"""

print("=== Step 3: Setting Up Named Entity Recognition ===")

# Load spaCy model (if available)
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
    print("spaCy model loaded successfully.")
except OSError:
    SPACY_AVAILABLE = False
    print("spaCy model not available. Using simple text matching.")

# Create name variations (first names, last names)
name_variations = {}
for full_name in full_character_names:
    parts = full_name.split()
    name_variations[full_name] = full_name
    for part in parts:
        if len(part) > 2:  # Avoid short words
            name_variations[part] = full_name

print(f"Created {len(name_variations)} name variations")
print("Sample variations:", list(name_variations.items())[:5])

print("\n=== Step 4: Extract Character Interactions ===")

def extract_interactions_simple(text, window_size=100):
    """Simple interaction extraction without spaCy."""
    interactions = []

    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)

    for sentence in sentences:
        # Find character names in this sentence
        found_chars = []
        for name, full_name in name_variations.items():
            if name.upper() in sentence.upper():
                found_chars.append(full_name)

        # Remove duplicates
        found_chars = list(set(found_chars))

        # Create interactions between characters in the same sentence
        for i in range(len(found_chars)):
            for j in range(i+1, len(found_chars)):
                interactions.append((found_chars[i], found_chars[j], sentence.strip()))

    return interactions

def extract_interactions_spacy(text, window_size=100):
    """Extract character interactions using spaCy NER."""
    interactions = []

    # Process text in chunks
    doc = nlp(text)

    # Find all person entities
    persons = [(ent.text, ent.start_char, ent.end_char)
               for ent in doc.ents if ent.label_ == "PERSON"]

    # Map to full character names
    mapped_persons = []
    for person, start, end in persons:
        if person in name_variations:
            mapped_persons.append((name_variations[person], start, end))

    # Find interactions within window
    for i, (char1, start1, end1) in enumerate(mapped_persons):
        for j, (char2, start2, end2) in enumerate(mapped_persons[i+1:], i+1):
            if abs(start1 - start2) <= window_size and char1 != char2:
                # Extract context
                context_start = max(0, min(start1, start2) - 50)
                context_end = min(len(text), max(end1, end2) + 50)
                context = text[context_start:context_end]

                interactions.append((char1, char2, context))

    return interactions

# Extract interactions using available method
if SPACY_AVAILABLE:
    interactions = extract_interactions_spacy(sample_screenplay_text)
    print("Using spaCy for interaction extraction")
else:
    interactions = extract_interactions_simple(sample_screenplay_text)
    print("Using simple text matching for interaction extraction")

print(f"Found {len(interactions)} potential interactions")

print("\n=== Step 5: Build the Character Network ===")

# Create NetworkX graph
G = nx.Graph()

# Add nodes (characters)
for char in full_character_names:
    G.add_node(char)

# Count interactions and add edges
interaction_counts = defaultdict(int)
for char1, char2, context in interactions:
    pair = tuple(sorted([char1, char2]))
    interaction_counts[pair] += 1

# Add edges with weights
min_threshold = 1  # Lower threshold for demo data
for (char1, char2), weight in interaction_counts.items():
    if weight >= min_threshold:
        G.add_edge(char1, char2, weight=weight)

# Print basic network statistics
print(f"Network has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
print(f"Network density: {nx.density(G):.3f}")
print(f"Is connected: {nx.is_connected(G)}")

if not nx.is_connected(G):
    components = list(nx.connected_components(G))
    print(f"Number of connected components: {len(components)}")
    if components:
        print(f"Largest component size: {len(max(components, key=len))}")

print("\n=== Step 6: Network Analysis - Centrality Measures ===")

# Calculate centrality measures (only for connected components)
if G.number_of_edges() > 0:
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # Only calculate closeness and eigenvector for connected components
    if nx.is_connected(G):
        closeness_centrality = nx.closeness_centrality(G)
        eigenvector_centrality = nx.eigenvector_centrality(G)
    else:
        # For disconnected graphs, calculate for largest component
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        closeness_centrality = nx.closeness_centrality(subgraph)
        eigenvector_centrality = nx.eigenvector_centrality(subgraph)

        # Fill in zeros for nodes not in largest component
        for node in G.nodes():
            if node not in closeness_centrality:
                closeness_centrality[node] = 0
            if node not in eigenvector_centrality:
                eigenvector_centrality[node] = 0

    # Create centrality DataFrame
    centrality_df = pd.DataFrame({
        'Character': list(G.nodes()),
        'Degree': [degree_centrality[node] for node in G.nodes()],
        'Betweenness': [betweenness_centrality[node] for node in G.nodes()],
        'Closeness': [closeness_centrality[node] for node in G.nodes()],
        'Eigenvector': [eigenvector_centrality[node] for node in G.nodes()]
    })

    # Sort by degree centrality
    centrality_df = centrality_df.sort_values('Degree', ascending=False)
    print("Top 5 most central characters:")
    print(centrality_df.head())
else:
    print("No edges in the network. Cannot calculate centrality measures.")
    centrality_df = pd.DataFrame()

print("\n=== Step 7: Community Detection ===")

if G.number_of_edges() > 0:
    # Detect communities using Louvain algorithm
    communities = nx.community.louvain_communities(G)

    print(f"Found {len(communities)} communities:")
    for i, community in enumerate(communities):
        print(f"Community {i+1}: {list(community)}")

    # Add community information to nodes
    community_map = {}
    for i, community in enumerate(communities):
        for node in community:
            community_map[node] = i

    nx.set_node_attributes(G, community_map, 'community')
else:
    print("No edges in the network. Cannot detect communities.")
    communities = []
    community_map = {}

print("\n=== Step 8: Basic Visualization ===")

if G.number_of_edges() > 0:
    # Create basic network visualization
    plt.figure(figsize=(12, 8))

    # Use spring layout
    pos = nx.spring_layout(G, k=1, iterations=50)

    # Draw nodes colored by community if communities exist
    if communities:
        colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
        for i, community in enumerate(communities):
            nx.draw_networkx_nodes(G, pos, nodelist=list(community),
                                  node_color=[colors[i]], node_size=500, alpha=0.8)
    else:
        nx.draw_networkx_nodes(G, pos, node_color='lightblue',
                              node_size=500, alpha=0.8)

    # Draw edges with thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w/2 for w in weights], alpha=0.6)

    # Draw labels (last names only for readability)
    labels = {node: node.split()[-1] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')

    plt.title("Conclave Character Network", size=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
else:
    print("No edges to visualize.")

print("\n=== Step 9: Advanced Network Metrics ===")

def analyze_network_structure(G):
    """Calculate additional network metrics."""
    metrics = {}

    # Basic metrics
    metrics['nodes'] = G.number_of_nodes()
    metrics['edges'] = G.number_of_edges()
    metrics['density'] = nx.density(G)

    # Connectivity
    metrics['is_connected'] = nx.is_connected(G)
    if nx.is_connected(G) and G.number_of_edges() > 0:
        metrics['diameter'] = nx.diameter(G)
        metrics['avg_path_length'] = nx.average_shortest_path_length(G)

    # Clustering
    if G.number_of_edges() > 0:
        metrics['avg_clustering'] = nx.average_clustering(G)
        metrics['transitivity'] = nx.transitivity(G)

        # Small-world properties
        # Compare with random graph
        try:
            random_G = nx.erdos_renyi_graph(G.number_of_nodes(), nx.density(G))
            random_clustering = nx.average_clustering(random_G)
            if random_clustering > 0:
                metrics['clustering_ratio'] = metrics['avg_clustering'] / random_clustering
        except:
            pass

    return metrics

# Analyze network structure
network_metrics = analyze_network_structure(G)
print("Network Structure Analysis:")
for metric, value in network_metrics.items():
    print(f"{metric}: {value}")

print("\n=== Step 10: Character Importance Ranking ===")

if not centrality_df.empty:
    def rank_characters(G, centrality_df):
        """Create comprehensive character ranking."""
        df = centrality_df.copy()

        # Normalize centrality measures
        for col in ['Degree', 'Betweenness', 'Closeness', 'Eigenvector']:
            col_min = df[col].min()
            col_max = df[col].max()
            if col_max > col_min:
                df[f'{col}_norm'] = (df[col] - col_min) / (col_max - col_min)
            else:
                df[f'{col}_norm'] = 0

        # Calculate composite importance score
        df['Importance_Score'] = (
            df['Degree_norm'] * 0.3 +
            df['Betweenness_norm'] * 0.3 +
            df['Closeness_norm'] * 0.2 +
            df['Eigenvector_norm'] * 0.2
        )

        # Add network properties
        df['Connections'] = [G.degree(node) for node in df['Character']]
        df['Community'] = [community_map.get(node, 0) for node in df['Character']]

        return df.sort_values('Importance_Score', ascending=False)

    # Rank characters
    character_ranking = rank_characters(G, centrality_df)
    print("Character Importance Ranking:")
    print(character_ranking[['Character', 'Importance_Score', 'Connections', 'Community']].head(10))
else:
    character_ranking = pd.DataFrame()

print("\n=== Step 11: Export Results ===")

def export_results(G, character_ranking, network_metrics):
    """Save results for further analysis."""
    try:
        # Save network as GraphML
        nx.write_graphml(G, "conclave_network.graphml")
        print("✓ Network saved as GraphML")

        # Save character rankings
        if not character_ranking.empty:
            character_ranking.to_csv("character_rankings.csv", index=False)
            print("✓ Character rankings saved")

        # Save network metrics
        with open("network_metrics.txt", "w") as f:
            for metric, value in network_metrics.items():
                f.write(f"{metric}: {value}\n")
        print("✓ Network metrics saved")

        # Save edge list with weights
        if G.number_of_edges() > 0:
            edge_data = []
            for u, v, data in G.edges(data=True):
                edge_data.append([u, v, data.get('weight', 1)])

            edge_df = pd.DataFrame(edge_data, columns=['Source', 'Target', 'Weight'])
            edge_df.to_csv("network_edges.csv", index=False)
            print("✓ Edge list saved")

        print("\nFiles created:")
        print("- conclave_network.graphml (network file)")
        print("- character_rankings.csv (character analysis)")
        print("- network_metrics.txt (network properties)")
        print("- network_edges.csv (edge list)")

    except Exception as e:
        print(f"Error saving files: {e}")

# Export all results
export_results(G, character_ranking, network_metrics)

print("\n=== Step 12: AI-Enhanced Analysis (Optional) ===")

if ANTHROPIC_AVAILABLE:
    print("Claude API is available. You can use it for relationship inference.")
    print("Example usage:")
    print("""
    import anthropic
    client = anthropic.Anthropic(api_key="your_api_key_here")

    # Analyze a sample of interactions
    sample_interactions = interactions[:5]
    # ... (see lecture slides for full implementation)
    """)
else:
    print("Claude API not available. Install 'anthropic' package to use AI analysis.")

print("\n=== Analysis Complete! ===")
print("You have successfully:")
print("✓ Extracted character interactions from text")
print("✓ Built a character network with NetworkX")
print("✓ Calculated centrality measures")
print("✓ Detected communities")
print("✓ Visualized the network")
print("✓ Exported results for further analysis")

print("\nNext steps:")
print("1. Try with the actual Conclave screenplay PDF")
print("2. Experiment with different interaction extraction methods")
print("3. Use the Claude API for relationship type inference")
print("4. Create interactive visualizations with Plotly")
print("5. Compare with other movie/book character networks")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("Script completed successfully!")
    print("Check the generated files for your analysis results.")
    print("="*50)