import os
import re


def get_project_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    m = re.match(r"^(.*)scripts", current_dir)
    return m.group(1)


def get_immediate_subdirectories(a_dir):
    dirs = [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]
    dirs2 = []
    for dir_ in dirs:
        if dir_[0] != ".":
            dirs2.append(dir_+"/")
    return dirs2


def get_immediate_ply_files(a_dir):
    only_files = [f for f in os.listdir(a_dir) if os.path.isfile(os.path.join(a_dir, f))]
    ply_files = []
    for f in only_files:
        if f[-4:] == ".ply":
            ply_files.append(f)
    return ply_files


def get_immediate_hist_files(a_dir):
    only_files = [f for f in os.listdir(a_dir) if os.path.isfile(os.path.join(a_dir, f))]
    hist_files = []
    for f in only_files:
        if f[-5:] == ".hist":
            hist_files.append(f)
    return hist_files


if __name__ == "__main__":
    print get_project_dir()
