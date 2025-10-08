from PIL import Image

imageSize= 500

img = Image.open('poulet.jpg')
long,larg = img.size

if long<larg:
    newlarg = imageSize
    newlong = imageSize*long/larg
else:
    newlong = imageSize
    newlarg = imageSize*larg/long

newlong = int(newlong)
newlarg = int(newlarg)

result = Image.new('L',(int(newlong),int(newlarg)))
img = img.resize((newlong,newlarg))

blackValue = [[0 for x in range(newlong)] for y in range(newlarg)]

for y in range(newlarg):
    for x in range(newlong):
        print(x,y)
        r,v,b = img.getpixel([x, y])
        blackValue[y][x] = ((r+v+b)/3)/255
        result.putpixel((x,y),int((r+v+b)/3))

print(blackValue)
result.show()