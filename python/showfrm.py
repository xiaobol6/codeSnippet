#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
import cv2, os, sys, re, getopt
import matplotlib.pyplot as plt


def showfrm2(sfile):
    temp_dict = {}
    with open(sfile, 'rb') as rfd:
        headline = rfd.readline().decode('ascii').strip().split('.')
        for idx in headline[1:]:
            tmp_line = rfd.readline().decode('ascii').strip()
            temp_dict[re.search(r'\w+', idx).group()] = int(tmp_line) if tmp_line.isdigit() else tmp_line
        rawdata = np.frombuffer(rfd.read(), dtype="uint" + str(temp_dict["type"]))
        with open(sfile + ".raw", 'wb') as wfd:
            wfd.write(rawdata)
        raw = rawdata.reshape((temp_dict["height"], temp_dict["width"]))
        pass
    #
    raw = raw >> 4

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


def showfrm(sfile):
    temp_dict = {}
    with open(sfile, 'rb') as rfd:
        headline = rfd.readline().decode('ascii').strip().split('.')
        for idx in headline[1:]:
            tmp_line = rfd.readline().decode('ascii').strip()
            temp_dict[re.search(r'\w+', idx).group()] = int(tmp_line) if tmp_line.isdigit() else tmp_line
        rawdata = np.frombuffer(rfd.read(), dtype="uint" + str(temp_dict["type"]))
        with open(sfile + ".raw", 'wb') as wfd:
            wfd.write(rawdata)
        raw = rawdata.reshape((temp_dict["height"], temp_dict["width"]))
        pass
    #
    raw = raw >> 4

    # 创建一个指定大小的图形，设置分辨率和背景色
    rgbImg = cv2.cvtColor(raw.astype("uint8"), cv2.COLOR_BayerGB2BGR)
    cv2.imshow("img", rgbImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def useage():
    print("""
    i input
    s show by plt or cv
    h help
    example:
    ./showfrm.py -i xxx.frm -s plt
    """)


funclist = {
    "plt": showfrm2,
    "cv": showfrm
}

if __name__ == '__main__':
    # showfrm("input_1920x1080_raw12_unpack_lsb_littleEndian.frm")
    srcinfo = {}
    opts, args = getopt.getopt(sys.argv[1:], '-i:-s:-h', ['input=', 'show=', "help"])
    for opt_name, opt_value in opts:
        if opt_name in ('-i', '--input'):
            srcinfo["file"] = opt_value
        elif opt_name in ('-s', '--show'):
            srcinfo["show"] = opt_value
        elif opt_name in ('-h', '--help'):
            useage()
        pass
    if "file" in srcinfo and "show" in srcinfo:
        funclist[srcinfo["show"]](srcinfo["file"])
    else:
        useage()
