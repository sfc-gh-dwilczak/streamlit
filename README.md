# dbt Cloud Semantic Layer on Streamlit

Use this streamlit app to view the metrics you've defined in your project.  The only thing you'll need to define is the `JDBC_URL` that you obtain from dbt Cloud.

# Developing

Clone the repo and run `poetry install`.  Activate the virtualenv created by running `poetry shell` and `pip install langchain` and `pip install openai` for LLM to work.

Finally, run your app:

```bash
streamlit run 🏠_Home.py
```
