import csv
import matplotlib.pyplot as plt
import numpy as np


def load_analysis_data(filepath):
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        data = {}
        for row in reader:
            shape_name = row['shape']
            angle_name = row['angle']
            mesh_name = row['mesh_name']
            if shape_name not in data:
                data[shape_name]={}

            if angle_name not in data[shape_name]:
                data[shape_name][angle_name]={}

            if mesh_name not in data[shape_name][angle_name]:
                data[shape_name][angle_name][mesh_name]={}

            keys = ['h_C_Gt_min','h_C_Gt_max','h_C_Gt_mean','h_C_Gt_RMS','h_Gt_C_min','h_Gt_C_max','h_Gt_C_mean','h_Gt_C_RMS','h_sym_min','h_sym_max','h_sym_mean','h_sym_RMS','divergence']
            for key in keys:
                data[shape_name][angle_name][mesh_name][key]=row[key]

    return data


def plot_symmetric_hausdorff(data):
    max_data_lists = {}
    mean_data_lists = {}

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # organize data into dict of lists
    for shape_name in data.keys():
        for angle_name in data[shape_name].keys():
            for mesh_name in data[shape_name][angle_name].keys():
                if mesh_name not in max_data_lists:
                    max_data_lists[mesh_name] = []

                if mesh_name not in mean_data_lists:
                    mean_data_lists[mesh_name] = []

                max_data_lists[mesh_name].append(float(data[shape_name][angle_name][mesh_name]['h_sym_max']))
                mean_data_lists[mesh_name].append(float(data[shape_name][angle_name][mesh_name]['h_sym_mean']))

    max_data = []
    max_std = []
    mean_data = []
    mean_std = []
    for key in mean_data_lists.keys():
        max_data.append(np.array(max_data_lists[key]).mean())
        max_std.append(np.array(max_data_lists[key]).std())
        mean_data.append(np.array(mean_data_lists[key]).mean())
        mean_std.append(np.array(mean_data_lists[key]).std())

    N = len(max_data)

    # necessary plotting variables
    ind = np.arange(N)
    width = 0.35

    # create the bars
    rects1 = ax.bar(ind, max_data, width, color='black', yerr=max_std, error_kw=dict(elinewidth=2,ecolor='red') )
    rects2 = ax.bar(ind+width, mean_data, width, color='red', yerr=mean_std, error_kw=dict(elinewidth=2,ecolor='black') )

    # axis and labels
    ax.set_xlim(-width, len(ind)+width)
    ax.set_ylim(0,0.2)
    ax.set_ylabel('Hausdorff Distance', fontsize = 14)
    ax.set_title('Mean and Max Hausdorff Distances by Completion Method', fontsize=14)
    xTickMarks = max_data_lists.keys()
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation='horizontal', fontsize=14)

    # add a legend
    ax.legend( (rects1[0], rects2[0]), ('Max', 'Mean') )

    plt.show()


def plot_divergence(data):
    divergence_data_lists = {}

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # organize data into dict of lists
    for shape_name in data.keys():
        for angle_name in data[shape_name].keys():
            for mesh_name in data[shape_name][angle_name].keys():
                if mesh_name not in divergence_data_lists:
                    divergence_data_lists[mesh_name]=[]
                divergence_data_lists[mesh_name].append(float(data[shape_name][angle_name][mesh_name]['divergence']))

    divergence_data = []
    divergence_std = []
    for key in divergence_data_lists.keys():
        divergence_data.append(np.array(divergence_data_lists[key]).mean())
        divergence_std.append(np.array(divergence_data_lists[key]).std())

    N = len(divergence_data)

    # necessary plotting variables
    ind = np.arange(N)
    width = 0.35

    # create the bars
    rects = ax.bar(ind+width/2, divergence_data, width, color='black', yerr=divergence_std, error_kw=dict(elinewidth=2,ecolor='red') )

    # axis and labels
    ax.set_xlim(-width, len(ind)+width)
    ax.set_ylim(0,0.73)
    ax.set_ylabel('Divergence', fontsize = 14)
    ax.set_title('Divergence of Geodesic Function by Completion Method', fontsize=14)
    xTickMarks = divergence_data_lists.keys()
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation='horizontal', fontsize=14)

    plt.show()


if __name__=="__main__":
    filename = '../data/analysis_results/comparison_data.csv'
    data = load_analysis_data(filename)
    plot_divergence(data)
    plot_symmetric_hausdorff(data)
