from pytube import YouTube
from pydub import AudioSegment
from pytube import Playlist
import os
from glob import glob
import random
#TODO: nzabbat el indexing bta3 el segments
#TODO: nektafy be sanya?
#TODO: create a df that stores in the names of the sewar using regex (/سورة\s[الء-ي]+/gm)(get what's before سورة and after l7ad a5er whitespace we abl ama anazl ha-check 3al esm be nafs el logic , law el list de feha sora mel swar de , harandomize taany)

def random_slicer(input_list, num_items=3):
    # Make a copy of the input list to avoid modifying the original list
    input_list = list(input_list)
    shuffled_list = input_list.copy()

    # Shuffle the list randomly
    random.shuffle(shuffled_list)

    # Slice the first 'num_items' elements from the shuffled list
    sliced_items = shuffled_list[:num_items]

    return sliced_items


def download_youtube_audio(url, output_path):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only("mp4")
    print(f'Downloading {audio_stream.title}')
    audio_stream.download(output_path)

def download_audio_from_playlist(url, output_path):
    playlist = Playlist(url)
    urls = playlist.video_urls
    shuffled_playlist = random_slicer(urls,3)
    for url in shuffled_playlist:
        download_youtube_audio(url, output_path)


def split_audio(input_path,prefix, output_path, segment_length=60 * 1000):  # 60 seconds in milliseconds
    audio = AudioSegment.from_file(input_path)

    # Calculate the number of segments
    num_segments = len(audio) // segment_length

    # Split the audio into segments
    for i in range(num_segments):
        start_time = i * segment_length
        end_time = (i + 1) * segment_length
        segment = audio[start_time:end_time]

        # Save each segment
        output_filename = f"{prefix}_segment_{i + 1}.mp3"
        segment.export(os.path.join(output_path, output_filename), format="mp3")

if __name__ == "__main__":
    # List of YouTube video URLs
    video_urls = [
        "https://www.youtube.com/playlist?list=PLSE-KCHIEexiq2fLNI_wXvy7GE2ZsscnA",

    ]

    output_dir = "output_audio"
    os.makedirs(output_dir, exist_ok=True)

    for i, url in enumerate(video_urls):
        # Download audio
        # download_audio_from_playlist(url, output_dir)
        audio_file_path = glob(os.path.join(output_dir,"*.mp4"))
        for audio in audio_file_path:
            prefix = f"video_{i + 1}"
            split_audio(audio,prefix, output_dir)

    print("Audio downloading and segmentation completed.")