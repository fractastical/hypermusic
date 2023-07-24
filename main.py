import networkx as nx
from music21 import stream, note, midi

# Create a hypergraph using a dictionary. The key is the hyperedge (chord), 
# and the value is a list of nodes (notes).
hypergraph = {
    "chord1": ["C4", "E4", "G4"],  # C Major chord
    "chord2": ["A4", "C5", "E5"]  # A minor chord
}

# Convert the hypergraph to a NetworkX bipartite graph
B = nx.Graph()
for chord, notes in hypergraph.items():
    for note in notes:
        B.add_edge(chord, note)

# Verify that the graph is bipartite
assert nx.is_bipartite(B)

# Use music21 to create a stream and add the notes of each chord to the stream
s = stream.Stream()

# Add each chord to the stream
for chord in hypergraph.keys():
    # Get the notes of this chord
    notes = [note.Note(n) for n in B.neighbors(chord)]
    # Add the notes to the stream
    for n in notes:
        s.append(n)

# Write the stream to a MIDI file
mf = midi.translate.streamToMidiFile(s)
mf.open("chords.mid", 'wb')
mf.write()
mf.close()
