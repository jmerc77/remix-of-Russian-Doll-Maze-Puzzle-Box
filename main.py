#!/usr/bin/env python3

# OPENSCAD_PATH = "P:/Program Files/OpenSCAD/openscad.com"
# If you keep OpenSCAD in an unusual location, uncomment the above line of code and
# set it to the full path to the openscad executable.
# Note: Windows/python now support forward-slash characters in paths, so please use
#       those instead of backslashes which create a lot of confusion in code strings.


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

skip = -1 # debug: skip all shells up to here (0 to n to enable)
halt = -1 # debug: terminate skipping this shell (0 to n to enable)



USE_SCAD_THREAD_TRAVERSAL = False
STL_DIR = "_files"#name gets tacked on later...
PREV_DIR = "maze_previews"

#tries to get the path to openscad
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
        return "C:/Program Files/OpenSCAD/openscad.com"
    # Default to linux-friendly CLI program name
    return "openscad"

#prepares folders
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

#checks threading availability
def has_scad_threading():
    cmd = [openscad(), "--help"]
    out = str(sp.check_output(cmd)).lower()
    if "--parallelism" in out:
        return True
    return False

#checks version
def scad_version():
    cmd = [openscad(), "--version"]
    ver=sp.Popen(cmd,stdout=sp.PIPE).stdout.readline().decode("utf-8")
    
    ver=ver.replace("\r","").replace("\n","").replace("-",".").replace("OpenSCAD version ","").split(".")
    for v in range(len(ver)):
        ver[v]=re.sub('[^0-9]','', ver[v])
    return (int(ver[0]), int(ver[1])) if ver else ()

#runs the scad
def execscad(threadid=0):
    global ext
    print("Executing OpenSCAD script...")
    cmd = [openscad()]
    if USE_SCAD_THREAD_TRAVERSAL:
        cmd.append("--enable=thread-traversal")
    cmd.extend(
        [
            "-o",
            os.path.join(os.getcwd(), STL_DIR, str(shell + 1) + "." + ext),
            os.path.join(os.getcwd(), "make_shells.scad"),
        ]
    )
    sp.run(cmd)

#updates the possible ways to cut the maze
def udnbers(n, vi, nc, mw, mh, stag):
    #with every tile
    for y in range(0, mh):
        for x in range(0, mw):
            #shift the vertical edge
            x3 = int((x + stag[y]) % mw)
            #next tile coords
            x2 = [x - 1, x + 1, x, x]
            y2 = [y, y, y - 1, y + 1]
            #look arround
            for i in range(0, 4):
                #did we shift the edge?
                if stag[y] % mw > 0:
                    #shift the next tile coords too
                    x2[i] = int((x2[i] + mw) % mw)
                else:
                    #constrain to bounds otherwise
                    if x2[i] < 0:
                        x2[i] = 0
                    if x2[i] > mw - 1:
                        x2[i] = mw - 1
                #is this cuttable and not out of bounds?
                if (
                    not ((x3 == 0 and i == 0) or (x3 == mh - 1 and i == 1))
                    and y2[i] > -1
                    and y2[i] < mh
                ):
                    #mark cuttable if we have not been there
                    n[x, y, i] = vi[int(x2[i]), int(y2[i])] == 0
                else:
                    #mark not cuttable
                    n[x, y, i] = 0
            #update count of cuttable tiles
            nc[x, y] = len(np.argwhere(n[x, y].astype("int")))

