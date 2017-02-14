#' Download and prepare image data from the Alberta Open Data Areas site
#' 
#' @section Overview:
#' Some things get done here.  TBD

# global defs, libraries
library(rvest)
library(plyr)
library(httr)
library(xml2)
# library(DT)
library(raster)
library(rgdal)
library(tools)

basesite="http://opendataareas.ca"
data_file<-"~/aoda_summary.rds"


data_summary<-function(baseSite=basesite, dataFile=data_file){
  # Get the data locations and metadata
  # returns a data.frame with metadata of datasets available for download from the ODAA website
  if(!file.exists(dataFile)){
    oda_site<-read_html(paste0(baseSite,"/data/"))
    # get the links to the region pages
    links<-oda_site %>% html_nodes("a") %>% html_attr("href")
    linklist<-paste0(baseSite,unique(links[grep('sft_product',links)]))
    
    # scan a region page and get the links to the data product pages
    scan_areapage<-function(target){
      target_page<-read_html(target)
      data_links<-target_page %>% html_nodes("a") %>% html_attr("href")
      unique(data_links[grep('data/products',data_links)])
    }
    
    # scan a single product page and return a data.frame of the important bits
    scan_dlpage<-function(target){
      target_page<-read_html(target)
      product_title<-target_page %>% html_nodes(".productTitle") %>% html_text(trim=TRUE)
      product_region<-target_page %>% html_nodes(".region") %>% html_text(trim=TRUE)
      metadata_labels<-target_page %>% html_nodes(".productData .node .label") %>% html_text(trim=TRUE)
      metadata_data<-target_page %>% html_nodes(".productData .node .data") %>% html_text(trim=TRUE)  
      dl_link<-strsplit((target_page %>% html_nodes("button#downloadData") %>% html_attr("onclick")),"'")[[1]][[2]]
      product_labels<-c("product_title","product_region",metadata_labels,"dl_link")
      product<-data.frame(t(c(product_title,product_region,metadata_data,dl_link)))
      names(product)<-product_labels
      product
    }
    
    all_links<-lapply(linklist,scan_areapage)
    s_links<-unlist(all_links,recursive = FALSE)
    aoda_summary<-ldply(s_links,scan_dlpage)
    aoda_summary$dl_link<-paste0(baseSite,aoda_summary$dl_link)
    # save the summary data right now
    saveRDS(aoda_summary,file=dataFile)
  } else {
    aoda_summary<-readRDS(dataFile)
  }
  return(aoda_summary)
}

dl_prep_raster<-function(srcUrl, targetDir){
  # download and prepare a raster dataset
  # what does prepare even mean?
  # - unzip if zipped
  if(!dir.exists(targetDir)){
    dir.create(targetDir)
  }
  targetFile<-basename(parse_url(srcUrl)$path)
  targetFile<-paste(targetDir,targetFile,sep="/")
  if(!file.exists(targetFile)){
    print("downloading the file now ...")
    download.file(srcUrl,targetFile)
  
    if(grep(".zip$",targetFile)){
      print("un-zipping some data ....")
      unzip(targetFile, overwrite = FALSE, exdir = targetDir)
    }
  }
  
}

summarize_data<-function(df, baseSite=basesite, dataFile=data_file){
  # some looks at the available data
  if( is.null(df) ){
    df<-data_summary(baseSite,dataFile)
  }
  datatable(df[,c(1,2,14)])
  
  return(count(df[,c(2,7,8)]))
}

summarize_images<-function(imgDir, fileType="*.TIF$"){
  # not used directly, see summarize_digitalglobe()
  # list the geotiff images in a directory tree
  tiflist<-list.files(imgDir, fileType, recursive=TRUE, ignore.case=TRUE, full.names=TRUE)
  if(length(tiflist) < 1){
    print(paste0("Found no files matching ", fileType, " in ", imgDir))
    return(NULL)
  }
  tifattr<-lapply(tiflist,GDALinfo)
  tifsummary<-as.data.frame(t(matrix(unlist(tifattr), nrow=length(unlist(tifattr[1])))))
  names(tifsummary)<-names(tifattr[[1]])
  tifsummary$filename<-tiflist

  return(tifsummary)

}

