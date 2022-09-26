import os

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.bq_utils import fetch_release_data
from utils.config import get_config
from utils.helper import get_keys_from_dict, left_join_lists

st.title('Google Cloud Release Notes')
config = get_config()
default_selection = ['Cloud Spanner', 'Dataflow', 'Pub/Sub', 'BigQuery', 'BigQuery ML','Cloud Storage', 'Vertex AI', 'Document AI', 'Dataform']
time_range = ["7", "14", "30", "60", "90"]

days_ago_selector = st.sidebar.selectbox("Time Range (Days Ago)", time_range)

@st.cache
def release_data(days_ago):
    data = fetch_release_data(days_ago)
    return data


with st.spinner('Updating Report...'):
    ## Data
    # Metrics setting and rendering

    gcp_service_df = release_data(days_ago_selector)

    gcp_service_list = gcp_service_df['product_name'].unique()
    release_note_type = gcp_service_df['release_note_type'].unique()


    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Releases", len(gcp_service_df))
    col2.metric("Total Features", len(gcp_service_df[gcp_service_df.release_note_type == "FEATURE"]))
    col3.metric("Total Fixes", len(gcp_service_df[gcp_service_df.release_note_type == "FIX"]))
    col4.metric("Total Issues Raised", len(gcp_service_df[gcp_service_df.release_note_type == "ISSUE"]))


    col_summary1, col_summary2= st.columns(2)
    product_name_df = gcp_service_df.product_name.value_counts()
    product_name_df = product_name_df.reset_index()
    product_name_df.columns = ['Product', 'Count']
    col_summary1.subheader('Product summary')
    col_summary1.dataframe(product_name_df, use_container_width=True)
    col_summary2.subheader('Release Type Summary')
    release_note_type_df =gcp_service_df.release_note_type.value_counts()
    release_note_type_df = release_note_type_df.reset_index()
    release_note_type_df.columns = ['Release Type', 'Count']
    col_summary2.dataframe(release_note_type_df, use_container_width=True)
    #
    # fig = px.pie(release_note_type_df, values='Count', names='Release Type')
    # st.plotly_chart(fig)
    #
    # fig = px.pie(product_name_df, values='Count', names='Product')
    # st.plotly_chart(fig)




    st.header("Release Details")
    col_service1, col_service2 = st.columns(2)
    service_list = col_service1.multiselect('Choose Service', gcp_service_list, default='BigQuery', help='Which Services do you want to explore')
    release_type = col_service2.multiselect('Release Type', release_note_type, default='FEATURE')

    filtered_service_list = gcp_service_df[gcp_service_df['product_name'].isin(service_list) & gcp_service_df['release_note_type'].isin(release_type)]

    df_table = filtered_service_list[['product_name', 'release_note_type', 'description']]
    st.table(df_table)


if __name__ == '__main__':
    data = fetch_release_data(7)
    fo="me"