import pandas as pd
import numpy as np
import pypst

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
    labels=["Q1", "Q2", "Q3", "Q4"],
)

channel_videos["quartile"] = channel_views["quartile"]

valid_growth = channel_views["growth_rate"].dropna()
valid_video_growth = channel_videos["video_growth_rate"].dropna()

quartile_growth = channel_views.groupby("quartile")["growth_rate"].agg(
    ["mean", "median", "count"]
)
quartile_video_growth = channel_videos.groupby("quartile")["video_growth_rate"].agg(
    ["mean", "median"]
)

concentration_df = pd.DataFrame(
    {
        "Metric": [
            "Total Views",
            "Top 10% Channels",
            "Top 20% Channels",
            "Top 50% Channels",
        ],
        "Value": [
            f"{total_views:,.0f}",
            f"{top_10_views / total_views * 100:.1f}%",
            f"{top_20_views / total_views * 100:.1f}%",
            f"{top_50_views / total_views * 100:.1f}%",
        ],
    }
).set_index("Metric")

growth_stats_df = pd.DataFrame(
    {
        "Metric": [
            "Channels (N)",
            "Positive Growth",
            "Negative Growth",
            "Mean Growth",
            "Median Growth",
            "Std Dev",
        ],
        "Value": [
            f"{len(channel_views)}",
            f"{(valid_growth > 0).sum()} ({(valid_growth > 0).mean() * 100:.1f}%)",
            f"{(valid_growth < 0).sum()} ({(valid_growth < 0).mean() * 100:.1f}%)",
            f"{valid_growth.mean():.1f}%",
            f"{valid_growth.median():.1f}%",
            f"{valid_growth.std():.1f}%",
        ],
    }
).set_index("Metric")

quartile_combined = pd.concat([quartile_growth, quartile_video_growth], axis=1)
quartile_combined.columns = [
    "Mean Growth (%)",
    "Median Growth (%)",
    "N",
    "Video Mean (%)",
    "Video Median (%)",
]
quartile_combined = quartile_combined.round(1)

table1 = pypst.Table.from_dataframe(concentration_df)
table1.stroke = "none"
table1.add_hline(1, stroke="1pt")
table1.add_hline(len(concentration_df) + 1, stroke="1pt")

table2 = pypst.Table.from_dataframe(growth_stats_df)
table2.stroke = "none"
table2.add_hline(1, stroke="1pt")
table2.add_hline(len(growth_stats_df) + 1, stroke="1pt")

table3 = pypst.Table.from_dataframe(quartile_combined)
table3.stroke = "none"
table3.add_hline(1, stroke="1pt")
table3.add_hline(len(quartile_combined) + 1, stroke="1pt")

fig1 = pypst.Figure(
    table1,
    caption=f'"Concentration of views (analysis period: {first_year}–{last_year})"',
)
with open("tables/growth_concentration.typ", mode="wt") as f:
    content = fig1.render().rstrip()
    f.write(content + " <tbl-growth_concentration>\n")

fig2 = pypst.Figure(table2, caption='"Channel growth statistics"')
with open("tables/growth_statistics.typ", mode="wt") as f:
    content = fig2.render().rstrip()
    f.write(content + " <tbl-growth_statistics>\n")

fig3 = pypst.Figure(table3, caption='"Growth by channel size (quartiles)"')
with open("tables/growth_quartile.typ", mode="wt") as f:
    content = fig3.render().rstrip()
    f.write(content + " <tbl-growth_quartile>\n")

print("Tables saved to tables/")
