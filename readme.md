## Setup

**For this project (M1/M2 Mac with miniforge):**

```bash
conda create -n anti-brainrot python=3.11
conda activate anti-brainrot
pip install -r requirements.txt
```

**Alternative (pip + venv on Intel Mac):**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Note:** This project uses miniforge on M1/M2 Macs because conda handles ARM-compatible package binaries better than pip alone.