# Theory Notes

## Elastic edge restraints
Hinged support - epsilon = 0  
Clamped support - epsilon = infinity

> it is not necessary to determine this stiffness to a high degree of accuracy since the influence of epsilon upon kc embraces a large range of stiffness ratios, as is shown in figure 17. When the stiffener rotational rigidity has been found, epsilon may be computed by forming the ratio of this rigidity to the rotational rigidity of the plate. 

... chart of kc for long plates as a function of b/t for strong and weak stiffeners
(ref. 31 and fig. 18). Above bit = 200 it is seen that most stiffeners will effectively clamp the plate edge.

(ref NACA-TN-3781, pg 33)

## Torsional Rigigity
GJ is torsional equivalent to EI  
jJ~ polar (second) moment of inertia  
J = (double integral)(x2^2 + x3^2)dA (ref Unified M4-6, pg 18 http://web.mit.edu/16.unified/www/SPRING/materials/Lectures/M4.6-Unified09.pdf)
x1 = long axis of stiffener
x2, x3 = cross-section axes of stiffener

## Mixed Boundary Conditions
Average buckling coefficient kavg = sqrt(k1 * k2) (ref NACA-TN-3781, pg 33, eq 49)

Figs 15 and 16

structx.com