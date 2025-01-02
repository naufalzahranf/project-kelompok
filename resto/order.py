import json

def tampilkan_menu():
    try:
        with open('menu.json', 'r') as file:
            kategori_menu = json.load(file)
            if not kategori_menu:
                print("Menu kosong. Admin belum menambah menu.")
                return None
    except FileNotFoundError:
        print("Menu belum tersedia. Admin belum menambah menu.")
        return None

    print("\n=== Menu Restoran ===")
    for kategori, menu_items in kategori_menu.items():
        print(f"\nKategori: {kategori}")
        for nama, detail in menu_items.items():
            deskripsi = ", ".join(detail.get('deskripsi', ['Tidak tersedia']))
            komposisi = ", ".join(detail.get('komposisi', ['Tidak tersedia']))
            print(f"- {nama}: Rp{detail['harga']}")
            print(f"  Deskripsi: {deskripsi}")
            print(f"  Komposisi: {komposisi}")
    return kategori_menu

def pilih_kategori(kategori_menu):
    while True:
        print("\nKategori yang tersedia:")
        for i, kategori in enumerate(kategori_menu.keys(), 1):
            print(f"{i}. {kategori}")
        
        pilihan = input("\nPilih nomor kategori (atau tekan Enter untuk selesai): ")
        if not pilihan:
            return None
        
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(kategori_menu):
            return list(kategori_menu.keys())[int(pilihan) - 1]
        print("Pilihan tidak valid. Silakan coba lagi.")

def buat_pesanan(kategori_menu):
    keranjang = {}
    total_belanja = 0

    while True:
        print("\n=== Order Menu ===")
        kategori_terpilih = pilih_kategori(kategori_menu)
        if not kategori_terpilih:
            break

        print(f"\nMenu dalam kategori {kategori_terpilih}:")
        for nama, detail in kategori_menu[kategori_terpilih].items():
            print(f"- {nama}: Rp{detail['harga']}")
            deskripsi = ", ".join(detail.get('deskripsi', ['Tidak tersedia']))
            komposisi = ", ".join(detail.get('komposisi', ['Tidak tersedia']))
            print(f"  Deskripsi: {deskripsi}")
            print(f"  Komposisi: {komposisi}")

        nama_item = input("\nMasukkan nama item yang ingin dipesan (atau tekan Enter untuk kembali): ").title()
        if not nama_item:
            continue

        if nama_item in kategori_menu[kategori_terpilih]:
            jumlah_input = input(f"Masukkan jumlah {nama_item}: ")
            if jumlah_input.isdigit() and int(jumlah_input) > 0:
                jumlah = int(jumlah_input)
                catatan = input(f"Tambahkan catatan khusus untuk {nama_item}: ").lower()

                kunci = f"{nama_item} ({catatan})"
                if kunci in keranjang:
                    keranjang[kunci]["jumlah"] += jumlah
                else:
                    keranjang[kunci] = {
                        "nama": nama_item,
                        "jumlah": jumlah,
                        "catatan": catatan,
                        "kategori": kategori_terpilih
                    }
                total_belanja += kategori_menu[kategori_terpilih][nama_item]["harga"] * jumlah
                print(f"{jumlah} {nama_item} dengan catatan '{catatan}' ditambahkan ke keranjang.")
            else:
                print("Jumlah harus berupa angka positif.")
        else:
            print("Item tidak ditemukan dalam menu kategori ini.")

    return keranjang, total_belanja

