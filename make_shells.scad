// Puzzle box by Adrian Kennard www.me.uk
//revised (Remixed?) by Jonathan Mercier (aka. spool2kool)
//Watermark removed...ummm, commented. (I do not like watermarks!)





//do not change below here.
//(Unless you know what you are doing!)
//Works so far.
include <shell_data.scad>

//computed 
nubscale=1.5+0;
eh=(tpp<1&&i==0)?0:s;
ih=(h1+1+((os == 0)?1:0))*s;
difference()
{
if(base)translate([lid?(id+s*4+iw*2+s*2)/2:0,0,0])makebase();
if(lid)
    difference()
{
    translate([base?-(id+s*4+iw*2+s*2)/2:0,0,0])makelid();
    side_emboss();
}
base_emboss();
}
module nub()
{
    if(oldnubs){
      rotate([0,0,-90])
    rotate([90,0,0])
        translate([0,0,s*td/8])hull()
    {
        cube([s/6*nubscale-m*2,s/6*nubscale-m*2,s*td/4],true);
        translate([0,0,-s*td/8-s/8])
        cube([s/2*nubscale-m*2,s/2*nubscale-m*2,s/4],true);
    }  
    }
    else{
    rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s*td/8])
    hull()
    {
        translate([0,0,0])cube([s/2-m*2,s/4*nubscale-m*2,s*td/4],true);
        translate([0,0,-s*td/8-s/8])
        cube([s/2-m*2,s/2*nubscale-m*2,s/4],true);
    }
}
}
module knob()
{
    if(oldnubs){
       rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s*td/8])
    hull()
    {
        cube([s/6*nubscale,s/6*nubscale,s*td/4],true);
        translate([0,0,-s*td/8-s/8])
        cube([s/2*nubscale,s/2*nubscale,s/4],true);
    }
    }
    else{
    rotate([0,0,-90])
    rotate([90,0,0])
    translate([0,0,s*td/8])
    hull()
    {
        translate([0,0,0])cube([s/2,s/4*nubscale,s*td/4],true);
        translate([0,0,-s*td/8-s/8])
        cube([s/2,s/2*nubscale,s/4],true);
    }
}
}

module right(w,i2,d=id/2+iw+s*td/2)
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

module up(i2,q,d=id/2+iw+s*td/2,stp=3)
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
       cylinder(r=(r-s)/cos(180/bs),h=h2-s,$fn=bs);
       cylinder(r1=0,r2=s,h=s,$fn=100);
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
module basemaze(maze,w,h,st,ex,i2)
{
    rotate([0,0,-st*360/w])
    {
    if(i2==0){ 
                
                    translate([0,0,s+s*nubscale/4]){
                        for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            
        rotate([0,0,st*360/w]){  
                
                //lock
            //knobr=atan2(360/p/4*s/(360/p),((id/2+iw+s/2)*2*PI/p/4));
            
                 if(os){
                     //for(b=[0:180/p/4/w:360/p/4])rotate([0,0,(lefty?b:-b)])translate([id/2+iw+s*td/2,0,s-b*s/(360/p)+s/6+s/4/nubscale])rotate([(lefty?-knobr:knobr),0,0])knob();
                     
                     for(b=[0:3.6:360/p/4-3.6])hull(){
                         rotate([0,0,(lefty?b:-b)])translate([id/2+iw+s*td/2+b*m*4/(360/p/4),0,0])knob();
                         rotate([0,0,(lefty?(b+3.6):-(b+3.6))])translate([id/2+iw+s*td/2+(b+3.6)*m*4/(360/p/4),0,0])knob();
                     }
                    
                     hull(){
                        translate([id/2+iw+s*td/2,0,0])knob();
                        translate([id/2+iw+s*td/2,0,s])knob();}
                     }
                     else
                     {
                         hull(){
                             translate([id/2+iw+s*td/2,0,-s])knob();
                             translate([id/2+iw+s*td/2,0,s])knob();
                             
                         }
                     }
            
                 }
             rotate([0,0,ex*360/w])translate([0,0,s+s*(h-1)])
            up(i2,2*s);
        }
        
        
        // Maze
        
        for(y=[0:1:h-1])
        translate([0,0,s+y*s])
        for(x=[0:1:w-1])
        rotate([0,0,x*360/w])
        {
            if(maze[y][x]==1 || maze[y][x]==3)right(w);
            if(maze[y][x]==2 || maze[y][x]==3)up(i2,s-m);
        }
    }
        }
        else if(is>0){
                   translate([0,0,s+s*nubscale/4])
            {
                for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            rotate([0,0,st*360/w])
           { 
                
                //lock
                //knobr=-atan2(360/p/4*s/(360/p),((id-s/2)*PI/p/4));
               
     //for(b=[0:180/p/4/w:360/p/4])rotate([0,0,(lefty?b:-b)])translate([id/2,0,s+s-b*s/(360/p)-s/2])rotate([0,0,180])rotate([(lefty?-knobr:knobr),0,0])knob();
               
               for(b=[0:3.6:360/p/4-3.6])hull(){
                   rotate([0,0,(lefty?b:-b)])translate([id/2-b*m*4/(360/p/4),0,s])rotate([0,0,180])knob();
                   
                   rotate([0,0,(lefty?(b+3.6):-(b+3.6))])translate([id/2-(b+3.6)*m*4/(360/p/4),0,s])rotate([0,0,180])knob();
               }
               
               
         //enter
                     hull(){translate([id/2,0,s])rotate([0,0,180])knob();
                         translate([id/2,0,s*2])rotate([0,0,180])knob();    
                         }
                     }
                     //exit
      rotate([0,0,ex*360/w])translate([0,0,s*2+s*(h-1)])
            up(i2,s*2,d=id/2);
                
        }
            // Maze
        for(y=[0:1:h-1])
        translate([0,0,s*2+y*s])
        
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
}
module makebase()
{
    //mm=(ih+s-s-s*h1)/2+s/2+m*2+eh+1;
    
