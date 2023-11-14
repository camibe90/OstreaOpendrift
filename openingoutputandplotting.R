require(ncdf4)

allfiles <- list.files("folder with simulations", pattern="*.nc", full.names=T)


library (gtools)
allfiles <- mixedsort(sort(allfiles))

files <- lapply(allfiles, nc_open)

require(lubridate)

df1<-list()
for (i in 1:17){
  file <- files[[i]]
  lon <- as.vector(ncvar_get(file,file$var$lon))
  lat <- as.vector(ncvar_get(file,file$var$lat))
  age <- as.vector(ncvar_get(file,file$var$age_seconds))
  status <- as.vector(ncvar_get(file,file$var$status))
  length <- as.vector(ncvar_get(file,file$var$length))
  weight <- as.vector(ncvar_get(file,file$var$weight))
  z <- as.vector(ncvar_get(file,file$var$z))
  temp <- as.vector(ncvar_get(file,file$var$sea_water_temperature))
  
  date <- as.vector(as.POSIXct( ncvar_get(file,file$dim$time), origin="1970-01-01 00:00:00"))
  fortnight <-as.vector(rep(paste(month(as.POSIXct(ncvar_get(file,file$dim$time), origin="1970-01-01 00:00:00"))[1],day(as.POSIXct(ncvar_get(file,file$dim$time),origin="1970-01-01 00:00:00"))[1]),length(lon))) 
  
  df <- data.frame(lon,lat,age,status,length, weight,z,temp, date, fortnight)
  df1[[i]] <- subset(df, status>0)
  dfstart <- subset (df,age==60*60)}

dftot <- reshape2::melt (df1, id.var=c("lon","lat","age","status","length", "weight", "z", "temp", "date","fortnight"))
require(ggplot2)
ggplot(dftot, aes(x=lon,y=lat)) + geom_point(aes(size=length,col=as.factor(L1), alpha=z, shape=as.factor(status))) + theme_classic()

write.csv(dftot, "filename.csv")



devtools::install_github("MikkoVihtakari/ggOceanMapsData") # required by ggOceanMaps
devtools::install_github("MikkoVihtakari/ggOceanMaps")
library(ggOceanMaps)
library(ggOceanMapsData)

dt <- data.frame(lon = c(), lat = c())


dftot$fortnight_ordered <- factor(dftot$fortnight, levels=unique(dftot$fortnight[order(as.numeric(substring(dftot$fortnight, 1, 2)))]))

basemap(data = dt, bathymetry = F) +
  geom_spatial_point(data=dftot,aes(x=lon,y=lat, col=z)) +
  stat_spatial_identity(crs=4326) + facet_wrap("fortnight_ordered") + geom_spatial_point(data = dt,aes(x=lon start,y=lat start), col="red")+
  annotation_scale(location = "br") +annotation_north_arrow(location = "tr", which_north = "true", 
                                                            
                                                            style = north_arrow_fancy_orienteering) 



