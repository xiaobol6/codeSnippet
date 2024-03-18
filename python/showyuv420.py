#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import cv2, os, sys, re, getopt, struct
import matplotlib.pyplot as plt

enum_format = {
    "NV21": cv2.COLOR_YUV2BGR_NV21,
    "NV12": cv2.COLOR_YUV2BGR_NV12,
}


def showCV(srcinfo):
    size = os.path.getsize(srcinfo["file"])
    # 定义像素值的格式
    if srcinfo["depth"] > 16:
        bpp = 32
        pixel_format = 'I'
        len = size >> 2
    elif srcinfo["depth"] > 8:
        bpp = 16
        pixel_format = 'H'
        len = size >> 1
    else:
        bpp = 8
        pixel_format = 'B'
        len = size >> 0
    # 拼接格式字符串以表示整个列表
    pixels_format = pixel_format * len
    with open(srcinfo["file"], 'rb') as rfd:
        if "endian" in srcinfo and srcinfo["endian"]:
            unpacked_pixels = struct.unpack('>' + pixels_format, rfd.read())
        else:
            unpacked_pixels = struct.unpack('<' + pixels_format, rfd.read())
        # print(type(unpacked_pixels), unpacked_pixels[:10])
        raw = np.array(unpacked_pixels).reshape((srcinfo["height"] + srcinfo["height"] // 2, srcinfo["width"]))
        # print(type(raw), raw[:1, :10])
        pass
    #
    if "msb" in srcinfo and srcinfo["msb"]:
        raw = raw >> (bpp - 8) if bpp > 8 else raw
    else:
        raw = raw >> (srcinfo["depth"] - 8) if srcinfo["depth"] > 8 else raw
    # 创建一个指定大小的图形，设置分辨率和背景色
    bgr_data = cv2.cvtColor(raw.astype(np.uint8), enum_format[srcinfo["cfa"].upper()])
    cv2.imwrite(srcinfo["file"] + ".jpg", bgr_data)
    cv2.imshow("img", bgr_data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass


def useage():
    print("""
    i input
    w width
    h height
    d depth
    p pack      0 unpack; 1 pack
    c cfa       rg; gr; gb; bg
    m msb       0 lsb; 1 msb
    e endian    0 little; 1 big
    H help
    example:
    ./showyuv420.py -i output7_09_ar0233.raw -w 1920 -h 1080
    """)


def cmd_line_parse(srcinfo):
    opts, args = getopt.getopt(sys.argv[1:], '-i:-w:-h:-d:-p:-c:-m:-e:-H',
                               ['input=', 'width=', 'height=', 'depth=', 'pack=', 'cfa=', 'msb=', 'endian=', "help"])
    for opt_name, opt_value in opts:
        if opt_name in ('-i', '--input'):
            srcinfo["file"] = opt_value
        elif opt_name in ('-w', '--width'):
            srcinfo["width"] = int(opt_value)
        elif opt_name in ('-h', '--height'):
            srcinfo["height"] = int(opt_value)
        elif opt_name in ('-d', '--depth'):
            srcinfo["depth"] = int(opt_value)
        elif opt_name in ('-p', '--pack'):
            srcinfo["pack"] = int(opt_value)
        elif opt_name in ('-c', '--cfa'):
            srcinfo["cfa"] = opt_value
        elif opt_name in ('-m', '--msb'):
            srcinfo["msb"] = int(opt_value)
        elif opt_name in ('-e', '--endian'):
            srcinfo["endian"] = int(opt_value)
        elif opt_name in ('-H', '--help'):
            useage()
            return True
        pass
    if not all(key in srcinfo for key in ["file", "width", "height"]):
        useage()
        return True
    return False


if __name__ == '__main__':
    srcinfo = {"depth": 8, "cfa": "NV21"}
    ret = cmd_line_parse(srcinfo)
    if ret:
        exit()
    # print(srcinfo)
    showCV(srcinfo)
