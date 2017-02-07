### Geodesic Comparison
Useful library for comparing meshes based off:


http://graphics.stanford.edu/courses/cs468-08-fall/pdf/hamza-krim.pdf

A. B. Hamza and H. Krim, “Geodesic object representation and
recognition,” in International conference on discrete geometry for
computer imagery. Springer, 2003, pp. 378–387.


####To Compute a Histogram for a mesh:
```
jvarley@skye:~/geodesic_comparison/build$ ./geodesic_function 
Usage: <Input filename (.ply)> <Output filename (.hist)>
```

####To Compare two Histograms from different meshes:
```
jvarley@skye:~/geodesic_comparison/build$ ./function_comparison 
Usage: <Histogram filename 1> <Histogram filename 2>
```
