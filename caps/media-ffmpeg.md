# media-ffmpeg

**What:** ffmpeg / ImageMagick による動画・音声・画像バッチ。  
**When:** ユーザーがメディア変換を明示したとき。  
**Not when:** 軽いリサイズ程度で Python/Pillow で足りる場合はそちら。重いのでデフォルトで入れない。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh media
source /workspace/.tools/env
```

## Use

```bash
ffmpeg -i in.mp4 -vn -acodec libmp3lame out.mp3
convert in.png -resize 50% out.png
```

## Hard no

- セッション開始時に入れない
- 巨大出力を workspace に置きっぱなしにしない（必要なら download_file）
