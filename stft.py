import pickle
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter
from scipy.signal import freqz
import os


def butter_bandpass(lowcut, highcut, fs, order=10):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=10):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def unpickle_values(file_path):
    with open(file_path, "rb") as fp:
        y_values = pickle.load(fp)

    return y_values


def short_term_fourier_transform(time_series, graph_name, file_location):
    # # St.Mike's data
    # fs = 500
    # # amp = 2 * np.sqrt(2)
    # amp = 2
    # window = signal.hamming(512)
    # f, t, Zxx = signal.stft(np.array(time_series), fs, nperseg=512, window=window, noverlap=511)

    # Public data
    fs = 250
    # amp = 2 * np.sqrt(2)
    amp = 0.00001
    window = signal.hamming(128)

    f, t, Zxx = signal.stft(np.array(time_series), fs, nperseg=128, window=window, noverlap=127)


    # # St.Mike's data
    # plt.pcolormesh(t, f, np.absolute(Zxx) * np.absolute(Zxx), vmin=0, vmax=amp)
    # # plt.title('Filtered STFT Spectrogram: ' + graph_name)
    # plt.title(graph_name + ' (filtered) Spectrogram')
    # plt.ylabel('Frequency (Hz)')
    # plt.xlabel('Time (seconds)')
    # plt.colorbar()
    #
    # plt.show()

    # Public Data
    fig = plt.figure(frameon=False)
    # fig, ax = plt.subplots(figsize=(1, 1))
    # fig.set_size_inches(1, 1)
    # ax = plt.Axes(fig, [0., 0., 1., 1.])
    # ax.set_axis_off()
    # fig.add_axes(ax)
    plt.pcolormesh(t, f, np.absolute(Zxx)*np.absolute(Zxx), vmin=0, vmax=amp)
    plt.axis('off')
    fig.savefig(file_location[:-2] + '_spec.png', bbox_inches='tight', pad_inches=0)
    plt.close()
    # plt.show()


def main():
    # # Old
    # fs = 500
    # lowcut = 0.5
    # highcut = 50.0
    #
    # svg_file_path = '../ecg-samples/MUSE_20180323_153150_73000.svg'
    #
    # graph_names = ['V1', 'II', 'V5']
    # for graph_name in graph_names:
    #     time_series = unpickle_values(svg_file_path[: -4] + "_" + graph_name + '_y_values.txt')
    #     print(time_series)
    #
    #     new_time_series = butter_bandpass_filter(time_series, lowcut, highcut, fs, order=5)
    #
    #     plt.plot(time_series, '-o', markersize=0.01)
    #     plt.title(graph_name)
    #     plt.show()
    #     plt.title(graph_name + ' (filtered)')
    #     plt.plot(new_time_series, '-o', markersize=0.01)
    #     plt.show()
    #     short_term_fourier_transform(new_time_series, graph_name)

    # Public Data
    fs = 250
    lowcut = 0.5
    highcut = 50.0
    folders_path = 'D:\\cygwin64\\home\\Bang\\wfdb-10.6.0\\afdb\\'

    folders = ['04015', '04043', '04048', '04126', '04746', '04908', '04936', '05091', '05121', '05261', '06426',
               '06453', '06995', '07162', '07859', '07879', '07910', '08215', '08219', '08378', '08405', '08434',
               '08455']

    for folder in folders:
        annotations = unpickle_values(folders_path + folder + '_labels\\' + folder + '_labels.p')
        annotations_count = 0
        for file_name in os.listdir(folders_path + folder + '_time_series\\'):
            if file_name[-3:] == '1.p':
                # print(file_name)
                time_series = unpickle_values(folders_path + folder + '_time_series\\' + file_name)
                # print(annotations[annotations_count])
                annotations_count += 1
                # print(time_series)

                new_time_series = butter_bandpass_filter(time_series, lowcut, highcut, fs, order=5)
                # filter a second time
                new_time_series_reversed = butter_bandpass_filter(np.flip(new_time_series), lowcut, highcut, fs, order=5)

                # plt.figure(figsize=(20, 2))
                # plt.plot(time_series, '-o', markersize=0.01)
                # plt.title('time_series')
                # plt.show()
                # plt.title('time_series (filtered)')
                # plt.plot(new_time_series, '-o', markersize=0.01)
                # plt.show()
                short_term_fourier_transform(new_time_series_reversed, 'time_series', folders_path + 'spectrograms\\' + file_name)
        print(folder, 'done')


if __name__ == "__main__":
    main()
