#Kamus
islogin = False		#Bernilai True jika sudah login (baru bisa menjalani fungsi lainnya)
admin = False		#Bernilai True jika user yang login adalah admin

#Function
def split(txt,case=';'):
    s=[]
    j=0
    for i in range (len(txt)):
        if case== txt [i]:
            s.append(txt[j:i])
            j=i+1
    s.append (txt[j:])
    return [ item for item in s if item ]

def convert_line_to_data(line):
#mengkonversi line/baris menjadi array of data, biar lebih readable aja.
    raw_array_of_data = split(line)
    array_of_data     = [data.strip() for data in raw_array_of_data]
    return array_of_data

def ready_to_use_user():
# untuk menyiapkan list yang dapat digunakan dari file user
    f = open("user.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines = [raw_line.replace("\n", "") for raw_line in raw_lines]
    # hapus baris pertama yang berisikan label 'id, 'username', ..., 'role'
    raw_header = lines.pop(0)
    header = convert_line_to_data(raw_header)
    # buat list baru kosong (akan berisi list data user) 
    data_user = []
    # untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
        real_values = array_of_data[:]  # mencopy dari array_of_data agar tidak langsung dimodifikasi
        for i in range(6):
            if(i==0):    # mengubah type kolom ke-1 (id) menjadi integer
                real_values[i] = int(real_values[i])
    # setelah dikonversi, tambahkan real_values ke list data_user
        data_user.append(real_values)
    return data_user

def ready_to_use_gadget():
# untuk menyiapkan list yang dapat digunakan dari file gadget
    f = open("gadget.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines = [raw_line.replace("\n", "") for raw_line in raw_lines]
    # hapus baris pertama yang berisikan label 'id, 'nama', ..., 'tahun_ditemukan'
    raw_header = lines.pop(0)
    header = convert_line_to_data(raw_header)
    # buat list baru kosong (akan berisi list data gadget) 
    data_gadget = []
    # untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
        real_values = array_of_data[:]  # mencopy dari array_of_data agar tidak langsung dimodifikasi
        for i in range(6):
            if(i==3 or i==5):    # mengubah type kolom ke-3 (jumlah) dan ke-5 (tahun) menjadi integer
                real_values[i] = int(real_values[i])
    # setelah dikonversi, tambahkan real_values ke list data_gadget
        data_gadget.append(real_values)
    return data_gadget

def ready_to_use_consumable():
# untuk menyiapkan list yang dapat digunakan dari file consumable
    f = open("consumable.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines = [raw_line.replace("\n", "") for raw_line in raw_lines]
    # hapus baris pertama yang berisikan label 'id, 'nama', ..., 'rarity'
    raw_header = lines.pop(0)
    header = convert_line_to_data(raw_header)
    # buat list baru kosong (akan berisi list data consumable) 
    data_consumable = []
    # untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
        real_values = array_of_data[:]  # mencopy dari array_of_data agar tidak langsung dimodifikasi
        for i in range(5):
            if(i==3):    # mengubah type kolom ke-3 (jumlah) menjadi integer
                real_values[i] = int(real_values[i])
    # setelah dikonversi, tambahkan real_values ke list data_consumable
        data_consumable.append(real_values)
    return data_consumable

#Prosedur Register - F01

#SPESIFIKASI
#Prosedur ini digunakan oleh Admin untuk menambahkan user baru

#Function
def isvalid(x,y):
    for line in y:
        if line[1] == x:
            return False
    return True

def createUsername():
    valid = False
    while valid == False:
        nama     = input("Masukan nama     : ")
        username = input("Masukan username : ")
        password = input("Masukan password : ")
        alamat   = input("Masukan alamat   : ")
        if nama == "" or username == "" or password == "" or alamat == "":
            print("Tidak boleh ada yang kosong!\n")
        else:
            valid = True
    role     = 'user'   # Sesuai spesifikasi, pengguna yg mendaftar secar otomatis memiliki role 'user'
    return [username,nama.capitalize(),alamat,password,role]

#Prosedur Utama
def register():
    # siapkan list user
    data_user = ready_to_use_user()

    # masukkan data yang ingin di register
    id_baru  = ((data_user[(len(data_user)-1)][0]) + 1) #id_baru didapat dari id terakhir pd data sebelumnya ditambah 1
    new_data_user = [id_baru]+createUsername() # Fungsi create Username dipisah
    if isvalid(new_data_user[1],data_user) == False:
        print("\nUsername telah diambil! Silahkan register ulang.")
    else:
        data_user.append(new_data_user) # expected output = [[],[],[]]
        f = open("user.csv","a")
        f.write(str(id_baru)+';'+new_data_user[1]+';'+new_data_user[2]+';'+new_data_user[3]+';'+new_data_user[4]+';'+new_data_user[5]+'\n')
        #User baru langsung disimpan ke user.csv
        #Output data username baru telah berhasil disimpan
        print("\nUser",new_data_user[1],"telah berhasil register ke dalam Kantong Ajaib.")


#Prosedur Login - F02

#SPESIFIKASI
#Prosedur ini digunakan oleh siapa saja untuk login


#Prosedur Utama
def login():
    # siapkan list user
    data_user = ready_to_use_user()

#Program akan meminta pengguna memasukan username dan password
    username = input("Masukan username: ")
    password = input("Masukan password: ")

#Username dan Password akan divalidasi dengan data setiap baris nya pada file user.csv

#Jika data yg dimasukan pengguna tidak sesuai dengan data baris ke 1,
#maka akan diperiksa/divalidasi dengan data baris ke 2 dan seterusnya
    i     = 0
    found = False
    while ((i < len(data_user)) and (found == False)):
        if ((data_user[i][1] == username) and (data_user[i][4] == password)):
            if data_user[i][5] == "admin":
                global admin
                admin = True
            found = True
        else : 
            i     = i+1

#Jika data uname dan password valid / sesuai dengan file, maka login berhasil         
    if (found == True) :
        print("")
        print("Halo "+str(username)+"! Selamat datang di Kantong Ajaib.")
        global islogin
        islogin = True
    else:
        print("\nUsername atau Password salah! Silahkan coba lagi")


#Prosedur Pencarian berdasarkan rarity  - F03

#SPESIFIKASI
#Prosedur ini digunakan untuk mencari gadget berdasarkan rarity-nya

#Prosedur Utama
def carirarity():
    # siapkan list gadget
    data_gadget = ready_to_use_gadget()

#Buatlah sebuah list baru (nantinya akan berisikan list data gadget dengan rarity yg dicari) 
    data_gadget_rarity = []

#Buat input variabel yang berisi rarity yang akan dicari (rarity pasti valid)
    rarity = input("Masukkan rarity: ").capitalize()
    print("\nHasil pencarian:\n")

#Buat loop untuk memasukkan gadget dengan rarity yang sesuai ingin dicari
    for line1 in data_gadget:
        if line1[4] == rarity:  #kolom ke 4 adalah rarity
            data_gadget_rarity.append(line1)

#Percabangan outputnya
    if len(data_gadget_rarity) == 0:    #Jika tidak ada gadget dengan rarity yang dicari
        print("Tidak ada gadget yang ditemukan.\n")
    else:
        for line2 in data_gadget_rarity:    #Mengeprint tiap gadget di array data_gadget_rarity
            print("Nama             :", line2[1])
            print("Deskripsi        :", line2[2])
            print("Jumlah           :", line2[3])
            print("Rarity           :", line2[4])
            print("Tahun Ditemukan  :", line2[5])
            print("")
    

#Prosedur Pencarian berdasarkan tahun  - F04

#SPESIFIKASI
#Prosedur ini digunakan untuk mencari gadget berdasarkan tahun dibuatnya

#Prosedur Utama
def caritahun():
    # siapkan list gadget
    data_gadget = ready_to_use_gadget()

#Buatlah sebuah list baru kosong lagi (nantinya akan berisikan list data gadget dengan tahun yg dicari) 
    data_gadget_tahun = []

#Buat input tahun yang ingin dicari user (sudah pasti valid)
    year = int(input("Masukkan tahun: "))

#Buat linput kategori yang ingin dicari user (sudah pasti valid)
    kategori = input("Masukkan kategori: ")
    print("\nHasil pencarian:\n")

#Buat loop untuk memasukkan gadget dengan tahun dan kategori yang sesuai ingin dicari
    for line1 in data_gadget:
        if kategori == "=":
            if line1[5] == year:  #kolom ke 5 adalah tahun
                data_gadget_tahun.append(line1)
        elif kategori == ">":
            if line1[5] > year:  #kolom ke 5 adalah tahun
                data_gadget_tahun.append(line1)
        elif kategori == "<":
            if line1[5] < year:  #kolom ke 5 adalah tahun
                data_gadget_tahun.append(line1)
        elif kategori == ">=":
            if line1[5] >= year:  #kolom ke 5 adalah tahun
                data_gadget_tahun.append(line1)
        elif kategori == "<=":
            if line1[5] <= year:  #kolom ke 5 adalah tahun
                data_gadget_tahun.append(line1)

#Percabangan outputnya
    if len(data_gadget_tahun) == 0:    #Jika tidak ada gadget dengan tahun yang dicari
        print("Tidak ada gadget yang ditemukan.\n")
    else:
        for line2 in data_gadget_tahun:    #Mengeprint tiap gadget di array data_gadget_tahun
            print("Nama             :", line2[1])
            print("Deskripsi        :", line2[2])
            print("Jumlah           :", line2[3])
            print("Rarity           :", line2[4])
            print("Tahun Ditemukan  :", line2[5])
            print("")


# Prosedur TambahItem - F05

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

def cari_ID_gadget(cari_ID, data_gadget):
    i = 0
    found = False
    while ((i < len(data_gadget)) and (found == False)):
        if (data_gadget[i][0] == cari_ID):
            found = True
        else : 
            i = i+1
    return [found, i]

def cari_ID_consumable(cari_ID, data_consumable):
    i = 0
    found = False
    while ((i < len(data_consumable)) and (found == False)):
        if (data_consumable[i][0] == cari_ID):
            found = True
        else : 
            i = i+1
    return [found, i]

# PROSEDUR UTAMA

def tambahitem():
    # siapkan list gadget dan consumable
    data_gadget = ready_to_use_gadget()
    data_consumable = ready_to_use_consumable()
    
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
                found = cari_ID_gadget(cari_ID, data_gadget)[0]
                i = cari_ID_gadget(cari_ID, data_gadget)[1]

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
                found = cari_ID_consumable(cari_ID, data_consumable)[0]
                i = cari_ID_consumable(cari_ID, data_consumable)[1]

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
        
# tambahitem()

# Prosedur HapusItem - F06

# PROSEDUR UTAMA

def hapusitem():
    # siapkan list gadget & consumable
    data_gadget = ready_to_use_gadget()
    data_consumable = ready_to_use_consumable()
    
    # input ID item yang ingin dihapus datanya
    cari_ID = input("Masukkan ID: ")

    # boolean "loop" digunakan untuk melakukan pengulangan input, 
    # apabila ID tidak ditemukan di database atau apabila admin ingin menghapus data lainnya
    loop = True

    while (loop):
        # validasi input ID agar lebih mudah filternya
        if (Is_ID_Valid(cari_ID) == False):     # input ID tidak valid
            print("\nTidak ada item dengan ID tersebut!")
            ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
            if (ulangi == 'Y'):
                cari_ID  = input("\nMasukkan ID: ")
            else:
                loop = False

        else:   # input ID valid
            if (cari_ID[0] == 'G'):     # item adalah gadget
                # mencari apakah ID ada di database
                found = cari_ID_gadget(cari_ID, data_gadget)[0]
                i = cari_ID_gadget(cari_ID, data_gadget)[1]
                if (found == False):     # ID gadget tidak ada di database
                    print("\nTidak ada item dengan ID tersebut!")
                    ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        cari_ID  = input("\nMasukkan ID: ")
                    else:
                        loop = False
                else:   # ID gadget ada di database
                    yakin = input("Apakah Anda yakin ingin menghapus " + data_gadget[i][1] + " (Y/N)? ")
                    if (yakin == 'Y'):
                        # hapus data pada baris tersebut
                        data_gadget.pop(i)
                        print("\nItem telah berhasil dihapus dari database.")
                        # simpan perubahan yang terjadi menggunakan prosedur save
                        #save()
                        ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False
                    else:
                        print("\nItem gagal dihapus dari database.")
                        ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False

            else:     # item adalah consumable
                # mencari apakah ID ada di database
                found = cari_ID_consumable(cari_ID, data_consumable)[0]
                i = cari_ID_consumable(cari_ID, data_consumable)[1]
                if (found == False):     # ID consumable tidak ada di database
                    print("\nTidak ada item dengan ID tersebut!")
                    ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        cari_ID  = input("\nMasukkan ID: ")
                    else:
                        loop = False
                else:   # ID consumable ada di database
                    yakin = input("Apakah Anda yakin ingin menghapus " + data_consumable[i][1] + " (Y/N)? ")
                    if (yakin == 'Y'):
                        # hapus data pada baris tersebut
                        data_consumable.pop(i)
                        print("\nItem telah berhasil dihapus dari database.")
                        # simpan perubahan yang terjadi menggunakan prosedur save
                        #save()
                        ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False
                    else:
                        print("\nItem gagal dihapus dari database.")
                        ulangi = input("Apakah Anda ingin menghapus item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False
        
# hapusitem()

# Prosedur UbahJumlah - F07

# PROSEDUR UTAMA

def ubahjumlah():
    # siapkan list gadget dan consumable
    data_gadget = ready_to_use_gadget()
    data_consumable = ready_to_use_consumable()
    
    # input ID item yang ingin diubah jumlahnya
    cari_ID = input("Masukkan ID: ")

    # boolean "loop" digunakan untuk melakukan pengulangan input, apabila ID tidak ditemukan di database,
    # atau apabila admin ingin menambah item lainnya
    loop = True

    while (loop):
        # validasi input ID agar lebih mudah filternya
        if (Is_ID_Valid(cari_ID) == False):     # input ID tidak valid
            print("\nTidak ada item dengan ID tersebut!")
            ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
            if (ulangi == 'Y'):
                cari_ID  = input("\nMasukkan ID: ")
            else:
                loop = False

        else:   # input ID valid
            if (cari_ID[0] == 'G'):     # item adalah gadget
                # mencari apakah ID ada di database
                found = cari_ID_gadget(cari_ID, data_gadget)[0]
                i = cari_ID_gadget(cari_ID, data_gadget)[1]

                if (found == False):     # ID gadget tidak ada di database
                    print("\nTidak ada item dengan ID tersebut!")
                    ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        cari_ID  = input("\nMasukkan ID: ")
                    else:
                        loop = False
                   
                else:   # ID gadget ada di database
                    # lakukan input jumlah yang ingin diubah
                    jumlah = input("Masukkan jumlah: ")
                    # cek validitas jumlah
                    while (Is_Integer(jumlah) == False):    
                        print("\nJumlah yang ingin diubah tidak valid! (Note: harus integer)")
                        jumlah = input("Masukkan jumlah: ")
                    # mengubah jumlah item
                    jumlah = int(jumlah)
                    jumlah_awal = data_gadget[i][3]
                    jumlah_baru = jumlah_awal + jumlah
            
                    if (jumlah < 0):    # jumlah item ingin dibuang (integer negatif)
                        jumlah = abs(jumlah)
                        if (jumlah_baru < 0):   # jumlah item yang baru tidak valid (integer negatif)
                            print("\n" + str(jumlah), data_gadget[i][1], "gagal dibuang karena stok kurang. Stok sekarang:", jumlah_awal, "(< " + str(jumlah) + ")")
                           
                            ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                            if (ulangi == 'Y'):
                                cari_ID  = input("\nMasukkan ID: ")
                            else:
                                loop = False

                        else:   # jumlah item yang baru valid
                            print("\n" + str(jumlah), data_gadget[i][1], "berhasil dibuang. Stok sekarang:", jumlah_baru)
                            # assign jumlah yang baru ke database
                            data_gadget[i][3] = jumlah_baru
                            # simpan perubahan yang terjadi menggunakan prosedur save
                            #save()
                        
                            ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                            if (ulangi == 'Y'):
                                cari_ID  = input("\nMasukkan ID: ")
                            else:
                                loop = False
                    
                    else:   # jumlah item ingin ditambah (integer positif)
                        print("\n" + str(jumlah), data_gadget[i][1], "berhasil ditambahkan. Stok sekarang:", jumlah_baru)
                        # assign jumlah yang baru ke database
                        data_gadget[i][3] = jumlah_baru
                        # simpan perubahan yang terjadi menggunakan prosedur save
                        #save()
                        
                        ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False

            else:   # item adalah consumable
                # mencari apakah ID ada di database
                found = cari_ID_consumable(cari_ID, data_consumable)[0]
                i = cari_ID_consumable(cari_ID, data_consumable)[1]

                if (found == False):     # ID consumable tidak ada di database
                    print("\nTidak ada item dengan ID tersebut!")
                    ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                    if (ulangi == 'Y'):
                        cari_ID  = input("\nMasukkan ID: ")
                    else:
                        loop = False
                   
                else:   # ID consumable ada di database
                    # lakukan input jumlah yang ingin diubah
                    jumlah = input("Masukkan jumlah: ")
                    # cek validitas jumlah
                    while (Is_Integer(jumlah) == False):    
                        print("\nJumlah yang ingin diubah tidak valid! (Note: harus integer)")
                        jumlah = input("Masukkan jumlah: ")
                    # mengubah jumlah item
                    jumlah = int(jumlah)
                    jumlah_awal = data_consumable[i][3]
                    jumlah_baru = jumlah_awal + jumlah
                    
                    if (jumlah < 0):    # jumlah item ingin dibuang (integer negatif)
                        jumlah = abs(jumlah)
                        if (jumlah_baru < 0):   # jumlah item yang baru tidak valid (integer negatif)
                            print("\n" + str(jumlah), data_consumable[i][1], "gagal dibuang karena stok kurang. Stok sekarang:", jumlah_awal, "(< " + str(jumlah) + ")")
                            ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                            if (ulangi == 'Y'):
                                cari_ID  = input("\nMasukkan ID: ")
                            else:
                                loop = False
                        else:   # jumlah item yang baru valid
                            print("\n" + str(jumlah), data_consumable[i][1], "berhasil dibuang. Stok sekarang:", jumlah_baru)
                            # assign jumlah yang baru ke database
                            data_consumable[i][3] = jumlah_baru
                            # simpan perubahan yang terjadi menggunakan prosedur save
                            #save()
                        
                            ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                            if (ulangi == 'Y'):
                                cari_ID  = input("\nMasukkan ID: ")
                            else:
                                loop = False
                    
                    else:   # jumlah item ingin ditambah (integer positif)
                        print("\n" + str(jumlah), data_consumable[i][1], "berhasil ditambahkan. Stok sekarang:", jumlah_baru)
                        # assign jumlah yang baru ke database
                        data_consumable[i][3] = jumlah_baru
                        # simpan perubahan yang terjadi menggunakan prosedur save
                        #save()
                        
                        ulangi = input("Apakah Anda ingin mengubah jumlah item lain (Y/N)? ")
                        if (ulangi == 'Y'):
                            cari_ID  = input("\nMasukkan ID: ")
                        else:
                            loop = False
        
# ubahjumlah()


#Prosedur Melihat Riwayat Peminjaman Gadget - F11

#SPESIFIKASI
#Prosedur ini digunakan oleh Admin sebagai bantuan
#untuk melihat riwayat peminjaman gadget.

#KAMUS LOKAL

#FUNCTION

def carinama(id_user):
    # siapkan list user
    data_user = ready_to_use_user()
  
#Mencari apakah id_user ada di data, kalau ada tentukan ada di data ke berapa
    i     = 0
    found = False
    while ((i < len(data_user)) and (found == False)):
        if (data_user[i][0] == id_user):
            found = True
        else : 
            i     = i+1
 #Jika sudah ditemukan, ubah id tersebut menjadi nama           
    if (found == True) :
        return(data_user[i][2])
    else:
        return("User tidak ditemukan")

def carigadget(id_gadget):
#mengubah id_gadget menjadi nama gadget yang ada di file gadget.csv
    # siapkan list gadget
    data_gadget = ready_to_use_gadget()
        
  
#Mencari apakah id_gadget ada di data, kalau ada tentukan ada di data ke berapa
    i     = 0
    found = False
    while ((i < len(data_gadget)) and (found == False)):
        if (data_gadget[i][0] == id_gadget):
            found = True
        else : 
            i = i+1
 #Jika sudah ditemukan, ubah id tersebut menjadi nama gadget          
    if (found == True) :
        return(data_gadget[i][1])
    else:
        return("Gadget tidak ditemukan")

#ALGORTIMA PROCEDURE UTAMA

def riwayatpinjam():

    import datetime

#Pertama, kita buka dulu file gadget_borrow_history.csv 
    f         = open("gadget_borrow_history.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines     = [raw_line.replace("\n", "") for raw_line in raw_lines]

#Hapus baris pertama yang berisikan label 'id, id_peminjam', .... , 'jumlah' 
#dari variabel lines
    raw_header = lines.pop(0)
    header     = convert_line_to_data(raw_header)
    

#Buatlah sebuah list baru kosong (nantinya akan berisikan list data history pinjam gadget)    
    data_history_peminjaman = []
#Untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
#Lalu ubah array data history peminjaman gadget menjadi value yang sesungguhnya, misal integer,float, atau sejenisnya
        real_values   = array_of_data[:] #mencopy dr array_data agar tidak langsung dimodifikasi
        for i in range(6):   #banyaknya kolom 
            if(i == 0)   :   #mengubah type kolom ke 0 (id) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 1) :   #mengubah type kolom ke 1 (id_peminjam) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 4) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 5) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = bool(real_values[i])
            
#Setelah dikonversi, tambahkan real_values ke list data_history_peminjaman
        data_history_peminjaman.append(real_values)

#Urutkan data_history_peminjaman berdasarkan kolom tanggal (descending)
#agar mencetak  data history yang terbaru

    if __name__ == "__main__":
        sorted_list = sorted(data_history_peminjaman,key=lambda x:datetime.datetime.strptime(x[3],"%d/%m/%Y"),reverse=True) #reverse=True -> supaya descending

        
#Jika jumlah data riwayatnya <= 5, maka cetak semua data
    if len(sorted_list) <= 5:
        for i in range((len(sorted_list))):
            print("ID Peminjaman      : ", str(sorted_list[i][0]))
            id_user    = sorted_list[i][1]
            nama       = carinama(id_user)
            print("Nama Pengambil     : ", nama)
            id_gadget  = sorted_list[i][2]
            namagadget = carigadget(id_gadget)
            print("Nama Gadget        : ",namagadget)
            print("Tanggal Peminjaman : ", str(sorted_list[i][3]))
            print("Jumlah             : ", str(sorted_list[i][4]))
            print("")

#Jika lebih dari 5, maka cetak 5 data/entry selanjutnya
    else :
        for i in range (5) :
            print("ID Peminjaman      : ", str(sorted_list[i][0]))
            id_user    = sorted_list[i][1]
            nama       = carinama(id_user)
            print("Nama Pengambil     : ", nama)
            id_gadget  = sorted_list[i][2]
            namagadget = carigadget(id_gadget)
            print("Nama Gadget        : ",namagadget)
            print("Tanggal Peminjaman : ", str(sorted_list[i][3]))
            print("Jumlah             : ", str(sorted_list[i][4]))
            print("")

#User diberi pilihan apakah ingin melihat entry data yang lain atau tidak.
        lanjut = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")

#Jika memilih "Ya", maka program akan menampilkan data/entry berikutnya
        if (lanjut == "Ya"):
            awal    = 5
            akhir   = 10
            yg_udah = 5

#Jika jumlah sisa data/entry masih lebih dari 5, maka program akan 
#mencetak 5 entry berikutnya dan kembali menawarkan apakah ingin
#melihat entry berikutnya atau tidak sampai jumlah sisa data/entry <= 5
            while ((len(sorted_list)-yg_udah) > 5):
                for i in range(awal,akhir):
                    print("ID Peminjaman      : ", str(sorted_list[i][0]))
                    id_user    = sorted_list[i][1]
                    nama       = carinama(id_user)
                    print("Nama Pengambil     : ", nama)
                    id_gadget  = sorted_list[i][2]
                    namagadget = carigadget(id_gadget)
                    print("Nama Gadget        : ",namagadget)
                    print("Tanggal Peminjaman : ", str(sorted_list[i][3]))
                    print("Jumlah             : ", str(sorted_list[i][4]))
                    print("")
      
                awal    += 5
                akhir   += 5
                yg_udah += 5
                lanjut   = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")
                if (lanjut == "Ya"):
                    continue
                else:
                    break

#Jika jumlah sisa data/entry kurang dari atau sama dengan lima, 
#maka program akan mencetak  data/entry  yang tersisa. 
            else :
                for i in range (awal, len(sorted_list)):
                    print("ID Peminjaman      : ", str(sorted_list[i][0]))
                    id_user    = sorted_list[i][1]
                    nama       = carinama(id_user)
                    print("Nama Pengambil     : ", nama)
                    id_gadget  = sorted_list[i][2]
                    namagadget = carigadget(id_gadget)
                    print("Nama Gadget        : ",namagadget)
                    print("Tanggal Peminjaman : ", str(sorted_list[i][3]))
                    print("Jumlah             : ", str(sorted_list[i][4]))
                    print("")

# riwayatpinjam()
#Prosedur selesai ^^





#Prosedur Melihat Riwayat Pengembalian Gadget - F12

#SPESIFIKASI
#Prosedur ini digunakan oleh Admin sebagai bantuan
#untuk melihat riwayat pengembalian gadget.

#KAMUS LOKAL

#FUNCTION

def cari_id_user(id_peminjaman):
#mengubah id_peminjaman menjadi id_user yg akan digunakan untuk mencari nama user

#Pertama, kita buka dulu file gadget_borrow_history.csv
    f         = open("gadget_borrow_history.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines     = [raw_line.replace("\n", "") for raw_line in raw_lines]

#Hapus baris pertama yang berisikan label 'id, id_peminjam, ....,is_returned' 
#dari variabel lines
    raw_header = lines.pop(0)
    header     = convert_line_to_data(raw_header)

#Buatlah sebuah list baru kosong (nantinya akan berisikan list data user)  
    data_peminjaman = []
#Untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
#Lalu ubah array data user menjadi value yang sesungguhnya, misal integer,float, atau sejenisnya
        real_values   = array_of_data[:]
        for i in range(6):   #banyaknya kolom 
            if(i == 0)   :   #mengubah type kolom ke 0 (id) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 1) :   #mengubah type kolom ke 1 (id_peminjam) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 4) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 5) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = bool(real_values[i])
#Setelah dikonversi, tambahkan real_values ke list data_peminjaman
        data_peminjaman.append(real_values)

#Mencari apakah id_peminjaman ada di data, kalau ada tentukan ada di data ke berapa
    i     = 0
    found = False
    while ((i < len(data_peminjaman)) and (found == False)):
        if (data_peminjaman[i][0] == id_peminjaman):
            found = True
        else : 
            i     = i+1
 #Jika sudah ditemukan, ubah id tersebut menjadi id_user           
    if (found == True) :
        return(data_peminjaman[i][1])
    else:
        return("User tidak ditemukan")



def cari_id_gadget(id_peminjaman):
#mengubah id_peminjaman menjadi id_gadget yg akan digunakan untuk mencari nama gadget

#Pertama, kita buka dulu file gadget_borrow_history.csv
    f         = open("gadget_borrow_history.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines     = [raw_line.replace("\n", "") for raw_line in raw_lines]

#Hapus baris pertama yang berisikan label 'id, id_peminjam, ....,is_returned' 
#dari variabel lines
    raw_header = lines.pop(0)
    header     = convert_line_to_data(raw_header)

#Buatlah sebuah list baru kosong (nantinya akan berisikan list data user)  
    data_peminjaman = []
#Untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
#Lalu ubah array data user menjadi value yang sesungguhnya, misal integer,float, atau sejenisnya
        real_values   = array_of_data[:]
        for i in range(6):   #banyaknya kolom 
            if(i == 0)   :   #mengubah type kolom ke 0 (id) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 1) :   #mengubah type kolom ke 1 (id_peminjam) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 4) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 5) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = bool(real_values[i])
#Setelah dikonversi, tambahkan real_values ke list data_peminjaman
        data_peminjaman.append(real_values)

#Mencari apakah id_peminjaman ada di data, kalau ada tentukan ada di data ke berapa
    i     = 0
    found = False
    while ((i < len(data_peminjaman)) and (found == False)):
        if (data_peminjaman[i][0] == id_peminjaman):
            found = True
        else : 
            i     = i+1
 #Jika sudah ditemukan, ubah id tersebut menjadi nama gadget          
    if (found == True) :
        return(data_peminjaman[i][2])
    else:
        return("Gadget tidak ditemukan")

#ALGORTIMA PROCEDURE UTAMA

def riwayatkembali():

    import datetime

#Pertama, kita buka dulu file gadget_borrow_history.csv 
    f         = open("gadget_return_history.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines     = [raw_line.replace("\n", "") for raw_line in raw_lines]

#Hapus baris pertama yang berisikan label 'id, id_peminjam', .... , 'jumlah' 
#dari variabel lines
    raw_header = lines.pop(0)
    header     = convert_line_to_data(raw_header)
    

#Buatlah sebuah list baru kosong (nantinya akan berisikan list data history pinjam gadget)    
    data_history_pengembalian = []
#Untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
#Lalu ubah array data history peminjaman gadget menjadi value yang sesungguhnya, misal integer,float, atau sejenisnya
        real_values   = array_of_data[:] #mencopy dr array_data agar tidak langsung dimodifikasi
        for i in range(3):   #banyaknya kolom 
            if(i == 0)   :   #mengubah type kolom ke 0 (id) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 1) :   #mengubah type kolom ke 1 (id_peminjam) menjadi integer
                real_values[i] = int(real_values[i])

            
#Setelah dikonversi, tambahkan real_values ke list data_history_peminjaman
        data_history_pengembalian.append(real_values)

#Urutkan data_history_peminjaman berdasarkan kolom tanggal (descending)
#agar mencetak  data history yang terbaru

    if __name__ == "__main__":
        sorted_list = sorted(data_history_pengembalian,key=lambda x:datetime.datetime.strptime(x[2],"%d/%m/%Y"),reverse=True) #reverse=True -> supaya descending

        
#Jika jumlah data riwayatnya <= 5, maka cetak semua data
    if len(sorted_list) <= 5:
        for i in range((len(sorted_list))):
            print("ID Pengembalian      : ", str(sorted_list[i][0]))
            id_user    = cari_id_user(sorted_list[i][1])
            nama       = carinama(id_user)
            print("Nama Pengambil       : ", nama)
            id_gadget  = cari_id_gadget(sorted_list[i][1])
            namagadget = carigadget(id_gadget)
            print("Nama Gadget          : ",namagadget)
            print("Tanggal Pengembalian : ", str(sorted_list[i][2]))
            print("")

#Jika lebih dari 5, maka cetak 5 data/entry selanjutnya
    else :
        for i in range (5) :
            print("ID Pengembalian      : ", str(sorted_list[i][0]))
            id_user    = cari_id_user(sorted_list[i][1])
            nama       = carinama(id_user)
            print("Nama Pengambil       : ", nama)
            id_gadget  = cari_id_gadget(sorted_list[i][1])
            namagadget = carigadget(id_gadget)
            print("Nama Gadget          : ",namagadget)
            print("Tanggal Pengembalian : ", str(sorted_list[i][2]))
            print("")

#User diberi pilihan apakah ingin melihat entry data yang lain atau tidak.
        lanjut = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")

#Jika memilih "Ya", maka program akan menampilkan data/entry berikutnya
        if (lanjut == "Ya"):
            awal    = 5
            akhir   = 10
            yg_udah = 5

#Jika jumlah sisa data/entry masih lebih dari 5, maka program akan 
#mencetak 5 entry berikutnya dan kembali menawarkan apakah ingin
#melihat entry berikutnya atau tidak sampai jumlah sisa data/entry <= 5
            while ((len(sorted_list)-yg_udah) > 5):
                for i in range(awal,akhir):
                    print("ID Pengembalian      : ", str(sorted_list[i][0]))
                    id_user    = cari_id_user(sorted_list[i][1])
                    nama       = carinama(id_user)
                    print("Nama Pengambil       : ", nama)
                    id_gadget  = cari_id_gadget(sorted_list[i][1])
                    namagadget = carigadget(id_gadget)
                    print("Nama Gadget          : ",namagadget)
                    print("Tanggal Pengembalian : ", str(sorted_list[i][2]))
                    print("")
      
                awal    += 5
                akhir   += 5
                yg_udah += 5
                lanjut   = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")
                if (lanjut == "Ya"):
                    continue
                else:
                    break

#Jika jumlah sisa data/entry kurang dari atau sama dengan lima, 
#maka program akan mencetak  data/entry  yang tersisa. 
            else :
                for i in range (awal, len(sorted_list)):
                    print("ID Pengembalian      : ", str(sorted_list[i][0]))
                    id_user    = cari_id_user(sorted_list[i][1])
                    nama       = carinama(id_user)
                    print("Nama Pengambil       : ", nama)
                    id_gadget  = cari_id_gadget(sorted_list[i][1])
                    namagadget = carigadget(id_gadget)
                    print("Nama Gadget          : ",namagadget)
                    print("Tanggal Pengembalian : ", str(sorted_list[i][2]))
                    print("")

# riwayatkembali()
#Prosedur selesai ^^





#Prosedur Melihat Riwayat Pengambilan Consumable - F13

#SPESIFIKASI
#Prosedur ini digunakan oleh Admin sebagai bantuan
#untuk melihat riwayat pengambilan consumable.

#KAMUS LOKAL

#FUNCTION

def cariconsumable(id_consumable):
#mengubah id_consumable menjadi nama consumable yang ada di file consumable.csv

    # siapkan list consumable
    data_consumable = ready_to_use_consumable()       
  
#Mencari apakah id_consumable ada di data, kalau ada tentukan ada di data ke berapa
    i     = 0
    found = False
    while ((i < len(data_consumable)) and (found == False)):
        if (data_consumable[i][0] == id_consumable):
            found = True
        else : 
            i = i+1
 #Jika sudah ditemukan, ubah id tersebut menjadi nama gadget          
    if (found == True) :
        return(data_consumable[i][1])
    else:
        return("Consumable tidak ditemukan")

#ALGORTIMA PROCEDURE UTAMA

def riwayatambil():

    import datetime

#Pertama, kita buka dulu file consumable_history.csv 
    f         = open("consumable_history.csv","r")
    raw_lines = f.readlines()
    f.close()
    lines     = [raw_line.replace("\n", "") for raw_line in raw_lines]

#Hapus baris pertama yang berisikan label 'id, id_pengambil', .... , 'jumlah' 
#dari variabel lines
    raw_header = lines.pop(0)
    header     = convert_line_to_data(raw_header)
    
#Buatlah sebuah list baru kosong (nantinya akan berisikan list data history consumable)    
    data_history_consumable = []
#Untuk setiap baris pada lines, konversikan menjadi array of data
    for line in lines:
        array_of_data = convert_line_to_data(line)
#Lalu ubah array data history consumable menjadi value yang sesungguhnya, misal integer,float, atau sejenisnya
        real_values   = array_of_data[:] #mencopy dr array_data agar tidak langsung dimodifikasi
        for i in range(5):   #banyaknya kolom 
            if(i == 0)   :   #mengubah type kolom ke 0 (id) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 1) :   #mengubah type kolom ke 1 (id_peminjam) menjadi integer
                real_values[i] = int(real_values[i])
            elif(i == 4) :   #mengubah type kolom ke 4 (jumlah) menjadi integer
                real_values[i] = int(real_values[i])
            
#Setelah dikonversi, tambahkan real_values ke list data_history_consumable
        data_history_consumable.append(real_values)

#Urutkan data_history_consumable berdasarkan kolom tanggal (descending)
#agar mencetak  data history yang terbaru

    if __name__ == "__main__":
        sorted_list = sorted(data_history_consumable,key=lambda x:datetime.datetime.strptime(x[3],"%d/%m/%Y"),reverse=True)#reverse=True -> supaya descending


#---Kelompok 4 Daspro---2020/2021---K05

#Jika jumlah data riwayatnya <= 5, maka cetak semua data
    if len(sorted_list) <= 5 :
        for i in range(len(sorted_list)):
            print("ID Pengambilan     : ", str(sorted_list[i][0]))
            id_user    = sorted_list[i][1]
            nama       = carinama(id_user)
            print("Nama Pengambil      : ", nama)
            id_consumable  = sorted_list[i][2]
            namaconsumable = cariconsumable(id_consumable)
            print("Nama Consumable     : ",namaconsumable)
            print("Tanggal Pengambilan : ", str(sorted_list[i][3]))
            print("Jumlah              : ", str(sorted_list[i][4]))
            print("")

#Jika lebih dari 5, maka cetak 5 data/entry selanjutnya
    else :
        for i in range (5) :
            print("ID Pengambilan      : ", str(sorted_list[i][0]))
            id_user    = sorted_list[i][1]
            nama       = carinama(id_user)
            print("Nama Pengambil      : ", nama)
            id_consumable  = sorted_list[i][2]
            namaconsumable = cariconsumable(id_consumable)
            print("Nama Consumable     : ",namaconsumable)
            print("Tanggal Pengambilan : ", str(sorted_list[i][3]))
            print("Jumlah              : ", str(sorted_list[i][4]))
            print("")

#User diberi pilihan apakah ingin melihat entry data yang lain atau tidak.
        lanjut = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")

#Jika memilih "Ya", maka program akan menampilkan data/entry berikutnya
        if (lanjut == "Ya"):
            awal    = 5
            akhir   = 10
            yg_udah = 5

#Jika jumlah sisa data/entry masih lebih dari 5, maka program akan 
#mencetak 5 entry berikutnya dan kembali menawarkan apakah ingin
#melihat entry berikutnya atau tidak sampai jumlah sisa data/entry <= 5
            while ((len(sorted_list)-yg_udah) > 5):
                for i in range(awal,akhir):
                    print("ID Pengambilan      : ", str(sorted_list[i][0]))
                    id_user    = sorted_list[i][1]
                    nama       = carinama(id_user)
                    print("Nama Pengambil      : ", nama)
                    id_consumable  = sorted_list[i][2]
                    namaconsumable = cariconsumable(id_consumable)
                    print("Nama Consumable     : ",namaconsumable)
                    print("Tanggal Pengambilan : ", str(sorted_list[i][3]))
                    print("Jumlah              : ", str(sorted_list[i][4]))
                    print("")
      
                awal    += 5
                akhir   += 5
                yg_udah += 5
                lanjut   = input("Apakah ingin melihat entry berikutnya? Ya/Tidak \nPilihan Anda: ")
                if (lanjut == "Ya"):
                    continue
                else:
                    break

#Jika jumlah sisa data/entry kurang dari atau sama dengan lima, 
#maka program akan mencetak  data/entry  yang tersisa. 
            else :
                for i in range (awal, len(sorted_list)):
                    print("ID Pengambilan      : ", str(sorted_list[i][0]))
                    id_user    = sorted_list[i][1]
                    nama       = carinama(id_user)
                    print("Nama Pengambil      : ", nama)
                    id_consumable  = sorted_list[i][2]
                    namaconsumable = cariconsumable(id_consumable)
                    print("Nama Consumable     : ",namaconsumable)
                    print("Tanggal Pengambilan : ", str(sorted_list[i][3]))
                    print("Jumlah              : ", str(sorted_list[i][4]))
                    print("")


# riwayatambil()
#Prosedur selesai ^^





#Prosedur Help  - F16

#SPESIFIKASI
#Prosedur ini digunakan untuk memberi tahu command yang tersedia untuk user dan fungsinya

#Prosedur Utama
def help(role):
	print("\n============ HELP ============")
	if role == "Admin":		#help jika user adalah admin
		print("register - untuk melakukan register user baru")
		print("carirarity - untuk mencari gadget berdasarkan rarity-nya")
		print("caritahun - untuk mencari gadget berdasarkan tahun ditemukannya")
		print("tambahitem - untuk menambah item ke dalam inventori")
		print("hapusitem - untuk menghapus suatu item dari database")
		print("ubahjumlah - untuk mengubah jumlah item dari database")
		print("riwayatpinjam - untuk melihat riwayat peminjaman gadget")
		print("riwayatkembali - untuk melihat riwayat pengembalian gadget")
		print("riwayatambil - untuk melihat riwayat pengambilan consumable")
		print("save - untuk melakukan penyimpanan penambahan, penghapusan, dan pengubahan jumlah item")
		print("exit - untuk keluar dari aplikasi")

	elif role == "User":	#help jika user adalah user
		print("pinjam - untuk melakukan peminjaman gadget")
		print("kembalikan -untuk mengembalikan gadget secara seutuhnya")
		print("minta - untuk melakukan permintaan consumable")
		print("save - untuk melakukan penyimpanan peminjaman, pengembalian, dan permintaan item")
		print("exit - untuk keluar dari aplikasi")
	print("==============================\n")


# help("Admin")	#Untuk menguji saja
# help("User")	#Untuk menguji saja


#Prosedur Exit - F17

#SPESIFIKASI
#Prosedur ini digunakan untuk menyimpan dan keluar dari program

#Function
import sys
def exit():
	#save()		#Menjalankan prosedur save
	sys.exit()	#Exit program


print("Silakan login terlebih dahulu.")
while islogin == False:
	login()
	
isexit = False
while isexit == False:
	command = input(">>>")
	if admin == True:
		if command.capitalize() == "Register":
			register()
		elif command.capitalize() == "Carirarity":
			carirarity()
		elif command.capitalize() == "Caritahun":
			caritahun()
		elif command.capitalize() == "Tambahitem":
			tambahitem()
		elif command.capitalize() == "Hapusitem":
			hapusitem()
		elif command.capitalize() == "Ubahjumlah":
			ubahjumlah()
		elif command.capitalize() == "Riwayatpinjam":
			riwayatpinjam()
		elif command.capitalize() == "Riwayatkembali":
			riwayatkembali()
		elif command.capitalize() == "Riwayatambil":
			riwayatambil()
		elif command.capitalize() == "Save":
			save()
		elif command.capitalize() == "Help":
			help("Admin")
		elif command.capitalize() == "Exit":
			exit()
		else:
			print("Command tidak ditemukan!")
	elif admin == False:
		if command.capitalize() == "Pinjam":
			pinjam()
		elif command.capitalize() == "Kembalikan":
			kembalikan()
		elif command.capitalize() == "Minta":
			minta()
		elif command.capitalize() == "Save":
			save()
		elif command.capitalize() == "Help":
			help("User")
		elif command.capitalize() == "Exit":
			exit()
		else:
			print("Command tidak ditemukan!")
