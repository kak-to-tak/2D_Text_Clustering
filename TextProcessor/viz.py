import pandas as pd
import os
import bs4


def concatDF(df1, df2):
	return(pd.concat([df1, df2], axis=1))


def Visualiser(df, mapping, folder, value='0.1'):

	mapping['value'] = value
	mapping = mapping[mapping.labels != -1]
	concated = concatDF(df, mapping)

	# Save data and visualisation
	visualisation_path = 'visualisations/{}/'.format(folder)

	if not os.path.exists(visualisation_path):
		os.makedirs(visualisation_path)

	concated.to_csv('{}data.csv'.format(visualisation_path))

	# Load and create index.html file
	with open("visualisations/main/main.html") as inf:
		txt = inf.read()
		soup = bs4.BeautifulSoup(txt, "html.parser")

	with open("{}index.html".format(visualisation_path), "w") as outf:
		outf.write(str(soup))




