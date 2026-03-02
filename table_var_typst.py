import pandas as pd

df = pd.read_parquet("data/out/videos.parquet")
variable_list = df.columns.tolist()

stats = {
    "n_variables": len(variable_list),
    "n_observations": len(df),
}

pd.DataFrame(stats.items(), columns=["key", "value"]).to_csv(
    "./tables/stats.csv", index=False
)
