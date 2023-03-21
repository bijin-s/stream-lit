
import streamlit as st
import os.path
import pathlib

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
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "streamlit-bucket"
st.write("""
# File Picker
""")
uploaded_file = st.file_uploader("Choose a CSV file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
preview = st.text_area("CSV Preview", "", height=150, key="preview")
upload_state = st.text_area("Upload State", "", key="upload_state")
def upload_to_bucket(bucket_name):
    """ Upload data to a bucket"""
     
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'creds.json')

    #print(buckets = list(storage_client.list_buckets())
    bucket = storage.Bucket(client, 'example-bucket-skytowner')

    blob = bucket.blob('uploaded_sample.csv')
    blob.upload_from_filename('sample.csv')
    
    #returns a public url
    return blob.public_url
def upload():
    if uploaded_file is None:
        st.session_state["upload_state"] = "Upload a file first!"
    else:
        data = uploaded_file.getvalue().decode('utf-8')
        parent_path = pathlib.Path(__file__).parent.parent.resolve()           
        save_path = os.path.join(parent_path, "data")
        complete_name = os.path.join(save_path, uploaded_file.name)
        upload_to_bucket(bucket_name)
     
st.button("Upload file to Sandbox", on_click=upload)

