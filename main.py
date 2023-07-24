import networkx as nx
import matplotlib.pyplot as plt
from music21 import stream, note, chord, midi

# Create a hypergraph using a dictionary. The key is the hyperedge (chord name), 
# and the value is a list of nodes (notes).
hypergraph = {
    "chord1": ["C4", "E4", "G4"],  # C Major chord
    "chord2": ["A4", "C5", "E5"]   # A minor chord
}

# Convert the hypergraph to a NetworkX bipartite graph
B = nx.Graph()
for chord_name, notes in hypergraph.items():
    for note_name in notes:
        B.add_edge(chord_name, note_name)

# Verify that the graph is bipartite
assert nx.is_bipartite(B)

# Use music21 to create a stream and add the notes of each chord to the stream
s = stream.Stream()

# Add each chord to the stream
for chord_name in hypergraph.keys():
    # Get the notes of this chord
    chord_notes = [note.Note(n) for n in B.neighbors(chord_name)]
    # Create a chord from these notes
    chord_to_add = chord.Chord(chord_notes)
    # Add the chord to the stream
    s.append(chord_to_add)

# Write the stream to a MIDI file
mf = midi.translate.streamToMidiFile(s)
mf.open("chords.mid", 'wb')
mf.write()
mf.close()

# Visualize the hypergraph (bipartite graph) using NetworkX and Matplotlib
pos = nx.spring_layout(B)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(B, pos, node_size=500)

# edges
nx.draw_networkx_edges(B, pos, width=6)

# labels
nx.draw_networkx_labels(B, pos, font_size=20, font_family="sans-serif")

plt.axis("off")  # turn off axis
plt.show()  # display the graph

