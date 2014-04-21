#! /bin/bash
sed -i "/input/ s/{.*/{$1}/" figure.tex
pdflatex figure
mv figure.pdf $(basename $1 .tex).pdf
