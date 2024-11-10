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
