from clean_all_data import *
from prep_dirs import *
from align_data import *
from extract_files import *
from construct_meshes import *
from align_meshes import *
from construct_mirrored import *
from copy_gts import *
from move_mirrored import *
from prep_for_grasping import *
from compute_geodesics import *
from compare_all import *


def run_all():

    print "CLEANING ALL DATA"
    clean_all_data()
    print "RESETTING DIRECTORY STRUCTURE"
    prep_dirs()
    print "EXTRACT DATA FROM SERVER"
    align_data()
    extract_files()
    print "GENERATE COMPLETIONS"
    import IPython
    IPython.embed()
    print "CONSTRUCTING SMOOTH, FEATURE, AND PARTIAL MESHES"
    construct_meshes()
    print "ALIGN MESHES"
    align_meshes()
    print "CONSTRUCTING MIRRORED MESHES"
    construct_mirrored()
    print "COPYING GROUND TRUTH MESHES"
    copy_gts()
    print "MOVING MIRRORED MESHES"
    move_mirrored()
    print "FORMATTING GROUND TRUTH AND MIRRORED MESHES FOR GRASPING"
    prep_for_grasping()
    print "COMPUTING GEODESIC HISTOGRAMS"
    compute_geodesics()
    print "GENERATING COMPARISON DATA"
    compare_all()

if __name__ == "__main__":
    run_all()
