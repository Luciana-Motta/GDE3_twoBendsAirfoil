# single_bend_airfoil

Estimate the performance of simple single-bend airfoils.

1. Set the desired angle of attack: variable "aoa" (degrees) in mesh/parameters.geo.
2. Gmsh meshing: gmsh -3 -o main.msh mesh/main.geo
3. OpenFOAM (see script for sub-steps): ./run.sh
4. Open "view.foam" in ParaView and/or view force coefficients in ./case/postProcessing/.


