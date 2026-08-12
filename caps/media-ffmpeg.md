# media-ffmpeg

**What:** Batch-convert video, audio, or images with ffmpeg / ImageMagick.  
**When:** the user explicitly requests media processing.  
**Not when:** a light edit is easier with existing Python tooling.

## Setup

Profile: `media`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
ffmpeg -i in.mp4 -vn -acodec libmp3lame out.mp3
convert in.png -resize 50% out.png
```

Do not install at session start or leave large derived files behind; use `download_file` for delivery.
