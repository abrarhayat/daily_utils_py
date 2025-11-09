# Daily Utils Python Project

This project contains two Streamlit apps:

- `fuel_economy.py`: Compare fuel costs between two vehicles for a given trip.
- `salary_sacrifice.py`: Calculate salary sacrifice savings for work devices in Australia.

## Quickstart

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd daily_utils_py
```

### 2. Create a Conda environment

It is recommended to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

```bash
conda create -n daily_utils_py_env python=3.10 -y
conda activate daily_utils_py_env
```

### 3. Install required libraries

Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit apps

To launch either app:

```bash
streamlit run fuel_economy.py
# or
streamlit run salary_sacrifice.py
```

## Requirements

See `requirements.txt` for all required Python packages.

---

## File Descriptions

- `fuel_economy.py`: Fuel cost comparison tool for two vehicles.
- `salary_sacrifice.py`: Salary sacrifice savings calculator for Australian employees.

## License

MIT License.
