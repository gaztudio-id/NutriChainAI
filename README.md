# NutriChainAI - Sistem Cerdas Terintegrasi Manajemen MBG

NutriChainAI adalah platform audit, pemantauan, dan verifikasi kualitas gizi serta keamanan pangan terintegrasi untuk program Makan Bergizi Gratis (MBG) Nasional. Platform ini dirancang menggunakan arsitektur modular yang menggabungkan 11 proyek kecerdasan buatan (Deep Learning) dari hulu ke hilir ke dalam satu alur operasional (Standard Operating Procedure/SOP) digital.

Proyek ini dibangun menggunakan Flask (Python) untuk backend, serta sistem desain Synthesis Capital yang bersih, modern, dan ergonomis (dilengkapi fitur tema Terang/Gelap otomatis, Dynamic Island Navbar, dan Floating Theme Switcher).

---

## Alur Integrasi Sistem (SOP Pipeline)

Operasional sistem terbagi menjadi 5 Fase Utama yang berjalan secara berurutan:

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

## Pembagian Modul Kerja Kelompok (Kelompok 1 - 11)

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

## Panduan Kerja Kolaboratif Menggunakan Git

Untuk menghindari konflik kode (merge conflicts) dan menjaga integritas file utama, setiap anggota kelompok wajib mengikuti prosedur kerja Git berikut secara disiplin:

### 1. Sebelum Melakukan Edit (Sinkronisasi Kode)
Selalu tarik versi kode terbaru dari repository pusat sebelum Anda mulai membuat perubahan. Hal ini mencegah terjadinya konflik akibat bekerja pada basis kode yang usang.
```bash
git pull origin main
```

### 2. Aturan Pembatasan Edit Berkas
* **Hanya Edit Berkas Kelompok Anda**: Batasi modifikasi Anda pada folder kelompok masing-masing (misal: `Web/Kelompok_X/`).
* **Hanya Edit Endpoint Anda di `Web/app.py`**: Jika kelompok Anda memerlukan penambahan endpoint Machine Learning pada server Flask, edit file `Web/app.py` hanya pada blok route/fungsi kelompok Anda (`/kelompok-X` atau endpoint buatan Anda sendiri). Jangan memodifikasi route inti seperti `/`, `/about`, `/dashboard`, `/status`, atau route milik kelompok lain.
* **JANGAN Edit Berkas CSS/JS Utama**: Jangan memodifikasi file style global `Web/static/style.css` atau fungsionalitas tema `Web/static/theme.js`. Jika memerlukan CSS kustom khusus kelompok, tulis CSS tersebut di dalam tag `<style>` di HTML kelompok Anda sendiri (`kelompok_X.html`).

### 3. Alur Penyimpanan dan Pengiriman (Stage, Commit & Push)
Setelah menguji kode Anda secara lokal dan memastikan server berjalan normal:
1. **Lakukan Stage Secara Spesifik**: Hindari penggunaan perintah `git add .` karena perintah ini dapat secara tidak sengaja menstagen file temporer atau file kelompok lain. Lakukan stage hanya pada file pekerjaan Anda:
   ```bash
   git add Web/Kelompok_X/
   git add Web/app.py
   ```
2. **Lakukan Commit dengan Format Standar**: Gunakan format commit yang seragam yaitu `type: isi nya`. Contoh:
   ```bash
   git commit -m "feat: kelompok 3 integrasi model prediksi kesukaan menu"
   ```
3. **Kirim Perubahan ke Server**: Kirim commit Anda ke branch utama:
   ```bash
   git push origin main
   ```

---

## Panduan Teknis Integrasi Model Machine Learning

### Langkah 1: Penyiapan Model
1. Simpan file bobot model Anda (seperti `.h5`, `.pt`, `.onnx`, atau `.bin`) ke dalam folder kelompok masing-masing (contoh: `Web/Kelompok_X/model.h5`).
2. Muat model tersebut pada server backend di `Web/app.py` menggunakan pustaka yang sesuai (seperti TensorFlow, PyTorch, atau ONNX Runtime).

### Langkah 2: Pembuatan Endpoint Prediksi di Backend (`Web/app.py`)
Tambahkan handler baru untuk menerima request prediksi, contoh:
```python
@app.route('/predict-kelompok-X', methods=['POST'])
def predict_kelompok_x():
    # Ambil input gambar atau data tabular dari request
    # Lakukan prapemrosesan data
    # Jalankan prediksi model
    # Kembalikan response dalam format JSON
    return jsonify({"status": "success", "result": prediction_value})
```

### Langkah 3: Desain UI Frontend (`kelompok_X.html`)
Desain antarmuka kelompok Anda secara profesional di dalam `<div class="container" style="max-width: 1100px;">`:
* Gunakan elemen input formulir yang bersih dan berlabel jelas.
* Gunakan Javascript `fetch` API untuk mengirim data input ke endpoint backend secara asinkron tanpa me-reload halaman.
* Tampilkan hasil inferensi secara dinamis pada elemen visual seperti grafik atau bounding box pada canvas.

---

## Cara Menjalankan Aplikasi Secara Lokal

1. Pastikan Python 3.8+ terinstal di sistem Anda.
2. Pasang dependensi Flask:
   ```bash
   pip install Flask
   ```
3. Pasang dependensi Machine Learning yang diperlukan kelompok Anda (seperti `tensorflow`, `torch`, `opencv-python`, dll).
4. Jalankan aplikasi:
   ```bash
   python app.py
   ```
5. Akses aplikasi melalui peramban pada alamat: http://127.0.0.1:5050
