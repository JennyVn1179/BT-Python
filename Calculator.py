import tkinter as tk

bieu_thuc = ""

def xu_ly_nhan(phim):
    global bieu_thuc
    bieu_thuc = bieu_thuc + str(phim)
    gia_tri_duoi.set(bieu_thuc)

def tinh_ket_qua():
    global bieu_thuc
    try:
        ket_qua = str(eval(bieu_thuc.replace('x', '*')))
        gia_tri_tren.set(bieu_thuc)
        gia_tri_duoi.set(ket_qua)
        bieu_thuc = ket_qua
    except Exception:
        gia_tri_duoi.set("Lỗi")
        bieu_thuc = ""

def xoa_tat_ca():
    global bieu_thuc
    bieu_thuc = ""
    gia_tri_tren.set("")
    gia_tri_duoi.set("")

def xoa_ky_tu():
    global bieu_thuc
    bieu_thuc = bieu_thuc[:-1]
    gia_tri_duoi.set(bieu_thuc)

def tinh_phan_tram():
    global bieu_thuc
    try:
        ket_qua = str(eval(bieu_thuc.replace('x', '*')) / 100)
        gia_tri_tren.set(bieu_thuc + "%")
        gia_tri_duoi.set(ket_qua)
        bieu_thuc = ket_qua
    except Exception:
        gia_tri_duoi.set("Lỗi")
        bieu_thuc = ""

def doi_dau():
    global bieu_thuc
    if bieu_thuc:
        if bieu_thuc.startswith('-'):
            bieu_thuc = bieu_thuc[1:]
        else:
            bieu_thuc = '-' + bieu_thuc
        gia_tri_duoi.set(bieu_thuc)

cua_so = tk.Tk()
cua_so.title("Calculator")
cua_so.geometry("320x450")
cua_so.configure(bg="#778899")

gia_tri_tren = tk.StringVar()
gia_tri_duoi = tk.StringVar()

khung_man_hinh = tk.Frame(cua_so, bg="white", bd=2, relief="sunken")
khung_man_hinh.grid(row=0, column=0, columnspan=15, sticky="nsew", padx=2, pady=2)

man_hinh_tren = tk.Label(khung_man_hinh, textvariable=gia_tri_tren, font=('Arial', 11), bg="white", fg="gray", anchor="e")
man_hinh_tren.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))

man_hinh_duoi = tk.Label(khung_man_hinh, textvariable=gia_tri_duoi, font=('Arial', 18, 'bold'), bg="white", fg="black", anchor="e")
man_hinh_duoi.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

cac_nut_so = [
    ('1', '2', '3'),
    ('4', '5', '6'),
    ('7', '8', '9'),
    ('+/-', '0', '.')
]

for chi_so_hang, hang in enumerate(cac_nut_so, start=1):
    cua_so.rowconfigure(chi_so_hang, weight=1)
    for chi_so_cot, phim in enumerate(hang):
        hanh_dong = doi_dau if phim == '+/-' else lambda k=phim: xu_ly_nhan(k)
        nut = tk.Button(cua_so, text=phim, font=('Arial', 12), bg="#b0c4de", relief="raised", bd=2, command=hanh_dong)
        nut.grid(row=chi_so_hang, column=chi_so_cot*5, columnspan=5, sticky="nsew", padx=1, pady=1)

cua_so.rowconfigure(5, weight=1)
cac_phep_tinh = ['+', '-', 'x', '/', '%']
for chi_so_cot, phim in enumerate(cac_phep_tinh):
    hanh_dong = tinh_phan_tram if phim == '%' else lambda k=phim: xu_ly_nhan(k)
    nut = tk.Button(cua_so, text=phim, font=('Arial', 12), bg="#b0c4de", relief="raised", bd=2, command=hanh_dong)
    nut.grid(row=5, column=chi_so_cot*3, columnspan=3, sticky="nsew", padx=1, pady=1)

cua_so.rowconfigure(6, weight=1)
cac_nut_cuoi = [('AC', xoa_tat_ca), ('⌫', xoa_ky_tu), ('=', tinh_ket_qua)]
for chi_so_cot, (phim, hanh_dong) in enumerate(cac_nut_cuoi):
    nut = tk.Button(cua_so, text=phim, font=('Arial', 12), bg="#b0c4de", relief="raised", bd=2, command=hanh_dong)
    nut.grid(row=6, column=chi_so_cot*5, columnspan=5, sticky="nsew", padx=1, pady=1)

for i in range(15):
    cua_so.columnconfigure(i, weight=1)

cua_so.mainloop()