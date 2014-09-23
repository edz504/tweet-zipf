library(ggmap)

cities.df <- read.csv(file='cities.csv', header=TRUE)

theme_set(theme_bw(16))

# ggsave(file="map.pdf", width=8, height=4.5)
us.map <- qmap("united states", zoom = 4)

us.map + geom_point(data=cities.df, aes(x = lng, y=lat), size=5)