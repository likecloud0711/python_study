#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob # 경로와 이름을 지정해 파일 처리 작업
import re
from functools import reduce # 2차원 리스트 -> 1차원 리스트

# nltk : 자연어 처리 패키지
from nltk.tokenize import word_tokenize # 단어 토큰화
from nltk.corpus import stopwords # 불용어 정보 제공
from nltk.stem import WordNetLemmatizer # 표제어 추출 

from collections import Counter # 갯수 자동 계산

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS # wordcloud용 불용어


# In[2]:


import nltk


# In[3]:


nltk.download() # 최초 한번은 nltk의 리소스를 다운로드 받아야함.


# In[4]:


all_files = glob.glob('data/myCabinetExcelData*.xls')
all_files


# In[5]:


all_files_data = [] 

for file in all_files:
    data_frame = pd.read_excel(file)
    all_files_data.append(data_frame)

all_files_data[0].head()


# In[7]:


all_files_data_concat = pd.concat(all_files_data, axis= 0 , ignore_index=True)
all_files_data_concat.tail()


# In[10]:


all_files_data_concat.to_csv('data/riss_AI.csv', encoding='utf-8', index=False)


# In[15]:


all_title = all_files_data_concat['제목']
all_title


# In[24]:


stopWords = set(stopwords.words('english'))
lemma = WordNetLemmatizer() # 표제어 추출 작업


# In[29]:


words = []  

for title in all_title:
    EnWords = re.sub(r"[^a-zA-Z]+", " ", str(title))
    EnWordsToken = word_tokenize(EnWords.lower())
    EnWordsTokenStop = [w for w in EnWordsToken if w not in stopWords]
    EnWordsTokenStopLemma = [lemma.lemmatize(word) for word in EnWordsTokenStop]
    words.append(EnWordsTokenStopLemma)


# In[30]:


print(words[:5])


# In[31]:


words2 = list(reduce(lambda x , y : x+y, words))
print(words2)


# In[32]:


count = Counter(words2)
count


# In[33]:


word_count = dict()

for tag, counts in count.most_common(50):
    if(len(str(tag)) > 1):
        word_count[tag] = counts 
        print("%s : %d" %(tag, counts))


# In[34]:


del word_count['ai']


# In[37]:


plt.figure(figsize=(12,5))
plt.xlabel("word")
plt.ylabel("count")
plt.grid(True)

sorted_Keys = sorted(word_count, key=word_count.get, reverse=True)
sorted_Values = sorted(word_count.values(), reverse=True)

plt.bar(range(len(word_count)), sorted_Values, align='center')
plt.xticks(range(len(word_count)), list(sorted_Keys), rotation='90')# x축 눈금

plt.show()


# In[40]:


all_files_data_concat['doc_count'] = 0
summary_year = all_files_data_concat.groupby('출판일', as_index=False)['doc_count'].count()
summary_year


# In[42]:


plt.figure(figsize=(12,5))
plt.xlabel("year")
plt.ylabel("doc-count")
plt.grid(True)

plt.plot(range(len(summary_year)), summary_year['doc_count'])
plt.xticks(range(len(summary_year)), [y for y in summary_year['출판일']], rotation='90')

plt.show()


# In[45]:


stopwords = set(STOPWORDS)
wc = WordCloud(background_color='white', colormap='autumn', stopwords=stopwords
              , width=1000, height=600)
cloud = wc.generate_from_frequencies(word_count)

plt.imshow(cloud)
plt.axis('off')
plt.show()

