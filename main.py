import fullcontrol as fc
import lab.fullcontrol as fclab

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

def main():
    steps = []

    # start points
    x = 50
    y = 50
    z = initial_z

    # side length
    size = 20

    perimeter = fc.rectangleXY(fc.Point(x=x, y=y, z=z), size, size)

    steps.append(perimeter)

    fill = fclab.fill_base_simple(perimeter, 3, 1, EW)
    steps.append(fill)

    box = fc.move(perimeter, fc.Vector(z=EH), copy=True, copy_quantity=round(size / EH))
    steps.extend(box)

    steps.append(fc.Hotend(temp=0))
    steps.append(fc.Buildplate(temp=0))
    steps.append(fc.travel_to(fc.Point(x=100, y=100, z=z + 25)))

    write_gcode(steps)

if __name__ == "__main__":
    main()
