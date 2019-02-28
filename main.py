from TextProcessor.features import text_features
from TextProcessor.reduction import Mapper
from TextProcessor.labeller import automatic_labelling
from TextProcessor.viz import Visualiser
from TextProcessor.viz import concatDF
from TextProcessor.cleaning import url_tagging
from TextProcessor.cleaning import nickname_tagging
from TextProcessor.cleaning import hashtag_tagging
from TextProcessor.cleaning import clean_text

import pandas as pd

def getTexts(csvfile, sep=','):
	df = pd.read_csv(csvfile, sep=sep)
	return df


def tagging(df):
	texts = df['text']
	print('Searching for hashtags')
	df['found_urls'] = url_tagging(texts)
	df['found_nicknames'] = nickname_tagging(texts)
	df['found_hashtags'] = hashtag_tagging(texts)
	print('Cleaning')
	df['clean_text'] = [clean_text(doc) for doc in texts]
	print('Finished!')
	# df['found_prices'] = price_tagging(texts)
	return(df)


if __name__ == "__main__":
	df = getTexts('./new_df.csv')
	corpus = df['dict_words']
	tf = text_features(corpus)
	data = Mapper(tf.values, corpus)
	mapping = automatic_labelling(data)
	Visualiser(df, mapping,folder='adverts')


