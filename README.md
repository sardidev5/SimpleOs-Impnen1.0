# Dokumentasi SimpleOS

## Ikhtisar
**SimpleOS** adalah simulasi sistem operasi ringan yang dibangun menggunakan Tkinter. Aplikasi ini dirancang untuk memberikan antarmuka yang ramah pengguna untuk melakukan operasi file dasar, pemantauan sistem, dan fungsionalitas penjelajahan web. SimpleOS bertujuan untuk memberikan pengalaman pengguna yang intuitif dan efisien.

## Fitur Utama
### 1. Manajemen File
- **Buat, Hapus, dan Edit File**: Pengguna dapat membuat file baru, menghapus file yang ada, dan mengedit konten file.
- **Daftar File**: Menampilkan semua file dalam direktori saat ini.
- **Kompresi dan Dekompresi**: Mendukung kompresi file ke format ZIP dan dekompresi file ZIP.

### 2. Pemantauan Sistem
- **Lihat Proses yang Berjalan**: Menampilkan daftar semua proses yang sedang berjalan di sistem.
- **Informasi Sistem**: Menyediakan informasi tentang sistem operasi, RAM, dan penggunaan disk.

### 3. Alat Jaringan
- **Ping Alamat IP**: Memungkinkan pengguna untuk melakukan ping ke alamat IP tertentu.
- **Pindai Port**: Memindai port terbuka pada alamat IP yang ditentukan.
- **Lihat Koneksi Jaringan Aktif**: Menampilkan semua koneksi jaringan yang sedang aktif.

### 4. Fitur Keamanan
- **Enkripsi dan Dekripsi File**: Mengamankan file dengan enkripsi dan memungkinkan dekripsi file yang telah dienkripsi.
- **Pemindaian Malware**: Memeriksa sistem untuk mendeteksi malware.
- **Pengelolaan Firewall**: Mengelola pengaturan firewall untuk meningkatkan keamanan.

### 5. Penjadwal Tugas
- **Jadwalkan Perintah**: Memungkinkan pengguna untuk menjadwalkan perintah untuk dijalankan setelah penundaan tertentu.

### 6. Penjelajahan Web
- **Buka Halaman Web**: Memungkinkan pengguna untuk membuka halaman web langsung dari aplikasi.

## Instalasi
Untuk menjalankan SimpleOS, pastikan Anda memiliki Python yang terinstal di sistem Anda. Anda juga perlu menginstal beberapa pustaka yang diperlukan. Gunakan perintah berikut untuk menginstal pustaka yang diperlukan:

pip install psutil cryptography tkhtmlview

## Penggunaan
1. **Jalankan Aplikasi**: Eksekusi skrip Python untuk meluncurkan antarmuka SimpleOS.
2. **Navigasi Menu**: Gunakan bilah menu untuk mengakses berbagai fungsionalitas:
   - **File**: Kelola file dan direktori.
   - **Web**: Buka halaman web.
   - **Bantuan**: Akses informasi tentang aplikasi.
   - **Keamanan**: Kelola fitur keamanan.
   - **Sistem**: Lihat informasi sistem dan kelola layanan.
   - **Tugas**: Jadwalkan tugas.

3. **Entri Perintah**: Gunakan bidang entri perintah untuk mengeksekusi perintah secara langsung.
4. **Area Output**: Lihat hasil perintah Anda di area output.

## Perintah
- `list`: Daftar file di direktori saat ini.
- `create <filename>`: Buat file baru dengan nama yang ditentukan.
- `delete <filename>`: Hapus file yang ditentukan.
- `dir`: Tampilkan daftar direktori saat ini.
- `exit`: Keluar dari aplikasi.

## Tangkapan Layar
![Tangkapan Layar SimpleOS](screenshot.png)

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Untuk informasi lebih lanjut, lihat file `LICENSE`.

## Kontribusi
Kami menyambut baik kontribusi dari semua orang. Jika Anda ingin berkontribusi pada proyek ini, silakan lakukan fork repositori ini dan kirimkan pull request.

## Kontak
Jika Anda memiliki pertanyaan atau saran, silakan hubungi kami di:
- Email: sardidevs.me@gmail.com
- GitHub: [SARDIDEV](https://github.com/sardidev5)

---

Terima kasih telah menggunakan SimpleOS! Kami berharap Anda menikmati pengalaman menggunakan aplikasi ini.
