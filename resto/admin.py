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

def tambah_menu(menu_item):
    """Menambahkan menu baru."""
    while True:
        print("\n=== Tambah Menu ===")
        nama_item = input("Masukkan nama item (atau tekan Enter untuk selesai): ").title()
        if not nama_item:
            break
        harga_input = input(f"Masukkan harga untuk {nama_item}: ")
        if harga_input.isdigit() and int(harga_input) > 0:
            harga = int(harga_input)
            deskripsi = input(f"Masukkan deskripsi untuk {nama_item}: ")
            komposisi = input(f"Masukkan komposisi untuk {nama_item} (pisahkan dengan koma, contoh: Ayam, Tepung, Rempah): ")
            menu_item[nama_item] = {
                "harga": harga,
                "deskripsi": deskripsi,
                "komposisi": [komponen.strip() for komponen in komposisi.split(",")]
            }
            print(f"{nama_item} telah ditambahkan.")
        else:
            print("Harga harus berupa angka positif.")

        lanjut = input("Apakah Anda ingin menambah menu lain? (ya/tidak): ").lower()
        if lanjut != 'ya':
            break

def update_menu(menu_item):
    """Memperbarui menu yang ada."""
    print("\n=== Update Menu ===")
    nama_item = input("Masukkan nama item yang ingin diperbarui: ").title()
    if nama_item in menu_item:
        print(f"Item ditemukan: {nama_item}")
        harga_input = input(f"Masukkan harga baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ")
        if harga_input.isdigit() and int(harga_input) > 0:
            menu_item[nama_item]['harga'] = int(harga_input)
        deskripsi = input(f"Masukkan deskripsi baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ")
        if deskripsi:
            menu_item[nama_item]['deskripsi'] = deskripsi
        komposisi = input(f"Masukkan komposisi baru untuk {nama_item} (kosongkan jika tidak ingin mengubah): ")
        if komposisi:
            menu_item[nama_item]['komposisi'] = [komponen.strip() for komponen in komposisi.split(",")]
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
    try:
        menu_item = tampilkan_menu()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        menu_item = {}

    try:
        reservations = tampilkan_reservasi()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
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
