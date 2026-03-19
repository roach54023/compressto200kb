#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-language page generator for compressto200kb.com
Generates /zh/ and /hi/ subdirectory versions of all pages.
Run: python3 gen_i18n.py
"""

import os, re, shutil, sys

# Import translation data from sibling files
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_zh import ZH
from i18n_hi import HI
from i18n_pt import PT
from i18n_es import ES
from i18n_ar import AR
from i18n_bn import BN
from i18n_id import ID
from i18n_fr import FR

BASE   = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://compressto200kb.com"

LANGS = {"zh": ZH, "hi": HI, "pt": PT, "es": ES, "ar": AR, "bn": BN, "id": ID, "fr": FR}

# (slug, en_html_path, default_kb, page_key)
PAGES = [
    ("",                                   "index.html",                                   200,  "home"),
    ("compress-image-to-100kb",            "compress-image-to-100kb/index.html",           100,  "100kb"),
    ("compress-image-to-50kb",             "compress-image-to-50kb/index.html",             50,  "50kb"),
    ("compress-image-to-20kb",             "compress-image-to-20kb/index.html",             20,  "20kb"),
    ("compress-image-to-500kb",            "compress-image-to-500kb/index.html",           500,  "500kb"),
    ("compress-image-to-1mb",              "compress-image-to-1mb/index.html",            1024,  "1mb"),
    ("compress-photo-for-government-form", "compress-photo-for-government-form/index.html", 100, "govform"),
    ("compress-image-for-passport",        "compress-image-for-passport/index.html",        50,  "passport"),
    ("compress-image-for-whatsapp",        "compress-image-for-whatsapp/index.html",       200,  "whatsapp"),
    ("compress-jpeg-to-200kb",             "compress-jpeg-to-200kb/index.html",            200,  "jpeg200"),
    ("compress-png-to-200kb",              "compress-png-to-200kb/index.html",             200,  "png200"),
]

# ── URL helpers ──────────────────────────────────────────────────────────────

def en_url(slug):
    return DOMAIN + ("/" if not slug else f"/{slug}/")

def lang_url(lang, slug):
    return DOMAIN + f"/{lang}/" + (f"{slug}/" if slug else "")

def nav_links(lang, t):
    """Build the translated nav <ul> items."""
    items = [
        ("",                                   t["nav_200"]),
        ("compress-image-to-100kb",            t["nav_100"]),
        ("compress-image-to-50kb",             t["nav_50"]),
        ("compress-image-to-20kb",             t["nav_20"]),
        ("compress-image-to-500kb",            t["nav_500"]),
        ("compress-image-to-1mb",              t["nav_1mb"]),
        ("compress-photo-for-government-form", "Gov Form"),
        ("compress-image-for-passport",        "Passport"),
        ("compress-image-for-whatsapp",        "WhatsApp"),
        ("compress-jpeg-to-200kb",             "JPEG"),
        ("compress-png-to-200kb",              "PNG"),
    ]
    li = []
    for slug, label in items:
        href = f"/{lang}/" + (f"{slug}/" if slug else "")
        li.append(f'<li><a href="{href}">{label}</a></li>')
    return "\n        ".join(li)

def hreflang_tags(slug):
    """Generate hreflang link tags for a given page slug."""
    tags = []
    tags.append(f'  <link rel="alternate" hreflang="en" href="{en_url(slug)}" />')
    for lang, t in LANGS.items():
        tags.append(f'  <link rel="alternate" hreflang="{t["lang_attr"]}" href="{lang_url(lang, slug)}" />')
    tags.append(f'  <link rel="alternate" hreflang="x-default" href="{en_url(slug)}" />')
    return "\n".join(tags)

# ── Read English source ──────────────────────────────────────────────────────

def read_en(en_path):
    full = os.path.join(BASE, en_path)
    with open(full, encoding="utf-8") as f:
        return f.read()

# ── Build translated page ────────────────────────────────────────────────────

def build_page(lang, slug, en_html, default_kb, page_key):
    t  = LANGS[lang]
    pt = t["pages"][page_key]
    la = t["lang_attr"]

    html = en_html

    # 1. lang attribute
    html = re.sub(r'<html\s+lang="[^"]*"', f'<html lang="{la}"', html)

    # 2. canonical
    html = re.sub(
        r'<link rel="canonical"[^>]*/?>',
        f'<link rel="canonical" href="{lang_url(lang, slug)}" />',
        html
    )

    # 3. title
    html = re.sub(r'<title>[^<]*</title>', f'<title>{pt["title"]}</title>', html)

    # 4. meta description
    html = re.sub(
        r'<meta name="description"[^>]*/?>',
        f'<meta name="description" content="{pt["description"]}" />',
        html
    )

    # 5. OG tags
    html = re.sub(r'(<meta property="og:title"[^>]*content=")[^"]*(")',
                  r'\g<1>' + pt["title"] + r'\g<2>', html)
    html = re.sub(r'(<meta property="og:description"[^>]*content=")[^"]*(")',
                  r'\g<1>' + pt["description"] + r'\g<2>', html)
    html = re.sub(r'(<meta property="og:url"[^>]*content=")[^"]*(")',
                  r'\g<1>' + lang_url(lang, slug) + r'\g<2>', html)

    # 6. Twitter tags
    html = re.sub(r'(<meta name="twitter:title"[^>]*content=")[^"]*(")',
                  r'\g<1>' + pt["title"] + r'\g<2>', html)
    html = re.sub(r'(<meta name="twitter:description"[^>]*content=")[^"]*(")',
                  r'\g<1>' + pt["description"] + r'\g<2>', html)

    # 7. Insert hreflang tags before </head>
    hreflang = hreflang_tags(slug)
    html = html.replace('</head>', hreflang + '\n</head>', 1)

    # 8. H1
    html = re.sub(r'(<h1[^>]*>).*?(</h1>)', r'\g<1>' + pt["h1"] + r'\g<2>', html, flags=re.DOTALL)

    # 9. Hero paragraph (first <p> after h1 in hero section)
    html = re.sub(
        r'(<section[^>]*class="[^"]*hero[^"]*"[^>]*>.*?<p>).*?(</p>)',
        r'\g<1>' + pt["hero_p"] + r'\g<2>',
        html, count=1, flags=re.DOTALL
    )

    # 10. Target size label
    html = html.replace('>Target size:<', f'>{t["target_size_label"]}<')
    html = html.replace('placeholder="custom"', f'placeholder="{t["custom_placeholder"]}"')

    # 11. Drop zone
    html = re.sub(r'(<p class="drop-title">)[^<]*(</p>)',
                  r'\g<1>' + t["drop_title"] + r'\g<2>', html)
    html = re.sub(r'(<p class="drop-sub">)[^<]*(</p>)',
                  r'\g<1>' + t["drop_sub"] + r'\g<2>', html)

    # 12. Buttons
    html = re.sub(r'(<button[^>]*id="selectBtn"[^>]*>)[^<]*(</button>)',
                  r'\g<1>' + t["select_btn"] + r'\g<2>', html)
    html = re.sub(r'(<span[^>]*id="compressingText"[^>]*>)[^<]*(</span>)',
                  r'\g<1>' + t["compressing"] + r'\g<2>', html)
    html = re.sub(r'(<button[^>]*class="[^"]*download-all[^"]*"[^>]*>)[^<]*(</button>)',
                  r'\g<1>' + t["download_all"] + r'\g<2>', html)

    # 13. Trust badges
    badge_map = [
        ("✓ Always Free",          t["badge_free"]),
        ("✓ No Server Upload",     t["badge_no_upload"]),
        ("✓ No Registration",      t["badge_no_reg"]),
        ("✓ Batch Processing",     t["badge_batch"]),
        ("✓ JPG · PNG · WEBP",     t["badge_formats"]),
    ]
    for en_badge, tr_badge in badge_map:
        html = html.replace(en_badge, tr_badge)

    # 14. Footer copyright
    html = re.sub(
        r'© 2025[^<]*CompressTo200KB\.com[^<]*',
        t["footer_copy"],
        html
    )

    # 15. Fix all internal links to point to lang subdirectory
    # nav links: href="/compress-... → href="/zh/compress-...
    def fix_href(m):
        href = m.group(1)
        # skip external, anchors, already-prefixed
        if href.startswith('http') or href.startswith('#') or href.startswith(f'/{lang}/'):
            return m.group(0)
        # skip asset paths
        if any(href.endswith(ext) for ext in ['.ico', '.svg', '.png', '.json', '.xml', '.txt', '.css', '.js']):
            return m.group(0)
        new_href = f'/{lang}{href}'
        return f'href="{new_href}"'

    html = re.sub(r'href="(/[^"]*)"', fix_href, html)

    # 16. Fix asset paths that got incorrectly prefixed — revert them
    for asset in ['/favicon.ico', '/favicon.svg', '/apple-touch-icon.png',
                  '/icon-192.png', '/icon-512.png', '/manifest.json',
                  '/og-image.png', '/robots.txt', '/sitemap.xml']:
        html = html.replace(f'href="/{lang}{asset}"', f'href="{asset}"')
        html = html.replace(f'src="/{lang}{asset}"', f'src="{asset}"')

    return html

# ── Write output ─────────────────────────────────────────────────────────────

def write_page(lang, slug, html):
    if slug:
        out_dir = os.path.join(BASE, lang, slug)
    else:
        out_dir = os.path.join(BASE, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {out_path.replace(BASE, '')}")

# ── Add hreflang to English pages ────────────────────────────────────────────

def patch_en_hreflang(slug, en_path):
    full = os.path.join(BASE, en_path)
    with open(full, encoding="utf-8") as f:
        html = f.read()

    # Remove existing hreflang tags to avoid duplicates
    html = re.sub(r'\s*<link rel="alternate" hreflang="[^"]*"[^>]*/>\n?', '', html)

    hreflang = hreflang_tags(slug)
    html = html.replace('</head>', hreflang + '\n</head>', 1)

    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  patched hreflang → {en_path}")

# ── Update sitemap ────────────────────────────────────────────────────────────

def update_sitemap():
    sitemap_path = os.path.join(BASE, "sitemap.xml")
    with open(sitemap_path, encoding="utf-8") as f:
        content = f.read()

    new_urls = []
    for slug, _, _, _ in PAGES:
        for lang in LANGS:
            url = lang_url(lang, slug)
            entry = f"""  <url>
    <loc>{url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>"""
            if url not in content:
                new_urls.append(entry)

    if new_urls:
        insert = "\n" + "\n".join(new_urls) + "\n"
        content = content.replace("</urlset>", insert + "</urlset>")
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  sitemap updated with {len(new_urls)} new URLs")
    else:
        print("  sitemap already up to date")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Generating i18n pages ===")
    for slug, en_path, default_kb, page_key in PAGES:
        en_html = read_en(en_path)
        for lang in LANGS:
            if page_key not in LANGS[lang]["pages"]:
                print(f"  SKIP {lang}/{slug or 'home'} (no translation)")
                continue
            html = build_page(lang, slug, en_html, default_kb, page_key)
            write_page(lang, slug, html)

    print("\n=== Patching English pages with hreflang ===")
    for slug, en_path, _, _ in PAGES:
        patch_en_hreflang(slug, en_path)

    print("\n=== Updating sitemap.xml ===")
    update_sitemap()

    print("\nDone!")

if __name__ == "__main__":
    main()
