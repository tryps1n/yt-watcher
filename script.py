from google import genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import time

GEMINI_API_KEY = "AIzaSyCNc8L5Fs5YYf73jH6xz1DlCgFRrlLfG1Q"
YT_API_KEY = "AIzaSyAcnJUalBErwLO8gM-yxF0gfnCn6SInNjA"

CHANNEL_IDS = {
    "AndrejKarpathy" : "UCXUPKJO5MZQN11PqgIvyuvQ",
    "ohnepixel": "UC3ti8PjJczdDKHSwk7TESkw"
}

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

client = genai.Client(api_key=GEMINI_API_KEY)

ytt_api = YouTubeTranscriptApi()

def get_uploads_playlist_id(channel_id):
    request = youtube.channels().list(
        part='contentDetails', 
        id=channel_id
    ) 
    response = request.execute()
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return uploads_id

def get_recent_videos(uploads_playlist_id, limit=5):
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=uploads_playlist_id,
        maxResults=limit
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        videos.append(item['contentDetails']['videoId'])
    return videos

def get_video_topic(video_ids):
    topics = {}
    for video in video_ids:
        transcript = ytt_api.fetch(video)
        raw_text = ""
        for snippet in transcript:
            raw_text += snippet.text

        response = client.models.generate_content(
            model='gemini-2.5-flash-lite', contents=f"Summarise the topic of the following video transcript provided in about 10 words. {raw_text[:200]}"
        )
        topics[video] = response.text

        time.sleep(2)
    
    return topics

uploads_id = get_uploads_playlist_id(CHANNEL_IDS["ohnepixel"])

recent_videos = get_recent_videos(uploads_id)

video_id = recent_videos[0]

print(get_video_topic(recent_videos))