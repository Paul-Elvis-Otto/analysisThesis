using CSV
using DataFrames
using StatsPlots
using GLM

function plot_view_comments(output_path::String)
    data = CSV.read("./data/videos.csv", DataFrame)

    p = @df data scatter(:view_count, :comment_count, label="Data Points")

    model = lm(@formula(comment_count ~ view_count), data)
    coeftable(model)

    y_hat = predict(model, data)
    plot!(p, data.view_count, y_hat, label="Regression Line", color=:red)

    savefig(p, output_path)
end

plot_view_comments("plots/scatter_view_comments.png")
