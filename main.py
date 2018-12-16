#!/usr/bin/env python

# If you keep OpenSCAD in an unusual location, uncomment the following line of code and
# set it to the full path to the openscad executable.
# Note: Windows/python now support forward-slash characters in paths, so please use
#       those instead of backslashes which create a lot of confusion in code strings.
# OPENSCAD_PATH = "C:/Program Files/OpenSCAD/openscad"

# do not edit below unless you know what you are doing!
import os
import configparser
import platform
from shutil import copy, rmtree
import shlex
import random as rd
import time
import numpy as np
import math
import re
from PIL import Image
import subprocess as sp

halt = -1  # debug: terminate skipping this shell (0 to n to enable)

# Make sure we have a fresh random seed
rd.seed()

USE_SCAD_THREAD_TRAVERSAL = False
STL_DIR = "stl_files"
PREV_DIR = "prev"

def openscad():
    try:
        if OPENSCAD_PATH:
            return OPENSCAD_PATH
    except NameError:
        pass
    if os.getenv("OPENSCAD_PATH"):
        return os.getenv("OPENSCAD_PATH")
    if platform.system() == "Darwin":
        return "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    if platform.system() == "Windows":
        # Note: Windows allows forward slashes now
        return '"C:/Program Files/OpenSCAD/openscad"'
    # Default to linux-friendly CLI program name
    return "openscad"


def prepwd():
    # Linux and other systems that use PATH variables don't need an absolute path configured.
    # if os.path.exists(openscad_exe) == False:
    #     input("ERROR: openscad path not found.")
    #     exit()

    if os.path.exists(STL_DIR):
        rmtree(STL_DIR)
    os.mkdir(STL_DIR)  # Default perms: world-writable

    if os.path.exists(PREV_DIR):
        rmtree(PREV_DIR)
    os.mkdir(PREV_DIR)  # Default perms: world-writable

def has_scad_threading():
    cmd = [openscad(), "--help"]
    # Note: help comes on stderr
    out = sp.check_output(cmd, stderr=sp.STDOUT, universal_newlines=True)
    m = re.search(r"enable experimental features:\s(.+?)\n\s*\n", out, flags=re.DOTALL)
    if m:
        return "thread-traversal" in re.split(r"\s*\|\s*", m[1])
    return False


def scad_version():
    cmd = [openscad(), "--version"]
    # Note: version comes on stderr
    out = sp.check_output(cmd, stderr=sp.STDOUT, universal_newlines=True)
    m = re.search(r"enable experimental features:\s(.+?)\n\s*\n", out, flags=re.DOTALL)
    m = re.match(r"^\s*OpenSCAD version (\d{4})\.(\d\d)\.(\d\d)\s*$", out)
    return (int(m[1]), int(m[2]), int(m[3])) if m else ()


def execscad(threadid=0):
    print("Executing OpenSCAD script...")
    cmd = [openscad()]
    if USE_SCAD_THREAD_TRAVERSAL:
        cmd.append("--enable=thread-traversal")
    cmd.extend(
        [
            "-o",
            os.path.join(os.getcwd(), STL_DIR, str(shell + 1) + ".stl"),
            os.path.join(os.getcwd(), "make_shells.scad"),
        ]
    )
    print(cmd)
    sp.run(cmd)
    
def udnbers(n, vi, nc, mw, mh, stag):
    for y in range(0, mh):
        for x in range(0, mw):
            x3 = int((x + stag[y]) % mw)
            x2 = [x - 1, x + 1, x, x]
            y2 = [y, y, y - 1, y + 1]
            for i in range(0, 4):
                if stag[y] % mw > 0:
                    x2[i] = int((x2[i] + mw) % mw)
                else:
                    if x2[i] < 0:
                        x2[i] = 0
                    if x2[i] > mw - 1:
                        x2[i] = mw - 1
                if (
                    not ((x3 == 0 and i == 0) or (x3 == mh - 1 and i == 1))
                    and y2[i] > -1
                    and y2[i] < mh
                ):
                    n[x, y, i] = vi[int(x2[i]), int(y2[i])] == 0
                else:
                    n[x, y, i] = 0
            nc[x, y] = len(np.argwhere(n[x, y].astype("int")))


