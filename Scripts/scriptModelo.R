library('stringr')
library('rminer')
library('kknn')


file <- 'FAUX.csv'

solar <- read.csv(file, sep=';', header=T)

M=loadmining("mlpe")
Value=predict(M,solar[,c(4:10)])
solar <- cbind(solar,Value)
solar <- solar[,c(1,2,3,11)]
#solar <- solar[sample(sample(seq(1:length(solar[,1])),8000)),]
nameFile <- 'FAUX1.csv'
write.table(solar, file = nameFile, append = FALSE, quote = F, sep = ";", row.names = FALSE, col.names = F)