#makes a maze
def genmaze(mw, mh, stag):
    #where we have cut a path already
    visited = np.zeros(mw * mh)
    #number of possible ways to cut
    nbercount = np.zeros(mw * mh)
    #possible ways to cut
    nbers = np.ones(mw * mh * 4)
    #walls of the maze tiles
    # walls are: 0=L 1=R 2=U 3=D
    walls = np.ones(mw * mh * 4,dtype="int")
    #start here
    r = rd.randint(0, mw*mh-1)
    #mark start as visited
    #number of places we have cut a path already
    vcount = 1
    visited[r] = 1
    #to make things easier
    visited = visited.reshape([mw, mh])
    nbers = nbers.reshape([mw, mh, 4])
    nbercount = nbercount.reshape([mw, mh])
    walls = walls.reshape([mw, mh, 4])
    
    #update the possible ways to cut
    udnbers(nbers, visited, nbercount, mw, mh, stag)
    #loop until maze is completed
    while vcount < (mw * mh):
        #all places we can continue cutting
        v = np.transpose(np.nonzero(np.logical_and(visited == 1, nbercount > 0)))
        # choose a tile to cut from
        if len(v) < 2:
            r=0
        else:
            r = rd.randint(0, len(v) - 1)
        c = v[r]
        #keep cutting until can't or min_branch is reached
        for i in range(min_branch):
            # choose wall to cut
            r = rd.randint(0, nbercount[c[0], c[1]] - 1)
            n = np.argwhere(nbers[c[0], c[1]])[r]
            # cut the wall
            walls[c[0], c[1], n] = 0
            #temp for the tile we are cutting
            c2 = c
            #the other side of the wall
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
            #wrap horizontally
            c2[0] = int((c2[0] + mw) % mw)
            #mark as visited
            visited[c2[0], c2[1]] = 1
            #cut the other side
            walls[c2[0], c2[1], n2] = 0
            #update the possible ways to cut again
            udnbers(nbers, visited, nbercount, mw, mh, stag)
            #update the number of places we have cut a path already
            vcount = np.sum(visited,dtype="int")
            #prepare cut again...
            c=c2
            #...if we can. otherwise break the for.
            if nbercount[c[0],c[1]]==0:
                break
    return walls

#makes and writes the preview image
def preview(maze):
        #a new image
        im = Image.new("L", [2 * mw + 1, 2 * mh + 1], 0)
        #start and end
        im.putpixel((1 + ex * 2, 0), 255)#end
        im.putpixel((1 + st * 2, mh * 2), 255)#start
        
        for y in range(0, mh):
            for x in range(0, mw):
                #tile pos
                imx = 1 + x * 2
                imy = 1 + y * 2
                #wall pixel coords
                imnx = [imx - 1, imx + 1, imx, imx]
                imny = [imy, imy, imy - 1, imy + 1]
                #center of tile
                im.putpixel((imx, imy), 255)
                #check walls
                for idx in range(0, 4):
                    #no wall?
                    if maze[x, y, idx] == 0:
                        #cut a hole!
                        
                        im.putpixel((imnx[idx], imny[idx]), 255)
        #fill in answer key                
        ans=ans_solver(maze,st,ex)
        for y in range(0, mh):
            for x in range(0, mw):
                imx = 1 + x * 2
                imy = 1 + y * 2
                if [x,y] in ans:
                    im.putpixel((imx, imy), 128)
                else:
                    im.putpixel((imx, imy), 255) 
        #transition shell maze 2?
        if tpp == 2:
            #save as maze 2
            im.save(os.path.join(os.getcwd(), PREV_DIR, str(shell + 1) + "a.png"))
        else:
            #save as maze 1
            im.save(os.path.join(os.getcwd(), PREV_DIR, str(shell + 1) + ".png"))
#for ans key in previews
def ans_solver(maze,s,e):
    ret=[[s,mh],[s,mh-1]]
    direction=1#r,u,l,d
    x=s
    y=mh-1
    direction2wall=[1,2,0,3]#r,u,l,d -> l,r,u,d
    direction2xy=[[1,0],[0,-1],[-1,0],[0,1]]#r,u,l,d
    while x!=e or y>0:
        #walls at x,y in the maze
        here=maze[x,y]
        #print(x,y,direction,4-np.sum(here))
        if here[direction2wall[(direction+3)%4]]==0:
            direction=(direction+3)%4
        #change direction until no wall in case of front wall
        if here[direction2wall[direction]]==1:
            
            while here[direction2wall[direction]]==1:
                #change direction
                #print(direction,here[direction2wall[direction]])
                direction=(direction+1)%4
        x=(x+direction2xy[direction][0]+mw)%mw
        y=y+direction2xy[direction][1]
        #are we backtracking?
        if x==ret[-2][0] and y==ret[-2][1]:
            ret=ret[0:-1]
            #print("backtracking")
        else:
            ret.append([x,y])
    #print(ret)    
    return ret[1:]

