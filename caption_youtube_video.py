import os
from dotenv import load_dotenv
import youtube_dl
import logging, verboselogs
import json
from time import sleep
import httpx
import argparse

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)

from deepgram_captions import (
    srt,
    webvtt,
    DeepgramConverter,
)

# environment
load_dotenv()

def transcribe_file(deepgram, payload):
    options = PrerecordedOptions(
        model="nova",
        smart_format=True,
        utterances=True,
        punctuate=True,
        diarize=True,
    )
            
    for i in range(1, 10):
        try:
            transcription_response = deepgram.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )
        except httpx.WriteTimeout as err:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(err).__name__, err.args)
            print(message)
        else:
            return transcription_response
        sleep(5)
        # print(f"Retry {i}...")

    raise Exception("Failed to transcribe file!")

def main(args):
    try:
        # download from youtube
        ydl_opts = {
            "outtmpl": "%(id)s.%(ext)s",
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        ydl = youtube_dl.YoutubeDL(ydl_opts)

        with ydl:
            video = ydl.extract_info(
                args.url,
                download=False,
            )

        sourceFilename = video["id"] + ".mp3"
        transcriptionFilename = video["id"] + ".json"
        captionFilename = video["id"] + ".srt"
        
        if os.path.isfile(sourceFilename):
            print(f"Delete leftover source file ({sourceFilename})!")
            os.remove(sourceFilename)

        if os.path.isfile(captionFilename):
            print(f"Delete leftover caption file ({captionFilename})!")
            os.remove(captionFilename)

        with ydl:
            video = ydl.extract_info(
                args.url,
            )

        # small delay
        sleep(5)

        # get the transcription for the audio file
        # config = DeepgramClientOptions(
        #     verbose=logging.DEBUG, # WARNING, VERBOSE, DEBUG, SPAM
        # )
        # deepgram = DeepgramClient("", config)
        deepgram = DeepgramClient()

        with open(sourceFilename, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        transcription_response = transcribe_file(deepgram, payload)

        # obtain the captioning from the transcription and save to file
        if os.path.isfile(transcriptionFilename):
            print(f"Delete leftover transcript file ({transcriptionFilename})!")
            os.remove(transcriptionFilename)

        rawJson = transcription_response.to_json()
        transcriptionFile = open(transcriptionFilename, "w")
        transcriptionFile.write(rawJson)
        transcriptionFile.close()

        # save caption to file
        myJson = json.loads(rawJson)

        captioner = DeepgramConverter(myJson)
        captions = srt(captioner, 10)

        captionFile = open(captionFilename, "w")
        captionFile.write(captions)
        captionFile.close()

        # TODO: take a second to review the caption file
        print("\n\nTake a second to review and replace the 'Speaker 0', 'Speaker 1', etc.")
        print(f"with the actual speaker names in the {captionFilename} file.")
        print("")
        print("TODO: provide an option to map Speaker 0, Speaker 1, etc. to actual names.")
        print("")
        input("Then press enter to continue.\n\n")

        # upload to youtube
        oauthClient = os.getenv("GOOGLE_OAUTH_CLIENT", None)
        flow = InstalledAppFlow.from_client_secrets_file(oauthClient, ["https://www.googleapis.com/auth/youtube.force-ssl"])
        credentials = flow.run_console()
        youtube = build("youtube", "v3", credentials=credentials)

        # delete existing captions?
        if not args.skip:
            results = youtube.captions().list(
                part="snippet",
                videoId=video["id"]
            ).execute()

            for item in results["items"]:
                caption_id = item["id"]
                name = item["snippet"]["name"]
                language = item["snippet"]["language"]
                
                print("Deleting caption track '%s(%s)' in '%s' language." % (name, caption_id, language))
                youtube.captions().delete(
                    id=caption_id
                ).execute()

        # upload new caption
        insert_result = youtube.captions().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    videoId=video["id"],
                    language="en",
                    name="Default",
                    isDraft=False
                )
            ),
            media_body=captionFilename
        ).execute()

        id = insert_result["id"]
        name = insert_result["snippet"]["name"]
        language = insert_result["snippet"]["language"]
        status = insert_result["snippet"]["status"]
        print("Uploaded caption track '%s(%s) in '%s' language, '%s' status." % (name, id, language, status))

        # clean up
        if os.path.isfile(sourceFilename):
            print(f"Cleaning up source file ({sourceFilename})!")
            os.remove(sourceFilename)

        print("Done!")

    except Exception as err:
        print(f"Exception: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--skip')
    parser.add_argument('-u', '--url')
    args = parser.parse_args()

    main(args)
