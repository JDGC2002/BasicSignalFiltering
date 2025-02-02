# 🚀 Signal Processing and Spectral Analysis 📊

This repository contains a Python program designed to process raw sensor signals and perform comprehensive spectral analysis. The program is capable of:

## ✨ Features

1. **🔍 Signal Filtering:** 
   - Applies multiple types of filters, including:
     - 🎯 **Notch Filter:** Removes specific frequencies to mitigate noise.
     - 🧹 **Low-Pass Filter:** Eliminates high-frequency components above a defined threshold.
   - The filters can be applied individually or combined for more robust signal cleaning.

2. **📈 Spectral Density Analysis:**
   - Computes the **Power Spectral Density (PSD)** of both raw and filtered signals, providing insights into the signal's frequency components. ⚡
   - **🎯 Band-Specific Spectral Density:** Analyzes power across up to 10 frequency bands (e.g., 0–10 Hz, 10–20 Hz, ..., 90–100 Hz) for detailed spectral segmentation.

3. **🖼️ Visualization:**
   - **⏱️ Time-Domain Plots:** Displays raw and filtered signals side by side for easy comparison.
   - **🌐 Frequency-Domain Analysis:** Graphs the PSD for both raw and cleaned signals, with log-scaled power representation.
   - **📊 Bar Charts:** Compares band power across different frequency bands before and after filtering.

## ⚙️ How It Works

- **🧪 Signal Generation:** Simulates a synthetic signal combining sine waves and random noise, mimicking real-world sensor data.
- **🧰 Filtering Process:** Sequentially applies notch and low-pass filters to clean the data.
- **🔬 Spectral Analysis:** Utilizes Fast Fourier Transform (FFT) to calculate the PSD and determine power distribution across frequency bands.
- **👀 Results Visualization:** Uses `matplotlib` for clear graphical representations of the processed data.

## 📦 Requirements

- 🐍 Python 3.x
- 📊 NumPy
- 🔢 SciPy
- 📉 Matplotlib

Install the required packages using:
```bash
pip install numpy scipy matplotlib
