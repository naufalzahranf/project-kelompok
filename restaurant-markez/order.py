menu_item = {
    "Nasi Goreng": {"harga": 30000},
    "Ayam Bakar": {"harga": 40000},
    "Teh Manis": {"harga": 10000},
    "Kopi Hitam": {"harga": 15000}
}

MINIMUM_BELANJA = 75000
keranjang = []

print("=== Selamat Datang di Restoran Markez ===")
print("Daftar menu:")
for item, info in menu_item.items():
    print(f"- {item}: Rp{info['harga']}")
for i in range(5):
    nama_item = input(f"\nMasukkan nama item yang ingin dipesan (pesanan ke-{i+1}, atau tekan Enter untuk selesai): ").title()
    if not nama_item:
        break
    if nama_item in menu_item:
        jumlah_input = input(f"Masukkan jumlah {nama_item}: ")
        if jumlah_input.isdigit() and int(jumlah_input) > 0:
            jumlah = int(jumlah_input)
            catatan = input(f"Tambahkan catatan khusus untuk {nama_item} (tekan Enter jika tidak ada): ")
            keranjang.append({"item": nama_item, "jumlah": jumlah, "catatan": catatan})
            print(f"{jumlah} {nama_item} ditambahkan ke keranjang dengan catatan: '{catatan}'.")
        else:
            print("Jumlah harus berupa angka positif.")
    else:
        print("Item tidak ditemukan dalam menu.")

        print("\nIsi keranjang belanja Anda:")
total_belanja = 0
for entri in keranjang:
    item = entri["item"]
    jumlah = entri["jumlah"]
    catatan = entri["catatan"]
    harga = menu_item[item]["harga"]
    total_belanja += harga * jumlah
    print(f"{item} (x{jumlah}) - Rp{harga * jumlah} | Catatan: '{catatan}'")

while True:
    aksi = input("\nApakah Anda ingin mengedit (e) atau menghapus (h) item? (tekan Enter untuk selesai): ").lower()
    if aksi in ['e', 'h']:
        item_tindakan = input("Masukkan nama item yang ingin diedit atau dihapus: ").title()
        item_ditemukan = False
        for entri in keranjang:
            if entri["item"] == item_tindakan:
                item_ditemukan = True
                if aksi == "e":
                    jumlah_edit_input = input(f"Masukkan jumlah baru untuk {item_tindakan} (sekarang x{entri['jumlah']}): ")
                    if jumlah_edit_input.isdigit() and int(jumlah_edit_input) > 0:
                        entri["jumlah"] = int(jumlah_edit_input)
                        print(f"Jumlah {item_tindakan} berhasil diubah menjadi {entri['jumlah']}.")
                    else:
                        print("Jumlah baru harus berupa angka positif.")
                elif aksi == "h":
                    jumlah_hapus_input = input(f"Masukkan jumlah {item_tindakan} yang ingin dihapus: ")
                    if jumlah_hapus_input.isdigit() and int(jumlah_hapus_input) > 0:
                        jumlah_hapus = int(jumlah_hapus_input)
                        if entri["jumlah"] >= jumlah_hapus:
                            entri["jumlah"] -= jumlah_hapus
                            print(f"{jumlah_hapus} {item_tindakan} telah dihapus dari keranjang.")
                            if entri["jumlah"] == 0:
                                keranjang.remove(entri)
                        else:
                            print("Jumlah yang ingin dihapus melebihi jumlah yang ada.")
                    else:
                        print("Jumlah yang ingin dihapus harus berupa angka positif.")
                break
        if not item_ditemukan:
            print("Item tidak ditemukan dalam keranjang.")
        lanjut = input("Apakah Anda ingin mengedit atau menghapus item lain? (ya/tidak): ").lower()
        if lanjut != 'ya':
            break
    else:
        break