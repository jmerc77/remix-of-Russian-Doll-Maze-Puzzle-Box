// Puzzle box by Adrian Kennard www.me.uk
//revised (Remixed?) by Jonathan Mercier (aka. spool2kool)
//Watermark removed...ummm, commented. (I do not like watermarks!)





//do not change below here.
//(Unless you know what you are doing!)
//Works so far.
include <options.scad>
include <config.scad>
include <maze.scad>

//computed 
eh2=1;// Extra height
nubscale=1.5;
bh=s-eh2;	// Base height
eh=(tpp<1&&i==0)?0:bh;// Extra height	
wt=bh;	// Base wall thickness
ih=(h1+1)*s;	// Inside height

if(base)translate([lid?(id+s*4+iw*2+wt*2)/2:0,0,0])makebase();
if(lid)translate([base?-(id+s*4+iw*2+wt*2)/2:0,0,0])makelid();

module nub()
{
    if(oldnubs){
      rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s/8]) 
    hull()
    {
        cube([s/6*nubscale,s/6*nubscale,s/4],true);
        translate([0,0,-s/4])
        cube([s/2*nubscale,s/2*nubscale,s/4],true);
    }  
    }
    else{
    rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s/8])
    hull()
    {
        translate([0,(s/6*nubscale)/2,0])cube([s/2*nubscale-m*2,s/3*nubscale,s/4],true);
        translate([0,0,-s/4])
        cube([s/2*nubscale-m*2,s/2*nubscale,s/4],true);
    }
}
}
module knob()
{
    if(oldnubs){
       rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s/8])
    hull()
    {
        cube([s/6*nubscale,s/6*nubscale,s/4],true);
        translate([0,0,-s/4])
        cube([s/2*nubscale,s/2*nubscale,s/4],true);
    }
    }
    else{
    rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s/8])
    hull()
    {
        translate([0,(s/6*nubscale)/2,0])cube([s/2*nubscale,s/3*nubscale,s/4],true);
        translate([0,0,-s/4])
        cube([s/2*nubscale,s/2*nubscale,s/4],true);
    }
}
}

module right(w,i2,d=id/2+iw+s/2)
{
    q=3.6;
    
    if(i2==1){
        for(a=[0:q:360/w])hull(){   
        rotate([0,0,a])        translate([d,0,0])        rotate([0,0,180])knob();
        rotate([0,0,min(a+q,360/w)])        translate([d,0,0])        rotate([0,0,180])knob();
        }
    }
    else{
    for(a=[0:q:360/w])
    hull(){
        rotate([0,0,a])
        translate([d,0,0])
        knob();
        rotate([0,0,min(a+q,360/w)])
        translate([d,0,0])
        knob();
    }
}
}

module up(i2,q,d=id/2+iw+s/2,stp=3)
{
    for(a=[q/stp:q/stp:q]){
    if(i2==1){
        
        translate([d,0,0])
        hull(){
            rotate([0,0,180])knob();
            translate([0,0,a])
            rotate([0,0,180])knob();
        } 
    }
else{    
    translate([d,0,0])
        hull()
        {
            knob();
            translate([0,0,a])
            knob();
        }
    }}
}

