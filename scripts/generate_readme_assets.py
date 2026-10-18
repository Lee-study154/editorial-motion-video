#!/usr/bin/env python3
"""Generate README proof assets from the approved film; requires Pillow and FFmpeg."""
import argparse
import io
import os
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--film', type=Path, required=True, help='Approved 1080p or 4K vertical master')
parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parents[1] / 'assets/readme')
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
PAPER, INK, BLUE = '#FCFCFB', '#12171E', '#002FA7'

def font(size):
    for name in [os.environ.get('README_FONT'), '/System/Library/Fonts/Supplemental/Arial.ttf', 'DejaVuSans.ttf']:
        if name:
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                pass
    return ImageFont.load_default(size=size)

def run(command, data=None):
    result = subprocess.run(command, input=data, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode())
    return result.stdout

def frame(time, width=360):
    data = run(['ffmpeg', '-v', 'error', '-ss', str(time), '-i', str(args.film),
                '-frames:v', '1', '-vf', f'scale={width}:-1', '-f', 'image2pipe', '-vcodec', 'png', '-'])
    return Image.open(io.BytesIO(data)).convert('RGB')

# Same finished film, three different passages. Preserve the entire 9:16 frame.
fps, duration, width, height = 12, 4.4, 252, 448
count = round(fps * duration)
starts = [0.3, 23.0, 38.5]
clips = []
for start in starts:
    data = run(['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(args.film),
                '-t', str(duration), '-vf', f'fps={fps},scale={width}:{height}',
                '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    chunk = width * height * 3
    clips.append([Image.frombytes('RGB', (width, height), data[i:i+chunk])
                  for i in range(0, len(data), chunk)])
count = min(count, *(len(c) for c in clips))
frames = []
for index in range(count):
    canvas = Image.new('RGB', (900, 540), INK)
    draw = ImageDraw.Draw(canvas)
    for col, label in enumerate(['01 / REAL PAGES', '02 / CHARACTER', '03 / CONTINUITY']):
        x = 36 + 288 * col
        draw.text((x, 19), label, fill=PAPER, font=font(19))
        canvas.paste(clips[col][index], (x, 58))
    draw.text((36, 516), 'THREE EXCERPTS / ONE 43.2-SECOND FILM', fill='#CDD3DF', font=font(15))
    frames.append(canvas)
# Short dissolve restores the first frame instead of a harsh loop cut.
for offset in range(5):
    index = count - 5 + offset
    frames[index] = Image.blend(frames[index], frames[0], (offset + 1) / 5)
# Open on the stable, complete character; preserve the original wrap dissolve.
pivot = count // 2
frames = frames[pivot:] + frames[:pivot]
for offset in range(5):
    index = count - 5 + offset
    frames[index] = Image.blend(frames[index], frames[0], (offset + 1) / 5)
frames[0].save(args.out / 'showcase.jpg', quality=90)
raw = b''.join(f.tobytes() for f in frames)
run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
     '-s', '900x540', '-r', str(fps), '-i', '-', '-filter_complex',
     '[0:v]split[a][b];[a]palettegen=max_colors=192:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle',
     '-loop', '0', str(args.out / 'showcase.gif')], raw)
# Six large, chronological full-frame samples; do not force twelve small portraits.
samples = [(2.5, '01  FEEDS'), (11.5, '02  REAL PAGES'), (16.0, '03  THE PROMISE'),
           (20.5, '04  ATTENTION'), (25.0, '05  IDENTITY'), (41.5, '06  WHOSE SCRIPT?')]
board = Image.new('RGB', (1200, 1488), PAPER)
draw = ImageDraw.Draw(board)
for index, (time, label) in enumerate(samples):
    x = 36 + 388 * (index % 3)
    y = 32 + 728 * (index // 3)
    draw.text((x, y), label, fill=BLUE, font=font(22))
    board.paste(frame(time), (x, y + 43))
    draw.text((x, y + 696), f'{time:04.1f}s', fill='#596271', font=font(20))
board.save(args.out / 'frames.jpg', quality=91)
print({'gifBytes': (args.out/'showcase.gif').stat().st_size, 'gifFrames': count,
       'frameboardBytes': (args.out/'frames.jpg').stat().st_size})
