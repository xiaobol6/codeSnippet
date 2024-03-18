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


def showraw(raw, srcinfo):
    # 定义像素值的格式
    if srcinfo["depth"] > 16:
        bpp = 32
    elif srcinfo["depth"] > 8:
        bpp = 16
    else:
        bpp = 8
    if srcinfo["msb"]:
        raw = raw >> (bpp - 8) if bpp > 8 else raw
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


def string_parse(value, key, srcinfo, dstinfo):
    if "," in value:
        srcinfo[key], dstinfo[key] = value.strip().split(',')
    else:
        dstinfo[key] = srcinfo[key] = value.strip()


def integer_parse(value, key, srcinfo, dstinfo):
    if "," in value:
        srcinfo[key], dstinfo[key] = [int(x) for x in value.strip().split(',')]
    else:
        dstinfo[key] = srcinfo[key] = int(value.strip())


def cmd_line_parse(srcinfo, dstinfo):
    opts, args = getopt.getopt(sys.argv[1:], '-i:-w:-h:-d:-p:-c:-m:-e:-s:-H',
                               ['input=', 'width=', 'height=', 'depth=', 'pack=', 'cfa=', 'msb=', 'endian=',
                                'show=', "help"])
    for opt_name, opt_value in opts:
        if opt_name in ('-i', '--input'):
            string_parse(opt_value, "file", srcinfo, dstinfo)
            if dstinfo["file"] == srcinfo["file"]:
                dstinfo["file"] = "output.raw"
        elif opt_name in ('-w', '--width'):
            integer_parse(opt_value, "width", srcinfo, dstinfo)
        elif opt_name in ('-h', '--height'):
            integer_parse(opt_value, "height", srcinfo, dstinfo)
        elif opt_name in ('-d', '--depth'):
            integer_parse(opt_value, "depth", srcinfo, dstinfo)
        elif opt_name in ('-p', '--pack'):
            integer_parse(opt_value, "pack", srcinfo, dstinfo)
        elif opt_name in ('-c', '--cfa'):
            string_parse(opt_value, "cfa", srcinfo, dstinfo)
        elif opt_name in ('-m', '--msb'):
            integer_parse(opt_value, "msb", srcinfo, dstinfo)
        elif opt_name in ('-e', '--endian'):
            integer_parse(opt_value, "endian", srcinfo, dstinfo)
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


def read_raw(srcinfo):
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
        raw = np.array(unpacked_pixels).reshape((srcinfo["height"], srcinfo["width"]))
        pass
    return raw


def write_raw(dstraw, dstinfo):
    # 定义像素值的格式
    if dstinfo["depth"] > 16:
        bpp = 32
        pixel_format = 'I'
    elif dstinfo["depth"] > 8:
        bpp = 16
        pixel_format = 'H'
    else:
        bpp = 8
        pixel_format = 'B'
    pixels_format = pixel_format * dstinfo["width"]
    with open(dstinfo["file"], 'wb') as wfd:
        for line in dstraw:
            if dstinfo["endian"]:
                # 使用'>'前缀指定大端字节序，并将像素值列表打包为二进制数据
                wfd.write(struct.pack('>' + pixels_format, *line))
            else:
                # 使用'<'前缀指定小端字节序，并将像素值列表打包为二进制数据
                wfd.write(struct.pack('<' + pixels_format, *line))
            pass
        pass
    pass