summarize_gisfiles<-function(imgDir, fileType="*PIXEL_SHAPE.shp$"){
  # not used directly, see summarize_digitalglobe()  
  # for Quickbird and Worldview imagery there are several shapefiles, be selective
  # by selecting for *PIXEL_SHAPE.shp type we expect to get the image extents
  # we may want the tile outlines, which are *TILE_SHAPE.shp
  
  # list the shapefiles in the directory tree
  shplist<-list.files(imgDir, fileType, recursive=TRUE, ignore.case=TRUE, full.names=TRUE)
  if(length(shplist) < 1){
    print(paste0("Found no files matching ", fileType, " in ", imgDir))
    return(NULL)
  } 
  # get a list of spatialpolygonsdataframes
  shps<-lapply(shplist,readOGR)
  # merge them into a single SPDF
  spdf<-do.call(rbind,shps)
  
  return(spdf)
}

summarize_digitalglobe<-function(imgDir, imgType = "*.TIF$", gisType = "*PIXEL_SHAPE.shp$" ){
  # given a directory containing some Digitalglobe imagery
  # get a summary of the image files and the polygons from the shapefiles
  # return a spatialpolygonsdataframe

  tifs<-summarize_images(imgDir, imgType)
  shps<-summarize_gisfiles(imgDir, gisType)
  if(length(tifs) < 1 || dim(tifs)[1] != length(shps))
    return(NULL)
  
  # futz with the file name data so the individual records may be matched up
  tifs$imgBase<-file_path_sans_ext(basename(tifs$filename))
  shps$imgBase<-strtrim(file_path_sans_ext(basename(as.character(shps$prodDesc))),nchar(tifs$imgBase[1]))

  # add a record for the quicklook?
  
  # merge all the data into one spatialpolygonsdataframe
  dgdata<-merge(shps, tifs, by.x="imgBase", by.y="imgBase")
  return(dgdata)
}

