import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import random

def khoi_tao_csdl():
    ket_noi = sqlite3.connect('university.db')
    con_tro = ket_noi.cursor()
    
    con_tro.execute('DROP TABLE IF EXISTS students')
    
    con_tro.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            major TEXT NOT NULL,
            gpa REAL NOT NULL
        )
    ''')
    
    sinh_vien_mau = [
        ('Nguyễn Văn Đạo', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Nguyễn Huy Tuấn', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Ngô Thế Anh', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Phí Hữu Hoàng Tùng', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Vũ Tuấn Minh', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Nguyễn Đinh Anh Quân', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Bùi Văn Huy', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Tạ Dũng Bình', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Phạm Văn Tài', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1)),
        ('Đậu Đăng Thiện', 'Công nghệ thông tin - CLC', round(random.uniform(1.0, 4.0), 1))
    ]
    con_tro.executemany("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)", sinh_vien_mau)
    ket_noi.commit()
    ket_noi.close()

class UngDungDaiHoc:
    def __init__(self, cua_so_chinh):
        self.cua_so_chinh = cua_so_chinh
        self.cua_so_chinh.title("Quản lý Sinh viên - University Database")
        self.cua_so_chinh.geometry("700x550")
        
        khung_nhap_lieu = tk.LabelFrame(self.cua_so_chinh, text="Thông tin Sinh viên")
        khung_nhap_lieu.pack(fill="x", padx=10, pady=10)
        
        tk.Label(khung_nhap_lieu, text="Tên (Name):").grid(row=0, column=0, padx=5, pady=5)
        self.o_nhap_ten = tk.Entry(khung_nhap_lieu, width=25)
        self.o_nhap_ten.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(khung_nhap_lieu, text="Ngành (Major):").grid(row=0, column=2, padx=5, pady=5)
        self.o_nhap_nganh = tk.Entry(khung_nhap_lieu, width=25)
        self.o_nhap_nganh.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(khung_nhap_lieu, text="GPA:").grid(row=1, column=0, padx=5, pady=5)
        self.o_nhap_gpa = tk.Entry(khung_nhap_lieu, width=25)
        self.o_nhap_gpa.grid(row=1, column=1, padx=5, pady=5)
        
        nut_them = tk.Button(khung_nhap_lieu, text="Thêm Sinh viên", command=self.them_sinh_vien, bg="#4CAF50", fg="white")
        nut_them.grid(row=1, column=2, columnspan=2, pady=5, sticky="we")

        khung_bang = tk.Frame(self.cua_so_chinh)
        khung_bang.pack(fill="both", expand=True, padx=10)
        
        cac_cot = ("id", "name", "major", "gpa")
        self.bang_du_lieu = ttk.Treeview(khung_bang, columns=cac_cot, show="headings")
        self.bang_du_lieu.heading("id", text="ID")
        self.bang_du_lieu.heading("name", text="Họ và Tên")
        self.bang_du_lieu.heading("major", text="Ngành học")
        self.bang_du_lieu.heading("gpa", text="GPA")
        
        self.bang_du_lieu.column("id", width=50, anchor="center")
        self.bang_du_lieu.column("name", width=200)
        self.bang_du_lieu.column("major", width=200)
        self.bang_du_lieu.column("gpa", width=100, anchor="center")
        
        self.bang_du_lieu.pack(fill="both", expand=True, side="left")
        
        thanh_cuon = ttk.Scrollbar(khung_bang, orient=tk.VERTICAL, command=self.bang_du_lieu.yview)
        self.bang_du_lieu.configure(yscroll=thanh_cuon.set)
        thanh_cuon.pack(side="right", fill="y")

        khung_chuc_nang = tk.LabelFrame(self.cua_so_chinh, text="Chức năng")
        khung_chuc_nang.pack(fill="x", padx=10, pady=10)
        
        tk.Button(khung_chuc_nang, text="Tất cả SV", command=self.tai_tat_ca).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(khung_chuc_nang, text="Lấy SV có GPA > 3.0", command=self.tai_gpa_lon_hon_3).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(khung_chuc_nang, text="Cập nhật GPA", command=self.cap_nhat_gpa).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(khung_chuc_nang, text="Xóa SV", command=self.xoa_sinh_vien, bg="#ff9800").grid(row=0, column=3, padx=5, pady=5)
        tk.Button(khung_chuc_nang, text="Xóa tất cả SV GPA < 2.0", command=self.xoa_gpa_nho_hon_2, bg="#f44336", fg="white").grid(row=0, column=4, padx=5, pady=5)

        self.tai_tat_ca()

    def thuc_thi_truy_van(self, cau_lenh, tham_so=()):
        ket_noi = sqlite3.connect('university.db')
        con_tro = ket_noi.cursor()
        con_tro.execute(cau_lenh, tham_so)
        du_lieu = con_tro.fetchall()
        ket_noi.commit()
        ket_noi.close()
        return du_lieu

    def hien_thi_du_lieu(self, du_lieu):
        for hang in self.bang_du_lieu.get_children():
            self.bang_du_lieu.delete(hang)
        for hang in du_lieu:
            self.bang_du_lieu.insert("", tk.END, values=hang)

    def tai_tat_ca(self):
        du_lieu = self.thuc_thi_truy_van("SELECT * FROM students")
        self.hien_thi_du_lieu(du_lieu)

    def tai_gpa_lon_hon_3(self):
        du_lieu = self.thuc_thi_truy_van("SELECT * FROM students WHERE gpa > 3.0")
        self.hien_thi_du_lieu(du_lieu)

    def them_sinh_vien(self):
        ten = self.o_nhap_ten.get()
        nganh = self.o_nhap_nganh.get()
        diem_gpa = self.o_nhap_gpa.get()
        
        if ten and nganh and diem_gpa:
            try:
                self.thuc_thi_truy_van("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)", (ten, nganh, float(diem_gpa)))
                messagebox.showinfo("Thành công", "Đã thêm sinh viên!")
                self.tai_tat_ca()
                self.o_nhap_ten.delete(0, tk.END)
                self.o_nhap_nganh.delete(0, tk.END)
                self.o_nhap_gpa.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Lỗi", "GPA phải là một số!")
        else:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ Tên, Ngành và GPA.")

    def cap_nhat_gpa(self):
        dong_duoc_chon = self.bang_du_lieu.focus()
        if not dong_duoc_chon:
            messagebox.showwarning("Chú ý", "Vui lòng click chọn 1 sinh viên trên bảng để cập nhật.")
            return
        
        ma_sv = self.bang_du_lieu.item(dong_duoc_chon, 'values')[0]
        gpa_moi = self.o_nhap_gpa.get()
        
        if gpa_moi:
            try:
                self.thuc_thi_truy_van("UPDATE students SET gpa = ? WHERE id = ?", (float(gpa_moi), ma_sv))
                messagebox.showinfo("Thành công", f"Đã cập nhật GPA cho sinh viên ID {ma_sv}")
                self.tai_tat_ca()
                self.o_nhap_gpa.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Lỗi", "GPA mới phải là một số!")
        else:
            messagebox.showwarning("Nhập liệu", "Vui lòng nhập điểm GPA mới vào ô GPA ở trên trước khi bấm Cập nhật.")

    def xoa_sinh_vien(self):
        dong_duoc_chon = self.bang_du_lieu.focus()
        if not dong_duoc_chon:
            messagebox.showwarning("Chú ý", "Vui lòng click chọn 1 sinh viên trên bảng để xóa.")
            return
        
        ma_sv = self.bang_du_lieu.item(dong_duoc_chon, 'values')[0]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa sinh viên ID {ma_sv}?"):
            self.thuc_thi_truy_van("DELETE FROM students WHERE id = ?", (ma_sv,))
            self.tai_tat_ca()

    def xoa_gpa_nho_hon_2(self):
        if messagebox.askyesno("Cảnh báo", "Bạn có chắc muốn xóa TẤT CẢ sinh viên có GPA < 2.0?"):
            self.thuc_thi_truy_van("DELETE FROM students WHERE gpa < 2.0")
            messagebox.showinfo("Thành công", "Đã dọn dẹp các sinh viên có GPA < 2.0")
            self.tai_tat_ca()

if __name__ == "__main__":
    khoi_tao_csdl()
    giao_dien = tk.Tk()
    ung_dung = UngDungDaiHoc(giao_dien)
    giao_dien.mainloop()