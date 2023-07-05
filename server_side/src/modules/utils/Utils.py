from src.modules.utils.codec import *
import numpy as np
import matplotlib.pyplot as plt
import io


def plot_subbands(Ytot, M, sample_rate=44100):
    # Create a figure and axes
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5, forward=True)
    subbands = np.transpose(Ytot)
    subbands_freq = np.fft.fft(subbands)

    # Calculate the frequency values for the x-axis
    frequency = np.fft.fftfreq(subbands.shape[1], d=1 / sample_rate)

    color = plt.cm.rainbow(np.linspace(0, 1, M))
    # Plot the magnitude spectrum for each subband
    for i in range(subbands_freq.shape[0]):
        magnitude_spectrum = np.abs(subbands_freq[i])
        ax.plot(frequency.tolist(), magnitude_spectrum.tolist(), label=f"Subband {i + 1}", c=color[i])

    # Add labels and a legend
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.legend(bbox_to_anchor=(1, 1))

    # Encode the plot as a byte array
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='PNG')
    image_stream.seek(0)
    # image_bytes = image_stream.read()
    plt.close()
    return image_stream


def create_analysis_filter_bank(filter: np.ndarray, num_subbands: int) -> np.ndarray:
    H = np.zeros([len(filter), num_subbands], dtype=np.float32)

    for i in range(1, num_subbands + 1):
        n = np.arange(filter.shape[0], dtype=np.int64)
        freq_i = (2 * i - 1) * np.pi / (2.0 * num_subbands)
        phas_i = -(2 * i - 1) * np.pi / 4.0
        tmp = np.cos(freq_i * n + phas_i)
        x = np.multiply(filter, tmp)
        H[:, i - 1] = x

    return H


def create_synthesis_filter_bank(filter: np.ndarray, num_subbands: int) -> np.ndarray:
    H = create_analysis_filter_bank(filter, num_subbands)
    L = len(filter)
    G = np.flip(H, axis=0)
    return G


def frame_sub_analysis(buffer: np.ndarray, H: np.ndarray, num_samples: int) -> np.ndarray:
    L, M = H.shape
    ind = np.zeros([num_samples, L])
    ind[0, :] = np.arange(L)

    for i in range(1, num_samples):
        ind[i, :] += ind[i - 1, :] + M
    ind = ind.astype(np.int64)
    X = buffer[ind]
    Y = np.einsum('ik,kj->ij', X, H)

    return Y


def frame_sub_synthesis(buffer: np.ndarray, G: np.ndarray) -> np.ndarray:
    L, M = G.shape
    N = int(np.ceil(L / M))

    Gr = G.reshape(M, M * N, order='F').copy()
    Z = np.zeros([1152])
    for n in range(buffer.shape[0] - N):
        tmp = buffer[n:n + N, :].T.flatten()
        yr = np.expand_dims(tmp, axis=-1)
        z = np.dot(Gr, yr)
        Z[n * M:(n + 1) * M] = M * np.flip(z[:, 0])
    return Z.T.flatten()


def encode(wav, filter, num_subbands, num_samples):
    # analyzing in the frequency spectrum
    H = create_analysis_filter_bank(filter=filter, num_subbands=num_subbands)

    L, _ = H.shape
    x_buffer_size, y_buffer_size = num_subbands * num_samples, num_samples
    x_buffer = None

    i = 0
    Y_total = np.empty((0, num_subbands))
    # reading MN samples each time until the total number of samples read is <= rows of H
    while (i + 1) * x_buffer_size <= wav.shape[0]:
        if (i + 1) * x_buffer_size + L - num_subbands <= wav.shape[0]:
            x_buffer = wav[i * x_buffer_size: (i + 1) * x_buffer_size + L - num_subbands]
        else:
            # zero padding at the end
            x_buffer = np.r_[wav[i * x_buffer_size: (i + 1) * x_buffer_size], np.zeros(L - num_subbands)]

        # calculating Ytot in case of return
        Y = frame_sub_analysis(buffer=x_buffer, H=H, num_samples=num_samples)
        Y_total = np.r_[Y_total, np.copy(Y)]
        i = i + 1

    return Y_total


def decode(Y_total, filter, num_subbands, num_samples):
    G = create_synthesis_filter_bank(filter, num_subbands)

    L, _ = G.shape
    y_buffer_size = num_samples
    y_buffer = None
    x_hat = None

    i = 0
    Y_h_total = np.empty((0, num_subbands))

    # reading N samples until number of samples read <= number of rows of Ytot
    while (i + 1) * y_buffer_size <= Y_total.shape[0]:
        # extracting row
        Yc = Y_total[i * y_buffer_size:(i + 1) * y_buffer_size, :]

        Y_h_total = np.r_[Y_h_total, np.copy(Yc)]

        i = i + 1

    i = 0
    x_hat = np.empty(0)
    while (i + 1) * y_buffer_size <= Y_total.shape[0]:
        if (i + 1) * y_buffer_size + L // num_subbands <= Y_total.shape[0]:
            # extracting rows
            y_buffer = Y_h_total[i * y_buffer_size:(i + 1) * y_buffer_size + L // num_subbands, :]
        else:
            # zero padding
            y_buffer = np.r_[
                Y_h_total[i * y_buffer_size:(i + 1) * y_buffer_size, :], np.zeros((L // num_subbands, num_subbands))]
        xsynth = frame_sub_synthesis(y_buffer, G)
        x_hat = np.r_[x_hat, xsynth]
        i = i + 1

    return x_hat


def compress_mp3(wav, filer, num_subbands, num_samples):
    return MP3codec(wav, filer, num_subbands, num_samples)


def calculate_compression_data(wav, total_stream, fs, bits_per_sample = 16):
    # calculating input and output data rates
    input_data_rate = fs * bits_per_sample
    output_data_rate = len(total_stream) / (len(wav) / fs)

    # calculating compression rate
    compression_rate = input_data_rate / output_data_rate
    return input_data_rate, output_data_rate, compression_rate
