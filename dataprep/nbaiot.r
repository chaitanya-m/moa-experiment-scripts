#system("wget      --recursive      --no-clobber      --page-requisites      --convert-links     --no-parent          https://archive.ics.uci.edu/ml/machine-learning-databases/00442/")
# might have to rename the folder to nbaiot- I don't remember if it was called nbaiot

#system("find nbaiot/*/ -name \"*.rar\"")
#system("cd nbaiot && find . -name \"benign_traffic.csv\"")

#system("find nbaiot -name benign_traffic.csv -print0 | xargs -0 cat > nbaiot/merged_benign_traffic.csv")

#system("find nbaiot -name mirai_attacks.rar -print0 | xargs -0 unrar") # puts in the wrong folder

# Using Stackoverflow suggestions... I ran this separately
#system("find nbaiot -type f -name '*.rar' -print0 | 
#    while IFS= read -r -d '' file; do
#        dir=$(dirname "$file")
#        rar=$(basename "$file")
#	#echo $dir
#	#echo $file
#        cd $dir && unrar x -ad -r "$rar"
#        cd -
#    done")


#system("find nbaiot/*/mirai_attacks -name ack.csv -print0 | xargs -0 cat > nbaiot/ack_mirai_merged.csv")
#system("find nbaiot/*/mirai_attacks -name scan.csv -print0 | xargs -0 cat > nbaiot/scan_mirai_merged.csv")
#system("find nbaiot/*/mirai_attacks -name syn.csv -print0 | xargs -0 cat > nbaiot/syn_mirai_merged.csv")
#system("find nbaiot/*/mirai_attacks -name udp.csv -print0 | xargs -0 cat > nbaiot/udp_mirai_merged.csv")
#system("find nbaiot/*/mirai_attacks -name udpplain.csv -print0 | xargs -0 cat > nbaiot/udpplain_mirai_merged.csv")
#
#system("find nbaiot/*/gafgyt_attacks -name combo.csv -print0 | xargs -0 cat > nbaiot/combo_gafgyt_merged.csv")
#system("find nbaiot/*/gafgyt_attacks -name scan.csv -print0 | xargs -0 cat > nbaiot/scan_gafgyt_merged.csv")
#system("find nbaiot/*/gafgyt_attacks -name junk.csv -print0 | xargs -0 cat > nbaiot/junk_gafgyt_merged.csv")
#system("find nbaiot/*/gafgyt_attacks -name udp.csv -print0 | xargs -0 cat > nbaiot/udp_gafgyt_merged.csv")
#system("find nbaiot/*/gafgyt_attacks -name tcp.csv -print0 | xargs -0 cat > nbaiot/tcp_gafgyt_merged.csv")
#system("mkdir nbaiot/merged")
#system("mv nbaiot/*merged*.csv merged")



#system(head -n 1 nbaiot/merged/scan_gafgyt_merged.csv | xargs -I{} grep -rnicI {} nbaiot/merged)
#system(head -n 1 nbaiot/demonstrate_structure.csv | xargs -I{} grep -rnicI {} nbaiot/merged)

#head -n 1 nbaiot/demonstrate_structure.csv | xargs -I{} grep -rnicI {} nbaiot/merged

#find nbaiot -type f -name '*merged.csv' -print0 | 
#    while IFS= read -r -d '' file; do
#	echo $file
#	head -n 1 nbaiot/demonstrate_structure.csv | xargs -I{} sed -i 's/{}//g' $file
#	head -n 1 nbaiot/demonstrate_structure.csv | xargs -I{} grep -rniI {} nbaiot/merged
#	cat nbaiot/demonstrate_structure.csv $file > temp && mv temp $file
#    done

