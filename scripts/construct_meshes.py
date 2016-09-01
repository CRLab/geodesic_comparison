import subprocess
from multiprocessing import Pool
from get_dirs_files import *
import shutil


def construct_mesh(task):
    executable = task["executable"]
    mesh_type = task["mesh_type"]
    out_path = task["out_path"]
    print out_path
    # if os.path.exists(out_path):
    #     return
    if mesh_type == "0" or mesh_type == "1":
        binvox_path = task["binvox_path"]
        pcd_path = task["pcd_path"]
        print "Getting Mesh"
        subprocess.call([executable, binvox_path, pcd_path, out_path, mesh_type])
    else:
        pcd_path = task["pcd_path"]
        print "Getting Partial Mesh"
        subprocess.call([executable, pcd_path, out_path])


def construct_meshes():
    project_dir = get_project_dir()
    in_dir = project_dir+"data/shape_completion_results/"
    completed_dir = project_dir+"data/completed_meshes/"

    in_binvox = "completion_cf.binvox"
    in_pcd = "partial_cf.pcd"

    exec_mesh_optimize = project_dir+"mesh_reconstruction/build/mesh_reconstruction"
    exec_mcubes = project_dir+"mesh_reconstruction/build/m_cubes"

    tasks = []
    # get all shape directories
    shape_dirs = get_immediate_subdirectories(completed_dir)
    for shape_dir in shape_dirs:

        # get angle directories
        angle_dirs = get_immediate_subdirectories(completed_dir+shape_dir)
        for angle_dir in angle_dirs:
            task1 = {}
            task1["binvox_path"] = in_dir + shape_dir + angle_dir + in_binvox
            task1["pcd_path"] = in_dir + shape_dir + angle_dir + in_pcd
            task1["executable"] = exec_mesh_optimize
            task1["mesh_type"] = "0"
            task1["out_path"] = completed_dir+shape_dir+angle_dir+"smooth.ply"
            tasks.append(task1)
            task2 = {}
            task2["binvox_path"] = in_dir + shape_dir + angle_dir + in_binvox
            task2["pcd_path"] = in_dir + shape_dir + angle_dir + in_pcd
            task2["executable"] = exec_mesh_optimize
            task2["mesh_type"] = "1"
            task2["out_path"] = completed_dir + shape_dir + angle_dir + "feature.ply"
            tasks.append(task2)
            task3 = {}
            task3["pcd_path"] = in_dir + shape_dir + angle_dir + in_pcd
            task3["executable"] = exec_mcubes
            task3["mesh_type"] = "-1"
            task3["out_path"] = completed_dir + shape_dir + angle_dir + "partial.ply"
            tasks.append(task3)
    if True:
        p = Pool(6)
        p.map(construct_mesh, tasks)
        p.close()
        p.join()
    else:
        for i, task in enumerate(tasks):
            print i
            construct_mesh(task)

    shutil.copy2(os.path.basename(__file__), project_dir+"data/scripts_history/"+os.path.basename(__file__))

if __name__ == "__main__":
    construct_meshes()
