# import csv
import os
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt


def get_time_series(path):
    class_labels_to_nums = {'AFIB': 1, 'N': 0, 'AFL': 0, 'J': 0}

    ecg_labels = []

    ecg_num = 0

    for file_name in os.listdir(path):
        if file_name[-3:] == 'csv':
            # print(path + file_name)
            data = pd.read_csv(path + file_name, encoding="ISO-8859-1")
            # data = pd.read_csv(path + file_name)
            annotations = open(path + file_name[:-3] + 'txt', 'r')
            annotation_lines = annotations.readlines()

            curr_annot_line = 1
            count_to_5_sec = 0

            ecg1 = []
            ecg2 = []

            for data_row in range(1, len(data)):
                # print('data.iloc[data_row]', data.iloc[data_row])
                # print('data.iloc[data_row, 0]', type(data.iloc[data_row, 0]))
                # print(curr_annot_line)
                # print('annotation_lines[curr_annot_line]', annotation_lines[curr_annot_line].split()[7][1:])
                if count_to_5_sec == 1250:
                    with open(path + file_name[:-4] + "_" + str(ecg_num) + "_1.p", "wb") as fp:
                        pickle.dump(ecg1, fp)
                    with open(path + file_name[:-4] + "_" + str(ecg_num) + "_2.p", "wb") as fp:
                        pickle.dump(ecg2, fp)
                    ecg_labels.append(class_labels_to_nums[annotation_lines[curr_annot_line].split()[7][1:]])
                    ecg1.clear()
                    ecg2.clear()
                    count_to_5_sec = 0
                    ecg_num += 1
                elif float(data.iloc[data_row, 0]) >= float(annotation_lines[curr_annot_line].split()[0]):
                    if curr_annot_line + 1 < len(annotation_lines) and \
                                    float(data.iloc[data_row, 0]) >= float(annotation_lines[curr_annot_line + 1].split()[0]):
                        ecg1.clear()
                        ecg2.clear()
                        curr_annot_line += 1
                        print(annotation_lines[curr_annot_line])
                        count_to_5_sec = 0
                    else:
                        ecg1.append(float(data.iloc[data_row, 1]))
                        ecg2.append(float(data.iloc[data_row, 2]))
                        count_to_5_sec += 1

    with open('ebg_labels', "wb") as fp:
        pickle.dump(ecg_labels, fp)


def main():
    folders_path = 'D:\\cygwin64\\home\\Bang\\wfdb-10.6.0\\afdb\\'

    folders = ['04015', '04043', '04048', '04126', '04746', '04908', '04936', '05091', '05121', '05261', '06426',
               '06453', '06995', '07162', '07859', '07879', '07910', '08215', '08219', '08378', '08405', '08434',
               '08455']

    for folder in folders:
        get_time_series(folders_path + folder + '\\')

    # with open(file_path + "04043._0_1.p", "rb") as fp:
    #     signals = pickle.load(fp)
    #
    # file_name = '04043.csv'
    #
    # data = pd.read_csv(file_path + file_name, encoding="ISO-8859-1")
    #
    # count_to_1k = 0
    #
    # ecg1 = []
    # ecg2 = []
    #
    # print(len(data))
    #
    # for data_row in range(1, 2502):
    #     # if count_to_1k == 2503:
    #     #     # with open(file_path + file_name[:-3] + "_0_1.p", "wb") as fp:
    #     #     #     pickle.dump(ecg1, fp)
    #     #     # with open(file_path + file_name[:-3] + "_0_2.p", "wb") as fp:
    #     #     #     pickle.dump(ecg2, fp)
    #     #     break
    #     # else:
    #     #     ecg1.append(data.iloc[data_row, 1])
    #     #     ecg2.append(data.iloc[data_row, 2])
    #     #     count_to_1k += 1
    #
    #     # print(data.iloc[data_row, 1])
    #     ecg1.append(float(data.iloc[data_row, 1]))
    #
    # print(ecg1)
    #
    # # print(len(signals))
    # print(min(ecg1))
    # print(max(ecg1))
    #
    # time = np.arange(2503)
    #
    # plt.plot(ecg1, linewidth=1.0)
    # # # plt.yticks(np.arange(min(ecg1), max(ecg1) + 1, step=0.1))
    # plt.show()
    # #
    # # plt.plot(time, ecg2)
    # # plt.yticks(np.arange(min(ecg2), max(ecg2) + 1, 1.0))
    # # plt.show()


if __name__ == "__main__":
    main()
