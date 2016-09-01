import subprocess
from get_dirs_files import *
import shutil


def move_mirrored():
    project_dir = get_project_dir()
    mirrored_dir = project_dir+"data/mirrored_results/"
    completed_dir = project_dir+"data/completed_meshes/"

    shape_dirs = get_immediate_subdirectories(mirrored_dir)
    for shape_dir in shape_dirs:

        angle_dirs = get_immediate_subdirectories(mirrored_dir+shape_dir)
        for angle_dir in angle_dirs:

            file_path = mirrored_dir+shape_dir+angle_dir+"meshSearch5_partial_of.ply"
            out_path = completed_dir+shape_dir+angle_dir+"mirrored_of.ply"
            subprocess.call(["mv", file_path, out_path])

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))

if __name__=="__main__":
    move_mirrored()
