using Plots
using CSV
using DataFrames

function plot_top_channels(filepath::String, top_n::Int=20)
  data = CSV.read(filepath, DataFrame)

  counts_df = combine(groupby(data, :channel_id), nrow => :video_count)
  sort!(counts_df, :video_count, rev=true)
  counts_df = first(counts_df, top_n)

  p = bar(
    counts_df.channel_id,
    counts_df.video_count,
    xlabel="Channel ID",
    ylabel="Number of Videos",
    title="Videos per Channel (Top $top_n)",
    legend=false,
    xrotation=45
  )
  display(p)
end

plot_top_channels("./data/videos.csv")
