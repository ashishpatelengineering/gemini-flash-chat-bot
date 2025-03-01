# pip install google-genai
import tempfile
import streamlit as st
import os
import time
from google import genai
from google.genai import types
from pypdf import PdfReader, PdfWriter, PdfMerger
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_page():
    """
    Set up the Streamlit page configuration, including the title, layout, and sidebar.
    """
    st.set_page_config(
        page_title="Multi-Modal Chatbot",
        layout="centered"
    )
    
    # Main header for the application
    st.header("Multi-Modal Chatbot",divider='blue')

    # Sidebar header with a divider
    st.sidebar.header("Options", divider='rainbow')

def get_choice():
    """
    Display a radio button in the sidebar for the user to choose the chat mode.
    """
    choice = st.sidebar.radio("Choose:", ["Chat with Assistant",
                                          "Chat with a PDF",
                                          "Chat with Multiple PDFs",
                                          "Chat with an Image",
                                          "Chat with Audio",
                                          "Chat with Video"])
    return choice

def get_clear():
    """
    Add a button in the sidebar to allow the user to start a new session.
    """
    clear_button = st.sidebar.button("Start new session", key="clear")
    return clear_button

def main():
    """
    Main function to handle the logic based on the user's choice of chat mode.
    """
    choice = get_choice()
    
    if choice == "Chat with Assistant":
        st.subheader("Chat with Assistant")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Initialize the chat session with the model
            chat = client.chats.create(model=MODEL_ID, config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant. Your answers need to be friendly and positive.",))
            prompt = st.chat_input("Enter your question here")
            if prompt:
                with st.chat_message("user", avatar="🟠"):
                    st.write(prompt)
        
                st.session_state.message += prompt
                with st.chat_message(
                    "assistant", avatar="🔵",  
                ):
                    response = chat.send_message(st.session_state.message)
                    st.markdown(response.text) 
                    st.sidebar.markdown(response.usage_metadata)
                st.session_state.message += response.text

    elif choice == "Chat with a PDF":
        st.subheader("Chat with a PDF")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Allow the user to upload a PDF file
            uploaded_file = st.file_uploader("Upload a PDF file", type=['pdf'], accept_multiple_files=False)
            if uploaded_file:
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Upload the file to the API
                file_upload = client.files.upload(file=tmp_file_path)
                chat2 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=file_upload.uri,
                                    mime_type=file_upload.mime_type),
                            ]
                        ),
                    ]
                )
                prompt2 = st.chat_input("Enter your question here")
                if prompt2:
                    with st.chat_message("user", avatar="🟠"):
                        st.write(prompt2)
            
                    st.session_state.message += prompt2
                    with st.chat_message(
                        "assistant", avatar="🔵",  
                    ):
                        response2 = chat2.send_message(st.session_state.message)
                        st.markdown(response2.text)
                        st.sidebar.markdown(response2.usage_metadata)
                    st.session_state.message += response2.text

    elif choice == "Chat with Multiple PDFs":
        st.subheader("Chat with Multiple PDFs")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Allow the user to upload multiple PDF files
            uploaded_files = st.file_uploader("Upload one or more PDF files", type=['pdf'], accept_multiple_files=True)
            if uploaded_files:
                # Merge all uploaded PDFs into a single file
                merger = PdfMerger()
                for file in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(file.getvalue())
                        tmp_file_path = tmp_file.name
                    merger.append(tmp_file_path)
    
                fullfile = "merged_all_files.pdf"
                merger.write(fullfile)
                merger.close()

                # Upload the merged file to the API
                file_upload = client.files.upload(file=fullfile) 
                chat2b = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=file_upload.uri,
                                    mime_type=file_upload.mime_type),
                            ]
                        ),
                    ]
                )
                prompt2b = st.chat_input("Enter your question here")
                if prompt2b:
                    with st.chat_message("user", avatar="🟠"):
                        st.write(prompt2b)
            
                    st.session_state.message += prompt2b
                    with st.chat_message(
                        "assistant", avatar="🔵",  
                    ):
                        response2b = chat2b.send_message(st.session_state.message)
                        st.markdown(response2b.text)
                        st.sidebar.markdown(response2b.usage_metadata)
                    st.session_state.message += response2b.text
            
    elif choice == "Chat with an Image":
        st.subheader("Chat with an Image")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Allow the user to upload an image
            uploaded_file = st.file_uploader("Upload an image (PNG or JPEG)", type=['png','jpg'], accept_multiple_files=False)
            if uploaded_file:
                # Display the uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Upload the file to the API
                file_upload = client.files.upload(file=tmp_file_path)
                chat3 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=file_upload.uri,
                                    mime_type=file_upload.mime_type),
                            ]
                        ),
                    ]
                )
                prompt3 = st.chat_input("Enter your question here")
                if prompt3:
                    with st.chat_message("user", avatar="🟠"):
                        st.write(prompt3)
            
                    st.session_state.message += prompt3
                    with st.chat_message(
                        "assistant", avatar="🔵",  
                    ):
                        response3 = chat3.send_message(st.session_state.message)
                        st.markdown(response3.text)
                    st.session_state.message += response3.text
                
    elif choice == "Chat with Audio":
        st.subheader("Chat with Audio")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Allow the user to upload an audio file
            uploaded_file = st.file_uploader("Upload an audio file (MP3 or WAV)", type=['mp3','wav'], accept_multiple_files=False)
            if uploaded_file:
                # Display the uploaded audio file
                st.audio(uploaded_file, format="audio/wav")
                
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Upload the file to the API
                file_upload = client.files.upload(file=tmp_file_path)
                chat4 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=file_upload.uri,
                                    mime_type=file_upload.mime_type),
                            ]
                        ),
                    ]
                )
                prompt5 = st.chat_input("Enter your question here")
                if prompt5:
                    with st.chat_message("user", avatar="🟠"):
                        st.write(prompt5)
            
                    st.session_state.message += prompt5
                    with st.chat_message(
                        "assistant", avatar="🔵",  
                    ):
                        response4 = chat4.send_message(st.session_state.message)
                        st.markdown(response4.text)
                    st.session_state.message += response4.text

    elif choice == "Chat with Video":
        st.subheader("Chat with Video")
        clear = get_clear()
        if clear:
            if 'message' in st.session_state:
                del st.session_state['message']
    
        if 'message' not in st.session_state:
            st.session_state.message = " "
        
        if clear not in st.session_state:
            # Allow the user to upload a video file
            uploaded_file = st.file_uploader("Upload a video file (MP4 or MOV)", type=['mp4','mov'], accept_multiple_files=False)
            if uploaded_file:
                # Display the uploaded video file
                st.video(uploaded_file, format="video/mp4")
                
                # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Upload the file to the API
                video_file = client.files.upload(file=tmp_file_path)
                while video_file.state == "PROCESSING":
                    time.sleep(10)
                    video_file = client.files.get(name=video_file.name)
                
                if video_file.state == "FAILED":
                    raise ValueError(video_file.state)
                
                chat5 = client.chats.create(model=MODEL_ID,
                    history=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(
                                    file_uri=video_file.uri,
                                    mime_type=video_file.mime_type),
                            ]
                        ),
                    ]
                )
                prompt4 = st.chat_input("Enter your question here")
                if prompt4:
                    with st.chat_message("user",avatar="🟠"):
                        st.write(prompt4)
            
                    st.session_state.message += prompt4
                    with st.chat_message(
                        "assistant", avatar="🔵",
                    ):
                        response5 = chat5.send_message(st.session_state.message)
                        st.markdown(response5.text)
                    st.session_state.message += response5.text
                    
if __name__ == '__main__':
    setup_page()
    api_key = os.environ.get('GOOGLE_API_KEY')
    client = genai.Client(api_key=api_key)
    MODEL_ID = "gemini-2.0-flash-001"
    main()
