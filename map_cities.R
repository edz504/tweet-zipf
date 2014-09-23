library(ggmap)
library(dplyr)

cities.df <- read.csv(file='cities.csv', header=TRUE)
# fix the negative sign
cities.df <- cities.df %>% mutate(lon=-lng)

theme_set(theme_bw(16))

# ggsave(file="map.pdf", width=8, height=4.5)
us.map <- qmap("united states", zoom = 4)

REG_SIZE <- 5
sq.mi <- scale(cities.df$sq_mi)

# color by lexicographical diversity
us.map + geom_point(data=cities.df, aes(x = lon, y=lat, colour=lex_div),
    size= REG_SIZE + sq.mi)

# color by zipfian fit