#finds the lengths from a start to all ends of a maze  
def solver(maze,s):
    #start here
    branches=[[s,mh-1,0,0,4]]#x,y,length,downcnt,last
    #return value
    ret=[]
    #loop until return value is full
    while len(ret)<mw:
        #temporarlily store new branches here
        temp=[]
        #loop through all current branches
        for branch in branches:
            x=branch[0]
            y=branch[1]
            length=branch[2]
            #count for how many times we go down toward start
            downcnt=branch[3]
            #must not back track.
            last=branch[4]
            #walls at x,y in the maze
            here=maze[x,y]
            #how many openings at x,y in maze
            opencnt=4-np.sum(here)
            #is this a posible end?
            if y==0:
                #include this length in return value.
                ret.append(length)
            #can we move on?
            if opencnt>0:
                #move on but do not bactrack.
                if here[0]==0 and last!=0:
                    #left
                    temp.append([(x+mw-1)%mw,y,length+1,downcnt,1])
                if here[1]==0 and last!=1:
                    #right
                    temp.append([(x+1)%mw,y,length+1,downcnt,0])
                    
                if here[2]==0 and last!=2:
                    #up
                    temp.append([x,y-1,length+1,downcnt,3])
                if here[3]==0 and last!=3:
                    #down
                    temp.append([x,y+1,length+1,downcnt+1,2])
        #copy the new branches over the old branches
        branches=temp.copy()
    return ret

#chooses a maze path (start and end) based on difficulty
def choose_path(maze):
    global st
    global ex
    #get path lengths...
    lengths=[]
    for s in range(mw):
        #find the lengths from this start to all ends
        lengths.append(solver(maze,s))
    #get sorted indexes
    sortedlengthidxs=np.argsort(np.asarray(lengths).flatten())
    #choose one
    chosen=sortedlengthidxs[int(difficulty/101*len(sortedlengthidxs))]
    #assign start and end
    st=chosen//mw#start
    ex=chosen%mw#end
    #make and write preview image
    preview(maze)
    
#makes parts
def gen():
    global shell
    global d2
    global mh
    global mw
    global i
    global tpp
    #are we done yet?
    if shell < shells:
        
        #debug halt
        if shell >= halt and halt > -1:
            return True
        #is the next shell the transition?
        if shell + 1 > 0 and shell + 1 < shells and shell + 2 == tp and tpp < 1:
            tpp = -1
        #part status
        if tpp < 1:
            print("part: " + str(shell + 1))
        #wall thickness
        wt = mwt
        #are we not in transitioning stage 2?
        if tpp < 1:
            #is this the first?
            if shell == 0:
                #set the diameter
                d = (mw * us * p) / np.pi / 2 - wt - marge * 2
                print("diameter:",d)
            else:
                #are we transitioning?
                if shell+1 == tp:
                    #keep the diameter the same
                    d = d2
                else:
                    #set the diameter
                    d = d2 + us + wt + marge * 2
                    print("diameter:",d)
                #is the maze on the outside?
                if i == 0:
                    #set the maze width
                    mw = int(math.ceil((d + us) * np.pi / us / p))
                else:
                    #set the maze width
                    mw = int(math.ceil((d2 + us) * np.pi / us / p ))
                #extra height for lid
                if shell == shells:
                    mh += 1
                #increase maze height
                mh += 1
        else:
            #set the diameter
            d = d2 + us + wt + marge * 2
            print("diameter:",d)
            #set the maze width
            mw = int(math.ceil((d + us) * np.pi / us / p))
            #increase maze height
            mh += 2

        # shift
        stag = np.zeros(mh)
        #is it a random shift?
        if stagmode in (1, 2):
            #loop through y
            for y in range(0, mh):
                #are we at end or shift mode is random?
                if y == 0 or stagmode == 1:
                    #random shift
                    stag[y] = rd.randint(0, mh - 1)
                else:
                    #random shift offset
                    stag[y] = stag[y - 1] + rd.randint(0, mh - 1)
        #is it a twist shift?
        elif stagmode == 3:
            #twist it!
            stag = np.multiply(np.arange(0, mh), stagconst).astype("int")
        #do we even have a maze with this part?
        if ((i == 0 and shell < shells - 1) or (i == 1 and shell > 0)) and tpp != 1:
            # maze
            marr = genmaze(int(mw), int(mh), stag)
            #get the path we want
            choose_path(marr)
            #convert to string
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
                matrix.append(",".join(row))
            s = "[["+"],[".join(matrix)+"]];"
        else:
            #empty maze
            s="[];"
        #write the maze
        if tpp < 1:
            maze_num = 1
            open_mode = "w"
        else:
            maze_num = 2
            open_mode = "a+"
        with open("maze.scad", open_mode) as maze:
            maze.write(
                "\n".join(["maze"+str(maze_num)+"="+s,
                  "h"+str(maze_num)+"="+str(mh)+";",
                  "w"+str(maze_num)+"="+str(mw*p)+";",
                  "st"+str(maze_num)+"="+str(st)+";",
                  "ex"+str(maze_num)+"="+str(ex)+";",
                  ""])
            )
        #non lid
        base = 1
        lid = 0
        #is it the lid?
        if shell > shells - 2:
            #lid
            lid = 1
            base = 0
            #no more to go
            mos = 0
        else:
            #how many are left to go
            mos = shells - shell - 2
        with open("config.scad", "w+") as cfg:
            cfg.write(
                "\n".join(["p="+str(p)+";",
                  "tpp="+str(tpp)+";",
                  "is="+str(shell)+";",
                  "os="+str(mos)+";",
                  "lid="+str(lid)+";",
                  "base="+str(base)+";",
                  "iw="+str(wt)+";",
                  "id="+str(d)+";",
                  "s="+str(us)+";",
                  "i="+str(i)+";",
                  "bd="+str(d + wt * 2 + us * 2)+";",
                  "m="+str(marge)+";",
                  ""])
            )
        #save diameter of this one for later
        if shell < shells - 2:
            d2 = d
        #was this the transition shell?
        if shell > 0 and shell < shells and shell+1 == tp and tpp < 1:
            #get ready for transition stage 2
            if i == 0:  # double nub transition
                tpp = 1
                i = 1
            else:  # double maze transition
                tpp = 2
                i = 0
        else:
            tpp = 0
        #are we done with this shell?
        if tpp < 1:
            #make it!
            #debug skip
            if shell >= skip or skip < 0:
                execscad()
            #on to the next
            shell = shell + 1
        #not done making parts
        return False
    else:
        #all done!
        return True

