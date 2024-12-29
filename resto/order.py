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
        # Cek apakah kunci deskripsi dan komposisi ada
        deskripsi = info.get('deskripsi', 'Tidak tersedia.')
        komposisi = info.get('komposisi', ['Tidak tersedia.'])
        print(f"  Deskripsi: {','.join(deskripsi)}")
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

def edit_pesanan(keranjang, menu_item):
     while True:
        print("\n=== Edit Keranjang ===")
        print("Keranjang Anda saat ini:")
        for item, data in keranjang.items():
            print(f"- {item} (x{data['jumlah']}) | Catatan: {data['catatan']}")

        pilihan = input("Apakah Anda ingin mengedit, menghapus, atau menambah item? (edit/hapus/tambah/selesai): ").lower()
        if pilihan not in ["edit", "hapus", "tambah", "selesai"]:
            print("Pilihan tidak valid. Silakan coba lagi.")
            continue

        if pilihan == "selesai":
            break

        if pilihan == "edit" or pilihan == "hapus":
            nama_item = input("Masukkan nama item yang ingin diubah: ").title()
            if nama_item in keranjang:
                if pilihan == "edit":
                    jumlah_input = input(f"Masukkan jumlah baru untuk {nama_item}: ")
                    if jumlah_input.isdigit() and int(jumlah_input) > 0:
                        jumlah = int(jumlah_input)
                        catatan = input(f"Masukkan catatan baru untuk {nama_item}: ")
                        keranjang[nama_item]["jumlah"] = jumlah
                        keranjang[nama_item]["catatan"] = catatan
                        print(f"Pesanan {nama_item} telah diperbarui.")
                    else:
                        print("Jumlah harus berupa angka positif.")
                elif pilihan == "hapus":
                    del keranjang[nama_item]
                    print(f"Pesanan {nama_item} telah dihapus dari keranjang.")
            else:
                print("Item tidak ditemukan dalam keranjang.")

        elif pilihan == "tambah":
            print("\n=== Daftar Menu ===")
            for item, info in menu_item.items():
                print(f"- {item}: Rp{info['harga']}")

            nama_item = input("Masukkan nama item yang ingin ditambahkan: ").title()
            if nama_item in menu_item:
                jumlah_input = input(f"Masukkan jumlah untuk {nama_item}: ")
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
                    print(f"{jumlah} {nama_item} ditambahkan ke keranjang.")
                else:
                    print("Jumlah harus berupa angka positif.")
            else:
                print("Item tidak ditemukan dalam menu.")

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

def hitung_split_bill(keranjang, menu_item):
    while True:
        print("\n=== Split Bill ===")
        jumlah_orang = input("Masukkan jumlah orang untuk membagi tagihan: ")
        if jumlah_orang.isdigit() and int(jumlah_orang) > 0:
            jumlah_orang = int(jumlah_orang)
            break
        else:
            print("Jumlah orang harus berupa angka positif.")

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
                        print("Jumlah melebihi pesanan yang tersedia.")
                else:
                    print("Jumlah harus berupa angka positif.")
            else:
                print("Item tidak ditemukan atau sudah habis.")

        print(f"Total untuk Orang {i}: Rp{total_orang}")
        total_per_orang.append({"Orang": i, "Total": total_orang})
        total_split += total_orang

    print("\n=== Total Split Bill ===")
    for data in total_per_orang:
        print(f"Orang {data['Orang']}: Rp{data['Total']}")

    print(f"\nTotal semua tagihan (split): Rp{total_split}")
    return total_split

menu_item = tampilkan_menu()
if menu_item:
        keranjang, total_belanja = buat_pesanan(menu_item)

        # Cek apakah total belanja memenuhi syarat minimal order
        while total_belanja < 75000:
            print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
            print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
            tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
            for item, data in tambahan_keranjang.items():
                if item in keranjang:
                    keranjang[item]["jumlah"] += data["jumlah"]
                else:
                    keranjang[item] = data
            total_belanja += tambahan_belanja

if 'keranjang' in locals() and 'total_belanja' in locals():
    while True:
        tampilkan_ringkasan(keranjang, total_belanja, menu_item)
        edit = input("Apakah Anda ingin mengedit pesanan Anda? (ya/tidak): ").lower()
        if edit == "ya":
            edit_pesanan(keranjang, menu_item)
            total_belanja = sum(menu_item[item]["harga"] * data["jumlah"] for item, data in keranjang.items())
            if total_belanja < 75000:
                print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
                print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
                tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
                for item, data in tambahan_keranjang.items():
                    if item in keranjang:
                        keranjang[item]["jumlah"] += data["jumlah"]
                    else:
                        keranjang[item] = data
                total_belanja += tambahan_belanja
        elif edit == "tidak":
            if total_belanja < 75000:
                print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
                print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
                tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
                for item, data in tambahan_keranjang.items():
                    if item in keranjang:
                        keranjang[item]["jumlah"] += data["jumlah"]
                    else:
                        keranjang[item] = data
                total_belanja += tambahan_belanja
            else:
                break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

    while True:
        if total_belanja < 75000:
            print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
            print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
            tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
            for item, data in tambahan_keranjang.items():
                if item in keranjang:
                    keranjang[item]["jumlah"] += data["jumlah"]
                else:
                    keranjang[item] = data
            total_belanja += tambahan_belanja
        else:
            pilihan = input("\nApakah Anda ingin membagi tagihan? (ya/tidak): ").lower()
            if pilihan == "ya":
                total_split = hitung_split_bill(keranjang, menu_item)
                if total_split < total_belanja:
                    print("\nAda perbedaan dalam perhitungan. Mohon periksa ulang pesanan masing-masing.")
                break
            elif pilihan == "tidak":
                print("Terima kasih! Silakan bayar di kasir.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
