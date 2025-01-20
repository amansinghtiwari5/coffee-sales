#!/usr/bin/env python
# coding: utf-8

# # Coffee sales data analyst project

# In[3]:


import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


# In[4]:


coffee_data = pd.read_csv('index.csv')


# In[8]:


coffee_data.head()


# In[9]:


coffee_data.info()


# In[10]:


coffee_data.isnull().sum()


# In[11]:


coffee_data.duplicated().sum()


# In[12]:


coffee_data.describe().T


# In[13]:


coffee_data.loc[:,['cash_type','card','coffee_name']].describe().T

There are 1033 transactions in the data.
89 missing values in the column 'card'.
No duplicates.
2 unique values of 'cash_type'.
8 different coffee types with 'Americano with Milk' is the most popular product.
# In[14]:


coffee_data[coffee_data['card'].isnull()]['cash_type'].value_counts()


# In[15]:


coffee_data['cash_type'].hist()


# In[16]:


coffee_data['cash_type'].value_counts(normalize=True)


# In[18]:


pd.DataFrame(coffee_data['coffee_name'].value_counts(normalize=True).sort_values(ascending=False).round(4)*100)

Americano with Milk and Latte are our most popular coffee products. In the second tier are Cappuccino and Americano, while Cortado, Hot Chocolate, Espresso, and Cocoa are less popular.
# In[19]:


#Convert date and datetime to datetme format
coffee_data['date']=pd.to_datetime(coffee_data['date'])
coffee_data['datetime']=pd.to_datetime(coffee_data['datetime'])

#Create column of Month, Weekdays, and Hours
coffee_data['month']=coffee_data['date'].dt.strftime('%Y-%m')
coffee_data['day']=coffee_data['date'].dt.strftime('%w')
coffee_data['hour']=coffee_data['datetime'].dt.strftime('%H')


# In[20]:


coffee_data.info()


# In[21]:


coffee_data.head()


# In[22]:


[coffee_data['date'].min(),coffee_data['date'].max()]

The overal revenue by products.
# In[23]:


revenue_data = coffee_data.groupby(['coffee_name']).sum(['money']).reset_index().sort_values(by='money',ascending=False)


# In[27]:


plt.figure(figsize=(10,4))
ax = sns.barplot(data=revenue_data,x='money',y='coffee_name',color='steelblue')
ax.bar_label(ax.containers[0],fontsize=6)
plt.xlabel('Revenue')

Latte is the product with the highest revenue, while Expresso is the one at the bottom.
# In[28]:


monthly_sales = coffee_data.groupby(['coffee_name','month']).count()['date'].reset_index().rename(columns={'date':'count'}).pivot(index='month',columns='coffee_name',values='count').reset_index()
monthly_sales


# In[29]:


monthly_sales.describe().T.loc[:,['min','max']]


# In[30]:


plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales)
plt.legend(loc='upper left')
plt.xticks(range(len(monthly_sales['month'])),monthly_sales['month'],size='small')

Americano with Milk and Latte, and Cappuccino are top selling coffee
types, while Cocoa and Expresso have lowest sales. Additionally, Americano with Milk and Latte show an
upward trending.
# In[31]:


weekday_sales = coffee_data.groupby(['day']).count()['date'].reset_index().rename(columns={'date':'count'})
weekday_sales


# In[33]:


plt.figure(figsize=(12,6))
sns.barplot(data=weekday_sales,x='day',y='count',color='steelblue')
plt.xticks(range(len(weekday_sales['day'])),['Sun','Mon','Tue','Wed','Thur','Fri','Sat'],size='small')

Tuesday has the highest sales of the week, while sales on the other days are relatively similar.
# In[34]:


daily_sales = coffee_data.groupby(['coffee_name','date']).count()['datetime'].reset_index().reset_index().rename(columns={'datetime':'count'}).pivot(index='date',columns='coffee_name',values='count').reset_index().fillna(0)
daily_sales


# In[35]:


daily_sales.iloc[:,1:].describe().T.loc[:,['min','max']]

This is the information about the sales of each day
# In[36]:


hourly_sales =coffee_data.groupby(['hour']).count()['date'].reset_index().rename(columns={'date':'count'})
hourly_sales


# In[37]:


sns.barplot(data=hourly_sales,x='hour',y='count',color='steelblue')

Two peak hours within each day can be observed: 10:00am and 7:00pm.
# In[39]:


hourly_sales_by_coffee =coffee_data.groupby(['hour','coffee_name']).count()['date'].reset_index().rename(columns={'date':'count'}).pivot(index='hour',columns='coffee_name',values='count').fillna(0).reset_index()
hourly_sales_by_coffee


# In[44]:


fig, axs = plt.subplots(2, 4, figsize=(20, 10))  
axs = axs.flatten()  

for i, column in enumerate(hourly_sales_by_coffee.columns[1:]): 
    axs[i].bar(hourly_sales_by_coffee['hour'], hourly_sales_by_coffee[column]) 
    axs[i].set_title(f'{column}') 
    axs[i].set_xlabel('Hour') 
    axs[i].set_ylabel('Sales') 

plt.tight_layout()  
plt.show()


# In[ ]:





# In[ ]:




