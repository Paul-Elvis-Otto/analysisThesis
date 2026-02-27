library(arrow)
library(ggplot2)

df <- read_parquet("./data/out/videos.parquet")

df
colnames(df)

lm(formula = view_count ~ like_count, data = df)

ggplot(df, aes(x = like_count, y = view_count)) +
  geom_point(alpha = 0.3) + # alpha helps see density if you have many videos
  geom_smooth(method = "lm") # this adds the regression line from your formula

plot(df$like_count, df$view_count)
plot(df$like_count, df$comment_count, log = "xy")

# Use log scales and better styling
plot(
  df$like_count,
  df$view_count,
  log = "xy", # Logarithmic scales for both axes
  pch = 16, # Solid circles instead of open ones
  col = rgb(0, 0, 0, 0.2), # Transparent black to see density
  main = "Views vs Likes",
  xlab = "Like Count (Log)",
  ylab = "View Count (Log)"
)

# Note: abline() won't work directly on log-log plots easily,
# but the plot above will show you the trend clearly.
