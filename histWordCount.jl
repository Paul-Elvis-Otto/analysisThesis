using CSV
using Plots
using StatsPlots
using DataFrames
using Random

function wc_hist(filepath::String; plotpath::Union{String,Nothing}=nothing, n::Integer=30)
  data = CSV.read(filepath, DataFrame)
  wc = data.word_count
  p = histogram(wc,
    bins=n,
    xlabel="Word count",
    ylabel="Frequency",
    title="Distribution of word_count",
    legend=false,
    dpi=300,
  )
  display(p)
  if !isnothing(plotpath)
    savefig(p, plotpath)
  end
end

wc_hist("./data/videos.csv", plotpath="./plots/hist_wordcount.png")
