# stdlib
import json

# third party
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# first party
from client import get_connection_attributes, submit_request
from queries import GRAPHQL_QUERIES

        
def prepare_app():
    
    with st.spinner(f'Gathering Metrics...'):
        payload = {'query': GRAPHQL_QUERIES['metrics']}
        json = submit_request(st.session_state.conn, payload)
        try:
            metrics = json['data']['metrics']
        except TypeError:
            
            # `data` is None and there may be an error
            try:
                error = json['errors'][0]['message']
                st.error(error)
            except (KeyError, TypeError):
                st.warning(
                    'No metrics returned.  Ensure your project has metrics defined '
                    'and a production job has been run successfully.'
                )
        else:
            st.session_state.metric_dict = {m['name']: m for m in metrics}
            st.session_state.dimension_dict = {dim['name']: dim for metric in metrics for dim in metric['dimensions']}
            for metric in st.session_state.metric_dict:
                st.session_state.metric_dict[metric]['dimensions'] = [
                    d['name'] for d in st.session_state.metric_dict[metric]['dimensions']
                ]
            if not st.session_state.metric_dict:
                # Query worked, but nothing returned
                st.warning(
                    'No Metrics returned!  Ensure your project has metrics defined '
                    'and a production job has been run successfully.'
                )
            else:
                st.success('Success!  Explore the rest of the app!')


st.set_page_config(
    page_title="dbt Semantic Layer - Home",
    page_icon="👋",
    layout='wide',
)

st.markdown('# Explore the dbt Semantic Layer')

st.markdown(
    """
    Use this app to query and view the metrics defined in your dbt project. It's important to note that this app assumes that you're using the new
    Semantic Layer, powered by [MetricFlow](https://docs.getdbt.com/docs/build/about-metricflow).  The previous semantic layer used the `dbt_metrics`
    package, which has been deprecated and is no longer supported for `dbt-core>=1.6`.
    
    ---
    
    To get started, input your `JDBC_URL` below.  You can find this in your project settings when setting up the Semantic Layer.
    After hitting Enter, wait until a success message appears indicating that the application has successfully retrieved your project's metrics information.
    """
)


jdbc_url = st.text_input(
    label='JDBC URL',
    value='',
    key='jdbc_url',
    help='JDBC URL is found when configuring the semantic layer at the project level',
)

if st.session_state.jdbc_url != '':
    st.cache_data.clear()
    st.session_state.conn = get_connection_attributes(st.session_state.jdbc_url)
    if 'conn' in st.session_state and st.session_state.conn is not None:
        prepare_app()

