#!/bin/bash

./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_8bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,8 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_10bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,10 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_14bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,14 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_16bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,16 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_20bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,20 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_22bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,22 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_depth_1920x1080_24bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,24 -p 0 -c gr -m 0,1 -e 0 -s cv

./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_128x128_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,128 -h 1080,128 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_320x240_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,320 -h 1080,240 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_640x480_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,640 -h 1080,480 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_800x600_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,800 -h 1080,600 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_1280x720_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,1280 -h 1080,720 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_1920x1080_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920 -h 1080 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_2592x1944_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,2592 -h 1080,1944 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_3840x2160_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,3840 -h 1080,2160 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_4096x3328_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,4096 -h 1080,3328 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
./rawResize.py -i simx385_1920x1080_20bits_gbrg_2320k_a.colorchecker_little_endian.raw,imx385_msize_5696x3328_12bits_gbrg_msb_little_endian_2320k_a.colorchecker.raw  -w 1920,5696 -h 1080,3328 -d 20,12 -p 0 -c gr -m 0,1 -e 0 -s cv
