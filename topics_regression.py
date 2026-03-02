import json
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np

# Load data
df = pd.read_parquet("data/out/videos.parquet")
df["views"] = np.log1p(df["view_count"])


# Parse top-1 topic
def get_top_label(x):
    if pd.isna(x):
        return None
    try:
        return json.loads(x)[0]["label"]
    except:
        return None


df["topic_label"] = df["topic_output"].apply(get_top_label)

# Keep valid rows
df = df[
    df["topic_label"].notna() & df["views"].notna() & df["channel_id"].notna()
].copy()

# Choose baseline topic
baseline = df["topic_label"].value_counts().idxmax()
print("Baseline topic:", baseline)

# Fixed effects regression with clustered SE
formula = f"views ~ C(topic_label, Treatment(reference='{baseline}')) + C(channel_id)"

model = smf.ols(formula, data=df)
results = model.fit(cov_type="cluster", cov_kwds={"groups": df["channel_id"]})

summary_df = results.summary2().tables[1]
summary_df.to_csv("data/out/regression_results.csv")