def genmaze(mw, mh, stag, st, ex):
    im = Image.new("L", [2 * mw + 1, 2 * mh + 1], 0)
    visited = np.zeros(mw * mh)
    nbercount = np.zeros(mw * mh)
    nbers = np.ones(mw * mh * 4)
    walls = np.ones(mw * mh * 4)
    r = int((mw * mh) / 2)
    vcount = 1
    visited[r] = 1
    visited = visited.reshape([mw, mh])
    nbers = nbers.reshape([mw, mh, 4])
    nbercount = nbercount.reshape([mw, mh])
    walls = walls.reshape([mw, mh, 4])
    udnbers(nbers, visited, nbercount, mw, mh, stag)
    while vcount < (mw * mh):
        v = np.transpose(np.nonzero(np.logical_and(visited == 1, nbercount > 0)))
        # choose branch
        r = rd.randint(0, len(v) - 1)
        c = v[r]
        # choose wall to break
        if nbers[c[0], c[1]][0] == 1 or nbers[c[0], c[1]][1] == 1:
            # horizontal bias when possible
            r = rd.randint(0, nbercount[c[0], c[1]] - 1 + hbias)
            if r > nbercount[c[0], c[1]] - 1:
                r = int(r - (nbercount[c[0], c[1]]))
                if nbers[c[0], c[1]][0] == 1 and nbers[c[0], c[1]][1] == 1:
                    r = int(r % 2)
                else:
                    r = 0
        else:
            # otherwise just vertical
            r = rd.randint(0, nbercount[c[0], c[1]] - 1)
        n = np.argwhere(nbers[c[0], c[1]])[r]
        # break wall
        walls[c[0], c[1], n] = 0
        c2 = c
        # walls: 0=L 1=R 2=U 3=D
        if n == 0:
            n2 = 1
            c2[0] = c[0] - 1
        elif n == 1:
            n2 = 0
            c2[0] = c[0] + 1
        elif n == 2:
            n2 = 3
            c2[1] = c[1] - 1
        else:
            n2 = 2
            c2[1] = c[1] + 1
        c2[0] = int((c2[0] + mw) % mw)
        visited[c2[0], c2[1]] = 1
        walls[c2[0], c2[1], n2] = 0
        udnbers(nbers, visited, nbercount, mw, mh, stag)
        vcount = vcount + 1
    # preview
    if ((i == 0 and shell < shells - 1) or (i == 1 and shell > 0)) and tpp != 1:
        im.putpixel((1 + ex * 2, 0), 255)
        im.putpixel((1 + st * 2, mh * 2), 255)
        for y in range(0, mh):
            for x in range(0, mw):
                imx = 1 + x * 2
                imy = 1 + y * 2
                imnx = [imx - 1, imx + 1, imx, imx]
                imny = [imy, imy, imy - 1, imy + 1]
                if visited[x, y] == 1:
                    im.putpixel((imx, imy), 255)
                for idx in range(0, 4):
                    if walls[x, y, idx] == 0:
                        im.putpixel((imnx[idx], imny[idx]), 255)
        if tpp == 2:
            im.save(os.path.join(os.getcwd(), PREV_DIR, str(shell + 1) + "a.png"))
        else:
            im.save(os.path.join(os.getcwd(), PREV_DIR, str(shell + 1) + ".png"))
    return walls


