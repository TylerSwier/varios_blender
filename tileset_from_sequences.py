'''
2016 Jorge Hernandez - Melendez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

# this script needs to be placed next to the sequence of images

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
