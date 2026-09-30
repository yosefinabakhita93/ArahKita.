# ArahKita — Website Terintegrasi

Antarmuka Streamlit untuk prototype akademik ArahKita. Paket ini mengintegrasikan knowledge base Qiara, forward-chaining engine Citra, dan UI/UX Malikha.

## Mulai di sini

1. Buka folder ini di terminal.
2. Buat lingkungan Python dan pasang dependensi:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Pada Windows, aktivasi lingkungan memakai `.venv\Scripts\activate`.
Buka alamat lokal yang ditampilkan Streamlit. Ini website lokal; belum dipublikasikan ke internet.

## Yang sudah tersedia

- Form dimulai tanpa pilihan bawaan; pertanyaan pendanaan hanya muncul saat user memilih lanjut studi.
- UI student-friendly dengan kontras navy–blue–teal yang tegas, navigasi singkat, progress form, dashboard hasil, rounded line icons, skor kecocokan transparan, filter peluang, analisis gap, dan action plan konkret.
- Kartu opportunity yang hanya menampilkan informasi penting; detail persyaratan tersedia secara opsional.
- Dua belas pilihan tujuan karier lintas data, teknologi, riset, laboratorium, klinis, mutu, produk, dan komunikasi sains.
- Empat arah karier teratas ditampilkan sebagai kartu berurutan; peringkat pertama menjadi fokus rekomendasi dan opsi dapat disimpan selama sesi.
- Tiga referensi awal Qiara dan 15 sumber hasil kurasi web, semuanya memiliki tautan yang dapat dibuka.
- Sumber tambahan mencakup lowongan spesifik, portal karier resmi internasional, dan program beasiswa resmi.
- Forward chaining, inference trace, fixed-point confirmation, dan automated integration test.

## Struktur

```text
app.py                       form dan komponen hasil
app_support.py               pembacaan data dan validasi output
career_catalog.py            katalog 12 jalur karier, skill, dan relasinya
engine_adapter.py            satu titik sambung ke engine Citra
citra_engine.py              fact builder dan forward-chaining engine
merge_opportunities.py       penggabung data
data/
  rules.json                     23 definite-clause rules
  recommendation_templates.json   salinan asli Qiara
  qiara_opportunities.json          salinan asli Qiara
  web_opportunities.json            15 sumber hasil kurasi web
  opportunities.json               dataset yang digunakan engine dan katalog
tests/
  test_integration.py
```

## Menambah data opportunity

```sh
python merge_opportunities.py data/qiara_opportunities.json data/web_opportunities.json
```

Setiap ID harus unik dan setiap record harus memiliki tautan sumber yang dapat diperiksa.

## Pemeriksaan

```sh
python -m unittest discover -s tests -v
```

Tes memeriksa sambungan form–engine, contract hasil Qiara, lima jalur rekomendasi, dan audit 192 kombinasi input utama.

## Batas data

Data Qiara disalin tanpa perubahan. Sebanyak 15 record tambahan dikurasi pada 29 September 2026 dari halaman lowongan publik, portal karier resmi, dan halaman resmi penyedia beasiswa. Dataset gabungan yang digunakan website berisi 18 record. Status lowongan, periode, dan persyaratan dapat berubah setelah tanggal tersebut, sehingga user tetap diarahkan untuk membuka halaman sumber sebelum melamar atau mendaftar.

Kelompok jurusan pada form lebih luas daripada syarat program. Form juga belum mengumpulkan umur, daftar dokumen lengkap, skor bahasa, masa berlaku sertifikat, atau konfirmasi kelulusan. Karena itu kecocokan opportunity bukan bukti memenuhi seluruh persyaratan. Detail yang belum diketahui ditampilkan untuk pemeriksaan manual.

Hasil website merupakan rekomendasi awal dan bukan jaminan penerimaan kerja, studi, atau beasiswa.
