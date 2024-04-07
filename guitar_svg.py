import svgwrite

def generate_guitar_chord_svg(chord_positions):
    black = svgwrite.rgb(80,80,80)
    # Define constants
    string_count = 6
    fret_count = 7 #max(chord_positions) + 1


    # Define dimensions
    neck_width = 120
    neck_height = 160
    fret_spacing = neck_height / (fret_count - 1)
    string_spacing = neck_width / (string_count - 1)
    dot_radius = 5
    x_margin = 6

    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(neck_width+2*x_margin, neck_height))

    # Draw frets
    for i in range(fret_count):
        y = i * fret_spacing
        dwg.add(dwg.line((x_margin, y), (neck_width+x_margin, y), stroke=black))

    # Draw strings
    for i in range(string_count):
        x = i * string_spacing + x_margin
        dwg.add(dwg.line((x, 0), (x, neck_height), stroke=black))

    # Draw chord positions
    for string_num, fret_num in enumerate(chord_positions):
        if fret_num == -1:
            x = (string_num-0.25) * string_spacing + x_margin
            y = fret_spacing*0.25
            # Adjust position for E strings
            dwg.add(dwg.line((x, y), (x+0.5*string_spacing, fret_spacing*0.75), stroke=svgwrite.rgb(250, 0, 0)))
            dwg.add(dwg.line((x, fret_spacing*0.75), (x+0.5*string_spacing, y), stroke=svgwrite.rgb(250, 0, 0)))
             
            
        if fret_num > 0:
            x = string_num * string_spacing + x_margin
            y = (fret_num - 1) * fret_spacing
            # Adjust position for E strings
            y += fret_spacing / 2
            dwg.add(dwg.circle(center=(x, y), r=dot_radius, fill=black))

    # Save SVG string
    return dwg.tostring()

# Example usage
if __name__=="__main__":
    chord_positions = (3, 2, 0, 0, 0, 3)  # G major chord
    svg_string = generate_guitar_chord_svg(chord_positions)
    print(svg_string)
