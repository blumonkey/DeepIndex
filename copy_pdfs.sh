for i in templates/*/;
do
	test -d "$i" || continue
    	echo $i
    	(cd $i ; echo "In ${PWD}";
	cp main-*.pdf meta-*.json ../../files/
	)
	
	# pdflatex main-*.tex && bibtex main-*.aux && pdflatex main-*.tex && pdflatex main-*.tex)
	# cd $i && rm main-*.* tmp*.tex meta-*.json;
done
