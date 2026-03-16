import os

subpages = [
    ('compress-image-to-100kb', '100KB', 'compress-image-to-100kb'),
    ('compress-image-to-50kb',  '50KB',  'compress-image-to-50kb'),
    ('compress-image-to-20kb',  '20KB',  'compress-image-to-20kb'),
    ('compress-image-to-500kb', '500KB', 'compress-image-to-500kb'),
    ('compress-image-to-1mb',   '1MB',   'compress-image-to-1mb'),
]

for slug, label, path in subpages:
    fpath = f'{slug}/index.html'
    if not os.path.exists(fpath):
        print(f'SKIP (not found): {fpath}')
        continue
    with open(fpath, 'r') as f:
        html = f.read()

    # 1. Add theme-color after viewport if missing
    if 'theme-color' not in html:
        html = html.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0" />',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <meta name="theme-color" content="#2563eb" />'
        )

    # 2. Add favicon links after canonical if missing
    if 'favicon.ico' not in html:
        canonical_tag = f'<link rel="canonical" href="https://compressto200kb.com/{path}/" />'
        favicon_block = canonical_tag + '\n  <link rel="icon" href="/favicon.ico" sizes="any" />\n  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />\n  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />'
        html = html.replace(canonical_tag, favicon_block)

    # 3. Add og:image + Twitter Card after og:url if missing
    if 'og:image' not in html:
        og_url_tag = f'  <meta property="og:url" content="https://compressto200kb.com/{path}/" />'
        og_extra = og_url_tag + f'''
  <meta property="og:image" content="https://compressto200kb.com/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:site_name" content="CompressTo200KB" />
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Compress Image to {label} Online Free" />
  <meta name="twitter:description" content="Compress image to {label} online for free. No server upload, 100% private." />
  <meta name="twitter:image" content="https://compressto200kb.com/og-image.png" />'''
        html = html.replace(og_url_tag, og_extra)

    # 4. Add BreadcrumbList Schema before </head> if missing
    if 'BreadcrumbList' not in html:
        breadcrumb = f'''  <!-- Structured Data: BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://compressto200kb.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "Compress to {label}", "item": "https://compressto200kb.com/{path}/" }}
    ]
  }}
  </script>
</head>'''
        html = html.replace('</head>', breadcrumb)

    # 5. Fix copyright year
    html = html.replace('\u00a9 2025 CompressTo200KB', '\u00a9 2025\u20132026 CompressTo200KB')

    with open(fpath, 'w') as f:
        f.write(html)
    print(f'Updated: {fpath}')

print('Done.')
