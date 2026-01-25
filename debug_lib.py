from youtube_transcript_api import YouTubeTranscriptApi

try:
    api = YouTubeTranscriptApi()
    vid = '5MgBikgcWnY'
    transcript = api.fetch(vid, languages=['en'])
    print(f"Type: {type(transcript)}")
    if isinstance(transcript, list):
        print(f"First item type: {type(transcript[0])}")
        print(f"First item: {transcript[0]}")
    else:
        print(f"Content: {transcript}")
        # try iterating
        for item in transcript:
            print(f"Item: {item}")
            break
except Exception as e:
    print(e)
