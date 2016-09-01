import numpy as np
import plyfile
from multiprocessing import Pool
from get_dirs_files import *
import shutil


def align_mesh(task):

    mesh_filepath = task["mesh_filepath"]
    model_pose_filepath = task["model_pose_filepath"]
    center_to_upright_filepath = task["center_to_upright_filepath"]
    mesh_out_filepath = task["mesh_out_filepath"]

    print mesh_filepath

    mesh = plyfile.PlyData.read(mesh_filepath)

    # nx4 array
    mesh_vertices = np.ones((mesh['vertex']['x'].shape[0], 4))
    mesh_vertices[:, 0] = mesh['vertex']['x']
    mesh_vertices[:, 1] = mesh['vertex']['y']
    mesh_vertices[:, 2] = mesh['vertex']['z']

    world_to_camera_transform = np.array([[0, 0, 1, -1], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
    model_pose = np.load(model_pose_filepath)

    transform = np.dot(model_pose.T, world_to_camera_transform)

    # 4xn array
    mesh_vertices_of = np.dot(transform, mesh_vertices.T)

    center_to_upright = np.load(center_to_upright_filepath)
    mesh_vertices_of[0:3, :] += center_to_upright.reshape(3, 1)

    mesh_of = mesh

    mesh_of['vertex']['x'] = mesh_vertices_of.T[:, 0]
    mesh_of['vertex']['y'] = mesh_vertices_of.T[:, 1]
    mesh_of['vertex']['z'] = mesh_vertices_of.T[:, 2]
    mesh_of.text = True
    mesh_of.write(mesh_out_filepath)


def align_meshes():

    project_dir = get_project_dir()

    shape_completion_dir = project_dir + "shape_completion_results/"
    completed_dir = project_dir + "completed_meshes/"

    tasks = []

    shapes = get_immediate_subdirectories(completed_dir)
    for shape in shapes:

        angles = get_immediate_subdirectories(completed_dir+shape)
        for angle in angles:

            task_dict1 = {}
            task_dict1["mesh_filepath"] = completed_dir + shape + angle + "smooth.ply"
            task_dict1["model_pose_filepath"] = shape_completion_dir + shape + angle + "model_pose.npy"
            task_dict1["center_to_upright_filepath"] = shape_completion_dir + shape + angle + "center_to_upright.npy"
            task_dict1["mesh_out_filepath"] = completed_dir + shape + angle + "smooth_of.ply"
            tasks.append(task_dict1)

            task_dict2 = {}
            task_dict2["mesh_filepath"] = completed_dir + shape + angle + "feature.ply"
            task_dict2["model_pose_filepath"] = shape_completion_dir + shape + angle + "model_pose.npy"
            task_dict2["center_to_upright_filepath"] = shape_completion_dir + shape + angle + "center_to_upright.npy"
            task_dict2["mesh_out_filepath"] = completed_dir + shape + angle + "feature_of.ply"
            tasks.append(task_dict2)

            task_dict3 = {}
            task_dict3["mesh_filepath"] = completed_dir + shape + angle + "partial.ply"
            task_dict3["model_pose_filepath"] = shape_completion_dir + shape + angle + "model_pose.npy"
            task_dict3["center_to_upright_filepath"] = shape_completion_dir + shape + angle + "center_to_upright.npy"
            task_dict3["mesh_out_filepath"] = completed_dir + shape + angle + "partial_of.ply"
            tasks.append(task_dict3)

    p = Pool(6)
    p.map(align_mesh, tasks)
    p.close()
    p.join()

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))


if __name__ == "__main__":
    align_meshes()