    difference()
    {
    union(){
    difference()
    {
        if(os)
        {
            if(bversion==2)
            {
	difference()
	{
   	   cylinder(d=bd+s*td/4-m*2,h=s,$fn=100);
	   translate([0,0,-0.01])
	   difference()
	   {
		   cylinder(d=bd+s*td/4+2-m*2,h=s/2);
		   cylinder(d1=bd+s*td/4-2-m*2,d2=bd+s*td/4+4-m*2,h=s/2,$fn=100);
	   }
	}
}
else
{
    difference()
	{
   	   cylinder(d=bd-m*2-iw*2,h=s,$fn=100);
	   translate([0,0,-0.01])
	   difference()
	   {
		   cylinder(d=bd+2-m*2-iw*2,h=2);
		   cylinder(d1=bd-2-m*2-iw*2,d2=bd+4-m*2,h=3,$fn=100);
	   }
	}
}
}
	else
        outer(s+s);
	
	if(os && bversion==0)
	{
           for(a=[0:360/w1:359])
           rotate([0,0,a])
	   up(0,s+eh,bd/2-m-iw,stp=1);
	}
    }
    
    
    difference()
    {
        translate([0,0,s-0.01])
        cylinder(d=id+iw*2+s*td-m*2,h=s+ih-s+eh,$fn=100);
	          
        translate([0,0,s])
           cylinder(d=id+m*2,h=ih+1+eh,$fn=100);
	   
	if(!is)
	{
           translate([0,0,s+ih-id/2-1+eh])
           cylinder(d1=0,d2=id+m*2+6,h=id/2+2,$fn=100);
            
	}
    //mazes
    if(tpp<1 || tpp==2)
    {
        
        translate([0,0,((os == 0)?s:0)]){
            if(tpp==2)
        {
            basemaze(maze1,w1,h1,st1,ex1,1);
            basemaze(maze2,w2,h2,st2,ex2,0);
        }
        else
        {
            basemaze(maze1,w1,h1,st1,ex1,i);
        }
}
    }
    }
    if((is && i==0 && tpp<1)||tpp==1)
	   {
              for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2,0,s+ih-s/4*nubscale+eh])
              nub();
	   }
       if(i==1 && tpp<2)
	   {
           if(!is){
            difference(){
             for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2+iw+s*td/2-m,0,s+ih-s/4*nubscale+eh])
              rotate([0,0,180])nub();
             
             translate([0,0,s+ih-id/2-1+eh+s])cylinder(d1=0,d2=id+m*2+6,h=id/2+2,$fn=100);
             }}
             else
             {
                 for(a=[0:360/p:359])
              rotate([0,0,a])
              translate([id/2+iw+s*td/2-m,0,s+ih-s/4*nubscale+eh])
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
                rotate([0,0,c])translate([(bd+s*td/4-m*2)/2,0,s])knob();
                rotate([0,0,c+3.6])translate([(bd+s*td/4-m*2)/2,0,s])knob();
            }
         if(tpp==2)
         {
            if(is)hull()
            {
                
                rotate([0,0,c])translate([id/2+s*td/2+iw,0,s+ih+eh])knob();
                rotate([0,0,c+3.6])translate([id/2+s*td/2+iw,0,s+ih+eh])knob();
            }
        }
        else if(is && (tpp>-1 || i==0))hull()
            {
                rotate([0,0,c])translate([id/2+s*td/2+iw,0,s+ih])knob();
                rotate([0,0,c+3.6])translate([id/2+s*td/2+iw,0,s+ih])knob();
            }
        }
        if(os&&(-i==tpp||tpp==2))for(c=[0:1:p-1])
        {
            hull()
            {
                rotate([0,0,360/p*c]){
                  translate([(bd+s*td/4-m*2)/2,0,s])knob();
                    translate([(bd+s*td/4-m*2)/2,0,0])knob();
                }
            }
        }
    }
  }
  
}


