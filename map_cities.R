library(ggmap)
library(dplyr)

cities.df <- read.csv(file='cities.csv', header=TRUE)
# # fix the negative sign
# cities.df <- cities.df %>% mutate(lon=-lng)


# ggsave(file="map.pdf", width=8, height=4.5)
us.map <- qmap("united states", zoom = 4, color='bw')

REG_SIZE <- 5
sq.mi <- scale(cities.df$sq_mi)

# color by lexical richness
us.map + geom_point(data=cities.df, 
    aes(x = lng, y=lat, colour=lex_div),
    size= REG_SIZE + sq.mi) + 
    scale_colour_gradient(low="#16a085", high="#f39c12")
ggsave(file="lex.png", width=8, height=4.5)

# color by zipfian fit
us.map + geom_point(data=cities.df, 
    aes(x = lng, y=lat, color=zipf_fit),
    size= REG_SIZE + sq.mi) + 
    scale_colour_gradient(low="#27ae60", high="#d35400")
ggsave(file="zf.png", width=8, height=4.5)

