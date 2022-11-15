#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols, glm
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


# 1. 다운로드한 CSV파일 정리하기

# In[2]:


red_df = pd.read_csv("winequality-red.csv", sep =";", header=0, engine='python')
white_df = pd.read_csv("winequality-white.csv", sep =";", header=0, engine='python')


# In[3]:


red_df.to_csv('winequality-red2.csv', index=False)
white_df.to_csv('winequality-white2.csv', index=False)


# 2. 데이터 병합하기

# In[4]:


red_df.head()


# In[5]:


red_df.insert(0, column='type', value='red')


# In[6]:


red_df.head()


# In[7]:


red_df.shape


# In[8]:


white_df.head()


# In[9]:


white_df.insert(0, column='type', value='white')


# In[10]:


white_df.head()


# In[11]:


white_df.shape


# In[12]:


wine = pd.concat([red_df, white_df])
wine.shape


# 3. 데이터 탐색

# In[13]:


wine.info()


# In[14]:


wine.describe()


# In[16]:


wine.columns = wine.columns.str.replace(' ','_')
wine.describe()


# In[17]:


sorted(wine.quality.unique())


# In[18]:


wine.quality.value_counts()


# describe( ) 함수로 그룹 비교하기

# In[19]:


wine.groupby('type')['quality'].describe()


# In[20]:


wine.groupby('type')['quality'].agg(['mean','std','max'])


# t-검정

# In[21]:


red_wine_quality = wine.loc[wine['type'] == 'red', 'quality']
white_wine_quality = wine.loc[wine['type']== 'white','quality']


# In[22]:


stats.ttest_ind(red_wine_quality, white_wine_quality, equal_var=False)


# In[25]:


Rformula = 'quality ~ fixed_acidity + volatile_acidity + citric_acid + residual_sugar + chlorides + free_sulfur_dioxide + total_sulfur_dioxide + density + pH + sulphates + alcohol'


# In[26]:


regression_result = ols(Rformula, data=wine).fit()


# In[27]:


regression_result.summary()


# 와인 품질 예측하기

# In[29]:


sample1 = wine[wine.columns.difference(['quality', 'type'])]


# In[30]:


sample1 = sample1[0:5][:]


# In[31]:


sample1_predict = regression_result.predict(sample1)


# In[32]:


sample1_predict


# In[33]:


wine[0:5]['quality']


# In[34]:


data = {"fixed_acidity" : [8.5, 8.1], "volatile_acidity":[0.8, 0.5],
"citric_acid":[0.3, 0.4], "residual_sugar":[6.1, 5.8], "chlorides":[0.055,
0.04], "free_sulfur_dioxide":[30.0, 31.0], "total_sulfur_dioxide":[98.0,
99], "density":[0.996, 0.91], "pH":[3.25, 3.01], "sulphates":[0.4, 0.35],
"alcohol":[9.0, 0.88]}


# In[35]:


sample2 = pd.DataFrame(data, columns=sample1.columns)


# In[36]:


sample2_predict = regression_result.predict(sample2)
sample2_predict


# 시각화

# In[38]:


import warnings
warnings.filterwarnings(action='ignore')


# In[42]:


sns.set_style('dark')
sns.distplot(red_wine_quality, kde = True, color='red', label='red wine')#kde 커널 밀도
sns.distplot(white_wine_quality, kde = True, label='white wine')
plt.title("Quality of Wine Type")
plt.legend()
plt.grid()
plt.show()


# In[46]:


others = list(set(wine.columns).difference(set(['quality','fixed_acidity'])))


# In[50]:


p, resids = sm.graphics.plot_partregress("quality", "fixed_acidity", others, data = wine, ret_coords = True)


# In[49]:


fig = plt.figure(figsize = (8, 13))
sm.graphics.plot_partregress_grid(regression_result, fig = fig)