#mydata <- read.csv("nbaiot/merged/ack_mirai_merged.csv")
#mydata$class <- rep("ack_mirai",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/ack_mirai.csv")
#
#mydata <- read.csv("nbaiot/merged/scan_mirai_merged.csv")
#mydata$class <- rep("scan_mirai",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/scan_mirai.csv")
#
#
#mydata <- read.csv("nbaiot/merged/syn_mirai_merged.csv")
#mydata$class <- rep("syn_mirai",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/syn_mirai.csv")
#
#
#mydata <- read.csv("nbaiot/merged/udp_mirai_merged.csv")
#mydata$class <- rep("udp_mirai",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/udp_mirai.csv")
#
#
#mydata <- read.csv("nbaiot/merged/udpplain_mirai_merged.csv")
#mydata$class <- rep("udpplain_mirai",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/udpplain_mirai.csv")
#
#
#
#
#
#mydata <- read.csv("nbaiot/merged/benign_traffic_merged.csv")
#mydata$class <- rep("benign_traffic",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/benign_traffic.csv")
#
#
#
#
#mydata <- read.csv("nbaiot/merged/combo_gafgyt_merged.csv")
#mydata$class <- rep("combo_gafgyt",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/combo_gafgyt.csv")
#
#mydata <- read.csv("nbaiot/merged/junk_gafgyt_merged.csv")
#mydata$class <- rep("junk_gafgyt",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/junk_gafgyt.csv")
#
#
#mydata <- read.csv("nbaiot/merged/tcp_gafgyt_merged.csv")
#mydata$class <- rep("tcp_gafgyt",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/tcp_gafgyt.csv")
#
#
#mydata <- read.csv("nbaiot/merged/udp_gafgyt_merged.csv")
#mydata$class <- rep("udp_gafgyt",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/udp_gafgyt.csv")
#
#mydata <- read.csv("nbaiot/merged/scan_gafgyt_merged.csv")
#mydata$class <- rep("scan_gafgyt",nrow(mydata))
#head(mydata)
#write.csv(mydata, file = "nbaiot/merged/scan_gafgyt.csv")
#
#system(for f in nbaiot/merged/*; do wc -l $f; done)

#head -1 nbaiot/merged/ack_mirai.csv > nbaiot/merged/header
#for f in nbaiot/merged/*.csv; do tail -n +2 $f >> nbaiot/merged/header; done
#for f in nbaiot/merged/*; do wc -l $f; done

#643822 nbaiot/merged/ack_mirai.csv
#555933 nbaiot/merged/benign_traffic.csv
#515157 nbaiot/merged/combo_gafgyt.csv
#7062607 nbaiot/merged/header
#261790 nbaiot/merged/junk_gafgyt.csv
#255112 nbaiot/merged/scan_gafgyt.csv
#537980 nbaiot/merged/scan_mirai.csv
#733300 nbaiot/merged/syn_mirai.csv
#859851 nbaiot/merged/tcp_gafgyt.csv
#946367 nbaiot/merged/udp_gafgyt.csv
#1230000 nbaiot/merged/udp_mirai.csv
#523305 nbaiot/merged/udpplain_mirai.csv


#mydata <- read.csv("nbaiot/nbaiot.csv") # This was taking too long!
#head(mydata)

#mv nbaiot/nbaiot.csv nbaiot/nbaiotr.csv 
#cut -f1 -d"," --complement nbaiot/nbaiotr.csv > nbaiot/nbaiot.csv # Much faster!
#java -Xmx30480M -cp  weka.jar weka.core.converters.CSVLoader  ../nbaiot/nbaiot.csv > ../nbaiot/nbaiot.arff
#time java -Xmx50480M -cp  weka.jar weka.core.converters.CSVLoader  ../nbaiot/nbaiot.csv -L "class:ack_mirai,scan_mirai,syn_mirai,udp_mirai,udpplain_mirai,combo_gafgyt,junk_gafgyt,scan_gafgyt,tcp_gafgyt,udp_gafgyt,benign_traffic" -B 100000 > ../nbaiot/nbaiot.arff