module outer(h2)
{
    r=bd/2+m;
    minkowski()
    {
       cylinder(r=(r-wt)/cos(180/bs),h=h2-wt,$fn=bs);
       cylinder(r1=0,r2=wt,h=wt,$fn=100);
    }
}
/*
module aa(w=100,white=0,$fn=100)
{   // w is the 100%, centre line of outer ring, so overall size (white=0) if 1.005 times that
    scale(w/100)
    {
        if(!white)difference()
        {
            circle(d=100.5);
            circle(d=99.5);
        }
        difference()
        {
            if(white)circle(d=100);
            difference()
            {
                circle(d=92);
                for(m=[0,1])
                mirror([m,0,0])
                {
                    difference()
                    {
                        translate([24,0,0])
                        circle(r=22.5);
                        translate([24,0,0])
                        circle(r=15);
                    }
                    polygon([[1.5,22],[9,22],[9,-18.5],[1.5,-22]]);
                }
            }
        }
    }
}*/
module basemaze(maze,w,h,st,ex,mm,i2)
{
    rotate([0,0,-st*360/w])
    {
    if(i2==0){ 
                for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            
        rotate([0,0,st*360/w]){  
                
                //lock
            knobr=atan2(360/p/4*bh/(360/p),
            ((id/2+iw+s/2)*2*PI/p/4));
            
                 if(os){
                     for(b=[0:180/p/4/w:360/p/4])rotate([0,0,(lefty?b:-b)])translate([id/2+iw+s/2,0,bh-b*bh/(360/p)+s/4+s/4/nubscale])rotate([(lefty?-knobr:knobr),0,0])knob();
                    hull(){
                        translate([id/2+iw+s/2,0,bh+m*2+s/3.5])knob();
                        translate([id/2+iw+s/2,0,bh+m*2+s])knob();}
                     }
                     else
                     {
                         hull(){
                             translate([id/2+iw+s/2,0,bh-s/2+s])knob();
                             translate([id/2+iw+s/2,0,bh+s*2.25])knob();
                             
                         }
                     }
            
                 }
             rotate([0,0,ex*360/w])translate([0,0,mm+s*(h-1)-s/8+((tpp<1&&i==0)?s:0)])
            up(i2,mm);
        }
        
        
        // Maze
        
        for(y=[0:1:h-1])
        translate([0,0,mm+y*s+((!os&&(i2==0||tpp==2))?s:0)-m*2-s/6+((tpp<1&&i==0)?s:0)])
        for(x=[0:1:w-1])
        rotate([0,0,x*360/w])
        {
            if(maze[y][x]==1 || maze[y][x]==3)right(w);
            if(maze[y][x]==2 || maze[y][x]==3)up(i2,s-m);
        }
        }
        else if(is>0){
                   translate([0,0,s])for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            rotate([0,0,st*360/w])
           { 
                
                //lock
                knobr=-atan2(360/p/4*bh/(360/p),
            ((id-s/2)*PI/p/4));
               
     hull()for(b=[0:180/p/4/w:360/p/4])rotate([0,0,(lefty?b:-b)])translate([id/2,0,eh+bh-b*bh/(360/p)+s/4])rotate([0,0,180])rotate([(lefty?-knobr:knobr),0,0])knob();
                     hull(){translate([id/2,0,bh+eh+s/2])rotate([0,0,180])knob();
                         translate([id/2,0,bh+eh+s+s/4/nubscale])rotate([0,0,180])knob();    
                         }
                     }
            
      rotate([0,0,ex*360/w])translate([0,0,bh+mm+s*(h-1)-m*2])
            up(i2,mm,d=id/2);
                
        }
            // Maze
        for(y=[0:1:h-1])
        translate([0,0,bh+mm+y*s+s-m*2])
        
