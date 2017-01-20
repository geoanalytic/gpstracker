FROM rocker/ropensci:latest

RUN apt-get update -y
RUN apt-get -y install binutils libproj-dev gdal-bin libgdal1-dev dans-gdal-scripts

## install devtools
RUN install2.r devtools 
RUN install2.r rgdal