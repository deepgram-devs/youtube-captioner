# YouTube Captioner by Deepgram

This is a utility/application for creating Subtitles (ie Captions) for **existing** videos on YouTube.

## Why the YouTube Captioner?

I created this utility mainly out of necessity and selfishness.

The necessity is that adding Subtitles (ie Captions) to your YouTube videos provides:

- individuals who are hard of hearing the ability to enjoy content on YouTube
- accurate subtitles thereby indexing of your YouTube content

The selfishness is that I produce a fair amount of content and creating subtitles was time consuming to go through this manual process for creating subtitles:

- find the mp4 or video that I wanted to create subtitles for
- generate subtitles/captioning by submitting the mp4 to a Speech-to-Text service like Deepgram
- navigate to YouTube, find the video and then upload the Subtitles to said video

There is a fair amount of setup to this project. So the complexity and time is front loaded, but when configured, this utility will:

- download your video from YouTube
- convert your video to mp3 (audio only) to reduce the upload time to Deepgram
- submit the mp3 to Deepgram to obtain the transcription
- convert the transcription to SRT subtitles
- upload and **publish** the SRT subtitles to your video

This utility does all that from a single command:

```bash
python caption_youtube_video.py --url "<your videos link in youtube>"
```

Depending on the length of your video, in about 30-60 seconds, you will have published subtitles on your video.

## Prerequisites

This utility makes use of:

- [youtube-dl](https://github.com/ytdl-org/youtube-dl/) - which is a open source library to download public YouTube videos (I have been using this for years)
- [Deepgram Python SDK](https://github.com/deepgram/deepgram-python-sdk) - this generates the SRT subtitles on the [Deepgram Platform](https://console.deepgram.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3) - specifically [Google's Python YouTube Data SDK](https://developers.google.com/youtube/v3/quickstart/python)

### Info About youtube-dl

The [youtube-dl](https://github.com/ytdl-org/youtube-dl/) is used widely, but since Google doesn't like individuals downloading YouTube videos, this project is unsanctioned by Google. Google occassionally changes things that breaks this project, but after a few days, things start working again.

This does mean that you need to `git clone` this project and do a developer install of this project into `pip`. After cloning, change directory into the repo on disk and then do a `pip install -e .` to make this library available to python.

### Deepgram Transcription

[Sign up](https://console.deepgram.com/signup?utm_source=dg-streamlit-blog) for a Deepgram account and get $200 in Free Credit (up to 45,000 minutes), absolutely free. No credit card needed!

We encourage you to explore Deepgram by checking out the following resources:

- [Deepgram API Playground](https://playground.deepgram.com/?smart_format=true&language=en&model=nova-2)
- [Deepgram Documentation](https://developers.deepgram.com/docs)
- [Deepgram Starter Apps](https://github.com/deepgram-starters)

#### Set your API Key as an Environment Variable named "DEEPGRAM_API_KEY"

Create an API in the Deepgram Console. Then set your API Key as an environment variable.

If using bash, this could be done in your `~/.bash_profile` like so:

```bash
export DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
```

### YouTube Data API

You need to have a [Google Cloud account](https://console.cloud.google.com/), but if you are using YouTube, you probably don't even know you actually have one. You might need to click a button that says "Try for Free", but that would be about it.

If you have the [YouTube Data API](https://developers.google.com/youtube/v3) enabled already, you can skip this step. Navigate to your [APIs & Services Dashboard](https://console.cloud.google.com/apis/dashboard) and select the project you want use for [YouTube Data API](https://developers.google.com/youtube/v3), click `+ Enable APIs & Services` and search for `YouTube Data API v3`, and then click `Enable` to enable the API.

![API & Services](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/1-api-and-services.png)

![Enable YouTube Data API v3](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/2-search-for-youtube-data-api-v3.png)

In order to access and manage your YouTube content, you need to create an OAuth Client ID. In `APIs & Services`, click `Credentials` and then click `Create Credentials`.

![Create an OAuth Client ID](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/3-create-oauth-client-id.png)

For your OAuth Client ID settings, select `Desktop app` in the `Application type` and then create a `Name` for your OAuth Client ID.

![OAuth Client ID Settings](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/4-oauth-settings.png)

Then you need to give your OAuth Client ID access to your YouTube content. First, click `OAuth consent screen`.

![OAuth Client ID Settings](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/5-oauth-consent-screen.png)

Then access is granted by email address. Scroll down and select `+ ADD USERS` and then enter the email account associated with your YouTube account/content.

![OAuth Client ID Settings](https://raw.githubusercontent.com/deepgram-devs/youtube-captioner/main/images/5-oauth-consent-screen.png)

### ffmpeg and ffprobe

The last thing you will need is [ffmpeg and ffprobe](https://www.ffmpeg.org/download.html) installed and accessible on your `PATH`. A typical location to install something like this would be `/usr/local/bin`. If the binaries don't have execute permissions, don't forget to `chmod +x ./ffmpeg` and `chmod +x ./ffprobe`.

## Running the Utility

If you chose to set an environment variable in your shell profile (ie `.bash_profile`) you can run the example at the root of this repo like so:

```bash
python caption_youtube_video.py --url "<your videos link in youtube>"
```

or this could also be done by a simple export of the API Key before executing your Go application:

```bash
DEEPGRAM_API_KEY="YOUR_DEEPGRAM_API_KEY" python caption_youtube_video.py --url "<your videos link in youtube>"
```

That's it! No joke!

## Development and Contributing

Interested in contributing? We ❤️ pull requests!

To make sure our community is safe for all, be sure to review and agree to our
[Code of Conduct](./CODE_OF_CONDUCT.md). Then see the
[Contribution](./CONTRIBUTING.md) guidelines for more information.

## Getting Help

We love to hear from you so if you have questions, comments or find a bug in the
project, let us know! You can either:

- [Open an issue](https://github.com/deepgram-devs/youtube-captioner/issues) on this repository
- Join us on [Discord](https://dpgr.am/discord)
- Ask a question, share the cool things you're working on, or see what else we have going on in our [Community Forum](https://github.com/orgs/deepgram/discussions/)
- Tweet at us! We're [@DeepgramAI on Twitter](https://twitter.com/DeepgramAI)

## Further Reading

Check out the Developer Documentation at [https://developers.deepgram.com/](https://developers.deepgram.com/)