        for(x=[0:1:w-1])
        rotate([0,0,x*360/w])
        {
            if(maze[y][x]==1 || maze[y][x]==3)
                right(w,i2,d=id/2);
            if(maze[y][x]==2 || maze[y][x]==3)
                up(i2,s,d=id/2);
        }
    }
}
}
module makebase()
{
    mm=(ih+wt-bh-s*h1)/2+s/2+m*2+eh+1;
    difference()
    {
    translate([0,0,(os)?0:eh])union(){
    difference()
    {
        if(os)
        {
            if(bversion==2)
            {
	difference()
	{
   	   cylinder(d=bd+s/4-m*2,h=bh,$fn=100);
	   translate([0,0,-0.01])
	   difference()
	   {
		   cylinder(d=bd+s/4+2-m*2,h=2);
		   cylinder(d1=bd+s/4-2-m*2,d2=bd+s/4+4-m*2,h=3,$fn=100);
	   }
	}
}
else
{
    difference()
	{
   	   cylinder(d=bd-m*2,h=bh,$fn=100);
	   translate([0,0,-0.01])
	   difference()
	   {
		   cylinder(d=bd+2-m*2,h=2);
		   cylinder(d1=bd-2-m*2,d2=bd+4-m*2,h=3,$fn=100);
	   }
	}
}
}
	else
        translate([0,0,-eh])outer(bh+wt);
	
	if(os && bversion==0)
	{
           for(a=[0:360/w1:359])
           rotate([0,0,a])
	   up(0,bh+eh,bd/2-m,stp=1);
	}
    }
    difference()
    {
        translate([0,0,bh-0.01])
        cylinder(d=id+iw*2+s-m*2,h=wt+ih-bh+eh+((!os&&(i==1||tpp==2))?s:0),$fn=100);
	           translate([0,0,wt+m*2])
           cylinder(d=id+m*2,h=ih+1+eh+((!os&&(i==1||tpp==2))?s:0),$fn=100);
	   
	if(!is)
	{
           translate([0,0,wt+ih-id/2-1+eh])
           cylinder(d1=0,d2=id+m*2+6,h=id/2+2,$fn=100);
            
	}
    //mazes
    if(tpp<1 || tpp==2)
    {
        
        if(tpp==2)
        {
            basemaze(maze1,w1,h1,st1,ex1,mm,1);
            basemaze(maze2,w2,h2,st2,ex2,mm,0);
        }
        else
        {
            basemaze(maze1,w1,h1,st1,ex1,mm,i);
        }
    }
    
    }
    if((is && i==0 && tpp<1)||tpp==1)
	   {
              for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2+m,0,wt+ih-s/4*nubscale+eh+((!os&&(i==1||tpp==2))?s:0)])
              nub();
	   }
       if(i==1 && tpp<2)
	   {
           if(!is){
            difference(){
             for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2+iw+s/2-m,0,wt+ih-s/4*nubscale+eh])
              rotate([0,0,180])nub();
             
             translate([0,0,wt+ih-id/2-1+eh])cylinder(d1=0,d2=id+m*2+6,h=id/2+2,$fn=100);
             }}
             else
             {
                 for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2+iw+s/2-m,0,wt+ih-s/4*nubscale+eh])
              rotate([0,0,180])nub();
             }
             
	   }
       
   }
   if(bversion==2 && (i==0 || tpp==-1 || tpp==2))
    {
        for(c=[0:3.6:359])
        {
            if(os&&(-i==tpp||tpp==2))hull()
            {
                rotate([0,0,c])translate([(bd+s/4-m*2)/2,0,bh])knob();
                rotate([0,0,c+3.6])translate([(bd+s/4-m*2)/2,0,bh])knob();
            }
         if(tpp==2)
         {
            if(is)hull()
            {
                
                rotate([0,0,c])translate([id/2+s/2+iw,0,bh+eh+h2*s])knob();
                rotate([0,0,c+3.6])translate([id/2+s/2+iw,0,bh+eh+h2*s])knob();
            }
        }
        else if(is && (tpp>-1 || i==0))hull()
            {
                rotate([0,0,c])translate([id/2+s/2+iw,0,bh+eh+h1*s+s+((!os&&(i==0))?s:0)])knob();
                rotate([0,0,c+3.6])translate([id/2+s/2+iw,0,bh+eh+h1*s+s+((!os&&(i==0))?s:0)])knob();
            }
        }
        if(os&&(-i==tpp||tpp==2))for(c=[0:1:1])
        {
            hull()
            {
                rotate([0,0,180*c]){
                  translate([(bd+s/4-m*2)/2,0,bh])knob();
                    translate([(bd+s/4-m*2)/2,0,0])knob();
                }
            }
        }
    }
  }
}


module makelid(){
mm=(ih-bh-s*h1)/2+s/2+eh;

    difference()
    {
        outer(ih-bh+wt*2+eh+s/2);
        
	    hull()
	    {
               translate([0,0,wt-1])
               cylinder(d=id+s+iw*2+m-2,h=ih+eh+s/2,$fn=100);
               translate([0,0,wt])
               cylinder(d=id+s+iw*1.5+m*2,h=ih+eh+s/2+0.01,$fn=100);
	    }
            
        
        
        if(i==1){
            rotate([0,0,-st1*360/w1])
            {
        for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            rotate([0,0,st1*360/w1])
            {
                
                translate([0,0,bh+eh+s])up(i,s);
            }
            rotate([0,0,ex1*360/w1])translate([0,0,eh/2+bh+mm*1.75+s*(h1-1)])up(i,mm/3);
        }
            // Maze
        for(y=[0:1:h1-1])        translate([0,0,eh+bh+mm+y*s+m+s/2])        
            for(x=[0:1:w1-1])        rotate([0,0,x*360/w1])
        {
            if(maze1[y][x]==1 || maze1[y][x]==3)               right(w1,i);
            if(maze1[y][x]==2 || maze1[y][x]==3)                up(i,s);
        }
    }
    }
                //signature
        //translate([0,0,wt-2])linear_extrude(height=wt)aa((id+s+iw*2+m*2-2)/1.1,white=1);
    }
    if(i==0){
            for(a=[0:360/p:359])
            rotate([0,0,a])
            translate([id/2+iw+s/2,0,ih-bh+wt*2+eh+s/4-s/4/nubscale])nub();}

}
