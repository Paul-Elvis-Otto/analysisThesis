using CSV
using DataFrames
using StatsPlots

function scatter_vc_cc(filepath::String)
  data = CSV.read(filepath, DataFrame)

  p = @df data scatter(
    :view_count,
    :comment_count,
    xlabel="View count",
    ylabel="Comment count",
    legend=false
  )

  display(p)
  return nothing
end

scatter_vc_cc("./data/videos.csv")
