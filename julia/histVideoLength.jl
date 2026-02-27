using CSV
using Plots
using StatsPlots
using DataFrames
using Random

function duration_hist(filepath::String; plotpath::Union{String,Nothing}=nothing, n::Integer=30)
  data = CSV.read(filepath, DataFrame)

  # Ensure column exists
  duration_seconds = data.duration_seconds

  p = histogram(duration_seconds,
    bins=n,
    xlabel="Duration (seconds)",
    ylabel="Frequency",
    title="Distribution of Video Duration",
    legend=false,
    dpi=300,
  )

  display(p)

  if !isnothing(plotpath)
    savefig(p, plotpath)
  end
end

duration_hist("./data/videos.csv", plotpath="./plots/hist_duration.png")
