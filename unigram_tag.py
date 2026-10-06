"""Unigram POS tagger berbasis Naive Bayes, tanpa paket tambahan.
Jalankan: python main.py. Semua file dibaca relatif terhadap lokasi script.
"""

from pathlib import Path
from collections import Counter, defaultdict

BASE_DIR = Path(__file__).resolve().parent


def baca_data(nama_file):
    data = []
    with (BASE_DIR / nama_file).open(encoding="utf-8-sig") as file:
        for nomor, baris in enumerate(file, 1):
            if not baris.strip():
                continue
            kalimat, potongan = [], []
            for bagian in baris.split():
                potongan.append(bagian)
                if "/" in bagian:
                    # Misalnya 'Dewan Keamanan/NN' menjadi satu pasangan.
                    kata, tag = " ".join(potongan).rsplit("/", 1)
                    if not kata or not tag:
                        raise ValueError(f"Format salah: {nama_file}, baris {nomor}")
                    kalimat.append((kata, tag))
                    potongan = []
            if potongan:
                raise ValueError(f"Tag belum ada: {nama_file}, baris {nomor}")
            data.append(kalimat)
    if not data:
        raise ValueError(f"File kosong: {nama_file}")
    return data


def training(data):
    jumlah_tag = Counter()
    jumlah_kata = defaultdict(Counter)
    kosakata = set()
    for kalimat in data:
        for kata, tag in kalimat:
            if tag == "??":
                raise ValueError("Data training harus memiliki tag yang benar.")
            kata = kata.lower()
            jumlah_tag[tag] += 1
            jumlah_kata[tag][kata] += 1
            kosakata.add(kata)
    return jumlah_tag, jumlah_kata, kosakata


def prediksi_tag(kata, model):
    jumlah_tag, jumlah_kata, kosakata = model
    kata = kata.lower()
    total = sum(jumlah_tag.values())
    ukuran = len(kosakata) + 1  # Satu kategori untuk kata tak dikenal.
    skor = {}
    for tag, jumlah in jumlah_tag.items():
        prior = jumlah / total
        likelihood = (jumlah_kata[tag][kata] + 1) / (jumlah + ukuran)
        skor[tag] = prior * likelihood
    return max(skor, key=skor.get)


def main():
    # Model belajar hanya dari train.txt.
    model = training(baca_data("train.txt"))
    data_test = baca_data("test.txt")
    hasil = [
        [(kata, prediksi_tag(kata, model)) for kata, _ in kalimat]
        for kalimat in data_test
    ]

    with (BASE_DIR / "result_test.txt").open("w", encoding="utf-8") as file:
        for kalimat in hasil:
            file.write(" ".join(f"{kata}/{tag}" for kata, tag in kalimat) + "\n")

    # Ground truth baru digunakan setelah prediksi selesai.
    ground_truth = baca_data("ground_truth.txt")
    kata_hasil = [[kata for kata, _ in kalimat] for kalimat in hasil]
    kata_gt = [[kata for kata, _ in kalimat] for kalimat in ground_truth]
    if kata_hasil != kata_gt:
        raise ValueError("Kalimat, kata, atau urutan test dan ground truth berbeda.")

    benar = total = 0
    rincian = ["Kata\tPrediksi\tGround truth\tStatus"]
    for kalimat, kalimat_gt in zip(hasil, ground_truth):
        for (kata, prediksi), (_, asli) in zip(kalimat, kalimat_gt):
            cocok = prediksi == asli  # Perbandingan label secara persis.
            benar += int(cocok)
            total += 1
            status = "Benar" if cocok else "Salah"
            rincian.append(f"{kata}\t{prediksi}\t{asli}\t{status}")

    akurasi = benar / total * 100
    ringkasan = f"Akurasi: {akurasi:.2f}% ({benar}/{total} tag benar)"
    (BASE_DIR / "evaluasi.txt").write_text(
        ringkasan + "\n\n" + "\n".join(rincian) + "\n", encoding="utf-8"
    )
    print(ringkasan)
    print(f"Prediksi: {BASE_DIR / 'result_test.txt'}")
    print(f"Perbandingan: {BASE_DIR / 'evaluasi.txt'}")


if __name__ == "__main__":
    main()

# OUTPUT
# Akurasi: 86.59% (71/82 tag benar)
# Prediksi: /Users/aliaatikahsana/NLP/tugas2-nlp/result_test.txt
# Perbandingan: /Users/aliaatikahsana/NLP/tugas2-nlp/evaluasi.txt