#path to openscad excluding the executable:
openscad_exe="P:/Program Files/OpenSCAD"
#never use "\" in the above path (use "\\" instead)!!!
#never put the trailing slashes in the above path!!!

#do not edit below unless you know what you are doing!
import os
from shutil import copy
import shlex
import random as rd
import time
import numpy as np
import math
from PIL import Image
import subprocess as sp
halt=-1#debug: terminate skipping this shell (0 to n to enable)
curdir=str.replace(os.getcwd(),"\\","/")

openscad_com="\""+openscad_exe+"/openscad\""

'''try:
    import threading
    pythreads=1
except:
    pythreads=0
    print("python threading unavailable!")
    
if pythreads==1:
    pythreads=int(input("python threads (how many shells to do at a time): "))
    if pythreads<1:
        pythreads=1'''
        
def rmfiles(d):
    for f in os.listdir(d):
        try:
            if os.path.isfile(d+"/"+f):
                os.remove(d+"/"+f)
        except Exception as e:
            print(e)
def prepwd():
    if(os.path.exists(openscad_exe)==False):
        input("ERROR: openscad path not found.")
        exit()
    if(os.path.exists("stl's")==False):
        os.mkdir("stl's",777)
    else:
        rmfiles("stl's")
    if(os.path.exists("prev")==False):
        os.mkdir("prev",777)
    else:
        rmfiles("prev")

    '''if pythreads>0:
        if(os.path.exists(curdir+"/threads")==False):
            os.mkdir("threads",777)
            for d in range(pythreads):
                if(os.path.exists(curdir+"/threads/"+str(d))==False):
                    os.mkdir("threads/"+str(d),777)
                copy(curdir+"/make_shells.scad",curdir+"/threads/"+str(d)+"/")
        else:
            rmfiles("threads")
            for d in range(pythreads):
                if(os.path.exists(curdir+"/threads/"+str(d))==False):
                    os.mkdir("threads/"+str(d),777)
                copy("make_shells.scad",curdir+"/threads/"+str(d)+"/")'''
prepwd()
#get scad version:
scadthreading=False
ver=sp.check_output(shlex.split(openscad_com+" --version"),shell=True)
ver=str(ver).replace("b'OpenSCAD version ","").replace("\\r\\n'","").split(".")
if not int(ver[0])>=2015:
    input("ERROR: invalid scad version. must be at least 2015.xx.xx .")
    exit()
if int(ver[0])>=2018 and int(ver[1])>=5 and int(ver[2])>=30 or int(ver[0])>=2018 and int(ver[1])>5 or int(ver[0])>2018:
    scadthreading=(str(input("multi-threading available. use it(y/n)?")).lower()=="y")
else:
    scadthreading=False  

d2=0
shell=0
'''def pythread1():
    if scadthreading:
        sp.run(shlex.split(openscad_com+" --enable=thread-traversal -o \""+curdir+"/stl\'s/"+str(shell+1)+".stl\" \""+curdir+"/make_shells.scad\""),shell=True)
    else:
        target=sp.run(shlex.split(openscad_com+" -o \""+curdir+"/stl\'s/"+str(shell+1)+".stl\" \""+curdir+"/threads/"+str(threadid)+"/make_shells.scad\""),shell=True)
    '''

def execscad(threadid=0):
    print("Executing OpenSCAD script...")
    #if pythreads<=1:
    if scadthreading:
        sp.run(shlex.split(openscad_com+" --enable=thread-traversal -o \""+curdir+"/stl\'s/"+str(shell+1)+".stl\" \""+curdir+"/make_shells.scad\""))
    else:
        sp.run(shlex.split(openscad_com+" -o \""+curdir+"/stl\'s/"+str(shell+1)+".stl\" \""+curdir+"/make_shells.scad\""))
        '''return None
    else:
        copy(curdir+"/maze.scad",curdir+"/threads/"+str(threadid)+"/")
        copy(curdir+"/config.scad",curdir+"/threads/"+str(threadid)+"/")
        ret=threading.Thread(target=pythread1)
        ret.daemon=True
        return ret'''
        
def udnbers(n,vi,nc,mw,mh,stag):
    for y in range(0,mh):
        for x in range(0,mw):
            x3=int((x+stag[y])%mw)
            x2=[x-1,x+1,x,x]
            x4=[x3-1,x3+1,x3,x3]
            y2=[y,y,y-1,y+1]
            for i in range(0,4):
                if(stag[y]%mw>0):
                    x2[i]=int((x2[i]+mw)%mw)
                else:
                        if(x2[i]<0):
                            x2[i]=0
                        if(x2[i]>mw-1):
                            x2[i]=mw-1
                if(not((x3==0 and i==0) or (x3==mh-1 and i==1)) and y2[i]>-1 and y2[i]<mh):
                    n[x,y,i]=vi[int(x2[i]),int(y2[i])]==0
                else:
                    n[x,y,i]=0
            nc[x,y]=len(np.argwhere(n[x,y].astype("int")))
