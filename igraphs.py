import json  
import plotly.graph_objects as go
import networkx as nx


def visualize_hypergraph_interactive(hypergraph):
    # Convert the hypergraph to a NetworkX bipartite graph
    B = nx.Graph()
    for chord_name, notes in hypergraph.items():
        for note_name in notes:
            B.add_edge(chord_name, note_name)

    # Verify that the graph is bipartite
    assert nx.is_bipartite(B)

    # Get positions of the nodes
    pos = nx.spring_layout(B)

    edge_x = []
    edge_y = []
    for edge in B.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in B.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(B.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{adjacencies[0]}, # of connections: {len(adjacencies[1])}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://www.github.com'> GitHub</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

    fig.show()

# Load the hypergraphs from the JSON file
with open('hypergraphs.json') as file:
    musical_systems = json.load(file)

# Generate a MIDI file and visualize each musical system
for system_name, hypergraph in musical_systems.items():
    filename = system_name + ".mid"  # Create a filename from the system name
    # generate_midi_from_hypergraph(hypergraph, filename)
    visualize_hypergraph_interactive(hypergraph)
