import pandas as pd
import pypst


df = pd.read_parquet("./data/out/videos.parquet")

variables = df.columns.to_frame(name="Variable")
variables["Description"] = ""
variables["Values"] = ""


table = pypst.Table.from_dataframe(variables, include_index=False)  # ty:ignore[possibly-missing-attribute]
table.stroke = "none"
# table.align = "(x, _) => if calc.odd(x) {left} else {right}"
table.add_hline(1, stroke="1.5pt")
table.add_hline(len(variables) + 1, stroke="1.5pt")

figure = pypst.Figure(
    table,  # ty:ignore[invalid-argument-type]
    caption='"List of all variables in the Dataset"',
)

with open("./tables/list_variables.typ", mode="wt") as f:
    content = figure.render().rstrip()
    f.write(content + " <tbl-listofvars>\n")
