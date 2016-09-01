import subprocess
import plyfile
from get_dirs_files import *
import shutil


def copy_gts():
    project_dir = get_project_dir()
    in_dir = project_dir+"data/shape_completion_results/"
    completed_dir = project_dir+"data/completed_meshes/"

    shape_dirs = get_immediate_subdirectories(in_dir)
    for shape_dir in shape_dirs:

        file_path = in_dir+shape_dir+"gt_of.ply"
        completed_path = completed_dir+shape_dir+"gt_of.ply"
        subprocess.call(["cp", file_path, completed_path])
        subprocess.call(["meshlabserver", "-s", "mlx_scripts/clean.mlx", "-i", completed_path, "-o", completed_path])
        ply = plyfile.PlyData.read(completed_path)
        if not ply.text:
            ply.text = True
            ply.write(open(completed_path, "w"))

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))

if __name__ == "__main__":
    copy_gts()
