#Sample output: http://imgur.com/a/1ufjg

import itertools
import copy
import math
#requires the animation module from https://github.com/kms70847/Animation/blob/master/lib/animation/__init__.py
import animation
from PIL import Image, ImageDraw

SQUARE_SIZE = 16
INTERSQUARE_MARGIN = 4
BORDER_MARGIN = 20
BACKGROUND_COLOR = (0,0,0)
ON_COLOR = (0, 255, 0)
OFF_COLOR = (32, 32, 32)

#renders an image containing the background color and empty slots for the given field.
#returns: image instance, imagedraw instance, rows int, cols int
def render_base(field):
    rows = len(field)
    assert rows > 0
    cols = len(field[0])
    assert cols > 0
    width  = SQUARE_SIZE * cols + INTERSQUARE_MARGIN * (cols-1) + BORDER_MARGIN * 2
    height = SQUARE_SIZE * rows + INTERSQUARE_MARGIN * (rows-1) + BORDER_MARGIN * 2
    img = Image.new("RGB", (width, height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img, "RGBA")
    for i in range(cols):
        for j in range(rows):
            x = BORDER_MARGIN + i * (SQUARE_SIZE + INTERSQUARE_MARGIN)
            y = BORDER_MARGIN + j * (SQUARE_SIZE + INTERSQUARE_MARGIN)
            draw.rectangle((x,y,x+SQUARE_SIZE,y+SQUARE_SIZE), OFF_COLOR)
    return img, draw, rows, cols
    

def render_with_row_rotation(field, row_to_rotate, f):
    img, draw, rows, cols = render_base(field)
    assert 0 <= row_to_rotate < rows

    for i in range(cols):
        for j in range(rows):
            if field[j][i]:
                x = BORDER_MARGIN + i * (SQUARE_SIZE + INTERSQUARE_MARGIN)
                y = BORDER_MARGIN + j * (SQUARE_SIZE + INTERSQUARE_MARGIN)
                opacity = 255
                if j == row_to_rotate:
                    x += int((SQUARE_SIZE + INTERSQUARE_MARGIN) * f)
                    if i == cols-1:
                        #fade out as you move off screen
                        opacity = int(255*(1-f))
                draw.rectangle((x,y,x+SQUARE_SIZE,y+SQUARE_SIZE), ON_COLOR + (opacity,))

    if field[row_to_rotate][-1]:
        x = BORDER_MARGIN + -1 * (SQUARE_SIZE + INTERSQUARE_MARGIN)
        y = BORDER_MARGIN + row_to_rotate * (SQUARE_SIZE + INTERSQUARE_MARGIN)
        x += int((SQUARE_SIZE + INTERSQUARE_MARGIN) * f)
        opacity = int(255*f)
        draw.rectangle((x,y,x+SQUARE_SIZE,y+SQUARE_SIZE), ON_COLOR + (opacity,))
        
    return img

def render_with_col_rotation(field, x, f):
    field = zip(*field)
    img = render_with_row_rotation(field, x, f)
    return img.transpose(Image.TRANSPOSE)

def render_with_new_pixels(field, new_pixels, f):
    img, draw, rows, cols = render_base(field)
    for i in range(cols):
        for j in range(rows):
            if field[j][i]:
                x = BORDER_MARGIN + i * (SQUARE_SIZE + INTERSQUARE_MARGIN)
                y = BORDER_MARGIN + j * (SQUARE_SIZE + INTERSQUARE_MARGIN)
                draw.rectangle((x,y,x+SQUARE_SIZE, y+SQUARE_SIZE), ON_COLOR)
    for i,j in new_pixels:
        size = int(f*SQUARE_SIZE)
        offset = (SQUARE_SIZE - size)/2
        x = BORDER_MARGIN + i * (SQUARE_SIZE + INTERSQUARE_MARGIN) + offset
        y = BORDER_MARGIN + j * (SQUARE_SIZE + INTERSQUARE_MARGIN) + offset
        draw.rectangle((x,y,x+size, y+size), ON_COLOR)
    return img

def render_regular(field):
    return render_with_new_pixels(field, (), 0)

def parse_data():
    extract_ints = lambda line: [int("".join(v)) for k,v in itertools.groupby(line, str.isdigit) if k]
    ret = []
    with open("input") as file:
        for line in file:
            data = extract_ints(line)
            if line.startswith("rect"):
                x,y = data
                ret.append({"kind": "rect", "x":data[0], "y":data[1]})
            else:
                if "row" in line:
                    ret.append({"kind": "row", "y":data[0], "amt":data[1]})
                elif "column" in line:
                    ret.append({"kind": "col", "x":data[0], "amt":data[1]})
    return ret

def row_rotated(field, y, amt):
    field = copy.deepcopy(field)
    for i in range(amt):
        field[y] = [field[y][-1]] + field[y][:-1]
    return field
    
def transpose(field):
    return list(map(list, zip(*field)))

def col_rotated(field, x, amt):
    field = transpose(field)
    result = row_rotated(field, x, amt)
    return transpose(result)
    

def ease(f):
    return math.cos(f*math.pi/4)

data = parse_data()
field = [[0 for i in range(50)] for j in range(6)]
frames = []
FRAMES_PER_INSTRUCTION = 8
for line_no, line in enumerate(data, 1):
    print("Processing instruction {} of {}...".format(line_no, len(data)))
    if line["kind"] == "rect":
        to_activate = [(x,y) for x in range(line["x"]) for y in range(line["y"]) if not field[y][x]]
        for i in range(FRAMES_PER_INSTRUCTION):
            f = float(i) / FRAMES_PER_INSTRUCTION
            frames.append(render_with_new_pixels(field, to_activate,f))
        for x,y in to_activate:
            field[y][x] = 1
    elif line["kind"] == "row":
        intermediate_fields = [row_rotated(field, line["y"], i) for i in range(1+line["amt"])]
        for i in range(FRAMES_PER_INSTRUCTION):
            f = float(i) / FRAMES_PER_INSTRUCTION
            cur_field, f = divmod(f*line["amt"], 1)
            frames.append(render_with_row_rotation(intermediate_fields[int(cur_field)], line["y"], f))
        field = intermediate_fields[-1]
    elif line["kind"] == "col":
        intermediate_fields = [col_rotated(field, line["x"], i) for i in range(1+line["amt"])]
        field = intermediate_fields[-1]
        for i in range(FRAMES_PER_INSTRUCTION):
            f = float(i) / FRAMES_PER_INSTRUCTION
            cur_field, f = divmod(f*line["amt"], 1)
            frames.append(render_with_col_rotation(intermediate_fields[int(cur_field)], line["x"], f))

frames.append(render_regular(field))
for i in range(64):
    frames.append(frames[-1])

print("Compositing {} frames...".format(len(frames)))

animation.make_gif(frames)