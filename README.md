# ex-canvas

This repository provides a minimal script to list Canvas objects exported from ChatGPT.

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

