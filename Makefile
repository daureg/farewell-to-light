SRC_FIGURES= mkfigs/city_time_cluster.tex \
	     mkfigs/cluster_day_3h_cl1.tex \
	     mkfigs/cluster_day_3h_cl2.tex \
	     mkfigs/cluster_day_3h_cl3.tex \
	     mkfigs/cluster_day_3h_cl4.tex \
	     mkfigs/cluster_day_3h_cl5.tex \
	     mkfigs/cluster_day_4h_cl1.tex \
	     mkfigs/cluster_day_4h_cl2.tex \
	     mkfigs/cluster_day_4h_cl3.tex \
	     mkfigs/cluster_day_4h_cl4.tex \
	     mkfigs/cluster_day_4h_cl5.tex \
	     mkfigs/daily_checkin.tex \
	     mkfigs/day_cluster_3h.tex \
	     mkfigs/day_cluster_4h.tex \
	     mkfigs/weekly_checkin.tex

all:
	@echo "make has no yet achieve self conciousness."
	@echo "Thus it can't choose a default task for you:"
	@echo "make thesis: generate complete pdf"
	@echo "make figure: generate all figures as pdf"
	@echo "make bib: strip full bib file"

thesis:
	latexmk -pdf ClassicThesis

figures: $(SRC_FIGURES)
	cd mkfigs
	for f in $^; sh mkfig.sh $f; done

bib: ${HOME}/aalto/thesis.bib
	sed -e '/url/d' $< > strip.bib
	sed -i '/issn/d'  strip.bib
	sed -i '/isbn/d'  strip.bib
	sed -i '/archivePrefix/d'  strip.bib
	sed -i '/pmid/d'  strip.bib
