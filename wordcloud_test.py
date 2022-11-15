#!/usr/bin/env python
# coding: utf-8

# In[2]:


words = {
    'python':1965,
    'domdom':1666,
    '티스토리':955,
    '돔돔':855,
    '워드':841,
    '클라우드':612,
    '파이썬':598,
    'tistory':576,
    '코딩':542,
    '장인':487,
    '블로그':412,
    '방문자':401,
    '댓글':397,
    '롤':391,
    '칼바람':308,
    '나락':284,
    '환영':255,
    '자바':231,
    '장고':175,
    '자바스크립트':152,
    '스프링':109,
    '부트':71,
    '스타벅스':68,
    '제주말차':59,
    '프라푸치노':21,
    '먹고싶다':19,
    '디저트':6,
    '꿀잼':2
}
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import numpy as np
from PIL import *

cand_mask=np.array(Image.open('alice_mask.png'))

wc=WordCloud(
    font_path = "c:/Windows/fonts/malgun.ttf", # 한글 글씨체 설정
   #font_path = '/Library/Fonts/NanumBarunGothic.ttf', # mac 한글글씨체 
    background_color='white', # 배경색은 흰색으로 
    colormap='Reds', # 글씨색은 빨간색으로
    #mask=cand_mask, # 워드클라우드 모양 설정
    width=800, height=600
)

cloud=wc.generate_from_frequencies(words)

plt.figure(figsize=(8,8))
plt.imshow(cloud)
plt.axis('off')
plt.show()

