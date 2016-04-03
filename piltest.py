from PIL import Image, ImageDraw
im = Image.new("RGB", (512, 512), "white")
draw = ImageDraw.Draw(im)
draw.ellipse(((100, 100), (200, 200)), fill=128)
im.save("HELLOWORLDTEST", "PNG")