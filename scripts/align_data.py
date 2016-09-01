import numpy as np
import os
import pcl
import subprocess
import plyfile
from multiprocessing import Pool
import yaml


def align_gt(task):

    gt_mesh_filepath = task["gt_mesh_filepath"]
    translate_filepath = task["translate_filepath"]
    gt_upright_filepath = task["gt_upright_filepath"]

    print gt_mesh_filepath

    gt_mesh = plyfile.PlyData.read(gt_mesh_filepath)

    gt_mesh_vertices = np.zeros((gt_mesh['vertex']['x'].shape[0], 4))
    gt_mesh_vertices[:, 0] = gt_mesh['vertex']['x']
    gt_mesh_vertices[:, 1] = gt_mesh['vertex']['y']
    gt_mesh_vertices[:, 2] = gt_mesh['vertex']['z']
    x_min = gt_mesh_vertices[:, 0].min()
    x_max = gt_mesh_vertices[:, 0].max()
    y_min = gt_mesh_vertices[:, 1].min()
    y_max = gt_mesh_vertices[:, 1].max()
    z_min = gt_mesh_vertices[:, 2].min()

    x_shift = -((x_min + x_max) / 2)
    y_shift = -((y_min + y_max) / 2)
    z_shift = -z_min

    translate = np.array([x_shift, y_shift, z_shift])
    np.save(translate_filepath, translate)

    gt_mesh['vertex']['x'] += x_shift
    gt_mesh['vertex']['y'] += y_shift
    gt_mesh['vertex']['z'] += z_shift
    gt_mesh.text = True
    gt_mesh.write(gt_upright_filepath)


def align_gts():

    server_path = "/home/adamjri/mnt_mainland/data/shape_completion_data/"

    dataset_dir = "grasp_database/"

    dset = yaml.load(open("./yaml_files/GRASP_590_Dataset.yaml", 'r'))
    # dset = yaml.load(open("./yaml_files/YCB_Dataset.yaml", 'r'))
    model_names = dset['holdout_model_names']
    # model_names = dset['train_model_names']

    tasks = []
    for model_name in model_names:
        task_dict = {}
        gt_mesh_filepath = server_path + dataset_dir + model_name + "/meshes/" + model_name + "_scaled.ply"
        if not os.path.exists(gt_mesh_filepath):
            gt_off_filepath = gt_mesh_filepath.replace(".ply", ".off")
            cmd_str = "meshlabserver -i " + gt_off_filepath + " -o " + gt_mesh_filepath
            subprocess.call(cmd_str.split(" "))
        task_dict["gt_mesh_filepath"] = gt_mesh_filepath
        task_dict["translate_filepath"] = server_path + dataset_dir + model_name + "/meshes/gt_center_to_upright.npy"
        task_dict["gt_upright_filepath"] = server_path + dataset_dir + model_name + "/meshes/gt_upright.ply"

        if not os.path.exists(task_dict["gt_upright_filepath"]):
            tasks.append(task_dict)

    p = Pool(6)
    p.map(align_gt, tasks)
    p.close()
    p.join()


def load_np_pc(filepath):
    pcd = pcl.load(filepath)
    # gt_np shape is (#pts, 3)
    np_temp = pcd.to_array()
    np_pc = np.ones((np_temp.shape[0], 4))
    np_pc[:, 0:3] = np_temp
    return np_pc


def align_partial(task):

    center_to_upright_filepath = task["center_to_upright_filepath"]
    model_pose_filepath = task["model_pose_filepath"]
    partial_filepath = task["partial_filepath"]
    partial_of_filepath = task["partial_of_filepath"]

    print partial_filepath

    center_to_upright = np.load(center_to_upright_filepath)
    model_pose = np.load(model_pose_filepath)
    # nx4 array
    partial_np_pc = load_np_pc(partial_filepath)

    world_to_camera_transform = np.array([[0, 0, 1, -1],[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
    transform = np.dot(model_pose.T, world_to_camera_transform)
    # 4xn array
    partial_np_pc_of = np.dot(transform, partial_np_pc.T)

    partial_np_pc_of[0:3, :] += center_to_upright.reshape(3, 1)

    partial_pcd_pc_of = pcl.PointCloud(np.array(partial_np_pc_of.T[:, 0:3], np.float32))

    # if not os.path.exists(partial_of_filepath):
    pcl.save(partial_pcd_pc_of, partial_of_filepath)


def align_partials():

    view_names = ['5_1_10',
                  '3_5_9',
                  '4_4_0',
                  '6_1_2',
                  '8_4_0',
                  '0_5_2',
                  '6_3_2',
                  '1_4_0',
                  '0_1_6',
                  '3_0_1']

    server_path = "/home/adamjri/mnt_mainland/data/shape_completion_data/"

    dataset_dir = "grasp_database/"

    dset = yaml.load(open("./yaml_files/GRASP_590_Dataset.yaml", 'r'))
    # dset = yaml.load(open("./yaml_files/YCB_Dataset.yaml", 'r'))
    model_names = dset['holdout_model_names']
    # model_names = dset['train_model_names']

    tasks = []
    for model_name in model_names:
        for view_name in view_names:
            task_dict = {}
            task_dict["center_to_upright_filepath"] = server_path + dataset_dir + \
                                                      model_name + "/meshes/gt_center_to_upright.npy"
            task_dict["model_pose_filepath"] = server_path + dataset_dir + model_name + \
                                               "/pointclouds/_" + view_name + "_model_pose.npy"
            task_dict["partial_filepath"] = server_path + dataset_dir + model_name + \
                                            "/pointclouds/_" + view_name + "_pc.pcd"
            task_dict["partial_of_filepath"] = server_path + dataset_dir + model_name + \
                                               "/pointclouds/_" + view_name + "_pc_of.pcd"
            if not os.path.exists(task_dict["partial_of_filepath"]):
                tasks.append(task_dict)

    p = Pool(6)
    p.map(align_partial, tasks)
    p.close()
    p.join()


def align_data():
    align_gts()
    align_partials()


if __name__ == "__main__":
    align_data()
