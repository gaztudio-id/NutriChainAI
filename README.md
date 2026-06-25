# NutriChainAI - Sistem Cerdas Terintegrasi Manajemen MBG

NutriChainAI adalah platform audit, pemantauan, dan verifikasi kualitas gizi serta keamanan pangan terintegrasi untuk program **Makan Bergizi Gratis (MBG) Nasional**. Platform ini dirancang menggunakan arsitektur modular yang menggabungkan 11 proyek kecerdasan buatan (Deep Learning) dari hulu ke hilir ke dalam satu alur operasional (Standard Operating Procedure/SOP) digital.

Proyek ini dibangun menggunakan **Flask (Python)** untuk backend, serta sistem desain **Synthesis Capital** yang bersih, modern, dan ergonomis (dilengkapi fitur tema Terang/Gelap otomatis, Dynamic Island Navbar, dan Floating Theme Switcher).

---

## 📋 Alur Integrasi Sistem (SOP Pipeline)

Operasional sistem terbagi menjadi **5 Fase Utama** yang berjalan secara berurutan:

1. **Fase 1: Perencanaan Menu & Logistik (Ruang Dapur)**
   * Mempersiapkan kecukupan gizi harian, estimasi sisa porsi menu, serta meramalkan kuantitas belanja logistik dapur umum.
2. **Fase 2: Pemeriksaan Kualitas Bahan Baku (Area Penerimaan)**
   * Menyaring bahan baku pangan segar (sayur, buah, protein) dari pemasok secara instan saat tiba di dapur.
3. **Fase 3: Perakitan & Keamanan Pangan (Conveyor Belt Perakitan Baki)**
   * Memvalidasi kelengkapan menu baki saji, memprediksi kandungan kalori visual, serta mendeteksi kontaminasi benda asing makro maupun mikro sebelum makanan disegel.
4. **Fase 4: Evaluasi Pasca-Konsumsi (Sekolah / Kelas)**
   * Menilai tingkat konsumsi siswa dari piring sisa makanan (Habis / Sisa) untuk melatih ulang preferensi menu di Fase 1 (Feedback Loop).
5. **Fase 5: Pemantauan Sentimen & Opini Publik (Dashboard Penyelenggara)**
   * Memantau tanggapan, ulasan, serta tren sentimen masyarakat terkait menu dan jalannya program MBG melalui media sosial.

---

## 🛠️ Pembagian Modul Kerja Kelompok (Kelompok 1 - 11)

Setiap kelompok bertanggung jawab untuk mengimplementasikan fungsionalitas algoritma AI masing-masing pada berkas template HTML yang telah disediakan di folder `Web/Kelompok_X/kelompok_X.html`. 

Berikut adalah rincian fungsionalitas dan model AI untuk setiap kelompok:

| Kelompok | Nama Modul | Metode / Algoritma | Fase SOP | Lokasi Berkas |
| :--- | :--- | :--- | :--- | :--- |
| **Kelompok 1** | Analisis Kandungan Gizi Makanan | CNN (Visual & Weight Input) | Fase 3 | `Web/Kelompok_1/kelompok_1.html` |
| **Kelompok 2** | Rekomendasi Menu Makanan | LSTM Sequence | Fase 1 | `Web/Kelompok_2/kelompok_2.html` |
| **Kelompok 3** | Prediksi Kesukaan Menu MBG | DNN / LSTM Tabular | Fase 1 | `Web/Kelompok_3/kelompok_3.html` |
| **Kelompok 4** | Analisis Sentimen Medsos | CNN-LSTM & Word Embedding | Fase 5 | `Web/Kelompok_4/kelompok_4.html` |
| **Kelompok 5** | Deteksi Kontaminasi Benda Asing Makro | YOLO Object Detection | Fase 3 | `Web/Kelompok_5/kelompok_5.html` |
| **Kelompok 6** | Analisis Sentimen Komentar YouTube | LSTM & Time Series Forecasting | Fase 5 | `Web/Kelompok_6/kelompok_6.html` |
| **Kelompok 7** | Deteksi Sisa Makanan Piring Kotor | CNN Transfer Learning | Fase 4 | `Web/Kelompok_7/kelompok_7.html` |
| **Kelompok 8** | Deteksi Kelengkapan Menu Tray | YOLOv8 Instance Segmentation | Fase 3 | `Web/Kelompok_8/kelompok_8.html` |
| **Kelompok 9** | Prediksi Kebutuhan Distribusi | Artificial Neural Network (ANN) | Fase 1 | `Web/Kelompok_9/kelompok_9.html` |
| **Kelompok 10**| Klasifikasi Kelayakan Gizi & Benda Asing Mikro | ERX Citra Hiperspektral | Fase 3 | `Web/Kelompok_10/kelompok_10.html` |
| **Kelompok 11**| Sortir Kualitas Kesegaran Bahan Baku | CNN MobileNetV2 | Fase 2 | `Web/Kelompok_11/kelompok_11.html` |

