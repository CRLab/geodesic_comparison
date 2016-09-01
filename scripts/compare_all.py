import subprocess
import math
from multiprocessing import Process, Queue
from get_dirs_files import *
import shutil


def hausdorff_distance(mesh1_filepath, mesh2_filepath):
    # get hausdorff dist from meshlab server
    return_dict = {}
    try:
        f = open(os.devnull, 'w')
        cmd_str = "meshlabserver -s mlx_scripts/distance.mlx -i " + mesh1_filepath + " " + mesh2_filepath
        output = subprocess.check_output(cmd_str.split(" "), stderr=f)
        result = output.split("\n")
        # parse result to get values
        data = ""
        num_pnts1 = 0
        num_pnts2 = 0
        for idx, line in enumerate(result):
            m = re.match(r"\s*Sampled (\d+) pts.*", line)
            if m is not None:
                num_pnts1 = int(m.group(1))
            if line == 'Hausdorff Distance computed':
                data = result[idx+2]
        m = re.match(r"\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)", data)
        return_dict["min1"] = float(m.group(1))
        return_dict["max1"] = float(m.group(2))
        return_dict["mean1"] = float(m.group(3))
        return_dict["RMS1"] = float(m.group(4))
        # get hausdorff dist in other direction
        output = subprocess.check_output(["meshlabserver", "-s", "distance.mlx", "-i", mesh2_filepath, mesh1_filepath])
        result = output.split("\n")
        # parse result to get values
        for idx, line in enumerate(result):
            m = re.match(r"\s*Sampled (\d+) pts.*", line)
            if m is not None:
                num_pnts2 = int(m.group(1))
            if line == 'Hausdorff Distance computed':
                data = result[idx+2]
        m = re.match(r"\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)", data)
        return_dict["min2"] = float(m.group(1))
        return_dict["max2"] = float(m.group(2))
        return_dict["mean2"] = float(m.group(3))
        return_dict["RMS2"] = float(m.group(4))

        return_dict["total_min"] = min(return_dict["min1"], return_dict["min2"])
        return_dict["total_max"] = max(return_dict["max1"], return_dict["max2"])
        sm = return_dict["mean1"]*num_pnts1+return_dict["mean2"]*num_pnts2
        return_dict["total_mean"] = sm/(num_pnts1+num_pnts2)
        ms = (return_dict["RMS1"]**2)*num_pnts1 + (return_dict["RMS2"]**2)*num_pnts2
        return_dict["total_RMS"] = math.sqrt(ms/(num_pnts1+num_pnts2))

        return_dict["is_valid"] = 1
        return return_dict

    except Exception:
        f = open("hausdorff_failed.txt", "a")
        dirs1 = mesh1_filepath.split("/")
        dirs2 = mesh2_filepath.split("/")
        if dirs1[-1] == "gt.ply":
            shape = dirs2[-3]
            angle = dirs2[-2]
            fname = dirs2[-1]
        else:
            shape = dirs1[-3]
            angle = dirs1[-2]
            fname = dirs1[-1]

        f.write(shape+" "+angle+" "+fname+"\n")
        f.close()

        return_dict["is_valid"] = 0
        return return_dict


def reader(input_queue, results_queue):
    while True:

        msg = input_queue.get()
        if msg == 'DONE':
            print "Reader done"
            break
        else:

            ply_path = msg["ply_path"]
            gt_ply_path = msg["gt_ply_path"]
            command_str = msg["command_str"]
            shape = msg["shape"]
            angle = msg["angle"]
            mesh_name = msg["mesh_name"]

            # get hausdorff distance
            h_dist = hausdorff_distance(ply_path, gt_ply_path)

            if h_dist["is_valid"]==1:

                # get divergence
                output = subprocess.check_output(command_str.split(" "))
                result = output.split("\n")
                divergence = result[0]

                # prepare string
                output = shape+","+angle+","+mesh_name
                output = output+","+str(h_dist["min1"])+","+str(h_dist["max1"]) + \
                         ","+str(h_dist["mean1"])+","+str(h_dist["RMS1"])
                output = output+","+str(h_dist["min2"])+","+str(h_dist["max2"]) + \
                         ","+str(h_dist["mean2"])+","+str(h_dist["RMS2"])
                output = output+","+str(h_dist["total_min"])+","+str(h_dist["total_max"]) + \
                         ","+str(h_dist["total_mean"])+","+str(h_dist["total_RMS"])
                output = output+","+divergence+"\n"
                results_queue.put(output)


def compare_all():
    project_dir = get_project_dir()
    completed_dir = project_dir+"data/completed_meshes/"
    analysis_dir = project_dir+"data/analysis_results/"
    filename = "comparison_data.csv"
    outpath = analysis_dir+filename
    header = "shape,angle,mesh_name,h_C_Gt_min,h_C_Gt_max,h_C_Gt_mean,h_C_Gt_RMS,h_Gt_C_min,h_Gt_C_max," \
             "h_Gt_C_mean,h_Gt_C_RMS,h_sym_min,h_sym_max,h_sym_mean,h_sym_RMS,divergence"
    # open file
    f = open(outpath, 'w')
    # write header
    f.write(header+"\n")

    input_queue = Queue()
    results_queue = Queue(maxsize=100)
    counter = 0

    print("starting readers")
    num_readers = 6

    for i in range(num_readers):
        reader_p = Process(target=reader, args=(input_queue, results_queue))
        reader_p.daemon = True
        reader_p.start()

    # get all shape directories
    shape_dirs = get_immediate_subdirectories(completed_dir)
    for shape_dir in shape_dirs:
        shape = shape_dir[:-1]

        gt_ply_path = completed_dir + shape_dir + "gt_of.ply"
        gt_hist_path = analysis_dir + shape_dir + "gt_of.hist"

        # get angle directories
        angle_dirs = get_immediate_subdirectories(completed_dir+shape_dir)
        for angle_dir in angle_dirs:
            angle = angle_dir[:-1]

            # iterate through ply files
            ply_files = ["smooth_of.ply", "feature_of.ply", "partial_of.ply", "mirrored_of.ply"]
            for ply_file in ply_files:
                hist_file = ply_file.replace(".ply", ".hist")

                mesh_name = ply_file.replace(".ply", "")

                # get paths for h dist
                ply_path = completed_dir+shape_dir+angle_dir+ply_file
                hist_path = analysis_dir+shape_dir+angle_dir+hist_file

                # get divergence command string
                executable = project_dir+"geodesic_comparison/build/function_comparison"
                command_str = executable+" "+hist_path+" "+gt_hist_path

                input_dict = {}
                input_dict["ply_path"] = ply_path
                input_dict["gt_ply_path"] = gt_ply_path
                input_dict["command_str"] = command_str
                input_dict["shape"] = shape
                input_dict["angle"] = angle
                input_dict["mesh_name"] = mesh_name
                input_queue.put(input_dict)
                counter += 1

    print("putting done statements on queue")
    for i in range(num_readers):
        input_queue.put('DONE')

    print("starting to write data to file")
    for i in range(counter):
        output = results_queue.get()
        f.write(output)

    f.close()

    shutil.copy2(os.path.basename(__file__), project_dir + "data/scripts_history/" + os.path.basename(__file__))


if __name__ == "__main__":
    compare_all()
