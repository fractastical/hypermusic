from music21 import pitch

def transpose_hypergraph(hypergraph, semitones):
    transposed_hypergraph = {}
    for chord_name, notes in hypergraph.items():
        transposed_notes = []
        for note_name in notes:
            p = pitch.Pitch(note_name)
            p = p.transpose(semitones)
            transposed_notes.append(p.nameWithOctave)
        transposed_hypergraph[chord_name] = transposed_notes
    return transposed_hypergraph
