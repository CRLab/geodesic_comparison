import subprocess
from get_dirs_files import *
import shutil
import yaml


def clean_all_data():

    project_dir = get_project_dir()
    shape_completion_dir = project_dir+"data/shape_completion_results/"
    completed_dir = project_dir+"data/completed_meshes/"
    mirrored_dir = project_dir+"data/mirrored_results/"
    analysis_dir = project_dir+"data/analysis_results/"
    dirs = [shape_completion_dir, completed_dir, mirrored_dir, analysis_dir]

    for dir_ in dirs:

      p = subprocess.Popen("%s %s" % ("rm", "-rf " + dir_ + "*"), shell=True,
                           stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
      p.wait()

    shutil.copy2(os.path.basename(__file__), project_dir+"data/scripts_history/"+os.path.basename(__file__))


if __name__ == "__main__":
    clean_all_data()
