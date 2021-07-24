import pandas as pd
import numpy as np
import io
import os


from pprint import pprint
#### from Lecture later model later

import gensim
from gensim.utils import simple_preprocess
import nltk
import gensim.corpora as corpora

from scipy.stats import entropy

#nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

class TheBeast:
    
    with io.open("algorithms/cleaned_files/breast_pathology_lecture.txt", encoding='utf8') as breast_lect:
        breast_lect_txt = breast_lect.read()
        
    questiondf = pd.read_pickle("algorithms/cleaned_files/usmle_sample_questions.pkl")

    def __init__(self, lect_data, num_topics=10):
        self.num_topics = num_topics
        self.lect_data = lect_data.split(' ')
        self.df = TheBeast.questiondf
        self.question_data = [question.split(' ') for question in (self.df['question_text']) if isinstance(question, str)] # removes relevant info like age and  lab results -> fix later

    def sent_to_words(self, sentences: list):
        for sentence in sentences:
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    def remove_stopwords(self, texts):
        return [[word for word in simple_preprocess(str(doc)) 
                if word not in stop_words] for doc in texts]

    def data2words(self, data):
        data_words = list(self.sent_to_words(data))
        data_words = self.remove_stopwords(data_words)
        return data_words

    def get_all_words(self):
        lect_words = self.data2words(self.lect_data)
        q_words = self.data2words(self.question_data[0])
        self.all_words = lect_words + q_words
        return self.all_words

    def get_vocab(self):
        self.vocab = corpora.Dictionary(self.all_words) # add q words to dictionary
        return self.vocab

    def get_big_corpus(self):
        texts = self.get_all_words()
        self.get_vocab()
        self.big_corpus = [self.vocab.doc2bow(text) for text in texts]
        return self.big_corpus

    def get_corpus(self, texts):
        corpus = [self.vocab.doc2bow(text) for text in texts]
        return corpus


    def get_lda_model(self):
        self.lda_model = gensim.models.LdaMulticore(corpus=self.big_corpus,
                                            id2word=self.vocab,
                                            num_topics=self.num_topics,
                                            )
        return self.lda_model

    def get_document_distribution(self, document_as_list):  # used try/except
        new_bow = self.vocab.doc2bow(document_as_list)
        raw_distrib = self.lda_model.get_document_topics(bow=new_bow)
        
        distrib_list = [0] * self.lda_model.num_topics
        for index, topic in raw_distrib:
            distrib_list[index] = topic
        new_doc_distribution = np.array(distrib_list)
        return new_doc_distribution


    def question_2_list(self, question_str):
        if isinstance(question_str,str):
            data = question_str.split(' ')
            question_as_list = self.data2words(data)
            return question_as_list[0]

    def j_shan(self, p, q): #must be same size arrays
        m = 0.5 * (p + q)
        return np.sqrt(0.5*(entropy(p,m) + entropy(q,m)))



    def get_scores(self):
        j_s_scores = []
        counter = 0
        for row in self.df.iloc():
            q_str = row['question_text']
            if isinstance(q_str, str):
                q_distrib = self.get_document_distribution(self.question_2_list(row['question_text']))
                ##
                ####
                the_corpus = self.get_big_corpus()
                lda = self.lda_model

                doc_topic_dist = np.array([[tup[1]  for tup in lst] for lst in lda[the_corpus]])

                total_dist = np.mean(doc_topic_dist, axis=0)
                ###
                ##
                score = self.j_shan(q_distrib, total_dist)
                j_s_scores.append((counter, score))

            else:
                j_s_scores.append((counter, 0.5))   
            counter += 1
        return j_s_scores


    def n_relevant_indexes(self, n=10):
        scores = self.get_scores()
        score_list = scores.copy()
        score_list.sort(key=lambda x: x[1])
        return score_list[:n]

    def score_list2index(self, score_list):
        indexes = []
        for tup in score_list:
            indexes.append(tup[0])
        return indexes

    def run(self):
        self.get_all_words()
        print('1')
        self.get_vocab()
        print('2')
        self.get_big_corpus()
        print('3')
        self.get_lda_model()
        print('4')
        self.get_scores()
        print('5')
        score_list = self.n_relevant_indexes(10)
        indexes = self.score_list2index(score_list)
        
        return indexes


if __name__ == '__main__':
    a = TheBeast()
    a.run()