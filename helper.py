import emoji.unicode_codes
from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud;
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns

# users stats
def fetch_stats(selected_user,df,chat_format):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. number of messages
    num_messages = df.shape[0]
    # 2. number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())
    # 3. number of media msgs
    if chat_format == 'Android':
        media_msg_pattern = r"<Media omitted>\n"
    else:  # iPhone
        media_msg_pattern = r"image omitted"
    num_media_msgs = df[df['message'].str.contains(media_msg_pattern)].shape[0]
    # 4. number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_msgs,len(links)

# busiest user
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})
    return x,df

# wordcloud
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words= f.read()

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "null\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,
                   min_font_size=10,
                   background_color='white'
                   )
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

# most common words
def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words= f.read()

    temp = df[df['user']!='group_notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]
    temp = temp[temp['message'] != "null\n"]

    words=[]
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# EMOJI ANALYSIS
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df 

# timeline - monthly
def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

# timeline - daily
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    return daily_timeline

# timeline - week activity
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


# HEATMAP OF ACTIVITY 
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_table = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_table
