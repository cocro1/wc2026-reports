"""Convert Dixon-Coles MD to teal-themed HTML article."""
import sys, re, os

def md2html(md_path, out_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Remove YAML frontmatter
    md = re.sub(r'^---\n.*?\n---\n', '', md, flags=re.DOTALL)

    lines = md.split('\n')
    html = []
    code_block = False
    table = False
    in_list = False

    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if not code_block:
                code_block = True
                html.append('<pre><code>')
            else:
                code_block = False
                html.append('</code></pre>')
            continue
        if code_block:
            html.append(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            continue

        # Tables
        if '|' in line and not line.strip().startswith('#'):
            if not table:
                html.append('<table>')
                table = True
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(re.match(r'^[-: ]+$', c) for c in cells):
                continue  # skip separator row
            tag = 'th' if table and html[-1] == '<table>' else 'td'
            html.append('<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>')
            continue
        else:
            if table:
                html.append('</table>')
                table = False

        # Headings
        m = re.match(r'^(#{1,4})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            htext = m.group(2)
            html.append(f'<h{level}>{htext}</h{level}>')
            continue

        # Horizontal rules
        if re.match(r'^---\s*$', line):
            html.append('<hr>')
            continue

        # Blockquotes
        m = re.match(r'^>\s*(.*)', line)
        if m:
            html.append(f'<blockquote>{m.group(1)}</blockquote>')
            continue

        # Inline formatting
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line = re.sub(r'`([^`]+)`', r'<code>\1</code>', line)
        line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', line)

        if line.strip():
            html.append(f'<p>{line}</p>')
        else:
            html.append('')

    if table:
        html.append('</table>')

    body = '\n'.join(html)

    title_match = re.search(r'<h1>(.+?)</h1>', body)
    title = title_match.group(1) if title_match else 'Dixon-Coles蒙特卡洛推演'

    css = '''<style>
:root {
  --ink: #0033A0; --brand-soft: #EEF3FC; --muted: #9CA3AF;
  --bg: #fff; --card: #ffffff; --text: #111827; --border: #E5E7EB;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.75;
  padding: 20px; max-width: 720px; margin: 0 auto;
}
h1 { font-size: 22px; color: var(--ink); margin: 24px 0 16px; line-height: 1.3; border-left: 4px solid var(--ink); padding-left: 12px; }
h2 { font-size: 18px; color: var(--ink); margin: 20px 0 12px; }
h3 { font-size: 16px; color: var(--ink); margin: 16px 0 8px; }
h4 { font-size: 14px; font-weight: 600; margin: 12px 0 6px; }
p { margin: 8px 0; font-size: 15px; }
hr { border: none; border-top: 1px solid var(--border); margin: 20px 0; }
table {
  width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px;
  border: 1px solid var(--border);
}
th, td { padding: 6px 10px; border: 1px solid var(--border); text-align: left; }
th { background: var(--brand-soft); color: var(--ink); font-weight: 600; }
tr:nth-child(even) td { background: #f9fafb; }
blockquote {
  margin: 12px 0; padding: 10px 14px; background: #fefce8; border-left: 3px solid #facc15;
  font-size: 14px; color: #92400e;
}
code { background: #f3f4f6; padding: 1px 5px; border-radius: 3px; font-size: 13px; }
pre { background: #1e293b; color: #e2e8f0; padding: 14px; border-radius: 6px; overflow-x: auto; margin: 12px 0; }
pre code { background: none; padding: 0; color: inherit; }
a { color: var(--ink); }
.back-link { display: inline-block; margin-bottom: 16px; color: var(--muted); font-size: 13px; text-decoration: none; }
.back-link:hover { color: var(--ink); }
</style>'''

    html_out = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{css}
</head>
<body>
<a class="back-link" href="../../index.html#simulation">← 返回首页</a>
{body}
</body>
</html>'''

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f'Written: {out_path}')

if __name__ == '__main__':
    md_dir = 'D:/我的坚果云/OB笔记/自媒体/fwc2026/content/dixon-coles-monte-carlo'
    out_dir = 'articles/simulation'
    for fname in os.listdir(md_dir):
        if fname.endswith('.md'):
            md_path = os.path.join(md_dir, fname)
            html_fname = fname.replace('.md', '.html')
            out_path = os.path.join(out_dir, html_fname)
            md2html(md_path, out_path)
