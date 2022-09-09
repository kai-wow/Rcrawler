
###########################
# A example for how to crawler the website data from douban
# Douban250
# author: CRQ
# date: 20181106
# version: 1.0
# encoding: utf-8
###########################

rm(list = ls())
gc()

# dir1 <- "F:\\StudyVideo\\R_video\\Rcrawler"
dir1 <- "D:\\R_wf"

if (!dir.exists(dir1)) dir.create(dir1)
setwd(dir1)

library(rvest)
library(RCurl)
library(stringr)
# help(package = "stringr")

myHttpheader <- c(
  
  "User-Agent" = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
  
  "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  
  "Accept-Language" = "zh-CN,zh;q=0.8",
  
  "Connection" = "keep-alive",
  
  "Accept-Encoding" = "gzip, deflate, sdch"
  
)
cHandle <- getCurlHandle(httpheader = myHttpheader)

url <- paste("https://movie.douban.com/top250?start=",c(0:9)*25,"&filter=",sep = "")

# step 1: get the linkage of all TOP 250 movies

hrefAll <- NULL

for (url1 in url){
  # url1 = url[1]
  Sys.sleep(sample(c(1:10),1, replace = TRUE))#replace重复，即有放回抽样
  d = debugGatherer()
  
  if (url.exists(url1)) {
    
    web <- read_html(url1,encoding="UTF-8")
    
  }
  
  
  href <- web %>% html_nodes("a") %>% html_attr("href")
  
  href <- href[grep("https://movie.douban.com/subject",href)]
  
  href <- unique(href)
  hrefAll <- c(hrefAll, href)
}

save(hrefAll, file = "douban250.RData")

# step 2: get the information about the movies

rm(list = ls())
gc()

# dir1 <- "D:\\R\\crawler"
dir1 <- "D:\\R_wf"
setwd(dir1)

library(rvest)

load("douban250.RData")

info250 <- NULL
noweb <- NULL
# hrefAll <- hrefAll[1:2]

for (url2 in hrefAll){
  #url2 <- hrefAll[1]
  Sys.sleep(sample(c(3:10),1, replace = TRUE))
  web <- try(read_html(url2,encoding="UTF-8"))
  if ('try-error' %in% class(web)) next
  # title and year
  titleyear <- gsub("\n","",web %>% html_nodes("h1") %>% html_text())
  titleyear <- trimws(unlist(strsplit(titleyear,"[\\(\\)]")))
  title <- titleyear[1]
  year <- titleyear[2]
  
  # information  
  info <- html_node(web, "div#info") %>% html_text() # very important, using chrome
  info <- gsub("[\n]","",info)
  info <- gsub("[ ]{2,}","",info)
  info <- gsub(" / ",";",info)
  # info <- unlist(strsplit(info, ":"))
  
  info <- strsplit(info, "(导演:)|(编剧:)|(主演:)|(类型:)|(制片国家/地区:)|(语言:)|(上映日期:)|(片长:)|(又名:)|(官方网站:)|(IMDb链接:)")
  info <- gsub("[\\:]","",info[[1]])
  info <- trimws(info)
  
  if (length(info)==11) {
    director <- info[2]
    scriptwriter <- info[3]
    actor <- info[4]
    type <- info[5]
    website <- ""
    region <- info[6]
    language <- info[7]
    date <- info[8]
    length <- info[9]
    title2 <- info[10]
    IMDb <- info[11]
  } 
  if (length(info)==12) {
    director <- info[2]
    scriptwriter <- info[3]
    actor <- info[4]
    type <- info[5]
    website <- info[6]
    region <- info[7]
    language <- info[8]
    date <- info[9]
    length <- info[10]
    title2 <- info[11]
    IMDb <- info[12]
  }
  
  # evaluate 
  # douban <- html_node(web, "strong.ll.rating_num") %>% html_text()
  douban <- web %>% 
    html_nodes(xpath = "/html/body/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/strong") %>%
    html_text()
    
  # people <- gsub("[人评价]","",html_node(web, "a.rating_people") %>% html_text())
  people <- str_extract(html_node(web, "a.rating_people") %>% html_text(), "[0-9]{1,}")
  #star <- gsub("[ \n]","",html_node(web, "div.rating_wrap.clearbox") 
  #             %>% html_text())
  #star <- unlist(strsplit(star,"[1-5]{1}???"))
  #star <- matrix(star[grep("%",star)],nrow = 1)
  star <- html_nodes(web, "span.rating_per") %>% html_text()
  star <- matrix(star, ncol = 5)
  # star <- html_nodes(web, 
  #                    xpath = "/html/body/div[3]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div/span[2]") %>% html_text()
  colnames(star) <- paste("star",c(5:1),sep = "")
  
  # summary
  
  summary <- html_node(web, "div.related-info") %>% html_node("span") %>% 
    html_text()
  summary <- gsub("[ \n\t]","",summary)
  summary <- gsub("\\(展开全部\\)","",summary)
  summary <- unlist(strsplit(summary,"　　"))[2]
  
  infoAll <- cbind(title, year, director, scriptwriter, actor, type,summary,website,
                   region, language, date, length, title2, IMDb,
                   douban,people,star)
  i <- unlist(strsplit(url2, "/"))[5]
  command <- paste("info", i, " <- infoAll", sep = "")
  eval(parse(text = command))
  info250 <- rbind(info250, infoAll)
  
  hrefAll <- setdiff(hrefAll, url2)
  
}

save(info250, noweb,file = "indbformation250.RData")


