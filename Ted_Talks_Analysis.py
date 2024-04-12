#!/usr/bin/env python
# coding: utf-8

# ## Importing the libraries

# In[1]:


#to read the dataframe
import pandas as pd

#to plot
import matplotlib.pyplot as plt
import seaborn as sns


# ## Reading the dataset as a dataframe

# In[2]:


# Reading dataframe
df = pd.read_csv('ted_main.csv')


# In[3]:


df['film_date'] = pd.to_datetime(df['film_date'], unit='s')
df['published_date'] = pd.to_datetime(df['published_date'], unit='s')


# In[4]:


df


# ## Discovering the dataset 

# In[5]:


#show the number of cells in the dataframe
print("dataset size: ", df.size)

#show the number of records (rows) in the dataframe
print("number of talks: ", len(df))

#show the number of features (columns) in the dataframe
print("number of features: ", len(df.columns)) 


# In[6]:


df.describe()


# In[7]:


df.dtypes


# In[8]:


#show the number of null values in each column with non-zero null values
nulls = df.isnull().sum()
nulls[nulls > 0]


# In[9]:


# Create a new DataFrame with only the duplicate rows
duplicate_rows = df[df.duplicated()]
print("Number of duplicate rows: ", duplicate_rows.size)


# In[10]:


df.head()


# ## Data Visualization 

# ### 1- Most viewed talks
# First step towards conducting the best TED-talk ever, is getting to know the competition. We will start with finding the most viewed talks so far on TED.

# In[11]:


pop_talks = df[['name', 'main_speaker', 'views', 'published_date']].sort_values('views', ascending=False)[:15]
pop_talks


# <b> Observations: </b>
# <ul>
#     <li>Do schools kill creativity? by Sir Ken Robinson	is the most viewed talk with almost <b> 48 million</b> views.
#     <li>Robinson's talk is closely followed by Amy Cuddy's talk on Your Body Language May Shape Who You Are.
#     <li>There are only 2 talks that have surpassed the <b> 40 million </b> mark and <b> 4 talks </b> that have crossed the <b> 30 million </b> mark.
# </ul>

# Let's plot these plots in a bar chart

# In[12]:


sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
g = sns.barplot(x='main_speaker', y='views', data=pop_talks)
plt.xticks(rotation=90)


# Okay, so the competition is tough, but aren't all worthy competitions are? let us investigate the summary statistics and the distribution of the views on various TED Talks.

# In[13]:


# The default plot for distplot is histogram so the videos are divided into equal-sized bins,
# kde = true shows a kernel density estimate to the data
sns.displot(df['views'], kde =True)
plt.ylim(1,600)
plt.xlim(0,1e7)


# In[14]:


df['views'].describe()


# <b>Observations</b>
# <ul>
#     <li> The average number of views on TED Talk videos is nearly <b> 2 million </b> and the median is <b> 1.7 million.</b> Good news! TED is popular. <b>If you ace your TED talk, your ideas will reach a large number of people. </b> </li>
# </ul>

# ### 2- Analysing TED Talks by the month and the year
# What are the most frequent times for TED talks? How many months do you have left to prepare? We need to know when will the battle take place!

# In[15]:


df['month'] = df['film_date'].dt.month


# In[16]:


df['year'] = df['film_date'].dt.year


# In[17]:


month_df = pd.DataFrame(df['month'].value_counts()).reset_index()

month_df.columns = ['month', 'talks']

month_df


# In[18]:


plt.figure(figsize = (6,6))
sns.barplot(x='month', y='talks', data=month_df)


# **February** is clearly the most popular month for TED Conferences followed by **March** whereas **August** and **January** are the least popular. February's popularity is largely due to the fact that the official TED Conferences are held in February.

# Finally, let's see how ted has grown over the year to see if it is truly worth it.

# In[19]:


year_df = pd.DataFrame(df['year'].value_counts().reset_index())

year_df.columns = ['year', 'talks']

year_df = year_df.sort_values('year')

plt.figure(figsize=(18,5))
sns.pointplot(x='year', y='talks', data=year_df)


# **Observation**
# <ul>
#     <li>It appears that the number of talks have been increasing over the years and truly spiked in <b>2009.</b>
#     <li>There is a sharp decrease in <b> 2017 </b></li>

# ### 3- Now let's see who is the most popular TED Talker
# To beat them you have to join them. Who are the most likely to be invited on TED?

# In[20]:


# First, seeing type of ted talk event
df['event'].value_counts()


