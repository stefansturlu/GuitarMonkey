import svgwrite


def generate_guitar_chord_svg(chord_positions: list[int], chord_notes: list[str] = None):
    # Font styles
    font = "Arial Narrow"
    black = svgwrite.rgb(80, 80, 80)
    red = svgwrite.rgb(250, 0, 0)
    text_colour = svgwrite.rgb(250, 80, 80)

    # Define constants
    string_count = 6
    fret_count = 7  # max(chord_positions) + 1

    # Define dimensions
    neck_width = 120
    neck_height = 160
    fret_spacing = neck_height / (fret_count - 1)
    string_spacing = neck_width / (string_count - 1)
    dot_radius = 9
    x_margin = 10
    y_margin = 20

    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(neck_width + 2 * x_margin, neck_height + 1.1 * y_margin))

    # Draw frets
    for i in range(fret_count):
        y = i * fret_spacing + y_margin

        dwg.add(dwg.line((x_margin, y), (neck_width + x_margin, y), stroke=black, stroke_width=1 + 3 * (i == 0)))

    # Draw strings
    is_high_on_neck = bool(max(chord_positions) >= 7)
    for i in range(string_count):
        x = i * string_spacing + x_margin
        y_lower = y_margin + fret_spacing * is_high_on_neck
        dwg.add(dwg.line((x, y_lower), (x, neck_height + y_margin), stroke=black))
        if is_high_on_neck and i not in {2, 3}:
            dwg.add(dwg.line((x, y_margin), (x, y_lower), stroke=black, stroke_dasharray=f"4,2"))

    # Handle if chord is high on neck
    if is_high_on_neck:
        min_positive_chord_position = min([c + 100 * (c <= 0) for c in chord_positions])
        chord_positions = [c + 2 - min_positive_chord_position if c > 0 else c for c in chord_positions]
        x = x_margin + neck_width / 2
        y = y_margin + fret_spacing * 0.7
        text_style = f"font-family: {font}, sans-serif; font-size: 12px; font-weight: lighter; letter-spacing: 1px"
        dwg.add(
            dwg.text(
                f"Fret {min_positive_chord_position}",
                insert=(x, y),
                text_anchor="middle",
                stroke=black,
                fill=black,
                style=text_style,
            )
        )

    # Draw chord positions
    for string_num, fret_num in enumerate(chord_positions):
        if fret_num == -1:
            x = (string_num - 0.25) * string_spacing + x_margin
            y_upper = fret_spacing * 0.25 + y_margin
            y_lower = fret_spacing * 0.75 + y_margin
            dwg.add(dwg.line((x, y_lower), (x + 0.5 * string_spacing, y_upper), stroke=red, stroke_width=2))
            dwg.add(dwg.line((x, y_upper), (x + 0.5 * string_spacing, y_lower), stroke=red, stroke_width=2))

        if fret_num > 0:
            x = string_num * string_spacing + x_margin
            y = (fret_num - 1) * fret_spacing + y_margin
            # Adjust position for E strings
            y += fret_spacing / 2
            dwg.add(dwg.circle(center=(x, y), r=dot_radius, fill=black))

        if chord_notes and fret_num >= 0:
            x = string_num * string_spacing + x_margin
            y = (fret_num - 0.36) * fret_spacing + y_margin + 3 * (fret_num == 0)
            # Adjust position for E strings
            text_size = 9 + 3 * (fret_num == 0)
            text_style = f"font-family: {font}, sans-serif; font-size: {text_size}px; font-weight: lighter"

            dwg.add(
                dwg.text(
                    chord_notes[string_num],
                    insert=(x, y),
                    text_anchor="middle",
                    stroke=text_colour,
                    fill=text_colour,
                    style=text_style,
                )
            )

    # Save SVG string
    return dwg.tostring()


# Example usage
if __name__ == "__main__":
    chord_positions = (3, 2, 0, 0, 0, 3)  # G major chord
    svg_string = generate_guitar_chord_svg(chord_positions)
    print(svg_string)
