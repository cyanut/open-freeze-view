#!/usr/bin/python
import sys
import struct
import subprocess


def usage():
    print sys.argv[0], "input.ffii", "output.webm"
    quit()

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage()


    f = open(sys.argv[1])
    m = f.read(8)
    height, width = struct.unpack(">2I", m)
    print(height, width)
    of =  sys.argv[2]
    rate = "15/4"
    if len(sys.argv) == 4:
        rate = sys.argv[3]

    cmdstr = ('ffmpeg', '-y', '-r', rate,\
            '-f', 'rawvideo',
            '-pix_fmt', 'gray',
            '-s', str(width)+"x"+str(height),
            '-i', '-',
            '-c:v', 'libvpx',
            '-crf', '10',
            of)

    p = subprocess.Popen(cmdstr, stdin=subprocess.PIPE, shell=False)
    
    while True:
        img = f.read(width*height)
        p.stdin.write(img)
        m = f.read(8)
        if not m:
            break
        width, height = struct.unpack(">2I", m)

