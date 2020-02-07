#!/usr/bin/env python
# coding: utf-8

# In[23]:


# Import the libraries that we will use for this project 
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as numpy


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M" # URL of where the data is located 
text_result = requests.get(url).text
Data = BeautifulSoup(text_result, 'lxml') 

# Time to create the DataFrame 
name_of_dataFrame_columns = ['Postal Code' , 'Borough' , 'Neighbourhood']
Toronto_Neighbourhoods_DataFrame = pd.DataFrame(columns = name_of_dataFrame_columns) # Created a dataframe with the appropriate column names as necessary 

content = Data.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0 # Set postal code equal to 0
borough = 0 # Set borough equal to 0 
neighborhood = 0 # Set neighbourhood to 0 

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0:
            postcode = td.text
            i = i + 1
        elif i == 1:
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','')
    Toronto_Neighbourhoods_DataFrame = Toronto_Neighbourhoods_DataFrame.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True) # Append the values to the df


Toronto_Neighbourhoods_DataFrame = Toronto_Neighbourhoods_DataFrame[Toronto_Neighbourhoods_DataFrame.Borough!='Not assigned']
Toronto_Neighbourhoods_DataFrame = Toronto_Neighbourhoods_DataFrame[Toronto_Neighbourhoods_DataFrame.Borough!= 0]
Toronto_Neighbourhoods_DataFrame.reset_index(drop = True, inplace = True)
i = 0
for i in range(0,Toronto_Neighbourhoods_DataFrame.shape[0]):
    if Toronto_Neighbourhoods_DataFrame.iloc[i][2] == 'Not assigned':
        Toronto_Neighbourhoods_DataFrame.iloc[i][2] = Toronto_Neighbourhoods_DataFrame.iloc[i][1]
        i = i+1
                                 
df = Toronto_Neighbourhoods_DataFrame.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head()
# Print the first 5 rows of the data frame 


# In[20]:


DataFrame_1= df.dropna()# Remove the missing values 
empty = 'Not assigned' # Have the empty values as not assigned as per the assignment speficiations 
DataFrame_1 = df[(df.Postalcode != empty ) & (df.Borough != empty) & (df.Neighborhood != empty)


# In[21]:


def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
grp = df.groupby(['Postalcode', 'Borough'])
DataFrame_Answer= grp.apply(neighborhood_list).reset_index(name='Neighborhood')

print(DataFrame_Answer.shape) # Use the shape method 
DataFrame_Answer.head(10) #Return the first 10 rows of the data frame 


# In[22]:


print('The DataFrame shape is', DataFrame_Answer.shape) #Use the shape method to return a tuple of the dimensions of the dataframe


# In[ ]:




