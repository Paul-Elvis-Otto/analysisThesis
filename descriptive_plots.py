import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import scienceplots

df = pd.read_parquet("./data/out/videos.parquet")

df["log_view"] = np.log1p(df["view_count"])
df["log_like"] = np.log1p(df["like_count"])
df["log_comment"] = np.log1p(df["comment_count"])

plt.style.use(["science"])  # scienceplots style
os.makedirs("./plots", exist_ok=True)

FIG_WIDTH = 3.5
FIG_HEIGHT = 2.5
DPI = 300


def density_plot(data, xlabel, filename):
    data = data.dropna()
    kde = gaussian_kde(data)

    x_vals = np.linspace(data.min(), data.max(), 1000)
    y_vals = kde(x_vals)

    plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
    plt.plot(x_vals, y_vals)
    plt.xlabel(xlabel)
    plt.ylabel("Density")
    plt.tight_layout()
    plt.savefig(f"./plots/{filename}", dpi=DPI)
    plt.close()


density_plot(df["word_count"], "Word Count", "distribution_word.png")

density_plot(df["log_view"], "Log(View Count + 1)", "distribution_views.png")

density_plot(df["log_comment"], "Log(Comment Count + 1)", "distribution_comment.png")

density_plot(df["log_like"], "Log(Like Count + 1)", "distribution_like.png")

density_plot(df["duration_seconds"], "Duration (seconds)", "distribution_duration.png")
