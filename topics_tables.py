import json
from pathlib import Path

import pandas as pd
import pypst


def build_topic_table(
    df: pd.DataFrame,
    caption: str,
    label: str,
    output_path: str,
) -> pd.DataFrame:
    """
    Subset df, extract topic labels, build a summary table with counts and
    percentages, render it as a Typst figure, and write it to *output_path*.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe containing a 'topic_output' column with JSON strings.
    caption : str
        Caption shown below the table.
    label : str
        Typst label (without angle brackets).
    output_path : str
        Path to the output .typ file.

    Returns
    -------
    pd.DataFrame
        The topic summary dataframe (Topic, Count, Percentage).
    """
    # --- Subset & extract ---
    df = df[df["topic_output"].notna()].copy()
    df["topic_label"] = (
        df["topic_output"].apply(json.loads).apply(lambda x: x[0]["label"])
    )

    # --- Summarise ---
    counts = df["topic_label"].value_counts().reset_index()
    counts.columns = ["Topic", "Count"]
    counts["Percentage"] = (counts["Count"] / counts["Count"].sum() * 100).round(1)
    counts["Percentage"] = counts["Percentage"].astype(str) + " %"

    # --- Render Typst table ---
    table = pypst.Table.from_dataframe(counts, include_index=False)
    table.stroke = "none"
    table.add_hline(1, stroke="1pt")
    table.add_hline(len(counts) + 1, stroke="1pt")

    figure = pypst.Figure(table, caption=f'"{caption}"')

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wt") as f:
        content = figure.render().rstrip()
        f.write(content + f" <{label}>\n")

    return counts


if __name__ == "__main__":
    df = pd.read_parquet("data/out/videos.parquet")

    summary = build_topic_table(
        df,
        caption="Distribution of video topics.",
        label="tbl-topics",
        output_path="tables/topic_distribution.typ",
    )

    print(Path("tables/topic_distribution.typ").read_text())
