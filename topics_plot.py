import json
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401
import pypst

plt.style.use("science")

df = pd.read_parquet("data/out/videos.parquet")

# --- Parse JSON column ---
df = df[df["topic_output"].notna()].copy()

df["topic_label"] = df["topic_output"].apply(json.loads).apply(lambda x: x[0]["label"])


# --- Count topics ---
topic_counts = df["topic_label"].value_counts()

# --- Plot ---
plt.figure()
topic_counts.plot(kind="bar")
plt.xlabel("Topic")
plt.ylabel("Number of Videos")
plt.title("Distribution of Top Topics")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
plt.close()
plt.savefig("plots/bar_topic_distribution.png", dpi=300)