def edit_pesanan(keranjang, kategori_menu):
    while True:
        print("\n=== Edit Keranjang ===")
        if not keranjang:
            print("Keranjang kosong. Tidak ada yang bisa diedit.")
            break

        print("Keranjang Anda saat ini:")
        keranjang_list = list(keranjang.items())
        for i, (item, data) in enumerate(keranjang_list, start=1):
            nama_menu = item.split(" (")[0]
            print(f"{i}. {nama_menu} (x{data['jumlah']}) | Kategori: {data['kategori']} | Catatan: {data['catatan']}")

        pilihan = input("Apakah Anda ingin mengedit, menghapus, atau menambah item? (edit/hapus/tambah/selesai): ").lower()

        if pilihan == "selesai":
            break

        if pilihan == "edit":
            nomor_item = input("Masukkan nomor item yang ingin diubah: ")
            if not nomor_item.isdigit() or int(nomor_item) < 1 or int(nomor_item) > len(keranjang_list):
                print("Nomor item tidak valid. Silakan coba lagi.")
                continue

            nomor_item = int(nomor_item) - 1
            item_key, data_item = keranjang_list[nomor_item]
            nama_menu = item_key.split(" (")[0]

            sub_pilihan = input("Apakah Anda ingin mengedit jumlah atau catatan? (jumlah/catatan): ").lower()

            if sub_pilihan == "jumlah":
                jumlah_baru = input(f"Masukkan jumlah baru untuk {nama_menu}: ")
                if jumlah_baru.isdigit() and int(jumlah_baru) > 0:
                    keranjang[item_key]["jumlah"] = int(jumlah_baru)
                    print(f"Jumlah untuk {nama_menu} telah diperbarui.")
                else:
                    print("Jumlah harus berupa angka positif.")

            elif sub_pilihan == "catatan":
                catatan_baru = input(f"Masukkan catatan baru untuk {nama_menu}: ")
                kunci_baru = f"{nama_menu} ({catatan_baru})"
                keranjang[kunci_baru] = {
                    "jumlah": data_item["jumlah"],
                    "catatan": catatan_baru,
                    "nama": nama_menu,
                    "kategori": data_item["kategori"]
                }
                del keranjang[item_key]
                print(f"Catatan untuk {nama_menu} telah diperbarui.")

            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

        elif pilihan == "hapus":
            nomor_item = input("Masukkan nomor item yang ingin dihapus: ")
            if not nomor_item.isdigit() or int(nomor_item) < 1 or int(nomor_item) > len(keranjang_list):
                print("Nomor item tidak valid. Silakan coba lagi.")
                continue

            nomor_item = int(nomor_item) - 1
            item_key, _ = keranjang_list[nomor_item]
            nama_menu = item_key.split(" (")[0]
            del keranjang[item_key]
            print(f"Item '{nama_menu}' telah dihapus dari keranjang.")

        elif pilihan == "tambah":
            tambahan_keranjang, tambahan_belanja = buat_pesanan(kategori_menu)
            for item, data in tambahan_keranjang.items():
                if item in keranjang:
                    keranjang[item]["jumlah"] += data["jumlah"]
                else:
                    keranjang[item] = data

        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def tampilkan_ringkasan(keranjang, total_belanja, kategori_menu):
    if total_belanja > 0:
        print("\n" + "="*60)
        print(" "*20 + "RINGKASAN PESANAN")
        print("="*60)
        
        print("\nDaftar Pesanan:")
        print("-"*60)
        print(f"{'No.':<4} {'Menu':<20} {'Kategori':<12} {'Jumlah':<8} {'Subtotal':<12} {'Catatan'}")
        print("-"*60)
        
        for idx, (kunci, data) in enumerate(keranjang.items(), start=1):
            jumlah = data["jumlah"]
            nama_item = data["nama"]
            kategori = data["kategori"]
            catatan = data["catatan"]
            subtotal = kategori_menu[kategori][nama_item]['harga'] * jumlah
            
            print(f"{idx:<4} {nama_item:<20} {kategori:<12} x{jumlah:<7} Rp{subtotal:<10} {catatan}")
        
        print("-"*60)
        print(f"{'Total Belanja:':<45} Rp{total_belanja}")
        print("="*60)
    else:
        print("\nTidak ada pesanan yang dibuat.")

def hitung_split_bill(keranjang, kategori_menu, total_belanja):
    # Tampilkan ringkasan pesanan terlebih dahulu
    print("\n" + "="*60)
    print(" "*20 + "RINGKASAN PESANAN")
    print("="*60)
    
    print("\nDaftar Pesanan:")
    print("-"*60)
    print(f"{'No.':<4} {'Menu':<20} {'Kategori':<12} {'Jumlah':<8} {'Subtotal':<12} {'Catatan'}")
    print("-"*60)
    
    for idx, (kunci, data) in enumerate(keranjang.items(), start=1):
        jumlah = data["jumlah"]
        nama_item = data["nama"]
        kategori = data["kategori"]
        catatan = data["catatan"]
        subtotal = kategori_menu[kategori][nama_item]['harga'] * jumlah
        print(f"{idx:<4} {nama_item:<20} {kategori:<12} x{jumlah:<7} Rp{subtotal:<10} {catatan}")
    
    print("-"*60)
    print(f"{'Total Belanja:':<45} Rp{total_belanja}")
    print("="*60)

    while True:
        print("\n=== Bagi Tagihan ===")
        jumlah_pelanggan = input("Masukkan jumlah pelanggan untuk membagi tagihan: ")
        if jumlah_pelanggan.isdigit() and int(jumlah_pelanggan) > 0:
            jumlah_pelanggan = int(jumlah_pelanggan)
            break
        else:
            print("Jumlah pelanggan harus berupa angka positif.")

    total_split = 0
    total_per_pelanggan = []
    pesanan_per_pelanggan = []
    sisa_keranjang = keranjang.copy()

    for i in range(1, jumlah_pelanggan + 1):
        print(f"\nPelanggan {i}:")
        total_pelanggan = 0
        pesanan_pelanggan = []
        
        while True:
            if all(data["jumlah"] == 0 for data in sisa_keranjang.values()):
                print("Semua pesanan telah dibagi.")
                break

            print("\nDaftar menu yang tersedia:")
            menu_tersedia = [(key, data) for key, data in sisa_keranjang.items() if data["jumlah"] > 0]
            for idx, (item, data) in enumerate(menu_tersedia, start=1):
                nama_menu = item.split(" (")[0]
                print(f"{idx}. {nama_menu} ({data['kategori']}) (tersisa {data['jumlah']}) | Catatan: {data['catatan']}")

            pilihan_menu = input("Masukkan nomor menu yang ingin dipesan (atau tekan Enter untuk selesai): ")
            if not pilihan_menu:
                break

            if pilihan_menu.isdigit() and 1 <= int(pilihan_menu) <= len(menu_tersedia):
                menu_dipilih, data_menu = menu_tersedia[int(pilihan_menu) - 1]
                jumlah_input = input(f"Masukkan jumlah untuk {menu_dipilih} (tersisa {data_menu['jumlah']}): ")
                
                if jumlah_input.isdigit() and int(jumlah_input) > 0:
                    jumlah = int(jumlah_input)
                    if jumlah <= data_menu["jumlah"]:
                        nama_menu = data_menu["nama"]
                        kategori = data_menu["kategori"]
                        total_item = kategori_menu[kategori][nama_menu]["harga"] * jumlah
                        total_pelanggan += total_item
                        sisa_keranjang[menu_dipilih]["jumlah"] -= jumlah
                        
                        pesanan_pelanggan.append({
                            "menu": nama_menu,
                            "kategori": kategori,
                            "jumlah": jumlah,
                            "total": total_item,
                            "catatan": data_menu["catatan"]
                        })
                        
                        print(f"Total untuk {menu_dipilih} (x{jumlah}): Rp{total_item}")
                    else:
                        print("Jumlah pesanan melebihi sisa yang tersedia.")
                else:
                    print("Jumlah pesanan harus berupa angka positif.")
            else:
                print("Nomor menu tidak valid. Silakan coba lagi.")

        print(f"\nTotal untuk Pelanggan {i}: Rp{total_pelanggan}")
        total_per_pelanggan.append({"Pelanggan": i, "Total": total_pelanggan})
        pesanan_per_pelanggan.append({"Pelanggan": i, "Pesanan": pesanan_pelanggan})
        total_split += total_pelanggan

    print("\n" + "="*60)
    print(" "*20 + "RINGKASAN BAGI TAGIHAN")
    print("="*60)

    for data_pelanggan in pesanan_per_pelanggan:
        pelanggan = data_pelanggan["Pelanggan"]
        pesanan = data_pelanggan["Pesanan"]
        total = next(x["Total"] for x in total_per_pelanggan if x["Pelanggan"] == pelanggan)
        
        print(f"\nPelanggan {pelanggan}:")
        print("-"*60)
        print(f"{'No.':<4} {'Menu':<20} {'Kategori':<12} {'Jumlah':<8} {'Subtotal':<12} {'Catatan'}")
        print("-"*60)
        
        for idx, item in enumerate(pesanan, start=1):
            print(f"{idx:<4} {item['menu']:<20} {item['kategori']:<12} x{item['jumlah']:<7} Rp{item['total']:<10} {item['catatan']}")
        
        print("-"*60)
        print(f"{'Total Bagian:':<45} Rp{total}")
        print("="*60)

    print(f"\nTotal semua tagihan: Rp{total_split}")
    return total_split
# Main program
kategori_menu = tampilkan_menu()
if kategori_menu:
    keranjang, total_belanja = buat_pesanan(kategori_menu)

    # Cek apakah total belanja memenuhi syarat minimal order
    while total_belanja < 75000:
        print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
        print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
        tambahan_keranjang, tambahan_belanja = buat_pesanan(kategori_menu)
        for item, data in tambahan_keranjang.items():
            if item in keranjang:
                keranjang[item]["jumlah"] += data["jumlah"]
            else:
                keranjang[item] = data
        total_belanja += tambahan_belanja

if 'keranjang' in locals() and 'total_belanja' in locals():
    while True:
        tampilkan_ringkasan(keranjang, total_belanja, kategori_menu)
        edit = input("Apakah Anda ingin mengedit pesanan Anda? (ya/tidak): ").lower()
        if edit == "ya":
            edit_pesanan(keranjang, kategori_menu)
            # Hitung ulang total belanja
            total_belanja = sum(
                kategori_menu[data["kategori"]][data["nama"]]["harga"] * data["jumlah"]
                for data in keranjang.values()
            )
            if total_belanja < 75000:
                print(f"Total belanja Anda saat ini Rp{total_belanja}. Minimal belanja adalah Rp75.000.")
                print("Silakan tambahkan pesanan untuk memenuhi syarat minimal belanja.")
                tambahan_keranjang, tambahan_belanja = buat_pesanan(kategori_menu)
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
                tambahan_keranjang, tambahan_belanja = buat_pesanan(kategori_menu)
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
            tambahan_keranjang, tambahan_belanja = buat_pesanan(kategori_menu)
            for item, data in tambahan_keranjang.items():
                if item in keranjang:
                    keranjang[item]["jumlah"] += data["jumlah"]
                else:
                    keranjang[item] = data
            total_belanja += tambahan_belanja
        else:
            pilihan = input("\nApakah Anda ingin membagi tagihan? (ya/tidak): ").lower()
            if pilihan == "ya":
                total_split = hitung_split_bill(keranjang, kategori_menu, total_belanja)
                if total_split < total_belanja:
                    print("\nAda perbedaan dalam perhitungan. Mohon periksa ulang pesanan masing-masing.")
                break
            elif pilihan == "tidak":
                print("Terima kasih! Silakan bayar di kasir.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
