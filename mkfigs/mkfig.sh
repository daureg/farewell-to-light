#! /bin/bash
sed -i "/%in/ s/{[^}]*/{$1/" figure.tex
pdflatex figure
mv figure.pdf $(basename $1 .tex).pdf
