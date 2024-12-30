import json
from datetime import datetime

def tampilkan_menu():
    try:
        with open('menu.json', 'r') as file:
            menu_item = json.load(file)
            if not menu_item:
                print("Menu kosong. Admin belum menambah menu.")
                return None
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
                    sub_pilihan = input("Apakah Anda ingin mengedit jumlah, catatan, atau keduanya? (jumlah/catatan/keduanya): ").lower()
                    if sub_pilihan == "jumlah" or sub_pilihan == "keduanya":
                        jumlah_input = input(f"Masukkan jumlah baru untuk {nama_item}: ")
                        if jumlah_input.isdigit() and int(jumlah_input) > 0:
                            jumlah = int(jumlah_input)
                            keranjang[nama_item]["jumlah"] = jumlah
                            print(f"Jumlah {nama_item} telah diperbarui menjadi {jumlah}.")
                        else:
                            print("Jumlah harus berupa angka positif.")
                    if sub_pilihan == "catatan" or sub_pilihan == "keduanya":
                        catatan = input(f"Masukkan catatan baru untuk {nama_item}: ")
                        keranjang[nama_item]["catatan"] = catatan
                        print(f"Catatan untuk {nama_item} telah diperbarui.")
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
                    catatan_baru= input(f"Tambahkan catatan khusus untuk {nama_item}: ")
                    if nama_item in keranjang:
                        keranjang[nama_item]["jumlah"] += jumlah
                        if catatan_baru:
                            keranjang[nama_item]["catatan"] += f"; {catatan_baru}"
                        else:
                            keranjang[nama_item] = {
                            "jumlah": jumlah,
                            "catatan": catatan_baru
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
            content = file.read().strip()  # Membaca isi file
            reservations = json.loads(content) if content else {}  # Periksa jika kosong
    except FileNotFoundError:
        reservations = {}  # Jika file tidak ditemukan, inisialisasi dictionary kosong

    print("\n=== Reservasi Meja ===")
    while True:
        meja = input("Masukkan nomor meja yang ingin dipesan (1-20): ").title()
        if meja.isdigit() and 1 <= int(meja) <= 20:
            meja = f"Meja {int(meja)}"
            break
        else:
            print("Input tidak valid. Pilih nomor meja dari 1 hingga 20 tanpa simbol atau huruf.")

    if meja in reservations:
        print(f"Maaf, {meja} sudah dipesan.")
        return meja 

    while True:
        nama_pelanggan = input("Masukkan nama Anda: ")
        if all(char.isalpha() or char.isspace() for char in nama_pelanggan) and nama_pelanggan.strip():
            break
        else:
            print("Nama hanya boleh berisi huruf dan spasi, dan tidak boleh kosong. Silakan coba lagi.")

    while True:
        tanggal = input("Masukkan tanggal kedatangan (YYYY-MM-DD): ")
        try:
            tanggal_kedatangan = datetime.strptime(tanggal, "%Y-%m-%d").date()
            if tanggal_kedatangan < datetime.now().date():
                print("Tanggal kedatangan tidak boleh di masa lalu. Silakan coba lagi.")
            else:
                break
        except ValueError:
            print("Format tanggal tidak valid. Masukkan dalam format YYYY-MM-DD (contoh: 2024-12-28).")

    while True:
        waktu = input("Masukkan waktu kedatangan (HH:MM): ")
        if len(waktu) == 5 and waktu[:2].isdigit() and waktu[3:].isdigit() and waktu[2] == ':' and 0 <= int(waktu[:2]) <= 23 and 0 <= int(waktu[3:]) <= 59:
            jam, menit = map(int, waktu.split(':'))
            if jam < 11:
                print("Maaf, resto belum buka. Jam operasional mulai pukul 11:00 pagi.")
            elif jam >= 21:
                print("Maaf, resto sudah tutup. Jam operasional sampai pukul 22:00 malam.")
            else:
                break
        else: 
            print("Format waktu tidak valid. Masukkan dalam format HH:MM (contoh: 19:00).")

    while True:
        jumlah_orang_input = input("Masukkan jumlah orang yang akan duduk di meja: ")
        if jumlah_orang_input.isdigit() and  1 <= int(jumlah_orang_input) <= 20:
            jumlah_orang = int(jumlah_orang_input)
            break
        else:
            print("Jumlah orang melebihi kapasitas. Jumlah orang harus berupa angka positif. Silakan coba lagi.")

    while True:
        no_telepon = input("Masukkan nomor telepon Anda (minimal 12 digit, maksimal 13 digit, format Indonesia): ")
        if no_telepon.isdigit() and 12 <= len(no_telepon) <= 13 and no_telepon.startswith("08"):
            break
        else:
            print("Nomor telepon harus berupa angka, memiliki 12-13 digit, dan diawali dengan '08'. Silakan coba lagi.")

    reservations[meja] = {
        "nama": nama_pelanggan,
        "tanggal": tanggal,
        "waktu": waktu,
        "jumlah_orang": jumlah_orang,
        "no_telepon": no_telepon
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

                # Memastikan pengecekan minimal belanja dilakukan setelah pesanan dibuat
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

                # Menampilkan ringkasan pesanan dan edit jika perlu
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

                    # Meminta pengguna untuk membagi tagihan atau tidak
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

            jam, menit = map(int, waktu.split(':'))
            jam_sebelum = (jam - 1) % 24
            waktu_sebelum = f"{jam_sebelum:02}:{menit:02}"
            print(f"\nTerima kasih! Anda diharapkan datang 1 jam sebelum waktu reservasi, yaitu pukul {waktu_sebelum}.")
            return
        elif pilihan == "2":
            jam, menit = map(int, waktu.split(':'))
            jam_sebelum = (jam - 1) % 24
            waktu_sebelum = f"{jam_sebelum:02}:{menit:02}"
            print(f"\nTerima kasih! Anda harus datang 1 jam sebelum waktu reservasi (pukul {waktu_sebelum}).")
            print("Silakan lakukan pemesanan di restoran saat tiba.")
        else:
            print("Pilihan tidak valid. Reservasi selesai tanpa pesanan.")

reservasi_meja()