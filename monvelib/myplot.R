## Installation of Packages ##
##############################
require(ggmap)
require(ggplot2)
require(mongolite)
require(tidyr)



## Script ##
############

# Connection to database
stations<-mongo(collection = "station", db = "velib", url = "mongodb://localhost",
                verbose = TRUE)

# Transforming into a dataframe
df=stations$find(query = '{}', fields = '{"_id" : 0}', sort = '{}', skip = 0, limit = 0, handler = NULL)
df <- separate(df, coord, into = c("latitude","longitude"), sep = ",", extra = "merge")
df <- separate(df, velos, into = c("shit","last_update","total_stands","stands","bikes","status"), sep = "=", extra = "merge")
df$latitude <- as.numeric(substring(df$latitude, 3))
df$longitude <-as.numeric(gsub("\\)","",substring(df$longitude,1,nchar(df$latitude)-1)))

df <- separate(df, bikes, into = c("bikes","le_reste"), sep = "\\)", extra = "merge")
df$bikes<-as.numeric(substring(df$bikes,nchar(df$bikes)-1,nchar(df$bikes)))

for (i in c("shit","last_update","total_stands","stands","status","le_reste")){
  df$i<-NULL
}

# Plotting
map.paris <- qmap("paris", source="stamen", zoom=12, messaging=FALSE, maptype="toner") 
map.paris<-map.paris +
  geom_point(data=df, aes(x=longitude, y=latitude, size=bikes, color=bikes), alpha=.9, na.rm=T) +
  scale_color_gradient(low="#33CC33", high="#003300", name="Number of available \nbikes") +
  scale_size(range=c(1,11) , guide="none")
png(file="/Users/louisdecharson/Programmation/Python/Velib/monvelib/static/img/map.png",width=1000,height=1000,bg="transparent")
plot(map.paris)
dev.off()



