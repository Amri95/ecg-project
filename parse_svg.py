import matplotlib.pyplot as plt
from xml.dom import minidom

svg_file = '../ecg-samples/MUSE_20180323_153150_73000.svg'

doc = minidom.parse(svg_file)  # parseString also exists
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

for path_string in path_strings:
    if path_string[0] == 'm':
        path_string_split = path_string.split()
        # print(path_string_split)
        cur_x = path_string_split[1].split(',')[0]
        cur_y = path_string_split[1].split(',')[1]
        x_values = []
        y_values = []
        x_values.append(int(cur_x))
        y_values.append(int(cur_y))

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
                    x_values.append(x_values[-1] + int(path_string_split[i]))
                    y_values.append(y_values[-1])
                # elif lineto_vertical:
                #     x_values.append(x_values[i - 1])
                #     y_values.append(y_values[i - 1] + int(path_string_split[i]))
            elif ',' in path_string_split[i]:
                delta_x = int(path_string_split[i].split(',')[0])
                delta_y = int(path_string_split[i].split(',')[1])
                x_values.append(x_values[-1] + delta_x)
                y_values.append(y_values[-1] + delta_y)
        print('x_values:', x_values)
        print('y_values:', y_values)

        plt.plot(x_values, y_values, '-o', markersize=0.0001)
        # plt.show()
    plt.savefig("../ecg-samples/MUSE_20180323_153150_73000_replot.pdf")
