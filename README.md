# Dokumentasi Program Probabilitas Bersyarat

## Deskripsi Program
Program ini adalah aplikasi web berbasis Flask yang digunakan untuk menghitung dan memvisualisasikan probabilitas bersyarat berdasarkan data tes medis. Program ini membantu pengguna memahami hubungan antara hasil tes medis dan kondisi sebenarnya dari pasien.

## Struktur Program
```
├── app.py                 # File utama aplikasi Flask
├── templates/            
│   └── index.html        # Template HTML untuk antarmuka pengguna
├── requirements.txt       # Daftar dependensi program
└── DOKUMENTASI.md        # File dokumentasi ini
```

## Dependensi
Program ini membutuhkan beberapa library Python:
```
flask==2.0.1
matplotlib==3.7.1
seaborn==0.12.2
Werkzeug==2.0.1
Jinja2==3.0.1
MarkupSafe==2.0.1
itsdangerous==2.0.1
click==8.0.1
```

## Cara Penggunaan

### 1. Instalasi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Program
```bash
python app.py
```
Buka browser dan akses `http://localhost:5000`

### 3. Input Data
Program menerima empat input data:
- Jumlah pasien sakit dengan hasil tes positif
- Jumlah pasien sakit dengan hasil tes negatif
- Jumlah pasien sehat dengan hasil tes positif
- Jumlah pasien sehat dengan hasil tes negatif

### 4. Output Program
Program akan menampilkan:
1. Keterangan data
2. Perhitungan probabilitas bersyarat
3. Visualisasi:
   - Diagram pohon probabilitas
   - Confusion matrix
   - Diagram batang
   - Diagram lingkaran

## Penjelasan Komponen Program

### 1. Perhitungan Probabilitas
Program menghitung beberapa probabilitas:

#### a. Probabilitas Dasar
- P(Sakit) = Total pasien sakit / Total semua pasien
- P(Sehat) = Total pasien sehat / Total semua pasien

#### b. Probabilitas Bersyarat
- P(Tes Positif|Sakit) = Pasien sakit hasil positif / Total pasien sakit
- P(Tes Positif|Sehat) = Pasien sehat hasil positif / Total pasien sehat

#### c. Probabilitas Total
- P(Tes Positif) = [P(Tes Positif|Sakit) × P(Sakit)] + [P(Tes Positif|Sehat) × P(Sehat)]

#### d. Probabilitas Akhir
- P(Sakit|Tes Positif) = [P(Tes Positif|Sakit) × P(Sakit)] / P(Tes Positif)

### 2. Visualisasi Data

#### a. Diagram Pohon Probabilitas
- Menampilkan struktur hierarki probabilitas
- Menggunakan warna berbeda untuk setiap kategori:
  - Merah muda: Pasien sakit
  - Hijau muda: Pasien sehat
  - Biru muda: Hasil tes positif
  - Kuning muda: Hasil tes negatif
- Menampilkan jumlah pasien dan probabilitas di setiap cabang

#### b. Confusion Matrix
- Menampilkan distribusi hasil tes dalam format matrix 2x2
- Menggunakan heatmap untuk visualisasi
- Menunjukkan:
  - True Positive (Sakit-Positif)
  - False Positive (Sehat-Positif)
  - False Negative (Sakit-Negatif)
  - True Negative (Sehat-Negatif)

#### c. Diagram Batang
- Membandingkan jumlah pasien dalam empat kategori:
  - True Positive
  - False Positive
  - True Negative
  - False Negative

#### d. Diagram Lingkaran
- Menampilkan proporsi setiap kategori dalam bentuk persentase

### 3. Fitur Interaktif

#### a. Perhitungan Otomatis
- Total baris dan kolom dihitung secara otomatis saat input diubah
- Hasil ditampilkan langsung di tabel

#### b. Tombol Reset
- Mengosongkan semua input
- Menghapus hasil perhitungan
- Mengembalikan form ke kondisi awal

#### c. Validasi Input
- Memastikan semua input diisi
- Hanya menerima input angka
- Menghindari pembagian dengan nol

## Rumus dan Perhitungan

### 1. Probabilitas Dasar
```
P(Sakit) = Total pasien sakit / Total semua pasien
P(Sehat) = Total pasien sehat / Total semua pasien
```

### 2. Probabilitas Bersyarat
```
P(Tes Positif|Sakit) = Pasien sakit hasil positif / Total pasien sakit
P(Tes Positif|Sehat) = Pasien sehat hasil positif / Total pasien sehat
```

### 3. Probabilitas Total
```
P(Tes Positif) = [P(Tes Positif|Sakit) × P(Sakit)] + [P(Tes Positif|Sehat) × P(Sehat)]
```

### 4. Teorema Bayes
```
P(Sakit|Tes Positif) = [P(Tes Positif|Sakit) × P(Sakit)] / P(Tes Positif)
```

## Contoh Penggunaan

### Input:
```
Pasien sakit, hasil positif: 90
Pasien sakit, hasil negatif: 10
Pasien sehat, hasil positif: 50
Pasien sehat, hasil negatif: 850
```

### Output:
```
Total pasien: 1000
Total pasien sakit: 100
Total pasien sehat: 900

P(Sakit) = 100/1000 = 0.1
P(Sehat) = 900/1000 = 0.9
P(Tes Positif|Sakit) = 90/100 = 0.9
P(Tes Positif|Sehat) = 50/900 ≈ 0.0556
P(Tes Positif) = (0.9 × 0.1) + (0.0556 × 0.9) = 0.14
P(Sakit|Tes Positif) = (0.9 × 0.1) / 0.14 ≈ 0.6429

Interpretasi: Jika hasil tes positif, peluang pasien benar-benar sakit adalah 64.29%
```