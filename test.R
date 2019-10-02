library(reticulate)
library(here)
use_python(here("venv", "bin", "python"), required=TRUE)
cnd <- import("pynd")
## nd <- import("calcnd.neighborhood_density_calc")

a <- read.csv(here("data", "signdata (33).csv"))
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

## out <- nd$MinimalPairND(dplyr::sample_n(a, 100), features)
## out$WriteCSVs(here("output"), "foo")

nbr <- import("pynd.neighbors")
my.nbrs <- nbr$Neighbors(dplyr::sample_n(a, 100), features)
my.nbrs$WriteCSVs(here("output"), "foo")

b.nd <- read.csv(here("output", "foo-nd.csv"), stringsAsFactors=FALSE, na.strings=c("NA", ""))
b.nbrs <- read.csv(here("output", "foo-neighbors.csv"), stringsAsFactors=FALSE, na.strings=c("NA", ""))
