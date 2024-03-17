import struct  
  
# 假设这是你的像素值列表，每个像素值是一个整数，范围在0到8192之间  
pixels = [1024, 2048, 4096, 0, 8191, 512, 768]  
  
# 定义像素值的格式，这里使用无符号整型（'I'），每个值占4个字节  
pixel_format = 'I'  
  
# 拼接格式字符串以表示整个列表  
pixels_format = pixel_format * len(pixels)  
  
# 以大端方式写入文件  
with open('pixels_big_endian.bin', 'wb') as f_big:  
    # 使用'>'前缀指定大端字节序，并将像素值列表打包为二进制数据  
    packed_pixels_big = struct.pack('>' + pixels_format, *pixels)  
    f_big.write(packed_pixels_big)  
  
# 以小端方式写入文件  
with open('pixels_little_endian.bin', 'wb') as f_little:  
    # 使用'<'前缀指定小端字节序，并将像素值列表打包为二进制数据  
    packed_pixels_little = struct.pack('<' + pixels_format, *pixels)  
    f_little.write(packed_pixels_little)

# 以大端方式读取文件  
with open('pixels_big_endian.bin', 'rb') as f_big:  
    packed_pixels_big = f_big.read()  
    # 使用'>'前缀和相同的格式字符串来解包数据  
    unpacked_pixels_big = struct.unpack('>' + pixels_format, packed_pixels_big)  
    print(unpacked_pixels_big)  
  
# 以小端方式读取文件  
with open('pixels_little_endian.bin', 'rb') as f_little:  
    packed_pixels_little = f_little.read()  
    # 使用'<'前缀和相同的格式字符串来解包数据  
    unpacked_pixels_little = struct.unpack('<' + pixels_format, packed_pixels_little)  
    print(unpacked_pixels_little)










# 读取raw图

import struct  
import numpy as np  
import matplotlib.pyplot as plt  
  
# 假设图像的宽度和高度  
width = 640  
height = 480  
  
# 打开二进制文件  
with open('image.raw', 'rb') as f:  
    # 读取整个文件内容  
    data = f.read()  
  
# 将数据转换为numpy数组  
# 注意：每个像素一个字节，所以使用'B'作为格式字符串，并且以小端模式读取（但实际上对于单个字节，大小端模式并不重要）  
img_data = np.array(struct.unpack(f'<{width*height}B', data)).reshape((height, width))  
  
# 使用matplotlib显示图像  
plt.imshow(img_data, cmap='gray')  
plt.show()
