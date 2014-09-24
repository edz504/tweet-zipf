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
    scale_colour_gradient(low="white", high="#3498db")

# color by zipfian fit
us.map + geom_point(data=cities.df, 
    aes(x = lng, y=lat, color=zipf_fit),
    size= REG_SIZE + sq.mi) + 
    scale_colour_gradient(low="white", high="#c0392b")

uq <- unique(cities.df$top_word)
topToInt <- function(word) {
    return(which(word == uq))
}

cities.df <- cities.df %>% 
    mutate(top_int=sapply(cities.df$top_word, topToInt))

REG_SIZE2 <- 50
# color by most common word
us.map + geom_point(data=cities.df, 
    aes(x = lng, y=lat, 
        colour=factor(cities.df$top_int),
        size= REG_SIZE2)) + 
    guides(colour = guide_legend(override.aes = list(alpha = 1)))