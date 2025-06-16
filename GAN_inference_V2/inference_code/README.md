
This repository contains scripts and configurations to run a machine learning-based emulator for downscaling CMIP6 GCM outputs using a GAN architecture. It supports historical and future scenarios and is optimized for running on NeSI's Maui and Mahuika HPC platforms.


---

## 📁 Project Structure

```

.
├── log/                          # Job logs
├── src/                          # Source code and utility scripts
├── apply\_emulator\_v3\_mahuika.sl # SLURM job script for Mahuika GPU
├── apply\_emulator\_v3\_maui.sl    # SLURM job script for Maui GPU
├── run\_emulator\_v4.py           # Main GAN-based downscaling script
├── run\_emulator\_v3.py           # (Legacy/alternate) emulator script
├── large\_ensemble.sh            # Batch script to submit multiple runs
├── \*.sh                         # Utility and setup scripts
├── inference\_test\_new\_scheme.ipynb # Jupyter notebook for local testing
└── util\_functions.py            # Helper functions

````

---

## 🧪 Purpose

This project evaluates the skill of a deep learning emulator (specifically a GAN) for downscaling daily CMIP6 climate variables (e.g., `tasmax`, `pr`) to a higher resolution, by comparing its historical and future climate signal performance against regional climate model (RCM) outputs.

---

## 🚀 Running the Emulator on NeSI

### 1. **Prepare Inputs**

Edit the following in `large_ensemble.sh`:
- `gcm`: List of GCMs to downscale.
- `variant`: Realization (e.g., `r1i1p1f1`).
- `ssps`: Scenarios (e.g., `ssp370`, `historical`).
- `variables`: Variables to downscale (e.g., `tasmax`, `pr`).

### 2. **Submit Jobs**
Submit the batch script to SLURM:
```bash
bash large_ensemble.sh
````

This script submits jobs to `apply_emulator_v3_mahuika.sl`, which runs the downscaling using `run_emulator_v4.py`.

---

## 📜 SLURM Job Details

### `apply_emulator_v3_mahuika.sl`

* Configured for Mahuika GPU queue (`niwa_work`)
* Loads necessary modules and environment (`Miniforge3`, `cuDNN`)
* Executes `run_emulator_v4.py` using Python from a specific conda environment

### `run_emulator_v4.py` Arguments:

```bash
python run_emulator_v4.py \
  "GAN" $variable $BASE_PATH $gcm $SCENARIO $variant \
  $output_dir "perfect_emulator" $CODE_DIR
```

* **\$variable**: Climate variable to downscale (`tasmax`, `pr`, etc.)
* **\$BASE\_PATH**: Path to input CMIP6 data
* **\$gcm**, **\$variant**, **\$SCENARIO**: Model configuration
* **\$output\_dir**: Where downscaled outputs are saved
* **"perfect\_emulator"**: Placeholder or mode
* **\$CODE\_DIR**: Path to this repo

---

## ⚙️ Dependencies

Modules loaded on NeSI:

* `Miniforge3` (for Python/conda)
* `cuDNN/8.6.0.163-CUDA-11.8.0`
* `gcc/9.3.0` (if needed)

Ensure the Python environment includes necessary packages (e.g., `tensorflow`, `xarray`, `numpy`).

---

## 📂 Output

Downscaled files are saved to:

```
/nesi/nobackup/niwa00018/ML_Downscaled_CMIP6/
```

Logs are saved in:

```
log/
```

---

## 🧼 Notes

* `.pyc` files and `__pycache__/` directories are ignored.
* Git LFS is recommended for storing large output files separately from the main repo.

---

## 📞 Contacts

For questions, contact:
**Neelesh Rampal** ([rampaln@niwa.co.nz](mailto:rampaln@niwa.co.nz))

