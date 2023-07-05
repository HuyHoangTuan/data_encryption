import numpy as np
import matplotlib.pyplot as plt
import io

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

def encode(wav, filter, num_subbands, num_samples):

    # analyzing in the frequency spectrum
    H = create_analysis_filter_bank(filter=filter, num_subbands=num_subbands)

    L,_ = H.shape
    x_buffer_size, y_buffer_size = num_subbands * num_samples, num_samples
    x_buffer = None
    
    i = 0
    Y_total = np.empty( ( 0, num_subbands ) )
    # reading MN samples each time until the total number of samples read is <= rows of H
    while (i+1) * x_buffer_size <= wav.shape[0]:
        if (i+1) * x_buffer_size + L - num_subbands <= wav.shape[0]:
            x_buffer = wav[i * x_buffer_size: (i+1) * x_buffer_size + L - num_subbands]
        else:
            # zero padding at the end
            x_buffer = np.r_[ wav[i*x_buffer_size: (i+1)*x_buffer_size],np.zeros(L-num_subbands)]

        # calculating Ytot in case of return
        Y = frame_sub_analysis(buffer= x_buffer, H= H, num_samples= num_samples)
        Y_total = np.r_[Y_total, np.copy(Y)]
        i = i + 1
    
    return Y_total



def plot_subbands(Ytot, M, sample_rate=44100):
    # Create a figure and axes
    fig, ax = plt.subplots()
    fig.set_size_inches(18.5, 10.5, forward=True)
    subbands = np.transpose(Ytot)
    subbands_freq = np.fft.fft(subbands)

    # Calculate the frequency values for the x-axis
    frequency = np.fft.fftfreq(subbands.shape[1], d=1/sample_rate)

    color = plt.cm.rainbow(np.linspace(0, 1, M))
    # Plot the magnitude spectrum for each subband
    for i in range(subbands_freq.shape[0]):
        magnitude_spectrum = np.abs(subbands_freq[i])
        ax.plot(frequency.tolist(), magnitude_spectrum.tolist(), label=f"Subband {i+1}", c = color[i])

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