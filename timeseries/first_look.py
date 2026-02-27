import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scienceplots


plt.style.use("science")

df = pd.read_parquet("./data/out/videos.parquet")

df["published_at"] = pd.to_datetime(df["published_at"], utc=True).dt.tz_convert(None)

df = df.dropna(subset=["published_at"])
df = df.sort_values("published_at")

df = df[df["published_at"] >= "2022-01-01"].copy()

df["sentiment"] = df["sentiment"].astype("string").str.strip().str.lower()

df["sentiment_index"] = df["sentiment_positive_prob"] - df["sentiment_negative_prob"]

df["sentiment_index"].describe()  # should be [-1,1]

monthly = (
    df.groupby(pd.Grouper(key="published_at", freq="ME"))
    .agg(
        n_videos=("id", "count"),
        avg_sentiment=("sentiment_index", "mean"),
        share_negative=("sentiment", lambda x: (x == "negative").mean()),
        share_positive=("sentiment", lambda x: (x == "positive").mean()),
        avg_views=("view_count", "mean"),
        avg_comments=("comment_count", "mean"),
        avg_anti_elitism=("llama-3b-inst-4bit_full_anti_elitism", "mean"),
    )
    .reset_index()
)

monthly["sentiment_roll3"] = monthly["avg_sentiment"].rolling(3).mean()
monthly["anti_elitism_roll3"] = monthly["avg_anti_elitism"].rolling(3).mean()
monthly["views_roll3"] = monthly["avg_views"].rolling(3).mean()

# Number of videos per month
plt.figure()
plt.plot(monthly["published_at"], monthly["n_videos"])
plt.xlabel("Month")
plt.ylabel("Count")
plt.tight_layout()
plt.show()
plt.savefig("./plots/line_avg_month_videos.png", dpi=300)

# Create two subplots side by side
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

# Left plot: Avg uploaded videos
ax1.plot(monthly["published_at"], monthly["n_videos"])
ax1.set_xlabel("Month")
ax1.set_ylabel("Avg Uploaded Videos")
ax1.tick_params(axis="x", rotation=45)

# Right plot: Avg views
ax2.plot(monthly["published_at"], monthly["avg_views"])
ax2.set_xlabel("Month")
ax2.set_ylabel("Avg Views per Month")
ax2.tick_params(axis="x", rotation=45)

fig.tight_layout()
plt.savefig("./plots/line_avg_month_videos_view", dpi=300)
plt.show()

plt.figure()
plt.plot(monthly["published_at"], monthly["avg_sentiment"])
plt.plot(monthly["published_at"], monthly["sentiment_roll3"])
plt.title("Sentiment Over Time (Pos − Neg)")
plt.xlabel("Month")
plt.ylabel("Mean Sentiment Index")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(monthly["published_at"], monthly["share_negative"])
plt.title("Share of Negative Videos")
plt.xlabel("Month")
plt.ylabel("Share")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(monthly["published_at"], monthly["avg_anti_elitism"])
plt.plot(monthly["published_at"], monthly["anti_elitism_roll3"])
plt.title("Anti-Elitism Over Time")
plt.xlabel("Month")
plt.ylabel("Mean Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

monthly["avg_log_views"] = np.log1p(monthly["avg_views"])

plt.figure()
plt.plot(monthly["published_at"], monthly["avg_log_views"])
plt.plot(monthly["published_at"], monthly["views_roll3"].apply(np.log1p))
plt.title("Average Views (Log Scale)")
plt.xlabel("Month")
plt.ylabel("log(Mean Views)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

monthly.loc[:, ["avg_sentiment", "avg_anti_elitism"]].corr()
