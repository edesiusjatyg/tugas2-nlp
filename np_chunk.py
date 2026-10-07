
from pathlib import Path
from nltk.chunk import RegexpParser
from nltk.chunk.util import tree2conlltags

BASE_DIR = Path(__file__).resolve().parent

# a. Grammar untuk mengenali frasa nomina (Noun Phrase)
GRAMMAR = r"""
NP: {<DT>?<CD>*<JJ>*<NN.*>+<JJ|X>*}
"""


def baca_lima_kalimat(nama_file):
    data = []

    with (BASE_DIR / nama_file).open(
        encoding="utf-8-sig"
    ) as file:
        for baris in file:
            if not baris.strip():
                continue

            kalimat = []
            potongan = []

            for bagian in baris.split():
                potongan.append(bagian)

                if "/" in bagian:
                    gabungan = " ".join(potongan)
                    kata, tag = gabungan.rsplit("/", 1)
                    kalimat.append((kata, tag))
                    potongan = []

            if kalimat:
                data.append(kalimat)

            if len(data) == 5:
                break

    return data


def main():
    data = baca_lima_kalimat("train.txt")
    parser = RegexpParser(GRAMMAR)

    with (BASE_DIR / "2_hasil_np_tree.txt").open(
        "w", encoding="utf-8"
    ) as file_tree, (
        BASE_DIR / "2_hasil_np_iob.txt"
    ).open("w", encoding="utf-8") as file_iob:

        file_tree.write("Grammar:\n" + GRAMMAR + "\n")

        for nomor, kalimat in enumerate(data, start=1):
            tree = parser.parse(kalimat)

            # Soal b: hasil parse tree dalam bentuk string
            file_tree.write(f"\nKalimat {nomor}:\n")
            file_tree.write(tree.pformat(margin=1000) + "\n")

            # Soal c: hasil chunking dalam format IOB
            file_iob.write(f"Kalimat {nomor}:\n")

            for token, pos, iob in tree2conlltags(tree):
                file_iob.write(
                    f"{token}\t{pos}\t{iob}\n"
                )

            file_iob.write("\n")

    print("Hasil tree: 2_hasil_np_tree.txt")
    print("Hasil IOB: 2_hasil_np_iob.txt")


if __name__ == "__main__":
    main()