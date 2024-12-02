print("hallo saya naufal")
print("kalau saya nugra")
print("hallo saya louisy")
print("hallo saya ikshan")

import json

def tampilkan_menu():
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
    except FileNotFoundError:
        print("Menu belum tersedia. Admin belum menambah menu.")
        return None

    print("\n=== Menu Restoran ===")
    for item, info in menu_item.items():
        print(f"- {item}: Rp{info['harga']}")
        deskripsi = info.get('deskripsi', 'Tidak tersedia.')
        komposisi = info.get('komposisi', ['Tidak tersedia.'])
        print(f"  Deskripsi: {deskripsi}")
        print(f"  Komposisi: {', '.join(komposisi)}")
    return menu_item

def buat_pesanan(menu_item):
    keranjang = []
    total_belanja = 0

    while True:
        print("\n=== Order Menu ===")
        nama_item = input("Masukkan nama item yang ingin dipesan (atau tekan Enter untuk selesai): ").title()
        if not nama_item:
            break
        if nama_item in menu_item:
            jumlah_input = input(f"Masukkan jumlah {nama_item}: ")
            if jumlah_input.isdigit() and int(jumlah_input) > 0:
                jumlah = int(jumlah_input)
                catatan = input(f"Tambahkan catatan khusus untuk {nama_item}: ")
                keranjang.append({"item": nama_item, "jumlah": jumlah, "catatan": catatan})
                total_belanja += menu_item[nama_item]["harga"] * jumlah
                print(f"{jumlah} {nama_item} ditambahkan ke keranjang.")
            else:
                print("Jumlah harus berupa angka positif.")
        else:
            print("Item tidak ditemukan dalam menu.")

    return keranjang, total_belanja

def tampilkan_ringkasan(keranjang, total_belanja, menu_item):
    if total_belanja > 0:
        print("\n=== Ringkasan Pesanan ===")
        for entri in keranjang:
            item = entri["item"]
            jumlah = entri["jumlah"]
            catatan = entri["catatan"]
            print(f"{item} (x{jumlah}) - Rp{menu_item[item]['harga'] * jumlah} | Catatan: {catatan}")
        print(f"Total harga: Rp{total_belanja}")
    else:
        print("Tidak ada pesanan yang dibuat.")

def minimal_belanja(keranjang, total_belanja, menu_item, minimal_order):
    while total_belanja < minimal_order:
        print(f"\nTotal belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp{minimal_order}.")
        print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
        tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
        keranjang.extend(tambahan_keranjang)
        total_belanja += tambahan_belanja
    return keranjang, total_belanja

def reservasi_meja():
    try:
        with open('reservations.json', 'r') as file:
            reservations = json.load(file)
    except FileNotFoundError:
        reservations = {}

    print("\n=== Reservasi Meja ===")
    meja = input("Masukkan nomor meja yang ingin dipesan (misal: Meja 1): ").title()
    if meja in reservations:
        print(f"Maaf, {meja} sudah dipesan.")
    else:
        nama_pelanggan = input("Masukkan nama Anda: ")
        waktu = input("Masukkan waktu kedatangan (misal: 19:00): ")
        while True:
            jumlah_orang_input = input("Masukkan jumlah orang yang akan duduk di meja: ")
            if jumlah_orang_input.isdigit() and int(jumlah_orang_input) > 0:
                jumlah_orang = int(jumlah_orang_input)
                break
            else:
                print("Jumlah orang harus berupa angka positif. Silakan coba lagi.")

        reservations[meja] = {
            "nama": nama_pelanggan,
            "waktu": waktu,
            "jumlah_orang": jumlah_orang
        }

        with open('reservations.json', 'w') as file:
            json.dump(reservations, file, indent=4)

        print(f"\nReservasi berhasil untuk {meja} pada pukul {waktu} atas nama {nama_pelanggan}.")
        print(f"Jumlah orang: {jumlah_orang}")

        # Pilihan untuk memesan makanan
        print("\nApakah Anda ingin memesan makanan sekarang atau saat tiba di restoran?")
        print("1. Pesan sekarang")
        print("2. Pesan saat tiba di restoran")
        pilihan = input("Masukkan pilihan Anda (1/2): ")

        if pilihan == "1":
            menu_item = tampilkan_menu()
            if menu_item:
                keranjang, total_belanja = buat_pesanan(menu_item)

                # Minimal belanja
                minimal_order = 75000
                keranjang, total_belanja = minimal_belanja(keranjang, total_belanja, menu_item, minimal_order)

                # Ringkasan pesanan
                tampilkan_ringkasan(keranjang, total_belanja, menu_item)

                # Split bill
                pilihan_split = input("\nApakah Anda ingin membagi tagihan? (ya/tidak): ").lower()
                if pilihan_split == "ya":
                    while True:
                        jumlah_orang_input = input("Masukkan jumlah orang untuk membagi tagihan: ")
                        if jumlah_orang_input.isdigit() and int(jumlah_orang_input) > 0:
                            jumlah_orang = int(jumlah_orang_input)
                            bagian_per_orang = total_belanja / jumlah_orang
                            print(f"Setiap orang harus membayar: Rp{bagian_per_orang:.2f}")
                            break
                        else:
                            print("Jumlah orang harus berupa angka positif.")
                else:
                    print("Terima kasih! Pesanan Anda telah tercatat.")
            print(f"\nTerima kasih! Anda diharapkan datang 1 jam sebelum waktu reservasi, yaitu pukul {int(waktu.split(':')[0]) - 1:00}:00.")
        elif pilihan == "2":
            waktu_sebelum = f"{int(waktu.split(':')[0]) - 1:00}:00"
            print(f"\nTerima kasih! Anda harus datang 1 jam sebelum waktu reservasi (pukul {waktu_sebelum}).")
            print("Silakan lakukan pemesanan di restoran saat tiba.")
        else:
            print("Pilihan tidak valid. Reservasi selesai tanpa pesanan.")


if __name__ == '__main__':
    reservasi_meja()