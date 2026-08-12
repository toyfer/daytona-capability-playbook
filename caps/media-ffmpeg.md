# media-ffmpeg

**What:** Batch-convert video, audio, or images with ffmpeg / ImageMagick.  
**When:** the user explicitly requests media processing.  
**Not when:** a light edit is easier with existing Python tooling.

## Setup

Profile: `media`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
ffmpeg -i in.mp4 -vn -acodec libmp3lame out.mp3
# ImageMagick on this sandbox is typically v6: use convert (magick may be absent)
convert in.png -resize 50% out.png
```

## Notes

- Prefer `convert` unless `command -v magick` succeeds (ImageMagick 7). Bootstrap accepts either.
- Do not install at session start or leave large derived files behind; use `download_file` for delivery.
