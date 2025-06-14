# ex-canvas

This repository provides a minimal script to list Canvas objects exported from ChatGPT.

The script scans `conversations.json` and prints a table of Canvas items found in your chats.
Missing fields are filled with sensible defaults.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Provide the path to `conversations.json` or an exported ZIP archive:

```bash
python canvas_list.py ~/Downloads/chatgpt_export.zip
```

You can filter by keyword using `-s` which searches both name and chat title:

```bash
python canvas_list.py conversations.json -s rust
```

Example output:

```text
Name      Type    Created              Chat
--------  ------  -------------------  ---------
Rust般若心経  code    2024-03-09 16:16:40  Chat#0611
```

Results are sorted by creation time (newest first) and duplicate canvases are
consolidated when multiple messages reference the same canvas. Missing values
fall back to defaults like `Untitled (Chat)` for names and `document` for types.

