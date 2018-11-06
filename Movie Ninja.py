
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[147]:

metadata=pd.read_csv("movie_metadata_with_score_metacritic.csv", index_col="Unnamed: 0") #Reading in metacritic dataset
metadata=metadata.loc[~metadata["metacritic_metascore"].isna()] #Removing rows with no metacritic data
metadata=metadata.drop(["homepage","keywords","overview","status","tagline","imdb_metascore"],1) #dropping unwanted columns
metadata=metadata.drop_duplicates() #dropping duplicates
metadata["release_year"]=metadata.release_date.str[0:4].astype(int)#creating column for year to compare with other dataset

#fixing missing information
metadata.at[4267,"title"]="Batman: The Movie"
metadata.at[4267,"original_title"]="Batman: The Movie"
metadata.at[4267,"metacritic_metascore"]=71.0
metadata.drop([3647],inplace=True)


# In[131]:


rev_data=pd.read_csv("Revenue.csv") #reading in revenue dataset
rev_data=rev_data.rename(columns={"Movie":"title"}) #changing title to match other dataset
rev_data=rev_data.drop_duplicates() #removing duplicates

#Adjusting the units to match
rev_data["Budget"]=rev_data["Budget($M)"]*1000000
rev_data["Worldwide Gross"]=rev_data["Worldwide Gross($M)"]*1000000
rev_data["Domestic Gross"]=rev_data["Domestic Gross($M)"]*1000000
rev_data=rev_data.drop(["Budget($M)","Domestic Gross($M)","Worldwide Gross($M)"],1)


# In[102]:


critic_revenue=metadata.merge(rev_data,on="title") #merging datasets
critic_revenue=critic_revenue.drop_duplicates() #dropping duplicates
critic_revenue=critic_revenue.loc[(critic_revenue["Worldwide Gross"]!=0) | (critic_revenue["revenue"]!=0)] #removing rows with no revenue data
critic_revenue=critic_revenue.loc[(np.abs(critic_revenue.release_year-critic_revenue.Year)<=5)] #removing rows where the years are far apart
