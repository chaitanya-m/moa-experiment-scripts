library(data.table) # for fread

awsarff_connection <- file("aws-spot-pricing-market.arff")
open(awsarff_connection, "r")

awscsv <- fread(input="aws-spot-pricing-market.arff", sep = "^", skip = 12, header=FALSE)[[1L]]

awsdf <- fread(text=awscsv, header=FALSE, fill=TRUE, sep=",")
head(awsdf)

library(arules)
awsdisc <- discretizeDF(awsdf, methods = list( V8 = list(method = "frequency", breaks = 10, 
			labels = c(1:10))),default = list(method = "none"))
head(awsdisc)
write.table( awsdisc, file = "aws_disc2", sep=",",  col.names=FALSE, row.names = FALSE, quote = FALSE )
 
# add the header by hand in shell

#
