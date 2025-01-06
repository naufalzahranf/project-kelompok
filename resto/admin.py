import json
import os
from datetime import datetime

def tampilkan_menu():
    """Menampilkan daftar menu."""
    try:
        with open('menu.json', 'r') as file:
            kategori_menu = json.load(file)
    except FileNotFoundError:
        kategori_menu = {}
    except json.JSONDecodeError:
        print("Format file menu.json tidak valid. Menggunakan menu kosong.")
        kategori_menu = {}

    if not kategori_menu:
        print("Menu kosong.")
    else:
        print("\n=== Daftar Menu ===")
        for nama, detail in menu_item.items():
            deskripsi = ", ".join(detail['deskripsi']) 
            komposisi = ", ".join(detail['komposisi'])
            print(f"- {nama}: Rp{detail['harga']}, Deskripsi: {deskripsi}, Komposisi: {komposisi}")
    return menu_item

def autentikasi_admin():
    """Memverifikasi password admin."""
    sandi_default = "admin123"
    maksimal_percobaan = 3
    percobaan = 0

    while percobaan < maksimal_percobaan:
        sandi = input("Masukkan sandi admin: ").strip()
        if sandi == sandi_default:
            print("Autentikasi berhasil. Selamat datang, Admin!")
            return True
        else:
            percobaan += 1
            print(f"Sandi salah. Anda memiliki {maksimal_percobaan - percobaan} kesempatan lagi.")
    
    print("Anda telah gagal memasukkan sandi. Keluar dari sistem.")
    return False

def validasi_input_abjad(pesan):
    """Memvalidasi input hanya berupa huruf dan spasi."""
    while True:
        value = input(pesan).strip()
        if value.replace(" ", "").isalpha():
            return value
        print("Input hanya boleh berupa huruf dan spasi. Coba lagi.")

def validasi_input_angka(pesan):
    """Memvalidasi input hanya berupa angka positif."""
    while True:
        value = input(pesan).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Input harus berupa angka positif. Coba lagi.")

def validasi_input_deskripsi(pesan):
    """Memvalidasi input deskripsi untuk memastikan hanya huruf, spasi, dan koma."""
    while True:
        value = input(pesan).strip()
        # Memisahkan input berdasarkan koma dan menghapus spasi di sekitar setiap kata
        deskripsi_list = [komponen.strip() for komponen in value.split(",") if komponen.strip()]
        if all(all(karakter.isalpha() or karakter.isspace() for karakter in komponen) for komponen in deskripsi_list):
            return deskripsi_list
        print("Input deskripsi hanya boleh berupa huruf dan spasi, dan dipisah dengan koma. Coba lagi.")

def validasi_input_komposisi(pesan):
    """Memvalidasi input komposisi untuk memastikan hanya huruf, spasi, dan koma."""
    while True:
        value = input(pesan).strip()
        # Memisahkan input berdasarkan koma dan menghapus spasi di sekitar setiap kata
        komposisi_list = [komponen.strip() for komponen in value.split(",") if komponen.strip()]
        if all(all(karakter.isalpha() or karakter.isspace() for karakter in komponen) for komponen in komposisi_list):
            return komposisi_list
        print("Input komposisi hanya boleh berupa huruf dan spasi, dan dipisah dengan koma. Coba lagi.")


def tambah_menu(kategori_menu):
    """Menambahkan menu baru."""
    if kategori_menu is None:
        kategori_menu = {}

    print("\n=== Tambah Menu ===")
    kategori = validasi_input_abjad("Masukkan kategori (contoh: Dessert, Minuman): ").title()
    if kategori not in kategori_menu:
        kategori_menu[kategori] = {}

    nama_item = validasi_input_abjad("Masukkan nama item: ").title()
    if not nama_item:
        print("Nama item tidak boleh kosong. Coba lagi.")
        return

    harga = validasi_input_angka(f"Masukkan harga untuk {nama_item}: ")
    deskripsi = validasi_input_deskripsi(f"Masukkan deskripsi untuk {nama_item}: ")
    komposisi = validasi_input_komposisi(f"Masukkan komposisi untuk {nama_item}: ")

    kategori_menu[kategori][nama_item] = {
        "harga": harga,
        "deskripsi": deskripsi,
        "komposisi": komposisi
    }
    print(f"{nama_item} telah ditambahkan ke kategori {kategori}.")

    simpan_menu(kategori_menu)

