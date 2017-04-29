from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse.csr import csr_matrix
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
import sys

# ~~ Example 1 ~~
corpus = ['row, row, row your boat','whatever floats your boat']
test_time = ['your boat floats really well interesting']

tf = TfidfVectorizer(input='content', analyzer='word', ngram_range=(1,1),
                     min_df = 0, sublinear_tf=True)

test_stuff = tf.fit_transform(test_time)
print(test_stuff)

tfidf_matrix = tf.fit_transform(corpus)
print(tfidf_matrix)

feature_names = tf.get_feature_names()
print(feature_names)


labels = np.array([[0, 1], [1, 0]])

classifier = OneVsRestClassifier(SGDClassifier()).fit(tfidf_matrix, labels)
y_pred = classifier.predict(test_stuff)
print("check result!")
print(y_pred)
sys.exit()
