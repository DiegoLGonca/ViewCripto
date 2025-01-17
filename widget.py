import tkinter as tk
from PIL import Image, ImageTk
import requests
from datetime import datetime
from ctypes import windll

root = tk.Tk()
root.title("Cripto Widget")
root.geometry("350x150")
root.configure(bg="#2a2a2a")
root.overrideredirect(True) 


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = screen_width - 370 
y_position = 20 
root.geometry(f"350x150+{x_position}+{y_position}")


def round_corners(window, radius):

    hwnd = windll.user32.GetParent(window.winfo_id())

    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    region = windll.gdi32.CreateRoundRectRgn(0, 0, width, height, radius, radius)
    windll.user32.SetWindowRgn(hwnd, region, True)
    
# AVAX e BTC
def fetch_prices():
    try:
        avax_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=AVAXUSDT")
        btc_response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")

        if avax_response.status_code == 200 and btc_response.status_code == 200:
            avax_price = float(avax_response.json()["price"])
            btc_price = float(btc_response.json()["price"])

            table_data = [
                ("AVAX/USD", f"${avax_price:,.2f}", avax_icon),
                ("BTC/USD", f"${btc_price:,.2f}", btc_icon),
            ]
            update_table(table_data)

            last_updated = datetime.now().strftime("%H:%M:%S")
            label_time.config(text=f"Última atualização: {last_updated}")
        else:
            raise Exception("Erro ao obter dados da Binance.")
    except Exception as e:
        label_time.config(text="Erro ao obter dados")
        print("Erro ao buscar preços:", e)
    # Att a cada 5 minutos
    root.after(300000, fetch_prices)

def update_table(data):
    for widget in table_frame.winfo_children():
        widget.destroy() 

    for i, (name, price, icon) in enumerate(data):
        icon_label = tk.Label(table_frame, image=icon, bg="#2a2a2a")
        icon_label.grid(row=i, column=0, padx=10, pady=5, sticky="nsew")
        name_label = tk.Label(table_frame, text=name, font=("Arial", 12), fg="white", bg="#2a2a2a", anchor="center")
        name_label.grid(row=i, column=1, padx=10, pady=5, sticky="nsew")
        price_label = tk.Label(table_frame, text=price, font=("Arial", 12), fg="white", bg="#2a2a2a", anchor="center")
        price_label.grid(row=i, column=2, padx=10, pady=5, sticky="nsew")

    table_frame.grid_columnconfigure(0, weight=1)
    table_frame.grid_columnconfigure(1, weight=1)
    table_frame.grid_columnconfigure(2, weight=1)

avax_icon = ImageTk.PhotoImage(Image.open("avax.png").resize((30, 30)))
btc_icon = ImageTk.PhotoImage(Image.open("btc.png").resize((30, 30)))

header_frame = tk.Frame(root, bg="#2a2a2a")
header_frame.pack(fill="x")

content_frame = tk.Frame(root, bg="#2a2a2a")
content_frame.pack(expand=True, fill="both")

table_frame = tk.Frame(content_frame, bg="#2a2a2a")
table_frame.pack(pady=10)

footer_frame = tk.Frame(root, bg="#2a2a2a")
footer_frame.pack(fill="x", side="bottom", pady=(0, 5))
label_time = tk.Label(footer_frame, text="Última atualização: Carregando...", font=("Arial", 10), fg="#aaaaaa", bg="#2a2a2a", anchor="center")
label_time.pack()

initial_data = [
    ("AVAX/USD", "Carregando...", avax_icon),
    ("BTC/USD", "Carregando...", btc_icon),
]
update_table(initial_data)

# init
fetch_prices()


root.update_idletasks() 
round_corners(root, radius=20)

root.mainloop()
