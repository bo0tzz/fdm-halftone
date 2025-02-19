from PIL import Image
import fullcontrol as fc
import lab.fullcontrol as fclab

from gcode import inputs

design_name = 'plain-box'
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
pixel_count = cube_side_length / pixel_res

def preview(steps):
    fc.transform(steps, 'plot', fc.PlotControls(style='line', zoom=0.7))

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

def mapper(image: Image):
    w, h = image.size # assumed square
    assert w == h
    factor = w / pixel_count
    def get_pixel(x, y):
        point = (round(x * factor), round(y * factor))
        return image.getpixel(point)
    return get_pixel

def make_box():
    steps = []

    # start points
    x = 50
    y = 50
    z = initial_z


    perimeter = fc.rectangleXY(fc.Point(x=x, y=y, z=z), cube_side_length, cube_side_length)

    steps.append(perimeter)

    fill = fclab.fill_base_simple(perimeter, 3, 1, EW)
    steps.append(fill)

    box = fc.move(perimeter, fc.Vector(z=EH), copy=True, copy_quantity=round(cube_side_length / EH))
    steps.extend(box)

    steps.append(fc.Hotend(temp=0))
    steps.append(fc.Buildplate(temp=0))
    steps.append(fc.travel_to(fc.Point(x=100, y=100, z=z + 25)))

def main():
    img = inputs.cross()
    get_pixel = mapper(img)
    print(get_pixel(1, 1))
    # box = make_box()
    # write_gcode(box)

if __name__ == "__main__":
    main()
