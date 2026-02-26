# List available recipes
default:
    @just --list

# Run all plot generation scripts
plots: scatterplots barplots histograms

# Run scatterplots.jl
scatterplots:
    julia --project=. scatterplots.jl

# Generate Histograms
histograms:
    julia --project=. histWordCount.jl

# Run regression tables
regressions: run_regressions convert_tables

# Genereate barplots
barplots:
    julia --project=. channelVideos.jl

run_regressions:
    julia --project=. regressionTables.jl

# Convert all .tex tables to typst
convert_tables:
    for f in tables/*.tex; do t2l "$f" -o "${f%.tex}.typ"; done

# Run a single plot script by name: just plot scatterplots.jl
plot script:
    julia --project=. {{ script }}
