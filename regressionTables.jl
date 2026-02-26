using CSV
using DataFrames
using GLM
using RegressionTables

data = CSV.read("./data/videos.csv", DataFrame)

models = [
    lm(@formula(view_count ~ word_count + duration_seconds + like_count), data),
    lm(@formula(comment_count ~ view_count + like_count + word_count), data),
    lm(@formula(like_count ~ view_count + word_count + duration_seconds), data),
]

regtable(models...; render=LatexTable(), file="plots/regression_table.tex")
println("Saved: plots/regression_table.tex")
