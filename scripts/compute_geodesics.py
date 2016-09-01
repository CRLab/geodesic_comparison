import subprocess
from multiprocessing import Pool
from get_dirs_files import *
import shutil


def handle_geodesic(command_str):
    subprocess.call(command_str.split(" "))


def compute_geodesics():
    project_dir = get_project_dir()
    completed_dir = project_dir+"data/completed_meshes/"
    analysis_dir = project_dir+"data/analysis_results/"

    p = Pool(6)
    tasks = []

    shape_dirs = get_immediate_subdirectories(completed_dir)
    for shape_dir in shape_dirs:

        # check if gt hist file already exists
        gt_ply_path = completed_dir+shape_dir+"gt_of.ply"
        gt_hist_path = analysis_dir+shape_dir+"gt_of.hist"
        if not os.path.exists(gt_hist_path):
            executable = project_dir + "geodesic_comparison/build/geodesic_function"
            command_str = executable + " " + gt_ply_path + " " + gt_hist_path
            tasks.append(command_str)

        angle_dirs = get_immediate_subdirectories(completed_dir+shape_dir)
        for angle_dir in angle_dirs:

            ply_files = ["smooth_of.ply", "feature_of.ply", "partial_of.ply"]
            hist_files = get_immediate_hist_files(analysis_dir+shape_dir+angle_dir)
            for ply_name in ply_files:

                # check if hist file already exists
                hist_name = ply_name.replace(".ply",".hist")
                if hist_name not in hist_files:
                    fpath = completed_dir+shape_dir+angle_dir+ply_name
                    outpath = analysis_dir+shape_dir+angle_dir+hist_name
                    executable = project_dir+"geodesic_comparison/build/geodesic_function"
                    command_str = executable+" "+fpath+" "+outpath
                    tasks.append(command_str)

    p.map(handle_geodesic, tasks)
    p.close()
    p.join()

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))


if __name__ == "__main__":
    compute_geodesics()
