# NutriChain AI: Sistem Cerdas Terintegrasi Manajemen MBG
## Audit, Pemantauan, dan Verifikasi Cerdas Makan Bergizi Gratis (MBG) Nasional
### Berbasis Deep Learning End-to-End - TA 2025/2026

NutriChain AI adalah platform digital terintegrasi yang dirancang untuk mengotomatisasi pengawasan, jaminan mutu, dan keamanan pangan dalam rantai distribusi program Makan Bergizi Gratis (MBG) nasional. Sistem ini mensinkronisasikan 11 modul Deep Learning ke dalam 5 fase Standard Operating Procedure (SOP) operasional secara asinkron dari hulu ke hilir.

---

## Hasil Evaluasi dan Analisis Kinerja Model (UAS Report)

| Kelompok | Fokus Modul AI | Arsitektur & Metode | Key Performance Metrics (Akurasi / Loss) |
| :--- | :--- | :--- | :--- |
| **Kelompok 1** | Analisis Kandungan Gizi | CNN | **Akurasi 80.88%** - Test Loss 0.9158 (20 klasifikasi makanan Indonesia) |
| **Kelompok 2** | Rekomendasi Menu | LSTM | **Akurasi Data Testing 97.67%** (Belajar >18.000 kombinasi resep) |
| **Kelompok 3** | Prediksi Kesukaan | DNN | **Balanced Accuracy 99.52%** - F1-Score 92.31% (Sisa makanan) |
| **Kelompok 4** | Sentimen TikTok & X | CNN-LSTM | **Akurasi 96.6%** pada data validasi (F1-Score 0.95) |
| **Kelompok 5** | Deteksi Kontaminasi Makro | YOLO | **mAP50 94.95%** - Confidence Score hingga 85% (5.1ms/gambar) |
| **Kelompok 6** | Sentimen YouTube | IndoBERT & LSTM | **Akurasi 87.51%** - Proyeksi 30 hari bebas overfitting |
| **Kelompok 7** | Deteksi Sisa Piring | CNN | **Akurasi Pengujian 98.96%** (Klasifikasi Suka / Bersisa) |
| **Kelompok 8** | Kelengkapan Tray | YOLOv8 | **mAP50 93.7%** (mAP50 Makanan Pokok 95.8%) |
| **Kelompok 9** | Prediksi Kebutuhan Logistik | ANN | **$R^2$ Score (Test):** SLB (0.934), SMP (0.891), SMK (0.878), SD (0.838), SMA (0.774) |
| **Kelompok 10**| Deteksi Anomali Hiperspektral | CNN | **Akurasi, Presisi, Recall, & AUC 100% (1.0000)** (NIR-HSI 96 band) |
| **Kelompok 11**| Klasifikasi Kualitas Bahan | MobileNetV2 | **Akurasi Validasi 98.67%** - Loss 0.0372 (Piecewise Linear) |

---

## Alur Kegiatan Operasional (SOP Pipeline)

Sistem operasi NutriChain AI terstruktur secara linear untuk mengawal aliran data dari dapur umum hingga laporan akhir:

```mermaid
flowchart TB

%%==============================
%% FASE 1
%%==============================
subgraph F1["Fase 1 - Perencanaan Menu & Logistik"]
direction TB
K2["K2<br/>Rekomendasi Menu<br/><b>LSTM</b>"]
K9["K9<br/>Prediksi Kebutuhan Logistik<br/><b>ANN</b>"]
K3["K3<br/>Prediksi Kesukaan / Sisa<br/><b>DNN</b>"]

K2 --> K9
K9 --> K3
end

%%==============================
%% FASE 2
%%==============================
subgraph F2["Fase 2 - Pengecekan Bahan Baku"]
direction TB
K11["K11<br/>Sortir Sayur & Buah<br/><b>CNN</b>"]
end

%%==============================
%% FASE 3
%%==============================
subgraph F3["Fase 3 - Inspeksi Perakitan Baki"]
direction TB
K8["K8<br/>Cek Kelengkapan Komponen<br/><b>YOLOv8</b>"]
K1["K1<br/>Validasi Nilai Gizi & Kalori<br/><b>CNN</b>"]
K5["K5<br/>Deteksi Kontaminasi Makro<br/><b>YOLO</b>"]
K10["K10<br/>Deteksi Anomali Mikro<br/><b>Hyperspectral</b>"]
end

%%==============================
%% FASE 4
%%==============================
subgraph F4["Fase 4 - Evaluasi Pasca Konsumsi"]
direction TB
K7["K7<br/>Deteksi Sisa Makanan Piring Kotor<br/><b>CNN</b>"]
end

%%==============================
%% FASE 5
%%==============================
subgraph F5["Fase 5 - Pemantauan Opini Publik"]
direction LR
T["Data TikTok & X"] --> K4["K4<br/>Sentimen Medsos<br/><b>CNN-LSTM</b>"]
Y["Data YouTube"] --> K6["K6<br/>Sentimen YouTube<br/><b>IndoBERT + LSTM</b>"]
end

%%==============================
%% DASHBOARD
%%==============================
DB(("Dashboard Evaluasi Pusat"))

%%==============================
%% ALUR UTAMA
%%==============================
K3 --> K11
K11 --> K8
K8 --> K1
K1 --> K5
K5 --> K10
K10 --> K7

%% Feedback
K7 -.->|Retrain Prediksi Sisa| K3
K7 -.->|Retrain Prediksi Logistik| K9

%% Dashboard
K7 --> DB
K4 --> DB
K6 --> DB
```

---

## Panduan Pengembangan dan Git Workflows (PENTING)

Untuk menjaga stabilitas ekosistem NutriChain AI selama integrasi kolaboratif:

### 1. Batasan Modifikasi Kode
- **Modul UI Kelompok**: Lakukan edit *hanya* pada folder template kelompok Anda (`web/templates/Kelompok_X/kelompok_X.html`).
- **Backend Flask (`web/app.py`)**: Lakukan modifikasi routing/api *hanya* pada blok penanda komentar kelompok Anda. Jangan mengutak-atik routing utama (`/`, `/status`, `/dashboard`) atau kelompok lain.
- **Dynamic CSS/Themes**: Tulis CSS kustom Anda di dalam tag `<style>` pada berkas HTML kelompok Anda sendiri. Dilarang mengubah stylesheet global `web/static/style.css` secara langsung.

### 2. Standar Commit & Pull
Sebelum memulai pekerjaan, tarik selalu update terbaru:
```bash
git pull origin main
```
Gunakan target file yang spesifik ketika melakukan stage file, lalu commit menggunakan format standar:
```bash
git add web/templates/Kelompok_X/
git add web/app.py
git commit -m "feat: kelompok X menyelesaikan integrasi model ke UI utama"
git push origin main
```

---

## Cara Menjalankan Aplikasi Secara Lokal

### 1. Prasyarat Sistem
- Python 3.8 - 3.10
- GPU Driver (Opsional, untuk inferensi YOLOv8 lebih cepat)

### 2. Pemasangan Dependensi
Pasang paket-paket inti yang dibutuhkan server web Flask:
```bash
pip install Flask pandas numpy opencv-python pillow ultralytics tensorflow scikit-learn joblib h5py flask-cors
```

### 3. Menjalankan Server
Eksekusi script Flask utama dari direktori root proyek:
```bash
python web/app.py
```
Aplikasi akan aktif secara lokal di: **http://127.0.0.1:5050**