def update_menu(kategori_menu):
    """Memperbarui menu yang ada."""
    print("\n=== Update Menu ===")
    kategori = validasi_input_abjad("Masukkan kategori: ").title()
    if kategori not in kategori_menu:
        print(f"Kategori {kategori} tidak ditemukan.")
        return

    nama_item = input("Masukkan nama item yang ingin diperbarui: ").title()
    if nama_item in kategori_menu[kategori]:
        print(f"Item ditemukan: {nama_item}")

        while True:
            harga_input = input(f"Masukkan harga baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ").strip()
            if not harga_input:
                break
            if harga_input.isdigit() and int(harga_input) > 0:
                kategori_menu[kategori][nama_item]['harga'] = int(harga_input)
                break
            else:
                print("Harga harus berupa angka positif. Coba lagi.")

        while True:
            deskripsi_input = input(f"Masukkan deskripsi baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ").strip()
            if not deskripsi_input:
                break
            deskripsi_list = [komponen.strip() for komponen in deskripsi_input.split(",") if komponen.strip()]
            if all(komponen.replace(" ", "").isalpha() for komponen in deskripsi_list):
                kategori_menu[kategori][nama_item]['deskripsi'] = deskripsi_list
                print("Deskripsi berhasil diperbarui.")
                break
            print("Input deskripsi tidak valid. Pastikan hanya menggunakan huruf dan koma untuk memisahkan.")

        while True:
            komposisi_input = input(f"Masukkan komposisi baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ").strip()
            if not komposisi_input:
                break
            komposisi_list = [komponen.strip() for komponen in komposisi_input.split(",") if komponen.strip()]
            if all(komponen.replace(" ", "").isalpha() for komponen in komposisi_list):
                kategori_menu[kategori][nama_item]['komposisi'] = komposisi_list
                print("Komposisi berhasil diperbarui.")
                break
            print("Input komposisi tidak valid. Pastikan hanya menggunakan huruf dan koma untuk memisahkan.")

        print(f"{nama_item} dalam kategori {kategori} telah diperbarui.")
        simpan_menu(kategori_menu)
    else:
        print(f"{nama_item} tidak ditemukan dalam kategori {kategori}.")

def hapus_menu(kategori_menu):
    """Menghapus menu."""
    print("\n=== Hapus Menu ===")
    kategori = validasi_input_abjad("Masukkan kategori: ").title()
    if kategori not in kategori_menu:
        print(f"Kategori {kategori} tidak ditemukan.")
        return

    nama_item = input("Masukkan nama item yang ingin dihapus: ").title()
    if nama_item in kategori_menu[kategori]:
        del kategori_menu[kategori][nama_item]
        print(f"{nama_item} telah dihapus dari kategori {kategori}.")

        if not kategori_menu[kategori]:
            del kategori_menu[kategori]  # Hapus kategori jika kosong

        simpan_menu(kategori_menu)
    else:
        print(f"{nama_item} tidak ditemukan dalam kategori {kategori}.")

def tampilkan_orderan():
    """Menampilkan daftar orderan."""
    try:
        order_files = [f for f in os.listdir("orders") if f.startswith("order_") and f.endswith(".json")]
        if not order_files:
            print("Tidak ada orderan yang ditemukan.")
            return

        print("\n=== Daftar Orderan ===")
        for i, filename in enumerate(order_files, 1):
            print(f"\nOrder {i}: {filename}")
            filepath = os.path.join("orders", filename)
            with open(filepath, 'r') as file:
                try:
                    order_data = json.load(file)
                    print(f"  Nama Pemesan: {order_data.get('nama_pemesan', 'Tidak diketahui')}")
                    print(f"  Tanggal: {order_data.get('tanggal', 'Tidak diketahui')}")
                    print(f"  Total Belanja: Rp{order_data.get('total_belanja', 0)}")
                    print("  Pesanan:")
                    for item in order_data.get('pesanan', []):
                        print(f"    - {item['nama']} (x{item['jumlah']}), Subtotal: Rp{item['subtotal']}, Catatan: {item['catatan']}")
                except json.JSONDecodeError:
                    print(f"  Error: File {filename} rusak.")
                except Exception as e:
                    print(f"  Error membaca file {filename}: {e}")

    except FileNotFoundError:
        print("Direktori 'orders' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menampilkan orderan: {e}")

