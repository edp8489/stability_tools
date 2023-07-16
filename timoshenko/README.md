# Timoshenko Bending-Compression Buckling
These scripts implement the method of determining the buckling coefficient for a simply-supported flat plate under arbitrary combinations of in-plane bending + uniaxial compression (or tension) as described in Timoshenko, *Theory of Elastic Stability*, Article 9.6.

Loading conditions per Article 9.6, eq (a):

$` N_0 \rightarrow `$ Load at top (compression) edge of plate  
$` N_x \rightarrow `$ Load at bottom edge of plate  
$`\alpha \rightarrow `$ non-dimensional factor representing load distribution defined by the following equation:   
$$N_x = N_0*\left(1 - \alpha*\frac{y}{b}\right)$$

$` \alpha = 0 \rightarrow `$ pure compression  
$` 0 < \alpha < 2 \rightarrow `$ combined compression & bending  
$` \alpha = 2 \rightarrow `$ pure bending  
$` \alpha > 2 \rightarrow `$ combined tension & bending
