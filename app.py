import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()  # Load all the env variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled # Correct import


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a Youtube Video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
with 250 words. please provide the summary of the text given here: """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
        return transcript

    except TranscriptsDisabled as e:
        st.error("Subtitles are disabled for this video.")
        st.stop()  # Stop execution if subtitles are disabled

    except Exception as e:
        raise e

# generate detailed content using Google's Gemini Pro model based on provided transcript text and a prompt.
def generate_gemini_content(transcript_text, prompt):

  model=genai.GenerativeModel("gemini-pro")
  response=model.generate_content(prompt+transcript_text)
  return response.text


# Streamlit interface
header = """
<div style="background-color: #EDF3FA; padding: 2px; text-align: center;">
    <h1 style="color: #333;">YouTube Video Transcript Summarizer</h1>
</div>
"""
st.markdown(header, unsafe_allow_html=True)

# Content
youtube_link = st.text_input("Enter YouTube Video Link:")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)