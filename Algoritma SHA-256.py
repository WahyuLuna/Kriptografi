import tkinter as tk
from tkinter import Label, Entry, Button, Text, messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import hashlib

def create_hash(data):
    # Membuat objek hash
    hasher = hashlib.sha256()

    # Mengupdate hash dengan data
    hasher.update(data.encode('utf-8'))

    # Mengambil nilai hash dalam format heksadesimal
    hash_value = hasher.hexdigest()

    return hash_value

def encrypt_message(key):
    # Menggunakan hasil hashing dari kunci sebagai kunci enkripsi
    hashed_key = create_hash(key)
    hashed_key = hashed_key.ljust(8)[:8]

    # Membuat objek DES Cipher dengan mode ECB
    cipher = DES.new(hashed_key.encode(), DES.MODE_ECB)
    return cipher

def encrypt(name, message, key):
    cipher = encrypt_message(key)
    # Melakukan enkripsi message
    padded_message = pad(message.encode(), DES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    
    # Melakukan enkripsi name
    padded_name = pad(name.encode(), DES.block_size)
    encrypted_name = cipher.encrypt(padded_name)
    
    # Melakukan enkripsi key
    padded_key = pad(key.encode(), DES.block_size)
    encrypted_key = cipher.encrypt(padded_key)
    
    a = b64encode(encrypted_name).decode()
    b = b64encode(encrypted_message).decode()
    c = b64encode(encrypted_key).decode()

    # Mengembalikan hasil enkripsi dalam bentuk string yang dapat dicetak
    return a, b, c

def decrypt_message(encrypted_name, encrypted_message, key):
    # Menggunakan hasil hashing dari kunci sebagai kunci dekripsi
    hashed_key = create_hash(key)
    hashed_key = hashed_key.ljust(8)[:8]

    # Membuat objek DES Cipher dengan mode ECB
    cipher = DES.new(hashed_key.encode(), DES.MODE_ECB)

    # Mendekripsi pesan
    decrypted_name = unpad(cipher.decrypt(b64decode(encrypted_name)), DES.block_size)
    decrypted_message = unpad(cipher.decrypt(b64decode(encrypted_message)), DES.block_size)

    a = decrypted_name.decode()
    b = decrypted_message.decode()

    # Mengembalikan pesan dalam bentuk string yang dapat dicetak
    return a, b

def display_result_in_text(result):
    hasil_text.config(state=tk.NORMAL)
    hasil_text.delete(1.0, tk.END)
    hasil_text.insert(tk.END, result)
    hasil_text.config(state=tk.DISABLED)
    
def display_result_in_text2(result):
    hasil_text2.config(state=tk.NORMAL)
    hasil_text2.delete(1.0, tk.END)
    hasil_text2.insert(tk.END, result)
    hasil_text2.config(state=tk.DISABLED)

def encrypt_decrypt_action():
    nama = nama_entry.get()
    pesan = pesan_entry.get()
    kunci = kunci_entry.get()

    if nama and pesan and kunci:
        try:
            nama_enk, pesan_enk, kunci_enk = encrypt(nama, pesan, kunci)
            result = f"Hasil enkripsi email: {nama_enk}\nHasil enkripsi password: {pesan_enk}\nHasil enkripsi kunci: {kunci_enk}"
            display_result_in_text(result)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    else:
        messagebox.showwarning("Peringatan", "Harap masukkan email, password, dan kunci.")

def decrypt_action():
    nama_terenkripsi = nama_terenkripsi_entry.get()
    pesan_terenkripsi = pesan_terenkripsi_entry.get()
    kunci_terenkripsi = kunci_terenkripsi_entry.get()

    if nama_terenkripsi and pesan_terenkripsi and kunci_terenkripsi:
        try:
            nama_dekripsi, pesan_dekripsi = decrypt_message(nama_terenkripsi, pesan_terenkripsi, kunci_terenkripsi)
            result = f"email terdekripsi: {nama_dekripsi}\npassword terdekripsi: {pesan_dekripsi}"
            display_result_in_text2(result)
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
    else:
        messagebox.showwarning("Peringatan", "Harap masukkan teks terenkripsi dan kunci.")

# GUI setup
root = tk.Tk()
root.title("Aplikasi Enkripsi dan Dekripsi")

# Frame Utama
main_frame = tk.Frame(root, bg="#FFE4C4", padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# Label dan Entry untuk Enkripsi
Label(main_frame, text="Masukkan email:", bg="#FFE4C4", font=("Arial", 14)).grid(row=0, column=0, pady=10)
nama_entry = Entry(main_frame, font=("Arial", 14))
nama_entry.grid(row=0, column=1, pady=10)

Label(main_frame, text="Masukkan password:", bg="#FFE4C4", font=("Arial", 14)).grid(row=1, column=0, pady=10)
pesan_entry = Entry(main_frame, font=("Arial", 14))
pesan_entry.grid(row=1, column=1, pady=10)

Label(main_frame, text="Masukkan kunci:", bg="#FFE4C4", font=("Arial", 14)).grid(row=2, column=0, pady=10)
kunci_entry = Entry(main_frame, font=("Arial", 14), show="*")  # Showing '*' for password entry
kunci_entry.grid(row=2, column=1, pady=10)

Button(main_frame, text="Enkripsi", command=encrypt_decrypt_action, font=("Arial", 14)).grid(row=3, column=0, columnspan=2, pady=10)

# Text widget untuk menampilkan hasil enkripsi
hasil_text = Text(main_frame, height=10, width=40, wrap=tk.WORD, font=("Arial", 12))
hasil_text.grid(row=4, column=0, columnspan=2, pady=10)
hasil_text.config(state=tk.DISABLED)

# Separator
tk.Frame(main_frame, height=2, bd=1, relief="sunken", bg="black").grid(row=5, column=0, columnspan=2, pady=10, sticky="we")

# Label dan Entry untuk Dekripsi
Label(main_frame, text="Masukkan teks terenkripsi (email):", bg="#FFE4C4", font=("Arial", 14)).grid(row=6, column=0, pady=10)
nama_terenkripsi_entry = Entry(main_frame, font=("Arial", 14))
nama_terenkripsi_entry.grid(row=6, column=1, pady=10)

Label(main_frame, text="Masukkan teks terenkripsi (password):", bg="#FFE4C4", font=("Arial", 14)).grid(row=7, column=0, pady=10)
pesan_terenkripsi_entry = Entry(main_frame, font=("Arial", 14))
pesan_terenkripsi_entry.grid(row=7, column=1, pady=10)

Label(main_frame, text="Masukkan kunci:", bg="#FFE4C4", font=("Arial", 14)).grid(row=8, column=0, pady=10)
kunci_terenkripsi_entry = Entry(main_frame, font=("Arial", 14), show="*")  # Showing '*' for password entry
kunci_terenkripsi_entry.grid(row=8, column=1, pady=10)

Button(main_frame, text="Dekripsi", command=decrypt_action, font=("Arial", 14)).grid(row=9, column=0, columnspan=2, pady=10)

# Text widget untuk menampilkan hasil dekripsi
hasil_text2 = Text(main_frame, height=10, width=40, wrap=tk.WORD, font=("Arial", 12))
hasil_text2.grid(row=10, column=0, columnspan=2, pady=10)
hasil_text2.config(state=tk.DISABLED)

root.mainloop()
