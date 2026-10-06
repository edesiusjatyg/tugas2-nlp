#!/usr/bin/env python3
"""
Convert POS tagger output (word\tTAG) to inline format (word/TAG)
Usage: python3 convert_postag.py input.txt output.txt
"""

import sys

def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    sentences = []
    current = []
    last_was_period = False

    for line in lines:
        line = line.rstrip('\n')
        stripped = line.strip()

        # Empty line = sentence boundary ONLY if previous token was a period
        if stripped == '':
            if current and last_was_period:
                sentences.append(current)
                current = []
                last_was_period = False
            continue

        # Split on tab
        parts = stripped.split('\t')
        if len(parts) == 2:
            word, tag = parts[0].strip(), parts[1].strip()
            current.append(f"{word}/{tag}")
            # Check if this is a sentence-ending punctuation
            last_was_period = (word in ['.', '?', '!'] and tag == 'Z')
        elif len(parts) == 1 and parts[0]:
            current.append(f"{parts[0]}/X")
            last_was_period = False

    # Don't forget last sentence
    if current:
        sentences.append(current)

    with open(output_path, 'w', encoding='utf-8') as f:
        for sent in sentences:
            f.write(' '.join(sent) + '\n')

    print(f"Done. {len(sentences)} sentences written to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 convert_postag.py <input> <output>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