def gen():
    global shell
    global d2
    global mh
    global mw
    global i
    global tpp
    if shell < shells:
        if shell == halt:
            exit()
        if shell + 1 > 0 and shell + 1 < shells and shell + 1 == tp and tpp < 1:
            tpp = -1
        if tpp < 1:
            print("part: " + str(shell + 1))
        wt = mwt
        if tpp < 1:
            if shell == 0:
                d = (mw * us * p) / np.pi + wt - marge * 2
            else:
                if shell == tp:
                    d = d2
                else:
                    d = d2 + us + wt + marge * 2
                if i == 0:
                    mw = int(math.ceil((d / p + us) * np.pi / 2 / us))
                    if shell == (shells - 2):
                        mh += 1
                else:
                    if shell == (shells - 1):
                        mw = int(math.ceil((d / p + us) * np.pi / 2 / us))
                    else:
                        mw = int(math.ceil((d2 / p + us) * np.pi / 2 / us))
                mh += 1
        else:
            d = d2 + us + wt + marge * 2
            mw = int(math.ceil((d / p + us) * np.pi / 2 / us))
            mh += 1

        # stag/shift
        stag = np.zeros(mh)
        if stagmode in (1, 2):
            for y in range(0, mh):
                if y == 0 or stagmode == 1:
                    stag[y] = rd.randint(0, mh - 1)
                else:
                    stag[y] = stag[y - 1] + rd.randint(0, mh - 1)
        elif stagmode == 3:
            stag = np.multiply(np.arange(0, mh), stagconst).astype("int")
        # maze
        st = rd.randint(0, mw - 1)
        ex = rd.randint(0, mw - 1)
        marr = genmaze(int(mw), int(mh), stag, st, ex)
        matrix = []
        for y in range(0, mh):
            row = []
            for x in range(0, mw * p):
                x2 = x % mw
                r = marr[x2, y, 1] == 0
                u = marr[x2, y, 3] == 0
                if u and r:
                    row.append("3")
                elif u:
                    row.append("2")
                elif r:
                    row.append("1")
                else:
                    row.append("0")
            matrix.append(f"[{','.join(row)}]")
        s = f"[{','.join(matrix)}];"

        if tpp < 1:
            maze_num = 1
            open_mode = "w"
        else:
            maze_num = 2
            open_mode = "a+"
        with open("maze.scad", open_mode) as maze:
            maze.write(f"maze{maze_num}=")
            maze.write(
                "\n".join(
                    [
                        s,
                        f"h{maze_num}={mh};",
                        f"w{maze_num}={mw * p};",
                        f"st{maze_num}={st};",
                        f"ex{maze_num}={ex};",
                    ]
                )
            )

        base = 1
        lid = 0
        if shell == shells - 1:
            lid = 1
            base = 0
        if shell > shells - 2:
            mos = 0
        else:
            mos = shells - shell - 2
        with open("config.scad", "w+") as cfg:
            cfg.write(
                "\n".join(
                    [
                        f"p={p};",
                        f"tpp={tpp};",
                        f"is={shell};",
                        f"os={mos};",
                        f"lid={lid};",
                        f"base={base};",
                        f"iw={wt};",
                        f"id={d};",
                        f"s={us};",
                        f"i={i};",
                        f"bd={d + wt * 2 + us * 2};",
                        f"m={marge};",
                    ]
                )
            )
        if shell < shells - 2:
            d2 = d

        if shell > 0 and shell < shells and shell == tp and tpp < 1:
            if i == 0:  # double nub transition
                tpp = 1
                i = 1
            else:  # double maze transition
                tpp = 2
                i = 0
        else:
            tpp = 0
        if tpp < 1:
            execscad()
            shell = shell + 1
        return False
    else:
        return True


if __name__ == "__main__":

    try:
        prepwd()
        # get scad version:
        if has_scad_threading():
            USE_SCAD_THREAD_TRAVERSAL = (
                input("multi-threading available. use it(y/n)?").lower() == "y"
            )

        version = scad_version()
        if version[0] < 2015:
            input("ERROR: invalid scad version. must be at least 2015.xx.xx .")
            exit(1)
    except FileNotFoundError:
        input("ERROR: Could not find OpenSCAD: " + openscad())
        exit(1)

    d2 = 0
    shell = 0

    # make parts:
    p = abs(int(input("nub count (0=2 nubs,1=3 nubs,2=4 nubs, ...):"))) + 2
    tpp = 0
    hbias = abs(
        int(input("difficulty (hbias); 0=none >0= bias; larger= more difficult:"))
    )
    stagconst = 0
    stagmode = int(input("shift mode (0=none 1=random 2=random change 3=twist):"))
    if stagmode == 3:
        stagconst = abs(int(input("twist amount:")))

    config = configparser.ConfigParser()
    config.read("opt.ini")
    if "DEFAULT" not in config:
        input("ERROR: No DEFAULT section in opt.ini")
        exit(1)
    config = config["DEFAULT"]

    shells = config.getint("levels") + 1  # levels
    marge = config.getfloat("tolerance")
    i = int(config.getboolean("maze_inside"))
    tp = config.getint("transition_shell")
    if tp >= shells:
        tp = 0
    us = config.getfloat("spacing")
    mh = config.getint("units_tall")
    mw = config.getint("units_wide")
    mwt = config.getfloat("wall_thickness")
    while not gen():
        continue
    print("done!")
