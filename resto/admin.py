import json

def tampilkan_menu():
    """Menampilkan daftar menu."""
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
    except FileNotFoundError:
        menu_item = {}

    if not menu_item:
        print("Menu kosong.")
    else:
        print("\n=== Daftar Menu ===")
        for nama, detail in menu_item.items():
            print(f"- {nama}: Rp{detail['harga']}, Deskripsi: {detail['deskripsi']}, Komposisi: {', '.join(detail['komposisi'])}")
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
        if all(komponen.replace(" ", "").isalpha() for komponen in value.split(",")):
            return [komponen.strip() for komponen in value.split(",")]
        print("Input deskripsi hanya boleh berupa huruf, spasi, dan koma. Coba lagi.")

def validasi_input_komposisi(pesan):
    """Memvalidasi input komposisi untuk memastikan hanya huruf, spasi, dan koma."""
    while True:
        value = input(pesan).strip()
        if all(komponen.replace(" ", "").isalpha() for komponen in value.split(",")):
            return [komponen.strip() for komponen in value.split(",")]
        print("Input komposisi hanya boleh berupa huruf, spasi, dan koma. Coba lagi.")

def tambah_menu(menu_item):
    """Menambahkan menu baru."""
    if menu_item is None:
        menu_item = {}
    while True:
        print("\n=== Tambah Menu ===")
        nama_item = validasi_input_abjad("Masukkan nama item (atau tekan Enter untuk selesai): ").title()
        if not nama_item:
            print("Nama item tidak boleh kosong. Coba lagi.")
            continue

        harga = validasi_input_angka(f"Masukkan harga untuk {nama_item}: ")

        deskripsi = validasi_input_deskripsi(f"Masukkan deskripsi untuk {nama_item}: ")

        komposisi = validasi_input_komposisi(f"Masukkan komposisi untuk {nama_item} (pisahkan dengan koma, contoh: Ayam, Tepung, Rempah): ")

        menu_item[nama_item] = {
            "harga": harga,
            "deskripsi": deskripsi,
            "komposisi": komposisi
        }
        print(f"{nama_item} telah ditambahkan.")
        break
    
def update_menu(menu_item):
    """Memperbarui menu yang ada."""
    print("\n=== Update Menu ===")
    nama_item = input("Masukkan nama item yang ingin diperbarui: ").title()
    if nama_item in menu_item:
        print(f"Item ditemukan: {nama_item}")

        while True:
            harga_input = input(f"Masukkan harga baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ").strip()
            if not harga_input:
                break
            if harga_input.isdigit() and int(harga_input) > 0:
                menu_item[nama_item]['harga'] = int(harga_input)
                break
            else:
                print("Harga harus berupa angka positif. Coba lagi.")

        deskripsi_input = input(f"Masukkan deskripsi baru untuk {nama_item} (pisahkan dengan koma, kosongkan jika tidak ingin mengubah): ").strip()
        if deskripsi_input:
            menu_item[nama_item]['deskripsi'] = [komponen.strip() for komponen in deskripsi_input.split(",")]

        komposisi_input = input(f"Masukkan komposisi baru untuk {nama_item} (pisahkan dengan koma, kosongkan jika tidak ingin mengubah): ").strip()
        if komposisi_input:
            menu_item[nama_item]['komposisi'] = [komponen.strip() for komponen in komposisi_input.split(",")]

        print(f"{nama_item} telah diperbarui.")
    else:
        print(f"{nama_item} tidak ditemukan.")

def hapus_menu(menu_item):
    """Menghapus menu."""
    print("\n=== Hapus Menu ===")
    nama_item = input("Masukkan nama item yang ingin dihapus: ").title()
    if nama_item in menu_item:
        del menu_item[nama_item]
        print(f"{nama_item} telah dihapus.")
    else:
        print(f"{nama_item} tidak ditemukan.")
        
def simpan_menu(menu_item):
    """Menyimpan menu ke file."""
    with open('menu.json', 'w') as file:
        json.dump(menu_item, file, indent=4)
    print("Menu berhasil disimpan.")

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
            print(f"- {meja}: Nama: {detail['nama']}, Waktu: {detail['waktu']}, Jumlah Orang: {detail['jumlah_orang']}")
    return reservations

def hapus_reservasi(reservations):
    """Menghapus reservasi."""
    print("\n=== Hapus Reservasi ===")
    nomor_meja = input("Masukkan nomor meja yang ingin dihapus (contoh: Meja 1): ").title()
    if nomor_meja in reservations:
        del reservations[nomor_meja]
        print(f"Reservasi pada {nomor_meja} telah dihapus.")
    else:
        print(f"Reservasi pada {nomor_meja} tidak ditemukan.")

def simpan_reservasi(reservations):
    """Menyimpan reservasi ke file."""
    with open('reservations.json', 'w') as file:
        json.dump(reservations, file, indent=4)
    print("Reservasi berhasil disimpan.")

def menu_admin():
    """Menu utama untuk admin."""
    if not autentikasi_admin():
        return
    
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
    except FileNotFoundError:
        menu_item = {}
    except json.JSONDecodeError:
        print("File json tidak ditemukan.")
        menu_item = {}

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
        print("7. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tampilkan_menu()
        elif pilihan == '2':
            tambah_menu(menu_item)
        elif pilihan == '3':
            update_menu(menu_item)
        elif pilihan == '4':
            hapus_menu(menu_item)
        elif pilihan == '5':
            tampilkan_reservasi()
        elif pilihan == '6':
            hapus_reservasi(reservations)
        elif pilihan == '7':
            simpan_menu(menu_item)
            simpan_reservasi(reservations)
            print("Keluar dari menu admin.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

menu_admin()
