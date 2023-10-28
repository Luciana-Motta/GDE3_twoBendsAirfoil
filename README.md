# GDE3_twoBendsAirfoil

Estimate the performance of simple two-bends airfoils:

1. Set the desired angle of attack: variable "aoa" (degrees) in mesh/parameters.geo.
2. Gmsh meshing: gmsh -3 -o main.msh mesh/main.geo
3. OpenFOAM (see script for sub-steps): ./run.sh
4. Open "view.foam" in ParaView and/or view force coefficients in ./case/postProcessing/.


To run GDE3, just run at the prompt: python gde3.py.

Installations required:

1. sudo apt-get install gmsh.
2. pip install platypus-opt
3. sudo apt-get install texlive-full
