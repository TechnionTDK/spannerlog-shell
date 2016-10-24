#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  echo "Missing argument"
  exit 1
fi

# s="${1}q;d"
# sed $s input/articles.tsv
s="${1}d;" 
sed -e $s input/articles.tsv > input/articles_new.tsv
rm input/articles.tsv
mv input/articles_new.tsv input/articles.tsv
splog compile
splog run
