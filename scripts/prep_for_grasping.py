import subprocess
from get_dirs_files import *
import shutil


def prep_for_grasping():
    project_dir = get_project_dir()
    completed_dir = project_dir+"data/completed_meshes/"
    analysis_dir = project_dir+"data/analysis_results/"

    shape_dirs = get_immediate_subdirectories(completed_dir)
    for shape_dir in shape_dirs:

        gt_path = completed_dir + shape_dir + "gt_of.ply"
        if os.path.exists(gt_path):
            new_gt_path = analysis_dir + shape_dir + "gt_smooth_of.ply"
            cmd_str = "meshlabserver -i " + str(gt_path) + " -o " \
                      + str(new_gt_path) + " -s mlx_scripts/smooth_downsample_gt.mlx"
            subprocess.call(cmd_str.split(" "))

        angle_dirs = get_immediate_subdirectories(completed_dir+shape_dir)
        for angle_dir in angle_dirs:

            mirrored_path = completed_dir+shape_dir+angle_dir+"mirrored_of.ply"
            if os.path.exists(mirrored_path):
                new_mirrored_path = analysis_dir+shape_dir+angle_dir+"mirrored_of.wrl"
                cmd_str = "meshlabserver -i " + str(mirrored_path) + " -o " + str(new_mirrored_path)
                subprocess.call(cmd_str.split(" "))

            partial_path = completed_dir + shape_dir + angle_dir+ "partial_of.ply"
            if os.path.exists(partial_path):
                new_partial_path = analysis_dir + shape_dir + angle_dir + "partial_smooth_of.ply"
                cmd_str = "meshlabserver -i " + str(partial_path) + " -o " \
                          + str(new_partial_path) + " -s mlx_scripts/smooth_partial.mlx"
                subprocess.call(cmd_str.split(" "))

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))

if __name__ == "__main__":
    prep_for_grasping()
