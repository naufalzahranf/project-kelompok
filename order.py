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