from PIL import Image

img = Image.open('poulet.jpg')
result = Image.new('L',img.size)

long,larg = img.size

for x in range(larg):
    for y in range(long):
        r,v,b = img.getpixel([x, y])
        result.putpixel((x,y),int((r+v+b)/3))

result.show()