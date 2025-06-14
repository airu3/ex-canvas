import argparse
import datetime
import json
import os
import zipfile
from tabulate import tabulate


def load_conversations(path):
    if path.lower().endswith('.zip'):
        with zipfile.ZipFile(path) as z:
            with z.open('conversations.json') as f:
                return json.load(f)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


def extract_canvas(conversations):
    canvases = {}
    for conv in conversations:
        chat_title = conv.get("title") or "Untitled Chat"
        conv_ct = conv.get("create_time")
        mapping = conv.get("mapping", {}) or {}
        for item in mapping.values():
            message = item.get("message")
            if not message:
                continue
            meta = message.get("metadata", {})
            if not isinstance(meta, dict):
                continue
            canvas_list = meta.get("canvas")
            if not canvas_list:
                continue
            if isinstance(canvas_list, dict):
                canvas_list = [canvas_list]
            msg_ct = message.get("create_time")
            for c in canvas_list:
                cid = c.get("id") or c.get("canvas_id") or c.get("name")
                name = c.get("name") or f"Untitled ({chat_title})"
                ctype = c.get("type") or "document"
                ts = msg_ct or conv_ct
                ts_val = None
                if isinstance(ts, (int, float)):
                    ts_val = ts
                    date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date = ""
                key = (chat_title, cid)
                prev = canvases.get(key)
                if not prev or (ts_val and ts_val > prev.get("_ts", -1)):
                    canvases[key] = {
                        "name": name,
                        "type": ctype,
                        "created": date,
                        "chat": chat_title,
                        "_ts": ts_val or 0,
                    }
    return list(canvases.values())


def main():
    parser = argparse.ArgumentParser(description='List Canvas objects from ChatGPT export')
    parser.add_argument('path', help='Path to conversations.json or export zip')
    parser.add_argument('-s', '--search', help='Filter canvases by keyword in name or chat title')
    args = parser.parse_args()

    conversations = load_conversations(args.path)
    canvases = extract_canvas(conversations)
    if args.search:
        kw = args.search.lower()
        canvases = [c for c in canvases if kw in c['name'].lower() or kw in c['chat'].lower()]

    canvases.sort(key=lambda x: x.get('_ts', 0), reverse=True)

    headers = ['Name', 'Type', 'Created', 'Chat']
    rows = [[c['name'], c['type'], c['created'], c['chat']] for c in canvases]
    print(tabulate(rows, headers=headers))


if __name__ == '__main__':
    main()
