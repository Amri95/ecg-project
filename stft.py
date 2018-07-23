import pickle


def unpickle_values(file_path):
    with open(file_path + "_x_values.txt", "rb") as fp:
        x_values = pickle.load(fp)
    with open(file_path + "_y_values.txt", "rb") as fp:
        y_values = pickle.load(fp)

    return x_values, y_values


def short_term_fourier_transform(x_values, y_values):
    return True


def main():
    svg_file_path = '../ecg-samples/MUSE_20180323_153150_73000.svg'

    graph_names = ['V1', 'II', 'V5']
    for graph_name in graph_names:
        x_values, y_values = unpickle_values(svg_file_path[: -4] + "_" + graph_name)
        # print(x_values)
        # print(y_values)
        short_term_fourier_transform(x_values, y_values)


if __name__ == "__main__":
    main()