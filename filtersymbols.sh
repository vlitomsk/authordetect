#!/bin/sh

cp -R $1 $2
cd $2
for file in `find . -type f`
do
  enconv $file
  sed -i ':a;N;$!ba;s/\n\|[^а-яА-Я]//g' $file
  sed -i 's/[[:upper:]]*/\L&/g' $file
done