def genmaze(mw,mh,stag,st,ex):
    im=Image.new('L',[2*mw+1,2*mh+1],0)
    visited=np.zeros(mw*mh)
    nbercount=np.zeros(mw*mh)
    nbers=np.ones(mw*mh*4)
    walls=np.ones(mw*mh*4)
    rd.seed(int(round(time.time() * 1000)))
    r=int((mw*mh)/2)
    vcount=1
    visited[r]=1
    visited=visited.reshape([mw,mh])
    nbers=nbers.reshape([mw,mh,4])
    nbercount=nbercount.reshape([mw,mh])
    walls=walls.reshape([mw,mh,4])
    #pos=np.argwhere(visited)[0]
    udnbers(nbers,visited,nbercount,mw,mh,stag)
    while(vcount<(mw*mh)):
        v=np.transpose(np.nonzero(np.logical_and(visited == 1,nbercount>0)))
        rd.seed(int(round(time.time() * 1000)))
        #choose branch
        r=rd.randint(0,len(v)-1)
        c=v[r]
        #choose wall to break
        if(nbers[c[0],c[1]][0]==1 or nbers[c[0],c[1]][1]==1):
            #horizontal bias when possible
            r=rd.randint(0,nbercount[c[0],c[1]]-1+hbias)
            if(r>nbercount[c[0],c[1]]-1):
                r=int(r-(nbercount[c[0],c[1]]))
                if(nbers[c[0],c[1]][0]==1 and nbers[c[0],c[1]][1]==1):
                    r=int(r%2)
                else:
                    r=0
        else:
            #otherwise just vertical
            r=rd.randint(0,nbercount[c[0],c[1]]-1)
        n=np.argwhere(nbers[c[0],c[1]])[r]
        #break wall
        walls[c[0],c[1],n]=0
        c2=c
        #walls: 0=L 1=R 2=U 3=D
        if(n==0):
            n2=1
            c2[0]=c[0]-1
        elif(n==1):
            n2=0
            c2[0]=c[0]+1
        elif(n==2):
            n2=3
            c2[1]=c[1]-1
        else:
            n2=2
            c2[1]=c[1]+1
        c2[0]=int((c2[0]+mw)%mw)
        visited[c2[0],c2[1]]=1
        walls[c2[0],c2[1],n2]=0
        udnbers(nbers,visited,nbercount,mw,mh,stag)
        vcount=vcount+1
    #prev
    if((i==0 and shell<shells-1)or(i==1 and shell>0))and tpp != 1:
        im.putpixel((1+ex*2,0),255)
        im.putpixel((1+st*2,mh*2),255)
        for y in range(0,mh):
            for x in range(0,mw):
                imx=1+x*2
                imy=1+y*2
                imnx=[imx-1,imx+1,imx,imx]
                imny=[imy,imy,imy-1,imy+1]
                if(visited[x,y]==1):
                    im.putpixel((imx,imy),255)
                for idx in range(0,4):
                    if(walls[x,y,idx]==0):
                        im.putpixel((imnx[idx],imny[idx]),255)
        if tpp==2:
            im.save(curdir+"/prev/"+str(shell+1)+"a.png")
        else:
            im.save(curdir+"/prev/"+str(shell+1)+".png")
    return walls
