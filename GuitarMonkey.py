import streamlit as st
from chords import Notes, ChordTypes, get_chord_notes, get_variations_456
from guitar_svg import generate_guitar_chord_svg


def run():
    st.markdown("# Chord searcher")
    col1, col2 = st.columns(2)

    base_note = col1.selectbox("Base note", options=[n for n in Notes])
    chord_type = col2.selectbox("Chord type", options=[n for n in ChordTypes])

    chord = get_chord_notes(base_note, chord_type)
    tuning = [Notes.E, Notes.A, Notes.D, Notes.G, Notes.B, Notes.E]
    variations = get_variations_456(tuning, chord, hand_range=4)
    # pprint(variations)

    num_cols = 3
    st.markdown("#### Variations")
    cols = st.columns(num_cols)

    i = 0
    too_high = []
    for v in variations:
        if len(v) == 4:
            v = (-1, -1, *v)
        if len(v) == 5:
            v = (-1, *v)
        if max(v) > 7:
            too_high.append(v)
            continue
        
        cols[i%num_cols].markdown("-".join([str(x) if x>=0 else "x" for x in v]))
        img = generate_guitar_chord_svg(v)
        cols[i%num_cols].image(img)
        i += 1

    st.markdown("#### Other variations")
    for v in too_high:

        st.markdown(v)

if __name__ == '__main__':
    run()