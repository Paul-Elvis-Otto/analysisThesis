import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401

plt.style.use("science")
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Computer Modern"],
    }
)

df = pd.read_parquet("./data/out/videos.parquet")

df["published_at"] = pd.to_datetime(df["published_at"])
df["year"] = df["published_at"].dt.year

df = df[df["published_at"] >= "2020-01-01"].copy()

channel_views = (
    df.groupby(["channel_id", "year"])["view_count"].sum().unstack(fill_value=0)
)
years = sorted(channel_views.columns)
first_year, last_year = years[0], years[-1]

channel_views["total_views"] = channel_views.sum(axis=1)
channel_views["first_year_views"] = channel_views[first_year]
channel_views["last_year_views"] = channel_views[last_year]
channel_views["growth_rate"] = (
    (channel_views["last_year_views"] - channel_views["first_year_views"])
    / channel_views["first_year_views"].replace(0, np.nan)
    * 100
)

channel_videos = df.groupby(["channel_id", "year"]).size().unstack(fill_value=0)
channel_videos["total_videos"] = channel_videos.sum(axis=1)
channel_videos["first_year_videos"] = channel_videos[first_year]
channel_videos["last_year_videos"] = channel_videos[last_year]
channel_videos["video_growth_rate"] = (
    (channel_videos["last_year_videos"] - channel_videos["first_year_videos"])
    / channel_videos["first_year_videos"].replace(0, np.nan)
    * 100
)

total_views = channel_views["total_views"].sum()
top_10_views = (
    channel_views["total_views"].nlargest(int(len(channel_views) * 0.1)).sum()
)
top_20_views = (
    channel_views["total_views"].nlargest(int(len(channel_views) * 0.2)).sum()
)
top_50_views = (
    channel_views["total_views"].nlargest(int(len(channel_views) * 0.5)).sum()
)

channel_views["quartile"] = pd.qcut(
    channel_views["total_views"],
    q=4,
    labels=["Q1 (smallest)", "Q2", "Q3", "Q4 (largest)"],
)

channel_videos["quartile"] = channel_views["quartile"]

quartile_growth = channel_views.groupby("quartile")["growth_rate"].agg(
    ["mean", "median", "count"]
)

print("=" * 60)
print("GROWTH ANALYSIS: Is growth driven by few channels or general?")
print("=" * 60)

print("\n--- 1. CONCENTRATION RATIOS ---")
print(f"Total views: {total_views:,}")
print(f"Top 10% of channels hold: {top_10_views / total_views * 100:.1f}% of views")
print(f"Top 20% of channels hold: {top_20_views / total_views * 100:.1f}% of views")
print(f"Top 50% of channels hold: {top_50_views / total_views * 100:.1f}% of views")

print("\n--- 2. CHANNEL GROWTH STATISTICS ---")
valid_growth = channel_views["growth_rate"].dropna()
print(f"Number of channels: {len(channel_views)}")
print(
    f"Channels with positive growth: {(valid_growth > 0).sum()} ({(valid_growth > 0).mean() * 100:.1f}%)"
)
print(
    f"Channels with negative growth: {(valid_growth < 0).sum()} ({(valid_growth < 0).mean() * 100:.1f}%)"
)
print(f"Mean growth rate: {valid_growth.mean():.1f}%")
print(f"Median growth rate: {valid_growth.median():.1f}%")
print(f"Std dev: {valid_growth.std():.1f}%")

print("\n--- 3. GROWTH BY CHANNEL SIZE (QUARTILES) ---")
print(quartile_growth.to_string())

print("\n--- 4. YEARLY VIEW COUNTS BY QUARTILE ---")
quartile_by_year = df.merge(
    channel_views[["quartile"]], left_on="channel_id", right_index=True
)
quartile_views = (
    quartile_by_year.groupby(["year", "quartile"])["view_count"].sum().unstack()
)
print(quartile_views.to_string())

quartile_views_pct = quartile_views.div(quartile_views.sum(axis=1), axis=0) * 100
print("\n--- 5. VIEW SHARE BY QUARTILE (%) ---")
print(quartile_views_pct.round(1).to_string())

plt.figure(figsize=(3.5, 2.5))
quartile_views_pct.plot(kind="area", stacked=True, alpha=0.8)
plt.xlabel("Year")
plt.ylabel("Share of Views (%)")
plt.legend(title="Quartile", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("plots/growthrate_quartile_share.png", dpi=300)
plt.close()

print("\n--- 6. VIDEO GROWTH BY CHANNEL SIZE ---")
valid_video_growth = channel_videos["video_growth_rate"].dropna()
print(f"Mean video upload growth: {valid_video_growth.mean():.1f}%")
print(f"Median video upload growth: {valid_video_growth.median():.1f}%")

quartile_video_growth = channel_videos.groupby("quartile")["video_growth_rate"].agg(
    ["mean", "median"]
)
print("\nVideo growth by quartile:")
print(quartile_video_growth.to_string())
