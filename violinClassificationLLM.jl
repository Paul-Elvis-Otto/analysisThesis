using Parquet2
using DataFrames
using StatsPlots
using Plots

function model_violin_plot(filepath::String, model::String; plotpath::Union{String,Nothing}=nothing)
    ds = Parquet2.Dataset(filepath)
    data = DataFrame(ds; copycols=false)

    # Filter by model_name
    df = filter(row -> row.model_name == model, data)

    if nrow(df) == 0
        error("No data found for model: $model")
    end

    # Columns to plot
    score_cols = [:anti_elitism, :people_centrism, :volonte_generale, :left_ideology, :right_ideology]

    # Keep only columns that exist and have non-missing data
    available_cols = [c for c in score_cols if c in propertynames(df) && !all(ismissing, df[!, c])]

    if isempty(available_cols)
        error("No valid score columns found for model: $model")
    end

    # Build long-form data
    labels = String[]
    values = Float64[]

    for col in available_cols
        for v in skipmissing(df[!, col])
            push!(labels, string(col))
            push!(values, Float64(v))
        end
    end

    p = violin(labels, values,
        xlabel="Dimension",
        ylabel="Score",
        title="Score Distribution — $model",
        legend=false,
        dpi=300,
        xrotation=20,
        fillalpha=0.6,
        linewidth=1,
    )

    boxplot!(labels, values,
        fillalpha=0.0,
        linewidth=1.5,
        outliers=false,
        legend=false,
    )

    display(p)

    if !isnothing(plotpath)
        savefig(p, plotpath)
        println("Plot saved to: $plotpath")
    end

    return p
end

model_violin_plot("./data/out/videos.parquet", "llama-3b-inst-4bit", plotpath="./plots/violin_llama-3b-inst-4bit.png")

