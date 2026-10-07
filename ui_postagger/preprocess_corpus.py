import re
import sys

def preprocess(text):
    text = text.replace('\r\n', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'(\w)([;:!?])', r'\1 \2', text)
    text = re.sub(r'([;:!?])(\w)', r'\1 \2', text)
    text = re.sub(r'(?<!\w)-(\w)', r'- \1', text)
    text = re.sub(r'(\w)-(?=\s|$)', r'\1 -', text)
    text = re.sub(r'\"(\w)', r'" \1', text)
    text = re.sub(r'(\w)\"', r'\1 "', text)

    sentences = re.split(r'(?<=[.?!])\s+', text)

    result = []
    for sent in sentences:
        sent = sent.strip()
        if sent:
            result.append(sent)

    return result

if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        raw = f.read()

    sentences = preprocess(raw)

    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        for sent in sentences:
            f.write(sent + '\n')