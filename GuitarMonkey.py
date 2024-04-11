import streamlit as st

from chords import ChordTypes, Notes, get_chord_notes, get_variations_456
from guitar_svg import generate_guitar_chord_svg

SAVED_CHORDS_KEY = "saved_chords_key"
if SAVED_CHORDS_KEY not in st.session_state:
    st.session_state[SAVED_CHORDS_KEY] = []


def run():
    st.set_page_config(layout="wide", page_icon="🎸")
    st.markdown("## 🎸 Chord search")
    with st.expander("Settings") as c:
        default_tuning = [Notes.E, Notes.A, Notes.D, Notes.G, Notes.B, Notes.E]
        st.markdown("Tuning:")
        strings = st.columns(6)
        tuning = [Notes.E for _ in range(6)]
        for i in range(6):
            tuning[i] = Notes(
                strings[i].selectbox(f"String {i+1}", options=[n for n in Notes], key=f"string_{i}", index=default_tuning[i].value)
            )

        num_cols = st.select_slider("Number of columns", options=[n + 1 for n in range(10)], value=8)
        show_notes = st.checkbox("Show notes", value=True)

    saved_chords = st.session_state[SAVED_CHORDS_KEY]
    if saved_chords:
        st.markdown("## Saved chords")
        cols = st.columns(num_cols)
        for i, places in enumerate(saved_chords):
            saved_note, saved_type, places = places
            cols[i % num_cols].markdown(f"{saved_note} {saved_type}")
            chord_notes_by_string = [t.add(places[i]) for i, t in enumerate(tuning)] if show_notes else []
            img = generate_guitar_chord_svg(places, chord_notes_by_string)
            cols[i % num_cols].image(img, caption=f"{saved_note}{saved_type}: {format_variation(places)}", use_column_width=True)

    col1, col2 = st.columns(2)
    base_note = col1.selectbox("Base note", options=[n for n in Notes])
    chord_type = col2.selectbox("Chord type", options=[n for n in ChordTypes])

    chord = get_chord_notes(base_note, chord_type)

    st.markdown(f"Chords: {', '.join([str(c) for c in chord])}. Guitar tuning: {' '.join([str(t) for t in tuning])}")
    variations = get_variations_456(tuning, chord, hand_range=4)

    st.markdown("#### Variations")
    cols = st.columns(num_cols)

    i = 0
    too_high = []
    for places in variations:
        if len(places) == 4:
            places = (-1, -1, *places)
        if len(places) == 5:
            places = (-1, *places)

        chord_notes_by_string = [t.add(places[i]) for i, t in enumerate(tuning)] if show_notes else []
        img = generate_guitar_chord_svg(places, chord_notes_by_string)
        cols[i % num_cols].image(img, caption=format_variation(places), use_column_width=True)
        cols[i % num_cols].button(
            "Save",
            key=f"chord_{places}",
            on_click=save_chord,
            args=(
                base_note,
                chord_type,
                places,
            ),
            type="secondary",
        )
        i += 1


def save_chord(note, type, v):
    st.session_state[SAVED_CHORDS_KEY].append((note, type, v))


def format_variation(v: list[int]) -> str:
    return "-".join([str(x) if x >= 0 else "x" for x in v])


if __name__ == "__main__":
    run()
