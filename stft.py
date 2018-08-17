import pickle
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter
from scipy.signal import freqz


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
    with open(file_path + "_x_values.txt", "rb") as fp:
        x_values = pickle.load(fp)
    with open(file_path + "_y_values.txt", "rb") as fp:
        y_values = pickle.load(fp)

    return x_values, y_values


def short_term_fourier_transform(time_series, graph_name):
    fs = 500
    # amp = 2 * np.sqrt(2)
    amp = 2
    window = signal.hamming(512)

    print("time_series len", len(time_series))

    f, t, Zxx = signal.stft(np.array(time_series), fs, nperseg=512, window=window, noverlap=511)

    plt.pcolormesh(t, f, np.absolute(Zxx)*np.absolute(Zxx), vmin=0, vmax=amp)
    plt.title('Filtered STFT Spectrogram: ' + graph_name)
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (seconds)')
    plt.colorbar()

    plt.show()


def main():
    fs = 500
    lowcut = 0.5
    highcut = 50.0

    svg_file_path = '../ecg-samples/MUSE_20180323_153150_73000.svg'

    graph_names = ['V1', 'II', 'V5']
    for graph_name in graph_names:
        x_values, time_series = unpickle_values(svg_file_path[: -4] + "_" + graph_name)
        # print(x_values)
        # print(y_values)

        new_time_series = butter_bandpass_filter(time_series, lowcut, highcut, fs, order=5)

        plt.plot(x_values, time_series, '-o', markersize=0.01)
        plt.show()
        plt.plot(x_values, new_time_series, '-o', markersize=0.01)
        plt.show()
        short_term_fourier_transform(new_time_series, graph_name)


if __name__ == "__main__":
    main()