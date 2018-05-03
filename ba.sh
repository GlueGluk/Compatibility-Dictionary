#!/bin/bash
if [ ! -d textfiles ] ; then
mkdir textfiles
fi
cd library;
for dir in * ; 
do
    cd ..;
    if [ ! -d textfiles/$dir ] ; then
    mkdir textfiles/$dir
    fi
    cd library;
    cd ./"$dir";
    echo "$dir";
    for file in `find . -name "*.pdf"`; do
        echo "================= $file";
        pdftotext -layout "$file";
        done
    for file in `find . -name "*.docx"`; do
        uniconv -f doc $file 
        done
    for file in `find . -name "*.doc"`; do
        tfile = `sed 's/.doc/.txt' "$file"`;
        antiword $file > $tfile ;
        done
    for ff in `find . -name "*.txt"` ; do
        mv "$ff" ../../textfiles/;
        done
    cd ..;
    done
cd ..;
