import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df = pd.read_parquet("./data/out/videos.parquet")

# --- 1. Remove LLM-related columns ---
llm_prefixes = (
    "llama-",
    "mistral-",
    "ministral-",
    "bert_output",
    "duration_",
    "licensed_",
)
video_df = df.loc[:, ~df.columns.str.startswith(llm_prefixes)].copy()

# --- 2. Keep numeric columns only ---
video_numeric = video_df.select_dtypes(include=[np.number]).copy()

# --- 3. Remove constant or empty columns ---
video_numeric = video_numeric.dropna(axis=1, how="all")
video_numeric = video_numeric.loc[:, video_numeric.nunique() > 1]

# --- 4. Compute correlation ---
corr = video_numeric.corr(method="pearson")

# --- 5. Plot FULL heatmap ---
plt.figure(figsize=(12, 10))

sns.heatmap(
    corr,
    cmap="coolwarm",
    center=0,
    square=True,
    linewidths=0.3,
    cbar_kws={"shrink": 0.8},
)

plt.title("Full Correlation Heatmap – Video Metrics Only")
plt.tight_layout()
plt.show()
