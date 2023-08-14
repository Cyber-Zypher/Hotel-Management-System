import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pymysql

class HotelBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Booking System")

        self.root.geometry("500x400")

        self.label_name = tk.Label(root, text="Guest Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(root)
        self.entry_name.pack()

        self.label_checkin = tk.Label(root, text="Check-in Date (YYYY-MM-DD):")
        self.label_checkin.pack()
        self.entry_checkin = tk.Entry(root)
        self.entry_checkin.pack()
        self.entry_checkin_var = tk.StringVar()
        self.entry_checkin["textvariable"] = self.entry_checkin_var
        self.entry_checkin_var.trace("w", lambda name, index, mode, sv=self.entry_checkin_var: self.auto_format_date(sv))

        self.label_checkout = tk.Label(root, text="Check-out Date (YYYY-MM-DD):")
        self.label_checkout.pack()
        self.entry_checkout = tk.Entry(root)
        self.entry_checkout.pack()
        self.entry_checkout_var = tk.StringVar()
        self.entry_checkout["textvariable"] = self.entry_checkout_var
        self.entry_checkout_var.trace("w", lambda name, index, mode, sv=self.entry_checkout_var: self.auto_format_date(sv))

        self.label_room = tk.Label(root, text="Room Type:")
        self.label_room.pack()

        self.room_type_options = ["Single", "Double", "Suite", "Family"]
        self.selected_room_type = tk.StringVar()
        self.room_type_combobox = ttk.Combobox(root, textvariable=self.selected_room_type, values=self.room_type_options)
        self.room_type_combobox.pack()

        # self.entry_room = tk.Entry(root)
        # self.entry_room.pack()

        self.button_book = tk.Button(root, text="Book Room", command=self.book_room)
        self.button_book.pack()

        self.button_display = tk.Button(root, text="Display Bookings", command=self.display_bookings)
        self.button_display.pack()

        self.db_connection = pymysql.connect(
            host="localhost",
            user="UNAME",
            password="PASSWD",
            database="DB_NAME"
        )
    
    def auto_format_date(self, sv):
        value = sv.get()
        if len(value) == 4 or len(value) == 7:
            value += "-"
            sv.set(value)

    def book_room(self):
        guest_name = self.entry_name.get()
        check_in = self.entry_checkin.get()
        check_out = self.entry_checkout.get()
        room_type = self.selected_room_type.get()

        if guest_name == "" or check_in == "" or check_out == "" or room_type == "":
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            with self.db_connection.cursor() as cursor:
                sql = "INSERT INTO bookings (guest_name, check_in, check_out, room_type) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (guest_name, check_in, check_out, room_type))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Room booked successfully!")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def display_bookings(self):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM bookings")
                bookings = cursor.fetchall()
                
                if bookings:
                    self.display_frame = tk.Toplevel(self.root)
                    self.display_frame.title("Bookings")
                    
                    self.display_frame.geometry("860x500")  # Adjust the size as needed
                    
                    scrollbar = tk.Scrollbar(self.display_frame)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    
                    listbox = tk.Listbox(self.display_frame, yscrollcommand=scrollbar.set, width=80)
                    for booking in bookings:
                        listbox.insert(tk.END, f"ID: {booking[0]}, Guest: {booking[1]}, Check-in: {booking[2]}, Check-out: {booking[3]}, Room Type: {booking[4]}")
                    
                    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
                    scrollbar.config(command=listbox.yview)
                    
                    delete_button = tk.Button(self.display_frame, text="Delete Selected", command=lambda: self.delete_booking(listbox))
                    delete_button.pack()
                else:
                    messagebox.showinfo("Info", "No bookings found.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_booking(self, listbox):
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Select a booking to delete.")
            return
        
        booking_info = listbox.get(selected_index)
        booking_id = booking_info.split(",")[0].split(":")[1].strip()  # Extracting the booking ID
        
        try:
            with self.db_connection.cursor() as cursor:
                sql = "DELETE FROM bookings WHERE booking_id = %s"
                cursor.execute(sql, (booking_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", "Booking deleted successfully.")
                listbox.delete(selected_index)
        except pymysql.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingSystem(root)
    app.run()
