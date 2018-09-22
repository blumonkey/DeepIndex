for i in templates/*/;
do
	test -d "$i" || continue
    	echo $i
    	(cd $i ; echo "In ${PWD}";
	for j in main-*.tex;
		do
			echo $j
			pdflatex $j
		done;
	for j in main-*.aux;
		do
			echo $j
			bibtex $j
		done;
	for j in main-*.tex;
		do
			echo $j
			pdflatex $j
		done;
	for j in main-*.tex;
		do
			echo $j
			pdflatex $j
		done;
	)
	
	# pdflatex main-*.tex && bibtex main-*.aux && pdflatex main-*.tex && pdflatex main-*.tex)
	# cd $i && rm main-*.* tmp*.tex meta-*.json;
done