def gen():
    global shell
    global d2
    global mh
    global mw
    global i
    global tpp
    threadlist=[]
    if(shell<shells):
        if shell==halt:
            exit()
        if shell+1>0 and shell+1<shells and shell+1==tp and tpp<1:
            tpp=-1
        if tpp<1:
            print("part: "+str(shell+1))
        wt=mwt
        if tpp<1:
            if(shell==0):
                d=(mw*us*p)/np.pi+wt-marge*2
                '''else:
                    d=(mw*us)/np.pi'''
            else:
                if shell==tp:
                    d=d2
                else:
                    d=d2+us+wt+marge*2
                if i==0:
                    mw=int(math.ceil((d/p+us)*np.pi/2/us))
                    if shell==(shells-2):
                        mh+=1
                else:
                    if shell==(shells-1):
                        mw=int(math.ceil((d/p+us)*np.pi/2/us))
                    else:
                        mw=int(math.ceil((d2/p+us)*np.pi/2/us))
                mh+=1
        else:
            d=d2+us+wt+marge*2
            mw=int(math.ceil((d/p+us)*np.pi/2/us))
            mh+=1
        #print(d)
        
        #stag/shift
        stag=np.zeros(mh)
        if(stagmode==1 or stagmode==2):
            for y in range(0,mh):
                if(y==0 or stagmode==1):
                    stag[y]=rd.randint(0,mh-1)
                else:
                    stag[y]=stag[y-1]+rd.randint(0,mh-1)
        elif(stagmode==3):
            stag=np.multiply(np.arange(0,mh),stagconst).astype("int")
        #maze
        rd.seed(int(round(time.time() * 1000)))
        st=rd.randint(0,mw-1)
        ex=rd.randint(0,mw-1)
        marr=genmaze(int(mw),int(mh),stag,st,ex)

        s="["
        for y in range(0,mh):
            s=s+"["
            for x in range(0,mw*p):
                x2=x%mw
                r=marr[x2,y,1]==0
                u=marr[x2,y,3]==0
                if(u and r):
                    s=s+"3,"
                elif(u):
                    s=s+"2,"
                elif(r):
                    s=s+"1,"
                else:
                    s=s+"0,"
            s=s[0:-1]+"],"

        rd.seed(int(round(time.time() * 1000)))
        if tpp<1:
            with open("maze.scad","w") as maze:
                maze.write("maze1=")
                maze.write(s[0:-1]+"];\nh1="+str(mh)+";\nw1="+str(mw*p)+";\nst1="+str(st)+";\nex1="+str(ex)+";\n")
                #maze.write("maze2=[];\n")
                #maze.write("h2=0;\nw2=0;\nst2=0;\nex2=0;")
        else:
            with open("maze.scad","a+") as maze:
                maze.write("maze2=")
                maze.write(s[0:-1]+"];\nh2="+str(mh)+";\nw2="+str(mw*p)+";\nst2="+str(st)+";\nex2="+str(ex)+";")

        base=1
        lid=0
        if(shell==shells-1):
            lid=1
            base=0
        if(shell>shells-2):
            mos=0
        else:
            mos=shells-shell-2
        with open("config.scad","w+") as cfg:
            cfg.write("p="+str(p)+";\ntpp="+str(tpp)+";\nis="+str(shell)+";\nos="+str(mos)+";\nlid="+str(lid)
                      +";\nbase="+str(base)+";\niw="+str(wt)+";\nid="+str(d)+";\ns="+str(us)+";\ni="+str(i)
                      +";\nbd="+str(d+wt*2+us*2)+";\nm="+str(marge)+";")
        if(shell<shells-2):
            d2=d
        time.sleep(2)
        
        
        if shell>0 and shell<shells and shell==tp and tpp<1:
            if i==0:#double nub transition
                tpp=1
                i=1
            else:#double maze transition
                tpp=2
                i=0
        else:
            tpp=0
        if tpp<1:
            '''if pythreads>0:
                threadlist.append(execscad(shell%pythreads))
                if shell%pythreads==pythreads-1:
                    print("starting the "+str(pythreads)+" threads...")
                    for t in threadlist:
                        t.start()
                    print("waiting on threads...")
                    for t in threadlist:
                        t.join()
                    time.sleep(2)
                    rmfiles(curdir+"/threads")
                    for d in range(pythreads):
                        copy(curdir+"/make_shells.scad",curdir+"/threads/"+str(d)+"/")
                    threadlist=[]
            else:'''
            execscad()
            shell=shell+1
        return False
    else:
        return True
    
#make parts:
p=abs(int(input("nub count (0=2 nubs,1=3 nubs,2=4 nubs, ...):")))+2
tpp=0
hbias=abs(int(input("difficulty (hbias); 0=none >0= bias; larger= more difficult:")))
stagconst=0
stagmode=int(input("shift mode (0=none 1=random 2=random change 3=twist):"))
if(stagmode==3):
    stagconst=abs(int(input("twist amount:")))
with open("opt.txt","r") as opt:
    while True:
        line=opt.readline().strip()
        if not line: continue
        word=line.split()[0]
        if not word.startswith("#"): break
    shells=int(word)+1#levels
    marge=float(opt.readline().split()[0])
    i=int(opt.readline().split()[0])
    tp=int(opt.readline().split()[0])
    if tp>=shells:
        tp=0
    us=float(opt.readline().split()[0])
    mh=int(opt.readline().split()[0])
    mw=int(opt.readline().split()[0])
    mwt=float(opt.readline().split()[0])

while(not gen()):
    continue
print("done!")
