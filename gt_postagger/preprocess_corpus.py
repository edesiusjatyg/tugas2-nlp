#!/usr/bin/env python3
"""
Pre-process Indonesian text before POS tagging.
Detaches punctuation glued to words, one sentence per line.
Usage: python3 preprocess.py input.txt output.txt
"""

import re
import sys

def preprocess(text):
    # Normalize whitespace and windows line endings
    text = text.replace('\r\n', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()

    # Detach colon, semicolon, exclamation, question mark glued to end of word
    # e.g. "bertentangan:" → "bertentangan :"
    text = re.sub(r'(\w)([;:!?])', r'\1 \2', text)

    # Detach colon etc glued to start of word (rare but possible)
    text = re.sub(r'([;:!?])(\w)', r'\1 \2', text)

    # Detach leading hyphen glued to word e.g. "-termasuk" → "- termasuk"
    text = re.sub(r'(?<!\w)-(\w)', r'- \1', text)

    # Detach trailing hyphen glued to word e.g. "besar-" → "besar -"
    # but keep infix hyphens like "negara-negara", "satu-satunya"
    # Rule: only detach if hyphen is followed by space or end
    text = re.sub(r'(\w)-(?=\s|$)', r'\1 -', text)

    # Detach quotes glued to words e.g. "\"perang" → "\" perang"
    text = re.sub(r'\"(\w)', r'" \1', text)
    text = re.sub(r'(\w)\"', r'\1 "', text)

    # Split into sentences on . ? !
    # Keep the punctuation attached for splitting, then re-add it
    sentences = re.split(r'(?<=[.?!])\s+', text)

    result = []
    for sent in sentences:
        sent = sent.strip()
        if sent:
            result.append(sent)

    return result

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 preprocess.py <input> <output>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        raw = f.read()

    sentences = preprocess(raw)

    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for sent in sentences:
            f.write(sent + '\n')

    print(f"Done. {len(sentences)} sentences written to {sys.argv[2]}")
