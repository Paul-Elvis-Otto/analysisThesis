# The last row in this table builder is messing up the table
from pandas
import pandas as pd
import pypst

df = pd.read_parquet("./data/out/videos.parquet")

videos_per_channel = (
    df.groupby("channel_title")
    .agg(video_count=("channel_title", "size"), total_views=("view_count", "sum"))
    .reset_index()
)

videos_per_channel = videos_per_channel.sort_values(by='total_views',ascending)

table = pypst.Table.from_dataframe(df=videos_per_channel, include_index=False)
table.stroke = "none"
table.add_hline(1, stroke="1.5pt")
table.add_hline(len(videos_per_channel) + 1, stroke="1.5pt")

figure = pypst.Figure(table, caption='"Videos and views per channel_id"')


with open("./tables/creator_videos.typ", mode="wt") as f:
    content = figure.render().rstrip()
    f.write(content + " <tbl-creator_videos>\n")

videos_per_channel
