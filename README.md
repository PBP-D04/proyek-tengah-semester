# Proyek Tengah Semester D04


## Nama Aplikasi: Bookphoria


## Anggota Kelompok
| Nama | NPM |
| :--------------: | :--------: |
| Chelsea Angelica | 2206025722 |
| Isa Citra Buana | 2206081465 |
| Jocelyn Nathanie Arwin | 2206082171 |
| Mahartha Gemilang | 2206819211 |
| Sheryl Ivana W. | 2206824943 |


## Cerita dan Manfaat Aplikasi
Aplikasi “Bookphoria” berangkat dari kesadaran untuk meningkatkan pentingnya literasi bagi masyarakat Indonesia yang semakin menurun setiap tahunnya.  Untuk mampu menyampaikan gagasan dengan baik, seseorang harus membudayakan literasi agar gagasan yang disampaikan berlandaskan pada data dan fakta. Aplikasi ini akan memuat beragam pilihan buku dari berbagai penulis yang dilengkapi dengan ulasan serta fitur download e-book (bila tersedia).


## Daftar Modul
- **Account**

Aplikasi Django ini mengatur autentikasi pengguna. Selain itu, juga memungkinkan untuk penggantian password dan pengeditan profil pengguna. Tidak hanya itu, di account, pengguna, dalam hal ini user, dapat melihat riwayat buku yang mereka sukai dan buku yang mereka review. Guest tidak dapat mengakses diarahkan langsung ke halaman login. Admin dapat mengakses halaman ini tetapi tidak memiliki fitur riwayat.
- **Books Pages**

Aplikasi Django ini berfungsi untuk menampilkan halaman utama antarmuka dataset buku dalam web ini. pada antarmuka tersebut juga disediakan fitur sorting, filter, dan search. Selain itu, juga terdapat opsi untuk fitur carousel-slider untuk buku-buku yang direkomendasikan. Fitur sorting didasarkan pada pilihan paling banyak diulas, paling banyak disukai, terbaru, dan terlama. Sementara itu, fitur filter berupa pemfilteran berdasarkan kategori buku. Ada juga halaman untuk menampilkan semua dataset buku. 
- **Dashboard App**

Aplikasi Django ini berfungsi untuk menyediakan layanan DML atau lebih dikenal fitur CRUD (Create, Read, Update, Delete). Objek yang dapat di-CRUD adalah buku. Buku yang dapat di-CRUD oleh pengguna tergantung pada otorisasi penggunanya. User hanya bisa melakukan CRUD terhadap buku yang dimilikinya atau dengan kata lain di-filter berdasarkan foreign key yang merujuk pada primary key dari setiap User. Admin tidak dapat melakukan CRUD secara penuh, hanya dapat melakukan perintah DELETE dan READ. Untuk admin, tidak ada batasan filter. Sementara itu, guest tidak dapat mengakses page ini dan akan langsung diarahkan ke halaman login.
- **Review App**

Aplikasi Django ini menyediakan fitur ulasan user terhadap buku. Ulasan tersebut berupa bintang, komentar (opsional), dan foto buku(opsional). Bintang pada ulasan ini memiliki range dari satu hingga lima. Hanya pengguna bertipe User yang dapat melakukan review terhadap buku. Guest yang mencoba membuat review akan diarahkan ke halaman login. Admin tidak memiliki akses untuk membuat review.
- **Detail Book App**

Aplikasi Django ini berfungsi untuk memuat informasi detail mengenai suatu buku atau e-book. Terdapat juga fitur download dalam bentuk PDF (opsional) dan love button untuk menyukai buku . Selain itu, template dari Review App untuk buku tersebut akan diletakkan di bagian bawah dari template aplikasi ini.


## Role Pengguna Aplikasi
- Guest

Pengguna yang mengakses web bookphoria tanpa autentikasi
- User

Pengguna yang dapat membuat dan mereview buku
- Admin

Pengguna yang dapat melakukan manipulasi berupa delete terhadap buku yang dianggap melakukan pelanggaran


## Sumber Dataset
https://developers.google.com/books/ 

(Google Books API)