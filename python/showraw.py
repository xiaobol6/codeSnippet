#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import cv2, os, sys, re, getopt, struct
import matplotlib.pyplot as plt


def showPlt(srcinfo, raw):
    # 创建一个指定大小的图形，设置分辨率和背景色
    plt.figure(dpi=200, facecolor='lightgrey', edgecolor='black')

    plt.subplot(2, 2, 1), plt.title('RG')  # 0 = R Gr Gb B
    rgb = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerRG2RGB)
    plt.imshow(rgb.astype("uint8")), plt.axis('off')

    plt.subplot(2, 2, 2), plt.title('GR')  # 1 = Gr R B Gb
    rgb = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerGR2RGB)
    plt.imshow(rgb.astype("uint8")), plt.axis('off')

    plt.subplot(2, 2, 3), plt.title('GB')  # 2 = Gb B R Gr
    rgb = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerGB2RGB)
    plt.imshow(rgb.astype("uint8")), plt.axis('off')

    plt.subplot(2, 2, 4), plt.title('BG')  # 3 = B Gb Gr R
    rgb = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerBG2RGB)
    plt.imshow(rgb.astype("uint8")), plt.axis('off')

    # 使用 tight_layout 自动调整子图参数
    plt.tight_layout()
    plt.show()


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
        if srcinfo["endian"]:
            unpacked_pixels = struct.unpack('>' + pixels_format, rfd.read())
        else:
            unpacked_pixels = struct.unpack('<' + pixels_format, rfd.read())
        # print(type(unpacked_pixels), unpacked_pixels[:10])
        raw = np.array(unpacked_pixels).reshape((srcinfo["height"], srcinfo["width"]))
        # print(type(raw), raw[:1, :10])
        pass
    #
    if srcinfo["msb"]:
        raw = raw >> (bpp - 8) if bpp> 8 else raw
    else:
        raw = raw >> (srcinfo["depth"] - 8) if srcinfo["depth"] > 8 else raw
    # show
    if ("show" in srcinfo and srcinfo["show"] == "plt") or not "cfa" in srcinfo:
        showPlt(srcinfo, raw)
    else:
        # 创建一个指定大小的图形，设置分辨率和背景色
        if srcinfo["cfa"].lower() == "rg":
            rgbImg = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerRG2BGR)
        elif srcinfo["cfa"].lower() == "gr":
            rgbImg = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerGR2BGR)
        elif srcinfo["cfa"].lower() == "gb":
            rgbImg = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerGB2BGR)
        else:
            rgbImg = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerBG2BGR)
        cv2.imshow("img", rgbImg)
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
    s show by plt or cv
    H help
    example:
    ./showraw.py -i xxx.raw -w 1920 -h 1080 -d 12 -p 0 -c gb -m 0 -e 0
    """)


def cmd_line_parse(srcinfo):
    opts, args = getopt.getopt(sys.argv[1:], '-i:-w:-h:-d:-p:-c:-m:-e:-s:-H',
                               ['input=', 'width=', 'height=', 'depth=', 'pack=', 'cfa=', 'msb=', 'endian=',
                                'show=', "help"])
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
        elif opt_name in ('-s', '--show'):
            srcinfo["show"] = opt_value
        elif opt_name in ('-H', '--help'):
            useage()
            return True
        pass
    if not all(key in srcinfo for key in ["file", "width", "height", "depth", "pack", "msb", "endian"]):
        useage()
        return True
    return False


if __name__ == '__main__':
    srcinfo = {}
    ret = cmd_line_parse(srcinfo)
    if ret:
        exit()
    # print(srcinfo)
    showCV(srcinfo)
