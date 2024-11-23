import json

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

        print(f"Reservasi berhasil untuk {meja} pada pukul {waktu} atas nama {nama_pelanggan}.")
        print(f"Jumlah orang: {jumlah_orang}")

if __name__ == '__main__':
    reservasi_meja()
