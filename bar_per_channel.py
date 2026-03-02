import pandas as pd
import matplotlib.pyplot as plt
import scienceplots

plt.style.use("science")
plt.rcParams.update(
    {
        "font.family": "serif",  # specify font family here
        "font.serif": ["Computer Modern"],  # specify font here
    }
)  # specify font size here

plt.style.use("science")

df = pd.read_parquet("./data/out/videos.parquet")

# Videos per Channel
channel_counts = df["channel_id"].value_counts().sort_values(ascending=False)
plt.figure(figsize=(3.5, 2.5))
channel_counts.plot(kind="bar")
plt.xlabel("Channel")
plt.ylabel("Total Videos")
plt.xticks([])
plt.tight_layout()
# plt.show()
plt.savefig("plots/bar_videos_per_channel.png", dpi=300)
plt.close()

# Views per Channel
views_per_channel = (
    df.groupby("channel_id")["view_count"].sum().sort_values(ascending=False)
)
plt.figure(figsize=(3.5, 2.5))
plt.style.use("science")
views_per_channel.plot(kind="bar")
plt.xlabel("Channel")
plt.ylabel("Total Views")
plt.xticks([])
plt.tight_layout()
# plt.show()
plt.savefig("plots/bar_views_per_channel.png", dpi=300)
plt.close()
