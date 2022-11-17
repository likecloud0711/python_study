#!/usr/bin/env python
# coding: utf-8

# # 11장. 분류 분석 (1) 로지스틱 회귀 분석을 이용한 유방암 진단 프로젝트

# ### 1) 데이터 수집

# In[1]:


import numpy as np
import pandas as pd

from sklearn.datasets import load_breast_cancer


# In[2]:


b_cancer = load_breast_cancer()


# ### 2) 데이터 수집 및 탐색

# In[3]:


print(b_cancer.DESCR)


# In[4]:


b_cancer_df = pd.DataFrame(b_cancer.data, columns = b_cancer.feature_names)


# In[7]:


b_cancer_df['diagnosis']= b_cancer.target


# In[8]:


b_cancer_df.head()


# In[9]:


print('유방암 진단 데이터셋 크기 : ', b_cancer_df.shape)


# In[10]:


b_cancer_df.info()


# In[11]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


# In[12]:


b_cancer_scaled = scaler.fit_transform(b_cancer.data)


# In[13]:


print(b_cancer.data[0])


# In[14]:


print(b_cancer_scaled[0])


# ### 3) 분석 모델 구축 : 로지스틱 회귀를 이용한 이진 분류 모델

# In[13]:


from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


# In[14]:


# X, Y 설정하기
Y = b_cancer_df['diagnosis']
X = b_cancer_scaled 


# In[15]:


# 훈련용 데이터와 평가용 데이터 분할하기
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)


# In[16]:


# 로지스틱 회귀 분석 : (1)모델 생성
lr_b_cancer = LogisticRegression()


# In[17]:


# 로지스틱 회귀 분석 : (2)모델 훈련
lr_b_cancer.fit(X_train, Y_train)


# In[18]:


# 로지스틱 회귀 분석 : (3)평가 데이터에 대한 예측 수행 -> 예측 결과 Y_predict 구하기
Y_predict = lr_b_cancer.predict(X_test)


# ### 4) 결과 분석 

# In[19]:


from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score


# In[20]:


# 오차 행렬 
confusion_matrix(Y_test, Y_predict)


# In[21]:


#성능 평가 지표
acccuracy = accuracy_score(Y_test, Y_predict)
precision = precision_score(Y_test, Y_predict)
recall = recall_score(Y_test, Y_predict)
f1 = f1_score(Y_test, Y_predict)
roc_auc = roc_auc_score(Y_test, Y_predict)


# In[22]:


print('정확도: {0:.3f}, 정밀도: {1:.3f}, 재현율: {2:.3f},  F1: {3:.3f}'.format(acccuracy,precision,recall,f1))


# In[23]:


print('ROC_AUC: {0:.3f}'.format(roc_auc))


# In[ ]:




