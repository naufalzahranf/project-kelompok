import json

def tambah_menu():
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
    except FileNotFoundError:
        menu_item = {}

    while True:
        print("\n=== Menu Admin ===")
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
            print(f"{nama_item} dengan harga Rp{harga}, deskripsi, dan komposisi telah ditambahkan.")
        else:
            print("Harga harus berupa angka positif.")

        lanjut = input("Apakah Anda ingin menambah menu lain? (ya/tidak): ").lower()
        if lanjut != 'ya':
            break

    with open('menu.json', 'w') as file:
        json.dump(menu_item, file, indent=4)
    print("Menu berhasil disimpan.")

if __name__ == '__main__':
    tambah_menu()