img_to_map<-function(imgFile,bandList=c(1,2,3),targetDir="/data/raster/quickbird",targetCRS=3857){
  # make a mapserver mapfile for a specified imagefile.

  
  # check source files exist
  if(!file.exists(imgFile)){
    print(paste0("Error file not found:  ",imgFile))
    return
  }
  # check destination directory exists
  if(!dir.exists(targetDir)){
    dir.create(targetDir)
  }
  
  # get hold of the image
  img<-raster(imgFile)
  srcFile<-imgFile

  # further processing will be done through virtual files
  tmpFile<-file.path(targetDir,"tmpImage.tif")
  vrtFile<-file.path(targetDir,"tmpImage.vrt")
  
  # make sure it's 8 bit rgb or pan and enhance
  print("Translating the image ...")
  if(length(bandList > 1)){
    bandstr<-paste("-b ",bandList, collapse = " ")
  }
  else{
    bandstr<-""
  }
  #    system(command = sprintf('gdal_translate -ot Byte -scale 0 2047 0 255 %s %s %s',bandstr, imgFile,tmpFile))
  system(command = sprintf('gdal_contrast_stretch -ndv 0 -percentile-range 0.02 0.98 %s %s', imgFile,tmpFile))
  system(command = sprintf('gdalbuildvrt -overwrite %s %s %s', bandstr,vrtFile,tmpFile))
  
  srcFile<-vrtFile
  
  
  # warp the image if it doesn't match our desired CRS
  targetFile<-file.path(targetDir,basename(imgFile))  
  if(targetCRS != showEPSG(proj4string(img))){
    if(!file.exists(targetFile)){
      print(paste0("Warping to file ", targetFile))
      if(length(bandList) > 1){
        system(command = sprintf('gdalwarp -t_srs epsg:%s -r cubic  -co "TILED=YES" -co "COMPRESS=JPEG" -co "PHOTOMETRIC=YCBCR" %s %s', targetCRS, srcFile, targetFile ))
      } else {
        system(command = sprintf('gdalwarp -t_srs epsg:%s -r cubic  -co "TILED=YES" -co "COMPRESS=JPEG" %s %s', targetCRS, srcFile, targetFile ))        
      }
    }
  } else {
    # if the file doesn't need to be warped, then just copy it
    # file.copy(srcFile, targetFile)
    system(command = sprintf('gdal_translate -co "TILED=YES" -co "COMPRESS=JPEG" -co "PHOTOMETRIC=YCBCR"  %s %s', srcFile, targetFile ))
  }

  # add overview tiles
  if(length(bandList) > 1){
    system(command = sprintf('gdaladdo -ro --config COMPRESS_OVERVIEW JPEG --config JPEG_QUALITY_OVERVIEW 80 --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL --config GDAL_CACHEMAX 200 %s 2 4 8 16 32 64 128 256', targetFile))
  } else {
    system(command = sprintf('gdaladdo -ro --config COMPRESS_OVERVIEW JPEG --config JPEG_QUALITY_OVERVIEW 80 --config INTERLEAVE_OVERVIEW PIXEL --config GDAL_CACHEMAX 200 %s 2 4 8 16 32 64 128 256', targetFile))
  }
    
  
  if(file.exists(tmpFile)){
    print("Removing temporary file")
    unlink(tmpFile)
    unlink(vrtFile)
  }
  
  # create a mapserver mapfile for the requested image
  mapFile<-paste0(file_path_sans_ext(targetFile),".map")
  if(file.exists(mapFile)){
    print("Map file already exists, overwriting")
  }
  
  # get hold of the image
  img<-raster(targetFile)  
  img.x<-extent(img)
  img.p<-proj4string(img)
  # open the mapfile and write the bare minimum data into it
  con<-file(mapFile, "w")
  
  writeLines("# Mapfile created by R img_to_map:",con = con)
  writeLines("MAP",con = con)
  writeLines("    PROJECTION                     # Required for WMS services",con=con)
  writeLines("        'init=epsg:3857'",con = con)
  writeLines("    END",con = con)
  writeLines("    IMAGETYPE      PNG",con = con)
  writeLines("    UNITS METERS",con = con)
  writeLines(paste("    EXTENT       ", img.x@xmin, img.x@ymin, img.x@xmax, img.x@ymax),con = con)
  writeLines("    SIZE           400 400",con = con)
  writeLines("    MAXSIZE        10000           # prevent the pink screen of death on large monitors",con = con)
  writeLines('    SHAPEPATH      "."',con = con)
  writeLines("    IMAGECOLOR     255 255 255",con = con)

  writeLines("    WEB ",con = con)
  writeLines("        METADATA",con = con)
  writeLines("            'ows_title'                  'quickbird'",con = con)
  writeLines("            'ows_srs'                    'EPSG:4326 EPSG:3857'",con = con)
  writeLines("            'ows_enable_request'         '*'",con = con)
  writeLines(sprintf("            'ows_onlineresource'         'http://webmap.positionbot.com/mapserv/?map=%s'",mapFile),con = con)
  writeLines("             'wms_feature_info_mime_type' 'text/html'",con = con)
  writeLines("        END # metadata",con = con)
  writeLines("    END # web",con = con)
  
  writeLines("    LEGEND",con = con)
  writeLines("        STATUS ON",con = con)
  writeLines("        LABEL",con = con)
  writeLines("            SIZE 8",con = con)
  writeLines("            COLOR 0 0 0",con = con)
  writeLines("        END # LABEL",con = con)
  writeLines("    END # LEGEND",con = con)
  


  
  writeLines("    LAYER # raster layer begins here",con = con)
  writeLines("        NAME         quickbird",con = con)
  writeLines(paste0("        DATA        '", basename(filename(img)),"'"),con = con)
  writeLines("        STATUS       ON",con = con)
  writeLines("        TYPE         RASTER",con = con)
#  if(nbands(img) > 1){
#    writeLines('        PROCESSING   "BANDS=1,2,3"',con = con)
#  }
#  writeLines("        OFFSITE      0 0 0",con = con)
  writeLines("        CLASS",con = con)
  writeLines("            NAME 'Quickbird'",con = con)
  writeLines("        END # of CLASS",con = con)
  writeLines("    END #  raster layer ends here",con = con)
  
  writeLines("    # End of LAYER DEFINITIONS -------------------------------",con = con)
  
  writeLines("END # of map file",con = con)
  close(con)
}
