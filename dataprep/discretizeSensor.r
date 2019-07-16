library(data.table) # for fread

arffcsv <- fread(input="gassensor2019.arff", sep = "^", skip = 25, header=FALSE)[[1L]]

df <- fread(text=arffcsv, header=FALSE, fill=TRUE, sep=",")
head(df)

library(arules)
dfdisc <- discretizeDF(df, methods = list( V2 = list(method = "frequency", breaks = 5, 
			labels = c(1:5))),default = list(method = "none"))
head(dfdisc)
write.table( dfdisc, file = "gassensor2019discretetail", sep=",",  col.names=FALSE, row.names = FALSE, quote = FALSE )
 
# add the header by hand in shell, change any type values in header as needed

#
