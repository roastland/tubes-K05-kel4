# Prosedur TambahItem - F05

# FUNGSI/PROSEDUR ANTARA

def di_split(str):
# memotong suatu string dengan pembatas ';' menjadi suatu array
    NewArray = []
    i = 0
    while (len(str) > i ): 
        if str[i] != ';':
            i += 1
        else:
            NewArray.append(str[:i])
            str = str[i+1:]
            i = 0
    NewArray.append(str)
    return NewArray

def convert_line_to_data(line):
# mengkonversi line/baris menjadi array of data, biar lebih readable
    raw_array_of_data = di_split(line)
    array_of_data     = [data.strip() for data in raw_array_of_data]
    return array_of_data

def Is_Integer(s):  # fungsi berikut diadaptasi dari StackOverflow
# untuk mengecek apakah input merupakan integer
    try:
        int(s)
        return True
    except ValueError:
        return False

def Is_ID_Valid(s):
# untuk mengecek validitas ID gadget/consumables
    if ((s[0]=='G' or s[0]=='C') and Is_Integer(s[1:])==True):
        return True
    else:
        return False

def Is_Rarity_Valid(s):
# untuk mengecek validitas rarity gadget/consumables
    if (s=='C' or s=='B' or s=='A' or s=='S'):
        return True
    else:
        return False

# PROSEDUR UTAMA

