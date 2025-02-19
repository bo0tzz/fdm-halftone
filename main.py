from PIL import Image
import fullcontrol as fc
import lab.fullcontrol as fclab

import inputs

design_name = 'phone-embossed-box'
nozzle_temp = 210
bed_temp = 65
print_speed = 1000
fan_percent = 0
printer_name='generic'

EW = 0.4 # extrusion width
EO = 0.8 # extrusion overlap %
EH = 0.2 # extrusion height (and layer height)
initial_z = EH*0.6 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion

cube_side_length = 20
pixel_res = EH
pixel_count = round(cube_side_length / pixel_res)

def preview(steps):
    fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7))

def write_gcode(steps):
    gcode_controls = fc.GcodeControls(
        printer_name=printer_name,
        initialization_data={
            'primer': 'front_lines_then_y',
            'print_speed': print_speed,
            'nozzle_temp': nozzle_temp,
            'bed_temp': bed_temp,
            'fan_percent': fan_percent,
            'extrusion_width': EW,
            'extrusion_height': EH})
    gcode = fc.transform(steps, 'gcode', gcode_controls)
    open(f'gcode/{design_name}.gcode', 'w').write(gcode)

def map_value(value, from_max, to_max):
    return min(value / from_max * to_max, to_max)

def map_point(point, source_res, target_res):
    x, y = point
    x = map_value(x, target_res, source_res)-1
    y = map_value(y, target_res, source_res)-1
    return round(x), round(y)

def mapper(image: Image, target_pixels):
    w, h = image.size # assumed square
    assert w == h
    def get_pixel(x, y):
        point = map_point((x, y), w, target_pixels)
        print(point)
        val = image.getpixel(point)
        print(f"=> {val}")
        return val
    return get_pixel

def emboss_face_line(perimeter, get_pixel):
    face = perimeter[:2]
    rest = perimeter[2:]

    face_from = face[0]
    face_to = face[1]
    assert face_from.y == face_to.y
    assert face_from.z == face_to.z
    y = face_from.y
    start = face_from.x
    target = face_to.x
    z = face_from.z

    line = [fc.GcodeComment(text="embossed face"), face_from]
    for point in range(pixel_count+1):
        x = point * pixel_res
        pixel_value = get_pixel(x, z)
        offset = map_value(pixel_value, 255, EW)
        print(offset)
        line.append(fc.Point(x=start+x, y=y+offset))
    assert line[-1].x == target
    line.append(fc.GcodeComment(text="perimeter"))
    line.extend(rest)
    return line

def make_box(get_pixel):
    steps = [fc.GcodeComment(text="layer 1")]

    # start points
    x = 50
    y = 50
    z = initial_z

    perimeter = fc.rectangleXY(fc.Point(x=x, y=y, z=z), cube_side_length, cube_side_length)

    steps.extend(perimeter)

    fill = fclab.fill_base_simple(perimeter, 3, 1, EW)
    steps.extend(fill)

    print("Generating layers")
    for layer in range(2, round(cube_side_length / EH)):
        steps.append(fc.GcodeComment(text=f"layer {layer}"))
        fan = min(70, (layer - 1) * 25)
        steps.append(fc.Fan(speed_percent=fan))
        z=layer * EH
        base = fc.move(perimeter, fc.Vector(z=z))
        steps.extend(emboss_face_line(base, get_pixel))

    steps.extend(fc.travel_to(fc.Point(x=100, y=100, z=z + 25)))
    steps.append(fc.Hotend(temp=0, wait=False))
    steps.append(fc.Buildplate(temp=0, wait=False))

    return steps

def main():
    img = inputs.phone()
    get_pixel = mapper(img, cube_side_length)
    box = make_box(get_pixel)
    # preview(box)
    write_gcode(box)

if __name__ == "__main__":
    main()
