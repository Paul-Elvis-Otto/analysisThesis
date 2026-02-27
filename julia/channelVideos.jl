using CSV, DataFrames, Plots

df = CSV.read("./data/videos.csv", DataFrame)

counts = combine(groupby(df, :channel_id), nrow => :n)
sort!(counts, :n, rev=true)

p = bar(string.(counts.channel_id),
  counts.n,
  legend=false,
  title="Videos per Channel",
  ylabel="n videos",
  xlabel="",
  xticks=false,
  dpi=300)
savefig(p, "plots/bar_videos_per_channel.png")