def tambahitem():
    # buka file gadget.csv dan consumable.csv
    fg = open("gadget.csv",'r')
    fc = open("consumable.csv",'r')
    raw_lines_gadget = fg.readlines()
    raw_lines_consumable = fc.readlines()
    fc.close()
    fg.close()
    lines_gadget = [raw_line.replace("\n", "") for raw_line in raw_lines_gadget]
    lines_consumable = [raw_line.replace("\n", "") for raw_line in raw_lines_consumable]

    # hapus baris pertama yang berisikan label 'id, 'nama', 'deskripsi', ..., 
    # dari variabel lines_gadget dan lines_consumable
    raw_header_gadget = lines_gadget.pop(0)
    raw_header_consumable = lines_consumable.pop(0)
    header_gadget = convert_line_to_data(raw_header_gadget)
    header_consumable = convert_line_to_data(raw_header_consumable)

    # buat 2 list baru kosong (nantinya akan berisikan list data gadget dan data consumable) 
    data_gadget = []
    data_consumable = []

    # untuk setiap baris pada lines_gadget, konversikan menjadi array of data
    for line_g in lines_gadget:
        array_of_data_g = convert_line_to_data(line_g)
    # setelah dikonversi, tambahkan array of data ke list data_gadget
        data_gadget.append(array_of_data_g)

    # untuk setiap baris pada lines_consumable, konversikan menjadi array of data
    for line_c in lines_consumable:
        array_of_data_c = convert_line_to_data(line_c)
    # setelah dikonversi, tambahkan array of data ke list data_consumable
        data_consumable.append(array_of_data_c)
    
    # buat list kosong baru lainnya (akan berisikan list data gadget dan data consumable yang diinput)
    new_data_gadget = []
    new_data_consumable = []

    # masukkan ID item
    id_baru  = input("Masukkan ID: ")

    # boolean "loop" digunakan untuk melakukan pengulangan input, apabila ID tidak valid, 
    # ID sudah ada di database, atau apabila admin ingin menambah item lainnya
    loop = True

    while (loop):
        # lakukan validasi input ID
        if (Is_ID_Valid(id_baru) == False):     # input ID tidak valid
            print("\nGagal menambahkan item karena ID tidak valid.")
            ulangi = input("Apakah Anda ingin menambahkan item lain (Y/N)? ")
            if (ulangi == 'Y'):
                id_baru  = input("\nMasukkan ID: ")
            else:
                loop = False

        else:   # input ID valid
            if (id_baru[0] == 'G'):     # item adalah gadget
                # mencari apakah ID ada di database, jika ada, ID tidak dapat ditambahkan
                i = 0
                found = False
                while ((i < len(data_gadget)) and (found == False)):
                    if (data_gadget[i][0] == id_baru):
                        found = True
                    else : 
                        i = i+1

                if (found == True):     # ID gadget ada di database
                    print("\nGagal menambahkan item karena ID sudah ada.")
                    ulangi = input("Apakah Anda ingin menambahkan item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        id_baru  = input("\nMasukkan ID: ")
                    else:
                        loop = False
                   
                else:   # ID gadget unik (belum ada di database)
                    # lakukan input data gadget
                    nama     = input("Masukkan nama: ")
                    deskripsi = input("Masukkan deskripsi: ")

                    jumlah = input("Masukkan jumlah: ")
                    # cek validitas jumlah
                    while (Is_Integer(jumlah) == False):    
                        print("\nJumlah gadget tidak valid! (Note: harus integer)")
                        jumlah = input("Masukkan jumlah: ")

                    rarity = input("Masukkan rarity: ")
                    # cek validitas rarity
                    while (Is_Rarity_Valid(rarity) == False):   
                        print("\nRarity gadget tidak valid! (Note: C, B, A, atau S)")
                        rarity = input("Masukkan rarity: ")

                    tahun = input("Masukkan tahun ditemukan: ")
                    # cek validitas tahun
                    while (Is_Integer(tahun) == False):     
                        print("\nTahun gadget ditemukan tidak valid! (Note: harus integer)")
                        tahun = input("Masukkan tahun ditemukan: ")

                    # input data gadget yang valid dimasukkan ke list gadget sementara
                    new_data_gadget.append(id_baru)
                    new_data_gadget.append(nama)
                    new_data_gadget.append(deskripsi)
                    new_data_gadget.append(jumlah)
                    new_data_gadget.append(rarity)
                    new_data_gadget.append(tahun)

                    # list data gadget tersebut digabungkan dengan list data gadget awal
                    data_gadget.append(new_data_gadget)

                    # simpan perubahan yang terjadi menggunakan prosedur save
                    #save()
                    
                    print("\nItem telah berhasil ditambahkan ke database.")
                    ulangi = input("Apakah Anda ingin menambahkan item lain (Y/N)? ")
                    # mengecek apakah admin ingin menambah item lain
                    if (ulangi == 'Y'):
                        id_baru  = input("\nMasukkan ID: ")
                    else:
                        loop = False

            else:   # item adalah consumable
                # mencari apakah ID ada di database, jika ada, ID tidak dapat ditambahkan
                i = 0
                found = False
                while ((i < len(data_consumable)) and (found == False)):
                    if (data_consumable[i][0] == id_baru):
                        found = True
                    else : 
                        i = i+1

                if (found == True):     # ID consumable ada di database
                    print("\nGagal menambahkan item karena ID sudah ada.")
                    ulangi = input("Apakah Anda ingin menambahkan item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        id_baru  = input("\nMasukkan ID: ")
                    else:
                        loop = False

                else:   # ID consumable unik (belum ada di database)
                    # lakukan input data consumable
                    nama     = input("Masukkan nama: ")
                    deskripsi = input("Masukkan deskripsi: ")

                    jumlah = input("Masukkan jumlah: ")
                    # cek validitas jumlah
                    while (Is_Integer(jumlah) == False):
                        print("\nJumlah consumable tidak valid! (Note: harus integer)")
                        jumlah = input("Masukkan jumlah: ")

                    rarity = input("Masukkan rarity: ")
                    # cek validitas rarity
                    while (Is_Rarity_Valid(rarity) == False):
                        print("\nRarity consumable tidak valid! (Note: C, B, A, atau S)")
                        rarity = input("Masukkan rarity: ")

                    # input data consumable yang valid dimasukkan ke list consumable sementara
                    new_data_consumable.append(id_baru)
                    new_data_consumable.append(nama)
                    new_data_consumable.append(deskripsi)
                    new_data_consumable.append(jumlah)
                    new_data_consumable.append(rarity)

                    # list data gadget tersebut digabungkan dengan list data gadget awal
                    data_consumable.append(new_data_consumable)

                    # simpan perubahan yang terjadi menggunakan prosedur save
                    #save()
                    
                    print("\nItem telah berhasil ditambahkan ke database.")
                    ulangi = input("Apakah Anda ingin menambahkan item lain (Y/N)? ")
                    # mengecek apakah admin ingin menambah item lain
                    if (ulangi == 'Y'):
                        id_baru  = input("\nMasukkan ID: ")
                    else:
                        loop = False
        
tambahitem()