#reads opt.ini
def readOpt():
    global shells
    global marge
    global us
    global mh
    global mw
    global mwt
    global i
    global p
    global tp
    global STL_DIR
    global stagmode
    global stagconst
    global difficulty
    global min_branch
    global ext
    config = configparser.ConfigParser()
    config.read("opt.ini")
    if "DEFAULT" not in config or "MAZE" not in config:
        print("ERROR: No DEFAULT and/or MAZE section in opt.ini; Must have both.\n")
        exit(1)
    mazeconfig=config["MAZE"]
    config = config["DEFAULT"]
    version = scad_version()
    if config.getboolean("o3mf") and version[0]>=2019:
        ext="3mf"
    else:
        ext="stl"
    p = abs(config.getint("nubs")-2) + 2
    shells = config.getint("levels") + 1
    marge = config.getfloat("tolerance")
    i = int(config.getboolean("maze_inside"))
    tp = config.getint("transition_shell")
    if tp > shells-1:
        tp = 0
    us = config.getfloat("spacing")
    mh = config.getint("units_tall")
    mw = config.getint("units_wide")
    mwt = config.getfloat("wall_thickness")
    name = config.get("name")
    STL_DIR=name+STL_DIR
    #maze options
    #seeding...
    seed=mazeconfig.get("seed").replace("\r","").replace("\n","")
    if not seed.isnumeric() or "\\" in seed or "." in seed:
        # Make sure we have a fresh random seed
        rd.seed()
    else:
        #use seed from ini
        rd.seed(int(seed))
    difficulty=abs(mazeconfig.getfloat("diff",100.0))
    if difficulty>100:
        difficulty=100
    min_branch=mazeconfig.getint("min_branch",5)
    if min_branch<1:
        min_branch=5
    stagmode = mazeconfig.getint("shift",1)
    stagconst = 0
    if stagmode == 3:
        stagconst = abs(mazeconfig.getint("twist",1))
    
if __name__ == "__main__":
    
    #read opt.ini
    readOpt()
    try:
        #prep folders
        prepwd()
        
        # get scad version:
        version = scad_version()
        if version[0] < 2015:
            print("ERROR: invalid scad version. must be at least 2015.xx.xx .\n")
            exit(1)
        #do we have threading?
        if has_scad_threading():
            USE_SCAD_THREAD_TRAVERSAL = (
                input("multi-threading available. use it(y/n)?").lower() == "y"
            )
    except FileNotFoundError:
        print("ERROR: Could not find OpenSCAD: " + openscad()+"\n")
        exit(1)
    #init vars
    st=0
    ex=0
    d2 = 0
    shell = 0
    tpp = 0
    
    # make parts:
    while not gen():
        continue
    print("done!")
    
