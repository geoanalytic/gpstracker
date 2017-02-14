#' Utility functions for getting data from the Alberta Open Data Areas site
#' 
#' @section Overview:
#' Some things get done here.  TBD

# global defs, libraries
library(rvest)
library(plyr)
library(httr)
library(xml2)


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