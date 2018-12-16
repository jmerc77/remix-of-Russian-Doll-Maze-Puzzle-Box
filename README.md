# Russian Doll Maze Puzzle Box Generator

Generator for [Thingiverse Thing 2980535](https://www.thingiverse.com/thing:2980535)

### System requirements

- OS
  - Windows 7 or greater
  - MacOS (tested with python3 installed via homebrew)
  - Linux may work but untested
- `python 3.5` or greater with:
  - numpy
  - pillow
- `openscad 2015.03-2` or later
- stl repair tool (I used netfab)

## Instructions

Install the above software before first use and edit the path in the python code to match your setup.
Make sure to install the python libs!

1. If OpenSCAD is in a nonstandard location, adjust path at top of `main.py` (folders for output and preview created when run)
2. (optional) Adjust the `bs` (lid sides) value in `make shells.scad` for a new look if you like
3. (optional) Adjust values in `opt.ini` as you see fit
4. (optional) Make a backup of `opt.ini` so you can reuse these values in the future
5. Open a python shell and run `main.py` (you may be able to just double click it)
   - You will be prompted whether to use multi-threadding (if available) then nub count, a difficulty level and a shift mode value.
   - Shifting is where each row of the maze is shifted and wrapped for the illusion of a bigger maze.
   - For shift mode 3, also input how much. It will be constrained by modulus, so large nums will not break it.
   - Stl files go in the `stl_files` folder and previews in the `prev` folder.
6. The stl files may need repair. Use a repair tool.
   - It is recomended to view all stl files to check that they will work.
7. Print a 2-part test print at 0.2mm layers. If they fit, print the rest.

### Tips

- Read `opt.ini`, it has important info about the options.
- Put all these files in a project folder.
- If using Windows, use the multi-thread openscad version: [32 bit](http://files.openscad.org/snapshots/OpenSCAD-2018.05.30-x86-32_multithread-Installer.exe) Or [64 bit](http://files.openscad.org/snapshots/OpenSCAD-2018.05.30-x86-64_multithread-Installer.exe).
- Preview the mazes in the `prev` folder. If using transition point, the one ending with "a" is of the same shell as without the "a".

### Notes

- Be patient: It may take a while to run the openscad scripts.
- `m=0.3` (`tolerance` in `opt.ini`) for 0.4mm nozzle worked well for me with ABS. PLA or PETG recomended as some shells can be large, nubs rub off easier with "soft" materials, and cheating can be possible with "flexible" materials.
- Editing during the run may not be possible.
- Openscad scripts run via shell in the python code. This speeds the process of stl export as this limits having to switch between apps.
- To make another or to adjust values, you will need to restart from step 2 as some parts may no longer fit.
