import os

import alt as alt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils.bq_utils import fetch_release_data
from utils.config import get_config
from utils.helper import get_keys_from_dict, left_join_lists

st.title('Google Cloud Release Notes')
config = get_config()
data_services = ['Cloud Spanner', 'Dataflow', 'Pub/Sub', 'BigQuery', 'BigQuery ML','Cloud Storage', 'Vertex AI', 'Document AI', 'Dataform']
time_range = ["7", "14", "30", "60", "90"]

days_ago_selector = st.sidebar.selectbox("Time Range (Days Ago)", time_range)


@st.cache
def release_data(days_ago):
    data = fetch_release_data(days_ago)
    return data


with st.spinner('Updating Report...'):
    # Fetch the data from BQ and Cache the results
    gcp_service_df = release_data(days_ago_selector)

    # List of all GCP Services that have had an update
    gcp_service_list = gcp_service_df['product_name'].unique()
    # List of all GCP Release Types that have had an update
    release_note_type = gcp_service_df['release_note_type'].unique()


    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Releases", len(gcp_service_df))
    col2.metric("Total Features", len(gcp_service_df[gcp_service_df.release_note_type == "FEATURE"]))
    col3.metric("Total Fixes", len(gcp_service_df[gcp_service_df.release_note_type == "FIX"]))
    col4.metric("Total Issues Raised", len(gcp_service_df[gcp_service_df.release_note_type == "ISSUE"]))

    tab1, tab2 = st.tabs(["Tables", "Charts"])

    with tab1:
        # Show the data in table format
        col_summary1, col_summary2 = st.columns(2)
        col_summary1.subheader('Product summary')
        product_name_df = gcp_service_df.product_name.value_counts()
        product_name_df = product_name_df.reset_index()
        product_name_df.columns = ['Product', 'Count']
        col_summary1.dataframe(product_name_df, use_container_width=True)

        col_summary2.subheader('Release Type Summary')
        release_note_type_df =gcp_service_df.release_note_type.value_counts()
        release_note_type_df = release_note_type_df.reset_index()
        release_note_type_df.columns = ['Release Type', 'Count']
        col_summary2.dataframe(release_note_type_df, use_container_width=True)

    with tab2:
        # Show the data in charts
        st.subheader('Product Summary')
        fig_product = px.bar(
            product_name_df,
            x="Product",
            y="Count",
            color="Product",
            text="Count",
        )

        st.plotly_chart(fig_product)

        st.subheader('Release Type Summary')
        fig_release = px.bar(
            release_note_type_df,
            x="Release Type",
            y="Count",
            color="Release Type",
            text="Count",
        )

        st.plotly_chart(fig_release)

    container1 = st.container()

    st.header("Release Details")
    col_service1, col_service2 = st.columns(2)
    # Retreive the gcp services groupings from the config file
    gcp_data_services_groups = get_keys_from_dict(config['gcp_data_services_groups'])

    with container1:
        # The 'All Services' options in not in the config file. It is appended to the list so that is maybe an option
        pregrouped_service_list = col_service1.radio(label="Filter Services By",
                                                     options=['All Services']+gcp_data_services_groups, index=0)

    container2 = st.container()
    col_service3, col_service4 = st.columns(2)

    if pregrouped_service_list != 'All Services':
        gcp_service_list = config['gcp_data_services_groups'][pregrouped_service_list]
    else:
        #By Default gcp_service_list will contain all the service that have been released
        pass

    with container2:
        service_list = col_service3.multiselect('Choose Service', gcp_service_list, default=gcp_service_list,
                                                help='Which Services do you want to explore')
        release_type = col_service4.multiselect('Release Type', release_note_type, default='FEATURE')

    # Filter the Cached Dataframe with the above filter criteria
    filtered_service_list = gcp_service_df[gcp_service_df['product_name'].isin(service_list) &
                                           gcp_service_df['release_note_type'].isin(release_type)]

    # Display only the relevant columns of the data frame
    df_table = filtered_service_list[['product_name', 'release_note_type', 'description']]
    st.table(df_table)


if __name__ == '__main__':
    data = fetch_release_data(7)