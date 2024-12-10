import json

def tampilkan_menu():
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
    except FileNotFoundError:
        print("Menu belum terse dia. Admin belum menambah menu.")
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
    keranjang = {}
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
                if nama_item in keranjang:
                    keranjang[nama_item]["jumlah"] += jumlah
                else:
                    keranjang[nama_item] = {
                        "jumlah": jumlah,
                        "catatan": catatan
                    }
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
        for item, data in keranjang.items():
            jumlah = data["jumlah"]
            catatan = data["catatan"]
            print(f"{item} (x{jumlah}) - Rp{menu_item[item]['harga'] * jumlah} | Catatan: {catatan}")
        print(f"Total harga: Rp{total_belanja}")
    else:
        print("Tidak ada pesanan yang dibuat.")


def minimal_belanja(keranjang, total_belanja, menu_item, minimal_order):
    while total_belanja < minimal_order:
        print(f"\nTotal belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp{minimal_order}.")
        print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
        tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
        for item, data in tambahan_keranjang.items():
            if item in keranjang:
                keranjang[item]["jumlah"] += data["jumlah"]
            else:
                keranjang[item] = data
        total_belanja += tambahan_belanja
    return keranjang, total_belanja


def hitung_split_bill(keranjang, menu_item):
    print("\n=== Split Bill ===")
    jumlah_orang = input("Masukkan jumlah orang untuk membagi tagihan: ")
    if jumlah_orang.isdigit() and int(jumlah_orang) > 0:
        jumlah_orang = int(jumlah_orang)
        total_split = 0
        total_per_orang = []
        sisa_keranjang = keranjang.copy()

        for i in range(1, jumlah_orang + 1):
            print(f"\nOrang {i}:")
            total_orang = 0
            while True:
                if all(data["jumlah"] == 0 for data in sisa_keranjang.values()):
                    print("Semua pesanan telah dibagi.")
                    break

                item_input = input("Masukkan nama item pesanan Anda (atau tekan Enter untuk selesai): ").title()
                if not item_input:
                    break
                if item_input in sisa_keranjang and sisa_keranjang[item_input]["jumlah"] > 0:
                    jumlah_input = input(f"Masukkan jumlah untuk {item_input} (tersisa {sisa_keranjang[item_input]['jumlah']}): ")
                    if jumlah_input.isdigit() and int(jumlah_input) > 0:
                        jumlah = int(jumlah_input)
                        if jumlah <= sisa_keranjang[item_input]["jumlah"]:
                            total_item = menu_item[item_input]["harga"] * jumlah
                            total_orang += total_item
                            sisa_keranjang[item_input]["jumlah"] -= jumlah
                            print(f"Total untuk {item_input} (x{jumlah}): Rp{total_item}")
                        else:
                            print("Jumlah melebihi pesanan yang tersedia")
                    else:
                        print("Jumlah harus berupa angka positif")
                else:
                    print("Item tidak ditemukan atau sudah habis")

            print(f"Total untuk Orang {i}: Rp{total_orang}")
            total_per_orang.append({"Orang": i, "Total": total_orang})
            total_split += total_orang

        print("\n=== Total Split Bill ===")
        for data in total_per_orang:
            print(f"Orang {data['Orang']}: Rp{data['Total']}")

        print(f"\nTotal semua tagihan (split): Rp{total_split}")
        return total_split
    else:
        print("Jumlah orang harus berupa angka positif.")
        return 0


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

        print("\nApakah Anda ingin memesan makanan sekarang atau saat tiba di restoran?")
        print("1. Pesan sekarang")
        print("2. Pesan saat tiba di restoran")
        pilihan = input("Masukkan pilihan Anda (1/2): ")

        if pilihan == "1":
            menu_item = tampilkan_menu()
            if menu_item:
                keranjang, total_belanja = buat_pesanan(menu_item)

                minimal_order = 75000
                keranjang, total_belanja = minimal_belanja(keranjang, total_belanja, menu_item, minimal_order)

                tampilkan_ringkasan(keranjang, total_belanja, menu_item)

                pilihan_split = input("\nApakah Anda ingin membagi tagihan? (ya/tidak): ").lower()
                if pilihan_split == "ya":
                    total_split = hitung_split_bill(keranjang, menu_item)
                    if total_split < total_belanja:
                        print("\nAda perbedaan dalam perhitungan. Mohon periksa ulang pesanan masing-masing.")
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
