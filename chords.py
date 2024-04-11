import itertools
from enum import Enum
from pprint import pprint

import numpy as np
from numpy.typing import NDArray

DEFAULT_HAND_RANGE = 5


class Notes(Enum):
    C = 0
    Cs = 1
    D = 2
    Ds = 3
    E = 4
    F = 5
    Fs = 6
    G = 7
    Gs = 8
    A = 9
    As = 10
    B = 11

    def add(self, i: int):
        return Notes((self.value + i) % 12)

    def __str__(self):
        # TODO: make flat or sharp conditional on chord
        notes_format = {
            Notes.C: "C",
            Notes.Cs: "C♯",  # or D♭",
            Notes.D: "D",
            Notes.Ds: "D♯",  # or E♭",
            Notes.E: "E",
            Notes.F: "F",
            Notes.Fs: "F♯",  # or G♭",
            Notes.G: "G",
            Notes.Gs: "G♯",  # or A♭",
            Notes.A: "A",
            Notes.As: "A♯",  # or B♭",
            Notes.B: "B",
        }
        return notes_format.get(self, "?")


class ChordTypes(Enum):
    major = (0, 4, 7)
    minor = (0, 3, 7)
    augmented = (0, 4, 8)
    diminished = (0, 3, 6)
    sus2 = (0, 2, 7)
    sus4 = (0, 5, 7)
    major7 = (0, 4, 7, 11)
    dom7 = (0, 4, 7, 10)
    minor7 = (0, 3, 7, 10)
    halfdim7 = (0, 3, 6, 10)
    dim7 = (0, 3, 6, 9)

    def __str__(self):
        chord_format = {
            ChordTypes.major: "Major",
            ChordTypes.minor: "Minor",
            ChordTypes.augmented: "Augmented",
            ChordTypes.diminished: "Diminished",
            ChordTypes.sus2: "sus2",
            ChordTypes.sus4: "sus4",
            ChordTypes.major7: "Major 7",
            ChordTypes.dom7: "Dom 7",
            ChordTypes.minor7: "Minor 7",
            ChordTypes.halfdim7: "Half diminished 7",
            ChordTypes.dim7: "Diminished 7",
        }
        return chord_format.get(self, "?")


def get_chord_notes(note: Notes, chord_type: ChordTypes) -> list[Notes]:
    return [note.add(step) for step in chord_type.value]


def get_guitar_neck(tuning: list[Notes], hand_range=DEFAULT_HAND_RANGE) -> NDArray:
    return np.stack([np.arange(len(Notes) + hand_range, dtype=int) + note.value for note in tuning]).T % 12


def get_bool_neck(neck: NDArray, chord: list[Notes]) -> NDArray:
    b = neck == chord[0].value
    for c in chord[1:]:
        b = b | (neck == c.value)
    return b


def get_variations(tuning: list[Notes], chord: list[Notes], hand_range=DEFAULT_HAND_RANGE):
    neck = get_guitar_neck(tuning, hand_range)
    out = set()
    open_notes = neck[
        0,
    ]
    for i in range(1, neck.shape[0] - hand_range + 1):
        reachable_notes = neck[
            i : i + hand_range,
        ]
        reachable_neck = np.vstack([open_notes, reachable_notes])
        correct_notes = get_bool_neck(reachable_neck, chord)
        frets, strings = correct_notes.nonzero()
        locations = np.vstack((frets, strings)).T

        valid_pos = [[] for _ in range(len(open_notes))]
        for f, s in locations:
            fret = f + i - 1 if f > 0 else 0
            valid_pos[s].append(fret)

        combinations = list(itertools.product(*valid_pos))
        for c in combinations:
            if validate_chord(neck, chord, c):
                out.add(c)
    return list(out)


def get_variations_456(tuning: list[Notes], chord: list[Notes], hand_range=DEFAULT_HAND_RANGE):
    base_note = chord[0]
    variations = get_variations(tuning, chord, hand_range)
    variations_5 = get_variations(tuning[1:], chord, hand_range)
    variations_4 = get_variations(tuning[2:], chord, hand_range)
    correct_vars = []
    for v in variations:
        if tuning[0].add(v[0]) == base_note:
            correct_vars.append(v)
    for v in variations_5:
        if tuning[1].add(v[0]) == base_note:
            correct_vars.append(v)
    for v in variations_4:
        if tuning[2].add(v[0]) == base_note:
            correct_vars.append(v)
    # sort by lowest non-zero. If equal, use sum of indices
    correct_vars.sort(key=lambda v: (min([z for z in v if z > 0]), sum(v)))
    return correct_vars


def validate_chord(neck, chord: list[Notes], places: tuple[int]):
    if not _validate_all_notes_present(neck, chord, places):
        return False
    return True


def _validate_all_notes_present(neck, chord: list[Notes], places: tuple[int]):

    found_notes = set()
    for i, p in enumerate(places):
        found_notes.add(neck[p, i])
    return found_notes == {n.value for n in chord}


if __name__ == "__main__":
    base_note = Notes.G
    chord = get_chord_notes(base_note, ChordTypes.dim7)
    tuning = [Notes.E, Notes.A, Notes.D, Notes.G, Notes.B, Notes.E]
    print(f"{chord=}")
    print(f"{tuning=}")
    variations = get_variations(tuning, chord)
    # pprint(variations)
    variations_5 = get_variations(tuning[1:], chord)
    variations_4 = get_variations(tuning[2:], chord)
    # print(variations_4)

    print("------------ Correct base notes ------------")
    neck = get_guitar_neck(tuning)
    correct_vars = []
    for v in variations:
        if Notes.E.add(v[0]) == base_note:
            correct_vars.append(v)
    for v in variations_5:
        if Notes.A.add(v[0]) == base_note:
            correct_vars.append(v)
    for v in variations_4:
        if Notes.D.add(v[0]) == base_note:
            correct_vars.append(v)
    # sort by lowest non-zero. If equal, use sum of indices
    correct_vars.sort(key=lambda v: (min([z for z in v if z > 0]), sum(v)))
    pprint(f"Total variations: {len(correct_vars)}. Showing first 20.")
    pprint(correct_vars[:20])
