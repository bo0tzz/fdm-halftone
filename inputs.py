from PIL import Image, ImageDraw

def pad(pil_img, amount):
    width, height = pil_img.size
    new_width = width + amount * 2
    new_height = height + amount * 2
    result = Image.new('L', (new_width, new_height), 255)
    result.paste(pil_img, (amount, amount))
    return result


def cross():
    img = Image.new('L', (1000, 1000), color=255)
    draw = ImageDraw.Draw(img)

    line_width = 200
    line_color = 0
    width, height = img.size  # Get actual dimensions

    # Draw both lines of the X
    draw.line((0, 0, width, height), fill=line_color, width=line_width)
    draw.line((width, 0, 0, height), fill=line_color, width=line_width)

    img = pad(img, 200)
    return img

def phone():
    img = Image.open("./inputs/phone-icon-th.png")
    bg = Image.new('L', img.size, 255)
    bg.paste(img, mask=img.split()[-1])

    return pad(bg, 10)

if __name__ == "__main__":
    phone().save("preview.png")
