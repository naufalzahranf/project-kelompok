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

def tampilkan_ringkasan(keranjang, total_belanja):
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

if __name__ == '__main__':
    menu_item = tampilkan_menu()
    if menu_item:
        keranjang, total_belanja = buat_pesanan(menu_item)

        # Cek apakah total belanja memenuhi syarat minimal order
        while total_belanja < 75000:
            print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
            print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
            tambahan_keranjang, tambahan_belanja = buat_pesanan(menu_item)
            keranjang.extend(tambahan_keranjang)
            total_belanja += tambahan_belanja

        tampilkan_ringkasan(keranjang, total_belanja)

        pilihan = input("\nApakah Anda ingin membagi tagihan? (ya/tidak): ").lower()
        if pilihan == "ya":
            jumlah_orang = input("Masukkan jumlah orang untuk membagi tagihan: ")
            if jumlah_orang.isdigit() and int(jumlah_orang) > 0:
                jumlah_orang = int(jumlah_orang)
                bagian_per_orang = total_belanja / jumlah_orang
                print(f"Setiap orang harus membayar: Rp{bagian_per_orang:.2f}")
            else:
                print("Jumlah orang harus berupa angka positif.")
        elif pilihan == "tidak":
            print("Terima kasih! Silakan bayar di kasir.")
        else:
            print("Pilihan tidak valid.")
