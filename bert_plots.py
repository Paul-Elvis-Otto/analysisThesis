# TODO: Fix the design
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import ast
import scienceplots

plt.style.use("science")

BERT_DIMS = ["anti_elitism", "people_centrism", "left_ideology", "right_ideology"]


def bert_violin_plot(filepath: str, plotpath: str = None):
    df = pd.read_parquet(filepath)

    def parse_tensor(val):
        if pd.isna(val):
            return None
        try:
            return ast.literal_eval(str(val))
        except:
            return None

    parsed = df["bert_output"].apply(parse_tensor).dropna()
    arr = np.array(parsed.tolist())  # shape (n, 4)

    records = []
    for i, dim in enumerate(BERT_DIMS):
        for val in arr[:, i]:
            records.append({"dimension": dim.replace("_", " "), "score": val})

    long_df = pd.DataFrame(records)

    # plt.style.use("ggplot")
    # mpl.rcParams.update(
    #     {
    #         "font.family": "sans-serif",
    #         "axes.facecolor": "#EBEBEB",
    #         "figure.facecolor": "white",
    #         "axes.grid": True,
    #         "grid.color": "white",
    #         "grid.linewidth": 1.2,
    #         "axes.edgecolor": "#EBEBEB",
    #         "axes.labelcolor": "#333333",
    #         "xtick.color": "#333333",
    #         "ytick.color": "#333333",
    #         "text.color": "#333333",
    #     }
    # )
    #
    # ggplot_palette = ["#F8766D", "#A3A500", "#00B0F6", "#E76BF3"]

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.violinplot(
        data=long_df,
        x="dimension",
        y="score",
        ax=ax,
        inner="box",
        hue="dimension",
        # palette=ggplot_palette,
        legend=False,
        linewidth=0.8,
    )

    # ax.set_title("PopBERT Score Distribution", fontsize=15, fontweight="bold", pad=12)
    # ax.set_xlabel("", fontsize=11)
    # ax.set_ylabel("Score", fontsize=11)
    # ax.tick_params(axis="x", rotation=20)

    plt.tight_layout()

    if plotpath:
        plt.savefig(plotpath, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {plotpath}")

    plt.show()


bert_violin_plot("./data/out/videos.parquet", plotpath="./plots/violin_bert.png")
