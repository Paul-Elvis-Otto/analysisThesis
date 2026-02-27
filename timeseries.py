from numba.core.transforms import find_region_inout_vars
from growthrate import total_views
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
import pypst

plt.style.use("science")
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Computer Modern"],
    }
)

df = pd.read_parquet("./data/out/videos.parquet")

df["published_at"] = pd.to_datetime(df["published_at"])
df["year_month"] = df["published_at"].dt.to_period("M")
df["year"] = df["published_at"].dt.year

df = df[df["published_at"] >= "2020-01-01"].copy()
videos_per_month = df.groupby("year_month").size()
views_per_month = df.groupby("year_month")["view_count"].sum()

videos_per_year = df.groupby("year").size()
views_per_year = df.groupby("year")["view_count"].sum()

# videos per year
plt.figure(figsize=(3.5, 2.5))
videos_per_month.plot(kind="line")
plt.xlabel("Month")
plt.ylabel("Uploaded Videos")
# plt.xticks([])
plt.tight_layout()
plt.savefig("plots/timeseries_avg_videos_per_month.png", dpi=300)
plt.close()

plt.figure(figsize=(3.5, 2.5))
videos_per_year.plot(kind="bar")
plt.xticks(rotation=0)  # needs to be in this exact location, will break otherwise
plt.xlabel("Year")
plt.ylabel("Uploaded Videos")
plt.tight_layout()
plt.savefig("plots/timeseries_videos_per_year.png", dpi=300)
plt.close()

# views per year
plt.figure(figsize=(3.5, 2.5))
views_per_month.plot(kind="line")
plt.xlabel("Month")
plt.ylabel("Views")
# plt.xticks([])
plt.tight_layout()
plt.savefig("plots/timeseries_avg_views_per_month.png", dpi=300)
plt.close()


plt.figure(figsize=(3.5, 2.5))
views_per_year.plot(kind="bar")
plt.xticks(rotation=0)  # needs to be in this exact location, will break otherwise
plt.xlabel("Year")
plt.ylabel("Views")
plt.tight_layout()
plt.savefig("plots/timeseries_views_per_year.png", dpi=300)
plt.close()

# summary table

summary_df = (
    pd.concat(
        [
            videos_per_year.rename("Videos"),
            views_per_year.rename("Views"),
        ],
        axis=1,
    )
    .reset_index()
    .rename(columns={"year": "Year"})
    .sort_values("Year")
)

summary_df["Avg Views per Video"] = (summary_df["Views"] / summary_df["Videos"]).round(
    0
)

# Format for presentation
summary_df["Videos"] = summary_df["Videos"].map("{:,}".format)
summary_df["Views"] = summary_df["Views"].map("{:,}".format)
summary_df["Avg Views per Video"] = summary_df["Avg Views per Video"].map("{:,}".format)


table = pypst.Table.from_dataframe(summary_df, include_index=False)
table.stroke = "none"
# table.align = "(x, _) => if calc.odd(x) {left} else {right}"
table.add_hline(1, stroke="1.5pt")
table.add_hline(len(summary_df) + 1, stroke="1.5pt")

figure = pypst.Figure(
    table,
    caption='"Videos, views, and average views per video by year"',
)

with open("./tables/time_summary.typ", mode="wt") as f:
    content = figure.render().rstrip()
    f.write(content + " <tbl-time_summary>\n")
