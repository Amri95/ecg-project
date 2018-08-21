import matplotlib.pyplot as plt
from xml.dom import minidom
import pickle


def get_time_series(svg_file_path):
    doc = minidom.parse(svg_file_path)  # parseString also exists
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()

    count = 0
    graph_names = ['V1', 'II', 'V5']

    for path_string in path_strings:
        if path_string[0] == 'm':
            if count > 17:
                path_string_split = path_string.split()
                # print(path_string_split)
                # cur_x = path_string_split[1].split(',')[0]
                # cur_y = path_string_split[1].split(',')[1]
                x_values = []
                y_values = []
                x_values.append(0.0)
                y_values.append(0.0)

                # print(x_values)
                # print(y_values)

                lineto_horizontal = False
                # lineto_vertical = False

                for i in range(2, len(path_string_split)):
                    if path_string_split[i].isalpha():
                        if path_string_split[i] == 'h':
                            lineto_horizontal = True
                            # lineto_vertical = False
                        # elif path_string_split[i] == 'v':
                        #     lineto_vertical = True
                        #     lineto_horizontal = False
                    elif path_string_split[i].isdigit():
                        if lineto_horizontal:
                            # print(i)
                            # print(x_values[-1])
                            # print(int(path_string_split[i]))
                            x_values.append(x_values[-1] + float(path_string_split[i]))
                            y_values.append(y_values[-1])
                        # elif lineto_vertical:
                        #     x_values.append(x_values[i - 1])
                        #     y_values.append(y_values[i - 1] + int(path_string_split[i]))
                    elif ',' in path_string_split[i]:
                        delta_x = float(path_string_split[i].split(',')[0])
                        delta_y = float(path_string_split[i].split(',')[1])
                        x_values.append(x_values[-1] + delta_x)
                        y_values.append(y_values[-1] + delta_y)
                print('x_values:', x_values)
                # print(len(x_values))
                print('y_values:', y_values)
                # print(len(y_values))
                print(abs(max(y_values, key=abs)))
                for i in range(len(x_values)):
                    if type(x_values[i]) != float or type(y_values[i]) != float:
                        print('not float')

                pickle_values(svg_file_path[: -4] + "_" + graph_names[count - 18], x_values, y_values)

                plt.figure(figsize=(20, 5))
                plt.title(graph_names[count - 18])
                plt.plot(x_values, y_values, '-o', markersize=0.01)
                # plt.savefig("../ecg-samples/MUSE_20180323_153150_73000_replot_" + graph_names[count - 18] + ".pdf")
                # plt.show()
            count += 1
        plt.show()


def pickle_values(file_name, x_values, y_values):
    print(file_name)
    with open(file_name + "_x_values.txt", "wb") as fp:
        pickle.dump(x_values, fp)
    with open(file_name + "_y_values.txt", "wb") as fp:
        pickle.dump(y_values, fp)


def unpickle_values(file_path):
    with open(file_path + "_x_values.txt", "rb") as fp:
        x_values = pickle.load(fp)
    with open(file_path + "_y_values.txt", "rb") as fp:
        y_values = pickle.load(fp)

    return x_values, y_values


def main():
    svg_file_path = '../ecg-samples/MUSE_20180323_153150_73000.svg'
    # svg_file_path = '../ecg-samples/ecg_1.svg'

    get_time_series(svg_file_path)

    # graph_names = ['V1', 'II', 'V5']
    # for graph_name in graph_names:
    #     x_values, y_values = unpickle_values(svg_file_path[: -4] + "_" + graph_name)
    #     print(x_values)
    #     print(y_values)


if __name__ == "__main__":
    main()
