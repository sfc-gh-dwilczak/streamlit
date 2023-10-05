# third party
import pandas as pd
import streamlit as st

# first party
from client import submit_request
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
                st.success('Success!  Connected to the DBT Semantic layer!')