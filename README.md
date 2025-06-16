# Downscaling-with-AI-reveals-large-role-of-internal-variability-in-fine-scale-projections-of-climate-extremes

## Supporting Repository for Manuscript

This repository contains information and code that supports the manuscript:  
**"Downscaling with AI reveals large role of internal variability in fine-scale projections of climate extremes"**, which is currently under review.

> **Note:** This repository does **not** include code for training the machine learning models. It focuses on **model inference** and generating a **large ensemble of climate projections**.

### Related Code Repositories

For the training code and additional information, please refer to the following repositories:

- [On-the-Extrapolation-of-Generative-Adversarial-Networks-for-downscaling-precipitation-extremes](https://github.com/nram812/On-the-Extrapolation-of-Generative-Adversarial-Networks-for-downscaling-precipitation-extremes)  
- [A-Robust-Generative-Adversarial-Network-Approach-for-Climate-Downscaling](https://github.com/nram812/A-Robust-Generative-Adversarial-Network-Approach-for-Climate-Downscaling)

### Associated Publications

- Rampal, N., Gibson, P. B., Sherwood, S., Abramowitz, G., & Hobeichi, S. (2025).  
  *A reliable generative adversarial network approach for climate downscaling and weather generation.*  
  *Journal of Advances in Modeling Earth Systems, 17(1), e2024MS004668.*

- Rampal, N., Gibson, P. B., Sherwood, S., & Abramowitz, G. (2024).  
  *On the extrapolation of generative adversarial networks for downscaling precipitation extremes in warmer climates.*  
  *Geophysical Research Letters, 51(23), e2024GL112492.*
  

## Manuscript Data and Figure Reproduction Instructions

The manuscript is based on over **15,000 years of 12km simulations over New Zealand**, generated using 20 CMIP6 GCMs, 4 SSPs, and 2 SMILES. These simulations are not publicly available as a dataset but can be shared upon request by contacting:  
📧 **Neelesh.Rampal@niwa.co.nz**

Instead, this repository provides **notebooks to reproduce the figures** in the manuscript (Figures 1–4 and several supplementary figures).

---

### Step-by-Step Instructions

#### (a) Downloading the CMIP6 Dataset

You must first download the **daily-averaged variables**:  
`u`, `v`, `q`, `t` for **20 GCMs × 4 SSPs × 2 SMILES**.  
> 🔹 Approximate data volume: **~30 TB globally**, but **< 500 GB** when subset to the New Zealand region.

- Data can be obtained via the [ESGF portal](https://esgf-node.ipsl.upmc.fr/search/cmip6-ipsl/), which provides `wget` scripts.
- A helper script to automate and parallelize downloads is provided here (including the WGET files are here):  
  `./GAN_inference/CMIP6_download_and_preprocessing/Download_CMIP6`

---

#### (b) Subsetting and Interpolation over New Zealand

Once downloaded, the data must be:
1. **Subset to the New Zealand region**
2. **Interpolated to the required grid resolution**

Scripts for subsetting and interpolation can be found in:
- `./GAN_inference/CMIP6_download_and_preprocessing/SUBSET`
- `./GAN_inference/CMIP6_download_and_preprocessing/Subset_CMIP6`

These scripts process raw CMIP6 files and prepare them for use with the emulator.

---

#### (c) Running Inference with the GAN Emulator

The trained models and inference scripts are located in:  
- `./GAN_inference/inference_code`

A `README` is included in this folder to guide you through running the inference on the preprocessed CMIP6 data.

---

#### (d) Generating Manuscript Figures

Once inference is complete, outputs can be used to generate manuscript figures.

Refer to the `./Figures` directory for:
- Plotting scripts
- Instructions on reproducing **Figures 1–4** and **Supplementary Figures**

---

If you encounter any issues or need the simulation data directly, please reach out.