# In[21]:


speaker_df = df.groupby('main_speaker').count().reset_index()[['main_speaker', 'views']]
speaker_df.columns = ['main_speaker', 'appearances']
speaker_df = speaker_df.sort_values('appearances', ascending=False)
speaker_df.head(10)


# **Hans Rosling** the mexican-amerian businessman & author and **Juan Enriquez** the Swedish physician have the most talks on TED. 

# ### 4- What about the occupation of the speakers? Is there a special job that TED prefers its speakers to have?

# In[22]:


occupation_df = df[df['speaker_occupation']!= 'Unknown'].groupby('speaker_occupation').count().reset_index()[['speaker_occupation', 'views']]
occupation_df.columns = ['occupation', 'appearances']
occupation_df = occupation_df.sort_values('appearances', ascending=False)
occupation_df


# In[23]:


plt.figure(figsize=(15,5))
sns.barplot(x='occupation', y='appearances', data=occupation_df.head(10))


# **Observations :**
# <ul>
#     <li> <b> Writers</b> are the most popular with more than 40 speakers identifying themselves as the aforementioned. </li>
#     <li> <b>Artist and Designer </b> come in second and third place with near results </li>
# </ul>

# ### 5- Ted Languages

# One remarkable aspect of TED Talks is the sheer number of languages in which it is accessible. Let us perform some very basic data visualisation and descriptive statistics about languages at TED.

# In[24]:


df['languages'].describe()


# On average, a TED Talk is available in 27 different languages. The maximum number of languages a TED Talk is available in is a staggering 72. Let us check which talk this is.

# In[25]:


df[df['languages'] == 72]


# The most translated TED Talk of all time is Matt Cutts' Try Something New in 30 Days. The talk does have a very universal theme of exploration. The sheer number of languages it's available in demands a little more inspection though as it has just over 8 million views, far fewer than the most popular TED Talks.

# #### 1. Filter for talks that have a minimum of 1 million views (include only "view_count" and "speaker_name" in the subdataframe):

# In[26]:


# Get a subset of the data with the required number of views
df_more_than_1million = df.loc[df.views >= 1000000,['main_speaker','views']]
df_more_than_1million


# #### 2. Filter all talks that have a comment count greater than 2,000 and are given by speakers with the occupation of "Artist":

# In[27]:


# Get a subset of the data with artist as an occupation and the number of comments greater than 2000
df_commented_artists = df.loc[(df.comments > 2000) & (df.speaker_occupation == 'Artist')]
df_commented_artists


# #### 3. Filter all talks that have a duration of more than 60 minutes:

# In[28]:


df_long_duration = df.loc[df.duration > 3600]
df_long_duration


# #### 4. Filter talks where the number of comments is greater than or equal to the duration:

# In[29]:


df_high_comments = df.loc[df.comments >= df.duration]
df_high_comments


# #### 5. Filter talks where the duration is not greater than nor equal to the average duration:

# In[30]:


df_short_talks = df.loc[~(df.duration >= df.duration.mean())]
df_short_talks


# #### 6. Select the speaker name of the highest talk in views which published in Jan or Aug and its speaker is "Journalist" or "Entrepreneur" and its duration is less than 3 min:

# In[31]:


# Filter talks that were published in either January or August
df['published_month'] = pd.to_datetime(df['published_date']).dt.month

df_jan_aug = df.loc[(df['published_month'] == 1) | (df['published_month'] == 8)]


# Filter talks with speakers who are journalists or entrepreneurs
df_journalists_entrepreneurs = df_jan_aug.loc[(df_jan_aug['speaker_occupation'] == 'Journalist') | (df_jan_aug['speaker_occupation'] == 'Entrepreneur')]

# Filter talks with a duration of less than 8 minutes (480 seconds)
df_below_8m_talks = df_journalists_entrepreneurs.loc[df_journalists_entrepreneurs['duration'] < 480]


# Get the talk with the highest views
highest_view_talk_speaker = df_below_8m_talks.loc[:,['main_speaker','views']].sort_values(by='views',ascending=False)[:1]
highest_view_talk_speaker


# #### 7. Select the name, speaker_name, and event columns for all talks with a view_count that is greater than 3 times the standard deviation of the view_count:

# In[32]:


df_talks_more_than_std = df.loc[df['views'] > (df['views'].mean() + 3 * df['views'].std()), ['name', 'main_speaker', 'event']]
df_talks_more_than_std 


# In[ ]:




