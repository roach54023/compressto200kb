#!/usr/bin/env python3
"""
Add RTL CSS overrides to all Arabic language pages.
Inserts a <style> block with RTL-specific overrides just before </style>.
"""
import os

ROOT = '/Users/jiangzihaojiangzihao/Documents/compressto200kb'

RTL_CSS = """
  /* RTL overrides for Arabic */
  [dir="rtl"] body { direction: rtl; }
  [dir="rtl"] .section h2,
  [dir="rtl"] .section h3,
  [dir="rtl"] .section p,
  [dir="rtl"] .hero h1,
  [dir="rtl"] .hero p { text-align: right; }
  [dir="rtl"] .size-table th { text-align: right; }
  [dir="rtl"] .size-table td { text-align: right; }
  [dir="rtl"] .faq-q { flex-direction: row-reverse; }
  [dir="rtl"] .faq-q::after { margin-left: 0; margin-right: 12px; }
  [dir="rtl"] .step { flex-direction: row-reverse; }
  [dir="rtl"] .step-body { text-align: right; }
  [dir="rtl"] nav { flex-direction: row-reverse; }
  [dir="rtl"] .result-item { flex-direction: row-reverse; }
  [dir="rtl"] .result-info { text-align: right; }
  [dir="rtl"] ol { padding-right: 20px; padding-left: 0; }
  [dir="rtl"] .size-row { flex-direction: row-reverse; justify-content: flex-end; }
  [dir="rtl"] .badges { flex-direction: row-reverse; }
"""

MARKER = '  </style>'

fixed = 0
ar_dir = os.path.join(ROOT, 'ar')
for dirpath, dirnames, filenames in os.walk(ar_dir):
    for fname in filenames:
        if fname == 'index.html':
            path = os.path.join(dirpath, fname)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already has RTL overrides
            if 'RTL overrides' in content:
                print(f"  Already has RTL CSS: {path.replace(ROOT, '')}")
                continue
            
            # Insert RTL CSS before </style>
            if MARKER not in content:
                print(f"  WARNING: No </style> found in {path.replace(ROOT, '')}")
                continue
            
            # Replace first occurrence of </style>
            new_content = content.replace(MARKER, RTL_CSS + MARKER, 1)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed += 1
            print(f"Fixed RTL CSS: {path.replace(ROOT, '')}")

print(f"\nDone: {fixed} files updated")
