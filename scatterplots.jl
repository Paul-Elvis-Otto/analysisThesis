using CSV
using DataFrames
using StatsPlots
using GLM

function scatter_with_regression(
  data::DataFrame,
  var1::Symbol,
  var2::Symbol;
  xlabel::String=String(var1),
  ylabel::String=String(var2),
  title::String="$ylabel vs $xlabel",
  output_dir::String="plots",
  dpi::Int=300
)
  mkpath(output_dir)

  p = @df data scatter(cols(var1), cols(var2),
    label="Data Points",
    xlabel=xlabel,
    ylabel=ylabel,
    title=title,  # ← used here
    dpi=dpi,
    legend=false)

  model = lm(FormulaTerm(term(var2), term(var1)), data)
  y_hat = predict(model, data)

  sorted_idx = sortperm(data[!, var1])
  plot!(p, data[sorted_idx, var1], y_hat[sorted_idx],
    label="Regression Line",
    color=:red,
    linewidth=2
  )

  filename = joinpath(output_dir, "scatter_$(var1)_$(var2).png")
  savefig(p, filename)
  println("Saved: $filename")
end

# --- Load data once ---
data = CSV.read("./data/videos.csv", DataFrame)

# --- Generate all your plots ---
scatter_with_regression(data, :view_count, :comment_count)
scatter_with_regression(data, :view_count, :like_count, ylabel="Likes")
scatter_with_regression(data, :like_count, :comment_count, xlabel="Likes", ylabel="Comments")
scatter_with_regression(data, :word_count, :view_count, xlabel="Likes", ylabel="Word Count")
scatter_with_regression(data, :word_count, :comment_count, xlabel="Likes", ylabel="Word Count")
scatter_with_regression(data, :duration_seconds, :view_count, xlabel="Duration in Seconds", ylabel="View count", title="Duration and Viewcount")
# add more pairs as needed...
