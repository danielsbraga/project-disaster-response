import numpy as np
import pandas as pd
import random
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download(['punkt', 'wordnet'])

class DataProcessor:
    
    def __init__(self):
        self.count_vectorizer = None
        self.tfidf_transformer = None
    
    def tokenize(self, text_data):
        tokens = word_tokenize(text_data)
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(tok).lower().strip() for tok in tokens]
    
    def vectorize_transform(self, df):
        self.count_vectorizer = CountVectorizer(tokenizer=self.tokenize, token_pattern=None, ngram_range=(1, 3))
        self.tfidf_transformer = TfidfTransformer()
        text_data_counts = self.count_vectorizer.fit_transform(df)
        text_data_tfidf = self.tfidf_transformer.fit_transform(text_data_counts)
        return text_data_tfidf, self.count_vectorizer, self.tfidf_transformer
    
    def get_tail_label(self, df):
        columns = df.columns
        n = len(columns)
        irpl = np.zeros(n)
        for column in range(n):
            irpl[column] = df[columns[column]].value_counts()[1]
        irpl = max(irpl) / irpl
        mir = np.average(irpl)
        tail_label = [columns[i] for i in range(n) if irpl[i] > mir]
        return tail_label
    
    def get_index(self, df):
        tail_labels = self.get_tail_label(df)
        index = set()
        for tail_label in tail_labels:
            sub_index = set(df[df[tail_label] == 1].index)
            index = index.union(sub_index)
        return list(index)
    
    def get_minority_instance(self, X, y):
        index = self.get_index(y)
        X_sub = X[X.index.isin(index)].reset_index(drop=True)
        y_sub = y[y.index.isin(index)].reset_index(drop=True)
        return X_sub, y_sub
    
    def nearest_neighbour(self, X):
        nbs = NearestNeighbors(n_neighbors=5, metric='euclidean', algorithm='kd_tree').fit(X)
        _, indices = nbs.kneighbors(X)
        return indices
    
    def MLSMOTE(self, X, y, n_sample, indices):
        X = pd.DataFrame(X.toarray())
        n = len(indices)
        new_X = np.zeros((n_sample, X.shape[1]))
        target = np.zeros((n_sample, y.shape[1]))

        for i in range(n_sample):
            reference = random.randint(0, n - 1)
            neighbour = random.choice(indices[reference, 1:])
            all_point = indices[reference]
            nn_df = y[y.index.isin(all_point)]
            ser = nn_df.sum(axis=0, skipna=True)
            target[i] = np.array([1 if val > 2 else 0 for val in ser])
            ratio = random.random()
            gap = X.loc[reference, :] - X.loc[neighbour, :]
            new_X[i] = np.array(X.loc[reference, :] + ratio * gap)

        new_X = pd.DataFrame(new_X, columns=X.columns)
        target = pd.DataFrame(target, columns=y.columns)
        target = pd.concat([y, target], axis=0)
        new_X = pd.concat([X, new_X], axis=0)
        new_X = csr_matrix(new_X.values)
        return new_X, target
    
    def vectorize_test(self, text_data):
        text_data_counts = self.count_vectorizer.transform(text_data)
        text_data_tfidf = self.tfidf_transformer.transform(text_data_counts)
        return text_data_tfidf
