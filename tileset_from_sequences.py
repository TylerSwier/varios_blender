import sys
# for install pil:
# pip install pillow
from PIL import Image

imagesNames = []
totalFrames = 53
nameSeq = "tvVideo_"
extSeq = ".jpg"
for i in range(0, totalFrames):
	padding = str("%03d" % (i)) # 03 is the padding
	filename = nameSeq + padding + extSeq
	# print(filename)
	imagesNames.append(filename)

# print(images)
# images = map(Image.open, ['Test1.jpg', 'Test2.jpg', 'Test3.jpg'])
images = map(Image.open, imagesNames)
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_img = Image.new('RGB', (total_width, max_height))

x_offset = 0
for img in images:
  new_img.paste(img, (x_offset,0))
  x_offset += img.size[0]

new_im.save('outputResult.jpg')
