import subprocess
from multiprocessing import Pool
from get_dirs_files import *
import shutil


def handle_mirrored(task):
    if os.listdir(task[1]) == []:
        subprocess.call(task[0])


def construct_mirrored():
    project_dir = get_project_dir()
    in_dir = project_dir+"data/shape_completion_results/"
    mirrored_dir = project_dir+"data/mirrored_results/"

    p = Pool(6)
    tasks = []

    shape_dirs=get_immediate_subdirectories(in_dir)
    for shape_dir in shape_dirs:

        angle_dirs=get_immediate_subdirectories(in_dir+shape_dir)
        for angle_dir in angle_dirs:

            executable = project_dir+"mirror_ws/devel/lib/mirror_objects/mirrorAndReconstruct"
            fpath = in_dir+shape_dir+angle_dir+"partial_of.pcd"
            camera_params = ["-p", "0", "-100", "0", "5"]
            outpath = mirrored_dir+shape_dir+angle_dir
            flags = "-f"
            calib = project_dir+"mirror_ws/src/mirror_objects/demo/calib.txt"
            print fpath
            function_call = [executable, fpath]
            function_call.extend(camera_params)
            function_call.append(outpath)
            function_call.append(flags)
            function_call.append(calib)
            tasks.append([function_call, outpath])

    p.map(handle_mirrored, tasks)
    p.close()
    p.join()

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))


if __name__ == "__main__":
    construct_mirrored()
