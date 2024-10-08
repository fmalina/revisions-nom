"""
Instagram picture webpage renderer.
Renders webpages out of Instaloader text files to TARGET_PATH
"""

from pathlib import Path
from django.template.defaultfilters import linebreaks
from pics import get_hashtags
import lzma
import json

TARGET_PATH = '../_assets/pic'
TPL = """
<!doctype html>
<html lang="sk">
<head>
    <meta charset="utf8">
    <link rel="stylesheet" href="/nom/style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{rel_name} 📸 {title}</title>
</head>
<body>
<main>
    <p><img class="feature" src="{img_src}"></p>
    <p><a href="/nom/{doc_name}#{hashtag}">{rel_name}</a>{credit}
    {desc}
</main>
</body>
"""

hashtags = get_hashtags()
docs_by_hashtag = dict([(y, (x, z)) for x, y, z in hashtags])


def render_text_files():
    for path in Path(TARGET_PATH).rglob('*.txt'):
        render(path)


def clean_name(name):
    no_digits = ''.join([x for x in name if not x.isdigit()])
    return no_digits.replace('.', '').strip()


def get_credit(path):
    json_path = str(path).replace('.txt', '.json.xz')
    try:
        json_data = lzma.open(json_path).read()
    except FileNotFoundError:
        return ''
    d = json.loads(json_data)
    try:
        username = d['node']['iphone_struct']['user']['username']
    except KeyError:
        return ''
    if username:
        return f' podľa @{username}'
    return ''


def render(path):
    path_name = path.name
    f = open(path).read()
    title = f.split('\n')[0][:40]
    if len(title) >= 40:
        title += '...'
    desc = linebreaks(f)
    img_src = path_name.replace('.txt', '.jpg')
    hashtag = str(path).split('/')[-2]
    doc_name, rel_name = docs_by_hashtag[hashtag]
    if rel_name:
        rel_name = clean_name(rel_name)
    credit = get_credit(path)
    contents = TPL.format(**locals())
    # print(str(path))
    fnw = str(path).replace('.txt', '.htm')
    fw = open(fnw, "w")
    fw.write(contents)
    fw.close()


if __name__ == '__main__':
    render_text_files()