def bilinear_interpolation(src, src_w, src_h, dst_w, dst_h):
    if src_w == dst_w and src_h == dst_h:
        return src
    # 中心对齐，目标像素在原图上的坐标
    width_src_p = np.array([(i + 0.5) * src_w / dst_w - 0.5 for i in range(dst_w)])
    height_src_p = np.array([(i + 0.5) * src_h / dst_h - 0.5 for i in range(dst_h)])
    # repeat，以便花式检索
    width_src_p = np.repeat(width_src_p.reshape(1, dst_w), dst_h, axis=0)
    height_src_p = np.repeat(height_src_p.reshape(dst_h, 1), dst_w, axis=1)

    # 坐标过滤，滤掉超边界数据
    width_src_p = np.clip(width_src_p, 0, src_w - 1)
    height_src_p = np.clip(height_src_p, 0, src_h - 1)
    # print(height_src_p)

    # 找出像素点P周围的4个Q点
    width_src_0 = np.clip(width_src_p, 0, src_w - 2).astype(np.int32)
    width_src_1 = width_src_0 + 1
    # print(width_src_1)
    height_src_0 = np.clip(height_src_p, 0, src_h - 2).astype(np.int32)
    height_src_1 = height_src_0 + 1
    # print(height_src_1)

    # 找出坐标像素点值
    f_00 = src[height_src_0, width_src_0]
    f_01 = src[height_src_0, width_src_1]
    f_10 = src[height_src_1, width_src_0]
    f_11 = src[height_src_1, width_src_1]
    # print(f_00)

    """计算权重"""
    w_00 = ((height_src_1 - height_src_p) * (width_src_1 - width_src_p))
    w_01 = ((height_src_1 - height_src_p) * (width_src_p - width_src_0))
    w_10 = ((height_src_p - height_src_0) * (width_src_1 - width_src_p))
    w_11 = ((height_src_p - height_src_0) * (width_src_p - width_src_0))

    """计算目标像素值"""
    return (w_00 * f_00 + w_01 * f_01 + w_10 * f_10 + w_11 * f_11)


def rawsclaer(srcraw, srcinfo, dstraw, dstinfo):
    src_00 = srcraw[::2, ::2]
    src_01 = srcraw[1::2, ::2]
    src_10 = srcraw[::2, 1::2]
    src_11 = srcraw[1::2, 1::2]
    #
    ssubh, ssubw = src_00.shape
    dsubw = dstinfo["width"] // 2
    dsubh = dstinfo["height"] // 2
    #
    dst_00 = bilinear_interpolation(src_00, ssubw, ssubh, dsubw, dsubh)
    dst_01 = bilinear_interpolation(src_01, ssubw, ssubh, dsubw, dsubh)
    dst_10 = bilinear_interpolation(src_10, ssubw, ssubh, dsubw, dsubh)
    dst_11 = bilinear_interpolation(src_11, ssubw, ssubh, dsubw, dsubh)
    #
    dstraw[::2, ::2] = dst_00
    dstraw[1::2, ::2] = dst_01
    dstraw[::2, 1::2] = dst_10
    dstraw[1::2, 1::2] = dst_11
    # 先纠正单pixel 位深
    if dstinfo["depth"] > srcinfo["depth"]:
        dstraw = dstraw << (dstinfo["depth"] - srcinfo["depth"])
    else:
        dstraw = dstraw >> (srcinfo["depth"] - dstinfo["depth"])
    # 再纠正msb、lsb数据位
    if dstinfo["depth"] > 16:
        bpp = 32
    elif dstinfo["depth"] > 8:
        bpp = 16
    else:
        bpp = 8
    # print(dstraw[:1,:10])
    if dstinfo["msb"]:
        dstraw = dstraw << (bpp - dstinfo["depth"]) if bpp > dstinfo["depth"] else dstraw
    write_raw(dstraw, dstinfo)
    # print(dstraw[:1, :10])
    #
    showraw(dstraw, dstinfo)



if __name__ == '__main__':
    srcinfo = {}
    dstinfo = {}
    ret = cmd_line_parse(srcinfo, dstinfo)
    if ret:
        exit()
    # print(srcinfo)
    # print(dstinfo)
    #
    srcraw = read_raw(srcinfo)
    #
    dstraw = np.zeros((dstinfo["height"], dstinfo["width"]), dtype=np.int32)
    rawsclaer(srcraw, srcinfo, dstraw, dstinfo)
    #
    # showraw(srcraw, srcinfo)
