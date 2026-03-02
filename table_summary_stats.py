import pandas as pd
import pypst

df = pd.read_parquet("data/out/videos.parquet")
raw_cols = ["view_count", "like_count", "comment_count"]

summary = df[raw_cols].describe().T
summary.reset_index(inplace=True)
summary.rename(columns={"index": "variable"}, inplace=True)

sci_cols = ["mean", "std", "min", "25%", "50%", "75%", "max"]


def format_value(x):
    if abs(x) >= 1_000_000:
        return f"{x:.2e}"
    return f"{x:.2f}"


summary[sci_cols] = summary[sci_cols].map(format_value)

print(summary)


table = pypst.Table.from_dataframe(summary, include_index=False)
table.stroke = "none"
table.add_hline(1, stroke="1pt")
table.add_hline(len(summary) + 1, stroke="1pt")

figure = pypst.Figure(table, caption='"Summary statistics for key video metrics"')

with open("tables/summary_statistics.typ", "wt") as f:
    content = figure.render().rstrip()
    f.write(content + " <tbl-summary_statistics>\n")
