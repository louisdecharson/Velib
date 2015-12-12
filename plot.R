





plotMyMap <- function(path_to_csv) {

    # Packages
    library(ggmap)
    library(ggplot2)

    #Variables
    dir<-"/Users/louisdecharson/Programmation/Python/Velib/plots/"

    df.velib_bikes <- read.csv(path_to_csv, sep=",", header=T) 
    myTitle<-paste("Available Velib in Paris - date :",toString(Sys.time()))
map.paris <- qmap("paris", source="stamen", zoom=12, messaging=FALSE, maptype="toner") 
map.paris<-map.paris +
    geom_point(data=df.velib_bikes, aes(x=longitude, y=latitude, size=available_bikes, color=available_bikes), alpha=.9, na.rm=T) +
    scale_color_gradient(low="#99e699", high="#145214", name="Number of available \nbikes") +
    scale_size(range=c(1,11) , guide="none") + 
    ggtitle(myTitle) +
    theme(text = element_text(family = "Helvetica", color="#666666")) +
    theme(plot.title = element_text(size=32, face="bold", hjust=0, vjust=.5))

    hour<-gsub(":","_",substring(toString(Sys.time()),12,20))
    name<-paste(dir,"bikes_",hour,".jpg",sep="")
    jpeg(file=name,width=1000,height=1000)
    plot(map.paris)
    dev.off()
} 




## map.paris +
##    geom_point(data=df.velib_bikes, aes(x=longitude, y=latitude, size=available_bike_stands, color=available_bike_stands), alpha=.9, na.rm=T) +
##    scale_color_gradient(low="#33CC33", high="#003300", name="Number of available\nbike stands") +
##    scale_size(range=c(1,11) , guide="none") + 
##    ggtitle("Available bike stands in Paris") +
##    theme(text = element_text(family = "Helvetica", color="#666666")) +
##    theme(plot.title = element_text( size=32, face="bold", hjust=0, vjust=.5))

## map_bonus.paris<-qmap("paris", source="stamen", zoom=12, maptype="toner") 
## map_bonus.paris<-map_bonus.paris+
##   geom_point(data=df.velib_bikes[df.velib_bikes$bonus=="True",], aes(x=longitude, y=latitude, size=3, color="#99e699"), alpha=.9, na.rm=T) +
##   ggtitle("Bonus Bike Stands") +
##   theme(legend.position="none") +
##   theme(text = element_text(family = "Helvetica", color="#666666")) +
##   theme(plot.title = element_text(size=32, face="bold", hjust=0, vjust=.5))
# hour<-gsub(":","_",substring(toString(Sys.time()),12,20))
# name<-paste(dir,"bonus_",hour,".jpg",sep="")
# jpeg(name)
# plot(map_bonus.paris)
# dev.off()



  

