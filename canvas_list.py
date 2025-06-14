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
        chat_title = conv.get('title') or conv.get('id')
        mapping = conv.get('mapping', {})
        for item in mapping.values():
            message = item.get('message')
            if not message:
                continue
            meta = message.get('metadata', {})
            if not isinstance(meta, dict):
                continue
            canvas_list = meta.get('canvas')
            if not canvas_list:
                continue
            if isinstance(canvas_list, dict):
                canvas_list = [canvas_list]
            for c in canvas_list:
                cid = c.get('id') or c.get('canvas_id')
                name = c.get('name') or 'Untitled'
                ctype = c.get('object_type') or c.get('type')
                ts = c.get('create_time') or c.get('update_time')
                if ts:
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    date = ''
                key = (chat_title, cid or name)
                item = canvases.get(key)
                if not item or (date and date > item['date']):
                    canvases[key] = {'name': name, 'type': ctype, 'date': date, 'chat': chat_title}
    return list(canvases.values())


def main():
    parser = argparse.ArgumentParser(description='List Canvas objects from ChatGPT export')
    parser.add_argument('path', help='Path to conversations.json or export zip')
    parser.add_argument('-s', '--search', help='Filter canvases by name keyword')
    args = parser.parse_args()

    conversations = load_conversations(args.path)
    canvases = extract_canvas(conversations)
    if args.search:
        canvases = [c for c in canvases if args.search.lower() in c['name'].lower()]

    canvases.sort(key=lambda x: x['date'], reverse=True)

    headers = ['Name', 'Type', 'Created', 'Chat']
    rows = [[c['name'], c['type'], c['date'], c['chat']] for c in canvases]
    print(tabulate(rows, headers=headers))


if __name__ == '__main__':
    main()
