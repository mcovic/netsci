# Lecture 11: Character Network Analysis - Conclave Case Study

## Overview

This lecture provides a hands-on case study in character network analysis using the 2024 movie "Conclave" screenplay. Students will learn to extract character relationships from text, build network graphs, and perform comprehensive social network analysis.

## Learning Objectives

By the end of this lecture, students will be able to:

1. **Extract text from PDF documents** using PyPDF2
2. **Identify character names** using Named Entity Recognition (NER) with spaCy
3. **Build character networks** from proximity-based interactions
4. **Calculate centrality measures** to identify important characters
5. **Detect communities** within character networks
6. **Visualize networks** using matplotlib and plotly
7. **Enhance analysis** using AI tools like Claude API
8. **Export results** for further analysis

## Files in This Directory

- `lecture.md` - Main lecture slides (Marp format)
- `generate_conclave_visuals.py` - Script to generate supporting images
- `conclave_analysis_notebook.py` - Complete analysis script for students
- `images/` - Generated visualizations and diagrams
- `README.md` - This file

## Prerequisites

### Required Python Packages

```bash
pip install networkx matplotlib spacy anthropic plotly
pip install PyPDF2 python-docx pandas numpy seaborn
python -m spacy download en_core_web_sm
```

### Optional Requirements

- **Anthropic API Key** - For AI-enhanced relationship analysis
- **Conclave Screenplay PDF** - Available from [ScriptSlug](https://www.scriptslug.com/script/conclave-2024)

## Quick Start Guide

### For Students

1. **Open Google Colab** and create a new notebook
2. **Install required packages** (see prerequisites above)
3. **Copy and run** the code from `conclave_analysis_notebook.py`
4. **Follow along** with the lecture slides
5. **Experiment** with different parameters and methods

### For Instructors

1. **Generate visuals** by running:
   ```bash
   python generate_conclave_visuals.py
   ```
2. **Present slides** using Marp or any Markdown presentation tool
3. **Guide students** through the hands-on analysis
4. **Encourage experimentation** with different texts and methods

## Analysis Workflow

The complete analysis follows these steps:

```
PDF Document → Text Extraction → Named Entity Recognition →
Character Mapping → Interaction Extraction → Network Construction →
Centrality Analysis → Community Detection → Visualization → Export
```

### Step-by-Step Process

1. **Data Loading**
   - Load screenplay PDF or use sample text
   - Extract clean text content

2. **Character Identification**
   - Define character name list
   - Create name variations (first/last names)
   - Use spaCy NER for entity recognition

3. **Interaction Extraction**
   - Find character co-occurrences in text
   - Use proximity-based relationship inference
   - Count interaction frequencies

4. **Network Construction**
   - Create NetworkX graph
   - Add characters as nodes
   - Add interactions as weighted edges

5. **Network Analysis**
   - Calculate degree, betweenness, closeness, eigenvector centrality
   - Detect communities using Louvain algorithm
   - Compute network-level metrics

6. **Visualization**
   - Create static plots with matplotlib
   - Generate interactive visualizations with plotly
   - Export network files for external tools

7. **AI Enhancement** (Optional)
   - Use Claude API for relationship type inference
   - Analyze interaction contexts
   - Generate insights about character dynamics

## Key Concepts Covered

### Network Analysis Fundamentals
- **Nodes and Edges**: Characters and their relationships
- **Centrality Measures**: Identifying important characters
- **Community Detection**: Finding character groups/factions
- **Network Metrics**: Density, clustering, path lengths

### Text Processing Techniques
- **Named Entity Recognition**: Automated character identification
- **Proximity Analysis**: Inferring relationships from co-occurrence
- **Text Preprocessing**: Cleaning and structuring screenplay text

### Visualization Methods
- **Static Networks**: matplotlib-based network plots
- **Interactive Networks**: plotly-based dynamic visualizations
- **Multi-panel Dashboards**: Comprehensive analysis views

## Expected Outputs

After completing the analysis, students will have:

1. **Character Network Graph** - Visual representation of relationships
2. **Centrality Rankings** - Importance scores for each character
3. **Community Structure** - Character groups and factions
4. **Network Metrics** - Quantitative network properties
5. **Exportable Files** - GraphML, CSV, and text formats

## Extensions and Variations

### Advanced Techniques
- **Temporal Analysis**: Track relationship changes over time
- **Sentiment Analysis**: Analyze emotional tone of interactions
- **Multi-layer Networks**: Separate formal vs. informal relationships
- **Comparative Analysis**: Compare with other movie/book networks

### Alternative Data Sources
- **Books and Novels**: Project Gutenberg texts
- **TV Show Scripts**: Episode-by-episode analysis
- **Social Media**: Twitter/Reddit conversation networks
- **Historical Documents**: Political correspondence networks

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **PDF Extraction Errors**
   - Try different PDF processing libraries
   - Use OCR for scanned documents
   - Manually copy text as fallback

3. **Empty Network**
   - Lower interaction threshold
   - Check character name variations
   - Verify text preprocessing

4. **Visualization Problems**
   - Adjust figure sizes and layouts
   - Use different layout algorithms
   - Filter nodes/edges for clarity

### Performance Tips

- **Large Texts**: Process in chunks
- **Memory Issues**: Use generators for large datasets
- **Slow Visualization**: Sample nodes/edges for display
- **API Limits**: Batch requests and add delays

## Assessment Ideas

### Individual Assignment
- Analyze a different movie/book of student's choice
- Compare network properties across different genres
- Write analysis report with insights and visualizations

### Group Project
- Collaborative analysis of TV series across seasons
- Cross-cultural comparison of storytelling networks
- Development of improved interaction extraction methods

### Research Extension
- Literature review of character network analysis
- Novel methodology development
- Application to non-fiction texts (news, academic papers)

## Resources and References

### Documentation
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [spaCy NER Guide](https://spacy.io/usage/linguistic-features#named-entities)
- [Plotly Network Graphs](https://plotly.com/python/network-graphs/)

### Academic Papers
- "Character Networks in Literature" - Digital Humanities approaches
- "Social Network Analysis in Narrative Fiction" - Computational methods
- "Automated Character Identification in Literary Texts" - NLP techniques

### Tools and Platforms
- **Gephi** - Advanced network visualization and analysis
- **Cytoscape** - Biological network analysis (adaptable to character networks)
- **NetworkX** - Python network analysis library
- **Palladio** - Web-based network visualization

### Datasets
- **Project Gutenberg** - Free literary texts
- **Internet Movie Script Database** - Movie screenplays
- **TV Tropes** - Character relationship data
- **Fandom Wikis** - Structured character information

## Contact and Support

For questions about this lecture or the analysis methods:

- **Course Forum** - Post questions for peer and instructor help
- **Office Hours** - Schedule one-on-one assistance
- **GitHub Issues** - Report technical problems with code
- **Email** - Direct contact for urgent issues

## License and Attribution

This educational material is provided for academic use. When using or adapting this content:

- **Cite the source** - Network Analysis Course, PMF-UNIST 2024/2025
- **Share improvements** - Contribute back to the educational community
- **Respect copyrights** - Use appropriate texts and data sources
- **Follow ethical guidelines** - Ensure responsible use of AI tools and APIs

---

*Last updated: December 2024*
*Course: Network Analysis - Data Science and Engineering Master Program*
*Institution: Faculty of Natural Science, University of Split*