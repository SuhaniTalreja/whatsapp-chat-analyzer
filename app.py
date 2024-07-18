import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    #converting bytes to string
    data= bytes_data.decode("utf-8")

    # preprocessing our chats
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis with respect to",user_list)

    if st.sidebar.button("Show Analysis") :

        # STATS AREA
        num_msgs,words,num_media_msgs,num_links = helper.fetch_stats(selected_user,df)
        st.title("TOP STATISTICS")
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_msgs)
        with col3:
            st.header("Links Shared")
            st.title(num_links)

        # TIMELINES

        # monthly
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='pink')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Busiest Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='magenta')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Busiest Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='magenta')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # HEATMAP
        st.title("Weekly Activity Heatmap")
        activity_table = helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax = sns.heatmap(activity_table,cmap='coolwarm')
        st.pyplot(fig)


        # FINDING THE BUSIEST USERS IN THE GROUP (GROUP LEVEL ONLY)
        if selected_user=='Overall':
            st.title("Most Busy Users")
            x , new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='yellow')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
        # WORDCLOUD
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # MOST COMMON WORDS
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        # EMOJI ANALYSIS
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
    