module makelid(){
//mm=(ih-s-s*h1)/2+s/2+eh;

    difference()
    {
        outer(ih-s+s*2+eh-s/2);
        
	    hull()
	    {
               translate([0,0,s-1])
               cylinder(d=id+s*td+iw*2+m-2,h=ih+eh+s/2,$fn=100);
               translate([0,0,s])
               cylinder(d=id+s*td+iw*1.5+m*2,h=ih+eh+s/2+0.01,$fn=100);
	    }
            
        
        
        if(i==1){
            /*rotate([0,0,-st1*360/w1])
            {
        for(a=[0:360/p:359])
        rotate([0,0,a])
        {
            rotate([0,0,st1*360/w1])
            {
                
                translate([0,0,s+eh])up(i,s);
            }
            rotate([0,0,ex1*360/w1])translate([0,0,eh/2+s+mm*1.75+s*(h1-2)])up(i,mm/3);
        }
            // Maze
        for(y=[0:1:h1-1])        translate([0,0,eh+s+mm+y*s+m-s/2])        
            for(x=[0:1:w1-1])        rotate([0,0,x*360/w1])
        {
            if(maze1[y][x]==1 || maze1[y][x]==3)               right(w1,i);
            if(maze1[y][x]==2 || maze1[y][x]==3)                up(i,s);
        }
    }*/
     basemaze(maze1,w1,h1,st1,ex1,i);       
    }
                //signature
        //translate([0,0,s-2])linear_extrude(height=s)aa((id+s+iw*2+m*2-2)/1.1,white=1);
    }
    if(i==0){
            for(a=[0:360/p:359])
            rotate([0,0,a])
            translate([id/2+iw+s*td/2,0,ih-s+s*2+eh+s/4-s/4/nubscale-s+m/2])nub();}

}

module side_emboss(h=0.6)
{
    sze=min(bd*PI/bs-2,(h1*s-s-s-2)/len(se)*8/6);
    
    if(ense)
    {
        rotate([0,0,180/bs])translate([-bd/2+h,0,s+ih/2])rotate([0,-90,0])linear_extrude(h*2)text(se,size=sze,font="Liberation Mono:style=Bold",halign="center",valign="center");
    }
}

module base_emboss(h=0.6)
{
    sze=id;
    
    if(enbe && is<len(be))
    {
        rotate([180,0,0])translate([0,0,-h])linear_extrude(h*2)text(be[is],size=sze,font="Liberation Mono:style=Bold",halign="center",valign="center");
    }
}
