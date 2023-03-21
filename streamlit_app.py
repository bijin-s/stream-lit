import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string()
    return content

bucket_name = "examplesx111"
file_path = "Only.csv"

content = read_file(bucket_name, file_path)

# Print results.
for line in content.strip().split("\n"):
   
    st.write(line.split("")[0])
