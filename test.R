library("reticulate")
library(dplyr)
# use_virtualenv("naomi")
cnd <- import("pynd")
## nd <- import("calcnd.neighborhood_density_calc")

a <- read.csv("~/naomi/data/signdata (33).csv")
features <- c("SignType.2.0",
              "MajorLocation.2.0",
              "MinorLocation.2.0",
              "SecondMinorLocation",
              "Movement.2.0",
              "Contact",
              "SelectedFingers.2.0",
              "Flexion.2.0",
              "FlexionChange",
              "Spread",
              "SpreadChange")

## out <- nd$MinimalPairND(sample_n(a, 100), features)
## out$WriteCSVSs("./output/", "foo")

nbr <- import("pynd.neighbors")
my.nbrs <- nbr$Neighbors(sample_n(a, 100), features)
my.nbrs$WriteCSVs("./output", "foo")

b.nd <- read.csv("./output/foo-nd.csv", stringsAsFactors=FALSE, na.strings=c("NA", ""))
b.nbrs <- read.csv("./output/foo-neighbors.csv", stringsAsFactors=FALSE, na.strings=c("NA", ""))