def hapus_orderan():
    """Menghapus orderan."""
    try:
        order_files = [f for f in os.listdir("orders") if f.startswith("order_") and f.endswith(".json")]
        if not order_files:
            print("Tidak ada orderan yang ditemukan.")
            return

        print("\n=== Hapus Orderan ===")
        for i, filename in enumerate(order_files, 1):
            print(f"{i}. {filename}")

        while True:
            pilihan = input("Masukkan nomor order yang ingin dihapus (atau tekan Enter untuk batal): ")
            if not pilihan:
                return

            if pilihan.isdigit() and 1 <= int(pilihan) <= len(order_files):
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

        filename_to_delete = order_files[int(pilihan) - 1]
        filepath_to_delete = os.path.join("orders", filename_to_delete)
        try:
            os.remove(filepath_to_delete)
            print(f"Orderan {filename_to_delete} telah dihapus.")
        except OSError as e:
            print(f"Terjadi kesalahan saat menghapus file: {e}")

    except FileNotFoundError:
        print("Direktori 'orders' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat menghapus orderan: {e}")

def tampilkan_reservasi():
    """Menampilkan daftar reservasi."""
    try:
        with open('reservations.json', 'r') as file:
            reservations = json.load(file)
    except FileNotFoundError:
        reservations = {}

    if not reservations:
        print("Reservasi kosong.")
    else:
        print("\n=== Daftar Reservasi ===")
        for meja, detail in reservations.items():
            print(f"- {meja}: Nama: {detail['nama']}, Tanggal: {detail['tanggal']}, Waktu: {detail['waktu']}, Jumlah Orang: {detail['jumlah_orang']}, Nomor Telepon: {detail['no_telepon']}")
    return reservations

def hapus_reservasi(reservations):
    """Menghapus reservasi."""
    print("\n=== Hapus Reservasi ===")
    nomor_meja = input("Masukkan nomor meja yang ingin dihapus (contoh: Meja 1): ").title()
    if nomor_meja in reservations:
        del reservations[nomor_meja]
        print(f"Reservasi pada {nomor_meja} telah dihapus.")
        
        # Simpan perubahan ke file
        simpan_reservasi(reservations)
    else:
        print(f"Reservasi pada {nomor_meja} tidak ditemukan.")

def simpan_reservasi(reservations):
    """Menyimpan reservasi ke file."""
    with open('reservations.json', 'w') as file:
        json.dump(reservations, file, indent=4)
    print("Reservasi berhasil disimpan.")

def simpan_menu(kategori_menu):
    """Menyimpan menu ke file."""
    with open('menu.json', 'w') as file:
        json.dump(kategori_menu, file, indent=4)
    print("Menu berhasil disimpan.")

def inisialisasi_sistem():
    """Memastikan semua direktori yang diperlukan sudah ada."""
    try:
        if not os.path.exists("orders"):
            os.makedirs("orders")
            print("Direktori orders berhasil dibuat.")
    except Exception as e:
        print(f"Error saat membuat direktori: {e}")

def menu_admin():
    """Menu utama untuk admin."""
    if not autentikasi_admin():
        return
    
    inisialisasi_sistem()
    
    try:
        with open('menu.json', 'r') as file:
            kategori_menu = json.load(file)
    except FileNotFoundError:
        kategori_menu = {}
    except json.JSONDecodeError:
        print("File json tidak ditemukan.")
        kategori_menu = {}

    try:
        with open('reservations.json', 'r') as file:
            reservations = json.load(file)
    except FileNotFoundError:
        reservations = {}
    except json.JSONDecodeError:
        print("Format file reservations.json tidak valid. Menggunakan reservasi kosong.")
        reservations = {}

    while True:
        print("\n=== Menu Admin ===")
        print("1. Tampilkan Menu")
        print("2. Tambah Menu")
        print("3. Update Menu")
        print("4. Hapus Menu")
        print("5. Tampilkan Reservasi")
        print("6. Hapus Reservasi")
        print("7. Tampilkan Orderan")  
        print("8. Hapus Orderan")      # Tambahkan ini
        print("9. Keluar")             # Tambahkan ini
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tampilkan_menu()
        elif pilihan == '2':
            tambah_menu(kategori_menu)
        elif pilihan == '3':
            update_menu(kategori_menu)
        elif pilihan == '4':
            hapus_menu(kategori_menu)
        elif pilihan == '5':
            tampilkan_reservasi()
        elif pilihan == '6':
            hapus_reservasi(reservations)
        elif pilihan == '7':
            tampilkan_orderan()
        elif pilihan == '8':           # Tambahkan ini
            hapus_orderan()
        elif pilihan == '9':           # Tambahkan ini
            print("Keluar dari menu admin.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
menu_admin()