import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from projects import Projects
from utils import clean_text

def create_streamlit_app(llm, projects, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.amazon.jobs/en/jobs/2888725/sde-ii-amazon")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            projects.load_projects()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = projects.query_links(skills)
                email = llm.write_mail(job, links)

                # Use a text area to display the email
                st.text_area("Generated Email", email, height=400)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    projects = Projects()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, projects, clean_text)
