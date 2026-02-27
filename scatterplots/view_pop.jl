using CSV
using Plots
using DataFrames
using Distributions
using StatsPlots
using KernelDensity


function plot_view_distribution(filepath::String)
  data = CSV.read(filepath, DataFrame)
  views = data.view_count
  p = histogram(views,
    xlabel="Views",
    ylabel="Frequency",
    title="Distribution of Video Views",
    legend=false
  )
  display(p)
end

function plot_view_dist_kde_fit(filepath::String)
  data = CSV.read(filepath, DataFrame)
  views = Float64.(filter(x -> x > 0, data.view_count))
  log_views = log10.(views)

  fitted = fit(LogNormal, views)
  println("Fitted: μ=", fitted.μ, " σ=", fitted.σ)

  p = histogram(log_views,
    normalize=:pdf,
    xlabel="Views (log₁₀ scale)",
    ylabel="Density",
    title="Video View Distribution",
    label="Empirical",
    fillalpha=0.4
  )

  x_range = range(minimum(log_views), maximum(log_views), length=500)
  # Jacobian correction to convert LogNormal pdf to log10 space
  y_vals = pdf.(fitted, 10 .^ x_range) .* (10 .^ x_range) .* log(10)

  plot!(p, x_range, y_vals,
    label="Fitted LogNormal",
    linewidth=2,
    color=:red
  )

  display(p)
end
plot_view_distribution("./data/videos.csv")
plot_view_dist_kde_fit("./data/videos.csv")
