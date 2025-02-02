import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def generate_signal(sample_rate, duration):
    """
    Generates a synthetic raw sensor signal composed of:
    - A 5 Hz sine wave
    - A 15 Hz sine wave
    - Random noise
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Combine sine waves + noise
    signal_data = (
        0.8 * np.sin(2 * np.pi * 5 * t)
        + 0.5 * np.sin(2 * np.pi * 15 * t)
        + 0.2 * np.random.randn(len(t))
    )
    return t, signal_data


def apply_notch_filter(signal_data, freq_to_remove, sample_rate, q_factor=30.0):
    """
    Applies a notch filter at freq_to_remove (in Hz) to remove that frequency.
    q_factor controls the sharpness (quality factor) of the notch.
    """
    nyquist_freq = sample_rate / 2.0
    notch_normalized_freq = freq_to_remove / nyquist_freq
    notch_num, notch_den = signal.iirnotch(notch_normalized_freq, q_factor)

    filtered = signal.filtfilt(notch_num, notch_den, signal_data)
    return filtered


def apply_lowpass_filter(signal_data, cutoff_freq, sample_rate, order=4):
    """
    Applies a low-pass Butterworth filter with the given cutoff frequency.
    """
    nyquist_freq = sample_rate / 2.0
    normalized_cutoff = cutoff_freq / nyquist_freq

    lp_num, lp_den = signal.butter(order, normalized_cutoff, btype='low')
    filtered = signal.filtfilt(lp_num, lp_den, signal_data)
    return filtered


def compute_psd(signal_data, sample_rate):
    """
    Computes the power spectral density (PSD) of a real signal using FFT.
    """
    fft_vals = np.fft.fft(signal_data)
    freqs = np.fft.fftfreq(len(signal_data), 1 / sample_rate)

    half_index = len(freqs) // 2
    freqs_pos = freqs[:half_index]
    psd = np.abs(fft_vals[:half_index]) ** 2

    return freqs_pos, psd


def compute_band_powers(freqs, psd, bands):
    """
    Given a list of (low_edge, high_edge) frequency bands,
    compute the total power within each band by summing the PSD.
    """
    band_powers = []
    for (low_edge, high_edge) in bands:
        band_indices = (freqs >= low_edge) & (freqs < high_edge)
        band_power = np.sum(psd[band_indices])
        band_powers.append(band_power)
    return band_powers


def plot_time_domain_separate(t, raw_signal, cleaned_signal):
    """
    Displays the raw and cleaned signals in separate subplots (time domain)
    in a SINGLE figure (window) with two stacked plots.
    """
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    # Plot Raw Signal in the first subplot
    axs[0].plot(t, raw_signal, color='blue')
    axs[0].set_title("Raw Signal (Time Domain)")
    axs[0].set_xlabel("Time (s)")
    axs[0].set_ylabel("Amplitude")

    # Plot Cleaned Signal in the second subplot
    axs[1].plot(t, cleaned_signal, color='red')
    axs[1].set_title("Cleaned Signal (Time Domain)")
    axs[1].set_xlabel("Time (s)")
    axs[1].set_ylabel("Amplitude")

    plt.tight_layout()
    plt.show()


def plot_psd_separate(freqs_raw, psd_raw, freqs_cleaned, psd_cleaned):
    """
    Displays the PSD of the raw and cleaned signals in separate subplots
    in a SINGLE figure (window) with two stacked plots.
    """
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))

    # Raw PSD (top)
    axs[0].semilogy(freqs_raw, psd_raw, color='blue')
    axs[0].set_title("Raw Signal PSD")
    axs[0].set_xlabel("Frequency (Hz)")
    axs[0].set_ylabel("Power (log scale)")

    # Cleaned PSD (bottom)
    axs[1].semilogy(freqs_cleaned, psd_cleaned, color='red')
    axs[1].set_title("Cleaned Signal PSD")
    axs[1].set_xlabel("Frequency (Hz)")
    axs[1].set_ylabel("Power (log scale)")

    plt.tight_layout()
    plt.show()


def plot_band_powers(bands, band_powers_raw, band_powers_cleaned):
    """
    Creates a grouped bar chart comparing the band powers
    of the raw signal vs. the cleaned signal.
    (Third window)
    """
    x_positions = np.arange(len(bands))
    bar_width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar(x_positions - bar_width/2, band_powers_raw,
            width=bar_width, label='Raw', color='skyblue')
    plt.bar(x_positions + bar_width/2, band_powers_cleaned,
            width=bar_width, label='Cleaned', color='salmon')

    band_labels = [f"{b[0]}-{b[1]} Hz" for b in bands]
    plt.xticks(x_positions, band_labels)

    plt.xlabel("Frequency Bands (Hz)")
    plt.ylabel("Power")
    plt.title("Comparison of Band Powers (Raw vs. Cleaned)")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    # 1. Generate a raw sensor signal
    sample_rate = 200  # Hz
    duration = 5.0     # seconds
    t, raw_signal = generate_signal(sample_rate, duration)

    # 2. Apply filters (notch at 15 Hz, then low-pass at 10 Hz)
    filtered_signal_notch = apply_notch_filter(
        raw_signal, freq_to_remove=15, sample_rate=sample_rate, q_factor=30.0
    )
    filtered_signal_low = apply_lowpass_filter(
        filtered_signal_notch, cutoff_freq=10, sample_rate=sample_rate, order=4
    )

    # 3. Time-domain comparison in separate subplots (first window)
    plot_time_domain_separate(t, raw_signal, filtered_signal_low)

    # 4. Compute PSDs
    freqs_raw, psd_raw = compute_psd(raw_signal, sample_rate)
    freqs_cleaned, psd_cleaned = compute_psd(filtered_signal_low, sample_rate)

    # 5. PSD comparison in separate subplots (second window)
    plot_psd_separate(freqs_raw, psd_raw, freqs_cleaned, psd_cleaned)

    # 6. Define 10 frequency bands from 0 to 100 Hz (10 Hz each)
    bands = [(i, i + 10) for i in range(0, 100, 10)]

    # 7. Compute band powers
    band_powers_raw = compute_band_powers(freqs_raw, psd_raw, bands)
    band_powers_cleaned = compute_band_powers(freqs_cleaned, psd_cleaned, bands)

    # Sum of all band powers
    total_power_raw = sum(band_powers_raw)
    total_power_cleaned = sum(band_powers_cleaned)

    # 8. Print band power results
    print("----- Raw Signal Band Powers -----")
    for i, b in enumerate(bands):
        print(f"Band {b[0]}-{b[1]} Hz: {band_powers_raw[i]:.2f}")
    print(f"Total power in all bands (Raw): {total_power_raw:.2f}")

    print("\n----- Cleaned Signal Band Powers -----")
    for i, b in enumerate(bands):
        print(f"Band {b[0]}-{b[1]} Hz: {band_powers_cleaned[i]:.2f}")
    print(f"Total power in all bands (Cleaned): {total_power_cleaned:.2f}")

    # 9. Bar chart of band powers (third window)
    plot_band_powers(bands, band_powers_raw, band_powers_cleaned)


if __name__ == "__main__":
    main()
