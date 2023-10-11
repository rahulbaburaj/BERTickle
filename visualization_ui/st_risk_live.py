import pandas as pd
import streamlit as st
from bertopic import BERTopic

st.set_page_config(page_title="Risk Live", layout="wide")

st.markdown("<h1 style='text-align: center; color: DARK RED;'><b></b>RISK LIVE EVALUATION</h1>", unsafe_allow_html=True)



st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 800px;  /* Adjust this to your desired width */
    }
</style>
""", unsafe_allow_html=True)


path = '/home/azureuser/risklive/risklivepilot/models/'
topic_model = BERTopic.load(f"{path}topic_model_supplychain")
topics_over_time = pd.read_csv(f"{path}topics_over_time_supplychain.csv")


user_input_keyword = st.text_input("Enter a keyword to search for related topics", "supply chain")
if user_input_keyword!="supply chain":
    topics, probabilities = topic_model.find_topics(user_input_keyword)  
    fig1= topic_model.visualize_barchart(topics=topics)
    fig2 = topic_model.visualize_topics_over_time(topics_over_time, topics=topics)
    # st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig1, use_container_width=True, config={'responsive': True})

    st.plotly_chart(fig2, use_container_width=True, config={'responsive': True})
    representative_docs = []
    # for topic in topics:
        # representative_docs.append(topic_model.get_representative_docs(topic))
else:
    fig1=topic_model.visualize_barchart()  
    fig2=topic_model.visualize_topics_over_time(topics_over_time)
    # st.plotly_chart(fig1)
    st.plotly_chart(fig1, use_container_width=True, config={'responsive': True})
    st.plotly_chart(fig2, use_container_width=True, config={'responsive': True})
    # representative_docs = topic_model.get_representative_docs()    