---

## ✍️ Panduan Pengisian dan Integrasi Kelompok

Setiap kelompok wajib mengikuti langkah-langkah di bawah ini untuk mengintegrasikan model Deep Learning mereka ke dalam platform NutriChainAI:

### Langkah 1: Persiapan Model
1. Letakkan file model Anda (format `.h5`, `.keras`, `.pt`, `.onnx`, atau `.bin`) di folder kelompok masing-masing (misal: `Web/Kelompok_X/model.h5`).
2. Tuliskan skrip inferensi Python di dalam handler rute kelompok Anda di file `Web/app.py` jika ingin melakukan inferensi real-time di server Flask.

### Langkah 2: Edit Berkas HTML (`kelompok_X.html`)
1. Buka berkas `Web/Kelompok_X/kelompok_X.html` di kode editor Anda.
2. Anda diperbolehkan memodifikasi bagian **Main Content** di dalam `<div class="container" style="max-width: 1100px;">` untuk menambahkan:
   * Form unggah gambar (untuk model deteksi citra seperti CNN/YOLO).
   * Input teks/angka parameter (untuk model prediksi tabular seperti ANN/LSTM).
   * Visualisasi grafik diagram batasan gizi, chart ulasan sentimen, atau bounding box deteksi objek.
3. **PENTING**: Jangan merubah struktur navigasi **Dynamic Island Navbar** (`.dynamic-island-container`) dan file javascript `theme.js` di bagian header karena sudah diseragamkan untuk menjaga konsistensi transisi page-load loader dan responsivitas web.

### Langkah 3: Integrasi API Flask (`Web/app.py`)
1. Buka file `Web/app.py`.
2. Cari rute `@app.route('/kelompok-<int:num>')` yang merender halaman Anda.
3. Anda dapat menambahkan logika endpoint baru (contoh: POST `/kelompok-X/predict`) untuk menerima input data dari frontend HTML kelompok Anda, melakukan inferensi menggunakan library deep learning pilihan Anda (TensorFlow/PyTorch/ONNX Runtime), dan mengembalikan data dalam format JSON untuk dirender secara dinamis menggunakan Javascript fetch API di HTML Anda.

### Langkah 4: Pengujian Mandiri
1. Jalankan server Flask lokal Anda:
   ```bash
   python app.py
   ```
2. Buka `http://127.0.0.1:5050` pada browser Anda.
3. Masuk ke halaman **Status Model** atau **Dashboard Operasional** lalu klik kelompok Anda untuk memverifikasi apakah layout UI terender dengan rapi, form input berfungsi, dan API inferensi mengembalikan output yang sesuai.

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. Pastikan Python 3.8+ sudah terinstal di sistem Anda.
2. Instal dependensi dasar Flask:
   ```bash
   pip install Flask
   ```
3. *(Opsional)* Instal dependensi machine learning Anda jika menggunakan inferensi sisi server (seperti `tensorflow`, `torch`, `opencv-python`, dll).
4. Jalankan aplikasi:
   ```bash
   python app.py
   ```
5. Akses web di: [http://127.0.0.1:5050](http://127.0.0.1:5050)
