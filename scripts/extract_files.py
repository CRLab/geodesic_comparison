from get_dirs_files import *
import subprocess
import yaml


def extract_gts():
    server_path = "/home/adamjri/mnt_mainland/data/shape_completion_data/"

    dataset_dir = "grasp_database/"

    dset = yaml.load(open("./yaml_files/GRASP_590_Dataset.yaml", 'r'))
    # dset = yaml.load(open("./yaml_files/YCB_Dataset.yaml", 'r'))
    model_names = dset['holdout_model_names']
    # model_names = dset['train_model_names']

    project_dir = get_project_dir()
    shape_completion_dir = project_dir+"data/shape_completion_results/"

    for model_name in model_names:
        gt_upright_path = server_path + dataset_dir + model_name + "/meshes/gt_upright.ply"
        out_path = shape_completion_dir + model_name + "/gt_of.ply"
        cmd_str = "cp " + gt_upright_path + " " + out_path
        subprocess.call(cmd_str.split(" "))


def extract_partials():
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

    project_dir = get_project_dir()
    shape_completion_dir = project_dir + "data/shape_completion_results/"

    for model_name in model_names:
        for view_name in view_names:
            partial_filepath = server_path + dataset_dir + model_name + "/pointclouds/_" + view_name + "_pc.pcd"
            partial_of_filepath = server_path + dataset_dir + model_name + "/pointclouds/_" + view_name + "_pc_of.pcd"
            pc_out_filepath = shape_completion_dir + model_name + "/" + view_name + "/partial_cf.pcd"
            pc_of_out_filepath = shape_completion_dir + model_name + "/" + view_name + "/partial_of.pcd"
            cmd_str1 = "cp " + partial_filepath + " " + pc_out_filepath
            cmd_str2 = "cp " + partial_of_filepath + " " + pc_of_out_filepath
            subprocess.call(cmd_str1.split(" "))
            subprocess.call(cmd_str2.split(" "))


def extract_transforms():
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

    project_dir = get_project_dir()
    shape_completion_dir = project_dir + "data/shape_completion_results/"

    for model_name in model_names:
        for view_name in view_names:
            model_pose_filepath = server_path + dataset_dir + model_name + \
                                  "/pointclouds/_" + view_name + "_model_pose.npy"
            camera_pose_filepath = server_path + dataset_dir + model_name + \
                                  "/pointclouds/_" + view_name + "_camera_pose.npy"
            center_to_upright_filepath = server_path + dataset_dir + model_name + "/meshes/gt_center_to_upright.npy"

            model_pose_out_filepath = shape_completion_dir + model_name + "/" + view_name + "/model_pose.npy"
            camera_pose_out_filepath = shape_completion_dir + model_name + "/" + view_name + "/camera_pose.npy"
            center_to_upright_out_filepath = shape_completion_dir + model_name + \
                                             "/" + view_name + "/center_to_upright.npy"

            cmd_str1 = "cp " + model_pose_filepath + " " + model_pose_out_filepath
            cmd_str2 = "cp " + camera_pose_filepath + " " + camera_pose_out_filepath
            cmd_str3 = "cp " + center_to_upright_filepath + " " + center_to_upright_out_filepath

            subprocess.call(cmd_str1.split(" "))
            subprocess.call(cmd_str2.split(" "))
            subprocess.call(cmd_str3.split(" "))


def extract_files():
    extract_gts()
    extract_partials()
    extract_transforms()


if __name__ == "__main__":
    extract_files()
