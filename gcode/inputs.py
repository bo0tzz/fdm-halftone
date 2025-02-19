from PIL import Image, ImageDraw


def cross():
    img = Image.new('L', (1000, 1000), color=255)
    draw = ImageDraw.Draw(img)

    margin = 200
    line_width = 200
    line_color = 0
    width, height = img.size  # Get actual dimensions

    # Calculate coordinates with margin
    x1, y1 = margin, margin  # Top-left start
    x2, y2 = width - margin, height - margin  # Bottom-end end
    x3, y3 = width - margin, margin  # Top-right start
    x4, y4 = margin, height - margin  # Bottom-left end

    # Draw both lines of the X
    draw.line((x1, y1, x2, y2), fill=line_color, width=line_width)
    draw.line((x3, y3, x4, y4), fill=line_color, width=line_width)

    return img
