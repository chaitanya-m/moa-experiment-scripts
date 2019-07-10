cat *.csv > gassensor2019.csv
head -1 gassensor2019.csv > gassensorhead
sed -i '/Time.*/d' gassensor2019.csv
sed -i '1s/^/\n/g' gassensor2019.csv
sed -i '1rgassensorhead' gassensor2019.csv
sed -i '1d' gassensor2019.csv
# work around the fact that you can't insert after line 0 in sed
# hopefully more efficient than cat, rewriting whole file
# insert in place with sed
