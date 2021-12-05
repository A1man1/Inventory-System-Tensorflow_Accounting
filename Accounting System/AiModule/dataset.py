import re

from sklearn.datasets import fetch_20newsgroups

categories=[
			'alt.atheism', 
			'comp.os.ms-windows.misc',
			'comp.sys.ibm.pc.hardware', 
			'comp.sys.mac.hardware', 
			'comp.windows.x', 
			'misc.forsale', 
			'rec.autos', 
			'rec.sport.hockey', 
			'sci.crypt', 
			'sci.electronics', 
			'sci.med', 
			'sci.space', 
			'talk.politics.guns', 
			'talk.politics.mideast', 
			'talk.politics.misc', 
			'talk.religion.misc'
		]
news_train=fetch_20newsgroups(subset='train',categories= categories,shuffle=True)
news_test=fetch_20newsgroups(subset='test',categories= categories,shuffle=True)
print(len(news_test),"data---> ",news_test.target_names)
\
data =[i.split('.') for i in news_test.data] 
print('Welcome to Geeks for Geeks'.replace('G','@'))

