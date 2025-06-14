# ex-canvas

This repository provides a minimal script to list Canvas objects exported from ChatGPT.

The script scans `conversations.json` and prints a table of unique Canvas items
found in your chats.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Provide the path to `conversations.json` or an exported ZIP archive:

```bash
python canvas_list.py ~/Downloads/chatgpt_export.zip
```

You can filter by keyword using `-s`:

```bash
python canvas_list.py conversations.json -s rust
```

Results are sorted by creation time (newest first) and duplicate canvases are
consolidated when multiple messages reference the same canvas.

