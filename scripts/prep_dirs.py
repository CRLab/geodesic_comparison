import subprocess
from get_dirs_files import *
import shutil
import yaml


def prep_dirs():

    dset = yaml.load(open("./yaml_files/GRASP_590_Dataset.yaml", 'r'))
    # dset = yaml.load(open("./yaml_files/YCB_Dataset.yaml", 'r'))
    model_names = dset['holdout_model_names']
    # model_names = dset['train_model_names']

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

    project_dir = get_project_dir()
    shape_completion_dir = project_dir + "data/shape_completion_results/"
    completed_dir = project_dir + "data/completed_meshes/"
    mirrored_dir = project_dir + "data/mirrored_results/"
    analysis_dir = project_dir + "data/analysis_results/"

    for model_name in model_names:
        cmd_str1 = "mkdir " + shape_completion_dir + model_name
        cmd_str2 = "mkdir " + completed_dir + model_name
        cmd_str3 = "mkdir " + mirrored_dir + model_name
        cmd_str4 = "mkdir " + analysis_dir + model_name
        subprocess.call(cmd_str1.split(" "))
        subprocess.call(cmd_str2.split(" "))
        subprocess.call(cmd_str3.split(" "))
        subprocess.call(cmd_str4.split(" "))
        for view_name in view_names:
            cmd_str1 = "mkdir " + shape_completion_dir + model_name + "/" + view_name
            cmd_str2 = "mkdir " + completed_dir + model_name + "/" + view_name
            cmd_str3 = "mkdir " + mirrored_dir + model_name + "/" + view_name
            cmd_str4 = "mkdir " + analysis_dir + model_name + "/" + view_name
            subprocess.call(cmd_str1.split(" "))
            subprocess.call(cmd_str2.split(" "))
            subprocess.call(cmd_str3.split(" "))
            subprocess.call(cmd_str4.split(" "))

    shutil.copy2(os.path.basename(__file__), project_dir+"data/scripts_history/"+os.path.basename(__file__))


if __name__ == "__main__":
    prep_dirs()