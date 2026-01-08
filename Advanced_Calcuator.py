import customtkinter as ctk
import tkinter as tk
import math
import re # Regex kütüphanesi (Otomatik düzeltmeler için)

# --- AYARLAR ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MuhendisApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Engineering Assistant v7.6 - Final Fix")
        self.geometry("1000x950")

        # --- HESAP MAKİNESİ DEĞİŞKENLERİ ---
        self.calc_memory = 0.0

        # --- DİL YÖNETİMİ ---
        self.current_lang = "TR"
        self.translations = {
            "TR": {
                "title": "Mühendislik İsviçre Çakısı",
                "tab_calc": "Hesap Mak.",
                "tab_resistor": "Direnç",
                "tab_led": "LED",
                "tab_smd": "SMD",
                "tab_cap": "Kapasitör",
                "tab_awg": "AWG Kablo",
                "tab_div": "G. Bölücü",
                "tab_opamp": "Op-Amp",
                "tab_555": "NE555",
                "tab_filter": "Filtreler",
                "tab_rf": "RF Güç",
                "tab_pcb": "PCB Yol",
                "tab_logic": "Mantık",
                "tab_heat": "Isı Analizi",
                "tab_batt": "Batarya",
                "tab_base": "Taban Çev.",
                "calc_err": "Hata",
                "res_band1": "1. Bant:", "res_band2": "2. Bant:", "res_band3": "Çarpan:", "res_band4": "Tolerans:",
                "res_result": "Sonuç:",
                "led_supply": "Kaynak Voltajı (V):", "led_color": "LED Rengi:", "led_current": "Akım:",
                "led_calc": "HESAPLA", "led_res": "Direnç:", "led_pwr": "Güç:",
                "led_err_v": "Voltaj Yetersiz!",
                "smd_title": "SMD Kodu (103, 4R7):", "smd_solve": "ÇÖZÜMLE", "smd_val": "Değer:",
                "div_vin": "Vin (Giriş):", "div_vout": "Vout (Çıkış):",
                "op_inv": "Eviren", "op_noninv": "Evirmeyen", "op_gain": "Kazanç (Av):",
                "555_freq": "Frekans:", "555_duty": "Duty Cycle:",
                "base_input": "Sayı Giriniz:", "base_conv": "ÇEVİR",
                "batt_cap": "Pil Kapasitesi (mAh):", "batt_cons": "Cihaz Tüketimi (mA):", 
                "batt_life": "Tahmini Ömür:", "batt_days": "Gün", "batt_hours": "Saat",
                "pcb_current": "Akım (Amper):", "pcb_temp": "Sıcaklık Artışı (°C):",
                "pcb_thick": "Bakır Kalınlığı (oz):", "pcb_layer": "Katman Tipi:",
                "pcb_ext": "Dış Katman (External)", "pcb_int": "İç Katman (Internal)",
                "pcb_width": "Min. Yol Genişliği:",
                "filt_type": "Filtre Tipi:", "filt_lp": "Alçak Geçiren (RC)", "filt_hp": "Yüksek Geçiren (CR)",
                "filt_cutoff": "Kesim Frekansı (fc):",
                "rf_val": "Değer Giriniz:", "rf_res": "Sonuç:",
                "cap_code": "Kodu Giriniz (104, 22p):", "cap_val": "Kapasite:",
                "awg_no": "AWG Numarası:", "awg_dia": "Çap:", "awg_area": "Kesit Alanı:", "awg_amp": "Max Akım (Tahmini):",
                "log_gate": "Kapı Tipi:", "log_inA": "Giriş A (0/1)", "log_inB": "Giriş B (0/1)", "log_out": "Çıkış (Q):",
                "heat_tj": "Max Çip Sıcaklığı (Tj °C):", "heat_ta": "Ortam Sıcaklığı (Ta °C):", 
                "heat_p": "Harcanan Güç (Watt):", "heat_res": "Max Termal Direnç (Rth):"
            },
            "EN": {
                "title": "Engineering Swiss Knife",
                "tab_calc": "Calculator",
                "tab_resistor": "Resistor",
                "tab_led": "LED",
                "tab_smd": "SMD",
                "tab_cap": "Capacitor",
                "tab_awg": "AWG Wire",
                "tab_div": "V. Divider",
                "tab_opamp": "Op-Amp",
                "tab_555": "NE555",
                "tab_filter": "Filters",
                "tab_rf": "RF Power",
                "tab_pcb": "PCB Trace",
                "tab_logic": "Logic Gates",
                "tab_heat": "Heatsink",
                "tab_batt": "Battery",
                "tab_base": "Base Conv.",
                "calc_err": "Error",
                "res_band1": "Band 1:", "res_band2": "Band 2:", "res_band3": "Multiplier:", "res_band4": "Tolerance:",
                "res_result": "Result:",
                "led_supply": "Source Voltage (V):", "led_color": "LED Color:", "led_current": "Current:",
                "led_calc": "CALCULATE", "led_res": "Resistor:", "led_pwr": "Power:",
                "led_err_v": "Low Voltage!",
                "smd_title": "SMD Code (103, 4R7):", "smd_solve": "DECODE", "smd_val": "Value:",
                "div_vin": "Vin (Input):", "div_vout": "Vout (Output):",
                "op_inv": "Inverting", "op_noninv": "Non-Inverting", "op_gain": "Gain (Av):",
                "555_freq": "Frequency:", "555_duty": "Duty Cycle:",
                "base_input": "Enter Number:", "base_conv": "CONVERT",
                "batt_cap": "Batt. Capacity (mAh):", "batt_cons": "Device Current (mA):", 
                "batt_life": "Est. Life:", "batt_days": "Days", "batt_hours": "Hours",
                "pcb_current": "Current (Amps):", "pcb_temp": "Temp Rise (°C):",
                "pcb_thick": "Copper Thickness (oz):", "pcb_layer": "Layer Type:",
                "pcb_ext": "External", "pcb_int": "Internal",
                "pcb_width": "Min. Trace Width:",
                "filt_type": "Filter Type:", "filt_lp": "Low Pass (RC)", "filt_hp": "High Pass (CR)",
                "filt_cutoff": "Cutoff Freq (fc):",
                "rf_val": "Enter Value:", "rf_res": "Result:",
                "cap_code": "Enter Code (104, 22p):", "cap_val": "Capacity:",
                "awg_no": "AWG Number:", "awg_dia": "Diameter:", "awg_area": "Area:", "awg_amp": "Max Current (Est):",
                "log_gate": "Gate Type:", "log_inA": "Input A (0/1)", "log_inB": "Input B (0/1)", "log_out": "Output (Q):",
                "heat_tj": "Max Chip Temp (Tj °C):", "heat_ta": "Ambient Temp (Ta °C):", 
                "heat_p": "Power Dissipated (Watt):", "heat_res": "Max Thermal Res (Rth):"
            }
        }

        # --- VERİ SETLERİ ---
        self.renk_kodlari = {'Siyah': 0, 'Kahverengi': 1, 'Kırmızı': 2, 'Turuncu': 3, 'Sarı': 4, 'Yeşil': 5, 'Mavi': 6, 'Mor': 7, 'Gri': 8, 'Beyaz': 9}
        self.renk_to_hex = {'Siyah': 'black', 'Kahverengi': '#8B4513', 'Kırmızı': 'red', 'Turuncu': 'orange', 'Sarı': 'yellow', 'Yeşil': 'green', 'Mavi': 'blue', 'Mor': 'purple', 'Gri': 'gray', 'Beyaz': 'white', 'Altın': '#FFD700', 'Gümüş': '#C0C0C0'}
        self.carpanlar = {'Siyah': 1, 'Kahverengi': 10, 'Kırmızı': 100, 'Turuncu': 1000, 'Sarı': 10000, 'Yeşil': 100000, 'Mavi': 1000000, 'Mor': 10000000, 'Altın': 0.1, 'Gümüş': 0.01}
        self.toleranslar = {'Kahverengi': 1, 'Kırmızı': 2, 'Yeşil': 0.5, 'Mavi': 0.25, 'Mor': 0.10, 'Gri': 0.05, 'Altın': 5, 'Gümüş': 10}

        # --- ÜST PANEL ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(pady=10, fill="x", padx=20)
        self.lbl_baslik = ctk.CTkLabel(self.top_frame, text=self.T("title"), font=("Roboto", 24, "bold"))
        self.lbl_baslik.pack(side="left", padx=20)

        self.lang_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.lang_frame.pack(side="right")
        ctk.CTkLabel(self.lang_frame, text="English", font=("Arial", 12)).pack(side="left", padx=5)
        self.btn_lang = ctk.CTkSwitch(self.lang_frame, text="", command=self.toggle_language, onvalue="TR", offvalue="EN", width=40)
        self.btn_lang.pack(side="left", padx=5)
        self.btn_lang.select()
        ctk.CTkLabel(self.lang_frame, text="Türkçe", font=("Arial", 12)).pack(side="left", padx=5)

        # --- SEKME YAPISI ---
        self.tabview = ctk.CTkTabview(self, width=950, height=850)
        self.tabview.pack(pady=10)
        self.init_tabs()

    def T(self, key):
        return self.translations[self.current_lang].get(key, key)

    def toggle_language(self):
        self.current_lang = self.btn_lang.get()
        self.lbl_baslik.configure(text=self.T("title"))
        self.tabview.destroy()
        self.tabview = ctk.CTkTabview(self, width=950, height=850)
        self.tabview.pack(pady=10)
        self.init_tabs()

    def init_tabs(self):
        self.tab_calc = self.tabview.add(self.T("tab_calc"))
        self.tab_direnc = self.tabview.add(self.T("tab_resistor"))
        self.tab_led = self.tabview.add(self.T("tab_led"))
        self.tab_smd = self.tabview.add(self.T("tab_smd"))
        self.tab_cap = self.tabview.add(self.T("tab_cap"))
        self.tab_awg = self.tabview.add(self.T("tab_awg"))
        self.tab_div = self.tabview.add(self.T("tab_div"))
        self.tab_opamp = self.tabview.add(self.T("tab_opamp"))
        self.tab_555 = self.tabview.add(self.T("tab_555"))
        self.tab_filter = self.tabview.add(self.T("tab_filter"))
        self.tab_rf = self.tabview.add(self.T("tab_rf"))
        self.tab_pcb = self.tabview.add(self.T("tab_pcb"))
        self.tab_logic = self.tabview.add(self.T("tab_logic"))
        self.tab_heat = self.tabview.add(self.T("tab_heat"))
        self.tab_batt = self.tabview.add(self.T("tab_batt"))
        self.tab_taban = self.tabview.add(self.T("tab_base"))
        
        self.setup_calculator_tab()
        self.setup_direnc_tab()
        self.setup_led_tab()
        self.setup_smd_tab()
        self.setup_cap_tab()
        self.setup_awg_tab()
        self.setup_bolucu_tab()
        self.setup_opamp_tab()
        self.setup_555_tab()
        self.setup_filter_tab()
        self.setup_rf_tab()
        self.setup_pcb_tab()
        self.setup_logic_tab()
        self.setup_heat_tab()
        self.setup_battery_tab()
        self.setup_taban_tab()

    # ==========================================
    # 0. SEKME: AKILLI HESAP MAKİNESİ (GÜNCELLENDİ)
    # ==========================================
    def setup_calculator_tab(self):
        frame = self.tab_calc
        self.lbl_memory = ctk.CTkLabel(frame, text="", font=("Arial", 12, "bold"), text_color="orange")
        self.lbl_memory.pack(pady=(5,0), padx=20, anchor="e")
        self.calc_display = ctk.CTkEntry(frame, width=450, height=70, font=("Arial", 32), justify="right")
        self.calc_display.pack(pady=(0, 20))
        self.calc_display.insert(0, "0")
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent"); btn_frame.pack()

        buttons = [
            ('MC', 0, 0, 4), ('MR', 0, 1, 4), ('M-', 0, 2, 4), ('M+', 0, 3, 4), ('C', 0, 4, 2),
            ('asin', 1, 0, 3), ('acos', 1, 1, 3), ('atan', 1, 2, 3), ('pow', 1, 3, 3), ('DEL', 1, 4, 2),
            ('sin', 2, 0, 3), ('cos', 2, 1, 3), ('tan', 2, 2, 3), ('log', 2, 3, 3), ('ln', 2, 4, 3),
            ('x²', 3, 0, 3), ('1/x', 3, 1, 3), ('sqrt', 3, 2, 3), ('%', 3, 3, 3), ('/', 3, 4, 1),
            ('(', 4, 0, 3), ('7', 4, 1, 0), ('8', 4, 2, 0), ('9', 4, 3, 0), ('*', 4, 4, 1),
            (')', 5, 0, 3), ('4', 5, 1, 0), ('5', 5, 2, 0), ('6', 5, 3, 0), ('-', 5, 4, 1),
            ('pi', 6, 0, 3), ('1', 6, 1, 0), ('2', 6, 2, 0), ('3', 6, 3, 0), ('+', 6, 4, 1),
            ('e', 7, 0, 3), ('+/-', 7, 1, 0), ('0', 7, 2, 0), ('.', 7, 3, 0), ('=', 7, 4, 1)
        ]
        
        for (text, row, col, color_type) in buttons:
            fg = ["#3b8ed0", "#e67e22", "#c0392b", "#34495e", "#27ae60"][color_type]
            hov = ["#36719f", "#d35400", "#922b21", "#2c3e50", "#1e8449"][color_type]
            ctk.CTkButton(btn_frame, text=text, width=85, height=60, font=("Arial", 18, "bold"), fg_color=fg, hover_color=hov, command=lambda t=text: self.on_calc_click(t)).grid(row=row, column=col, padx=3, pady=3)

    def on_calc_click(self, key):
        current = self.calc_display.get()
        
        # --- 0 SİLME DÜZELTMESİ (FIX) ---
        # Eğer ekranda sadece "0" varsa ve basılan tuş bir sayı veya fonksiyonsa "0"ı sil.
        # Ancak işlem (+, -, *, /) veya nokta (.) ise "0"ı koru (örn: 0.5 veya 0+2)
        special_actions = ['C', 'DEL', '+/-', '%', 'MC', 'MR', 'M+', 'M-', '='] # Bu tuşlar kendi mantığını çalıştırır
        
        if key not in special_actions:
            if current == "0":
                # 0'ı KORUMASI gereken tuşlar: İşlemler, nokta, kare alma (0**2), kapama parantezi
                keep_zero_keys = ['+', '-', '*', '/', '.', 'x²', ')'] 
                
                if key not in keep_zero_keys:
                    self.calc_display.delete(0, tk.END) # 0'ı sil
        # ------------------------------------

        if key == 'C': self.calc_display.delete(0, tk.END); self.calc_display.insert(0, "0")
        elif key == 'DEL': 
            if len(current) > 1: self.calc_display.delete(len(current)-1, tk.END)
            else: self.calc_display.delete(0, tk.END); self.calc_display.insert(0, "0")
        elif key == '+/-':
            try:
                if current.lstrip('-').replace('.', '', 1).isdigit(): self.calc_display.delete(0, tk.END); self.calc_display.insert(0, str(float(current)*-1).rstrip('0').rstrip('.'))
                else: self.calc_display.insert(0, "-("); self.calc_display.insert(tk.END, ")")
            except: pass
        elif key == '%':
            try: self.calc_display.delete(0, tk.END); self.calc_display.insert(0, str(eval(current)/100))
            except: pass
        elif key == 'x²': self.calc_display.insert(tk.END, "**2")
        elif key == '1/x': self.calc_display.insert(tk.END, "1/")
        elif key == 'MC': self.calc_memory = 0.0; self.lbl_memory.configure(text="")
        elif key == 'MR': self.calc_display.delete(0, tk.END); self.calc_display.insert(0, str(self.calc_memory).rstrip('0').rstrip('.'))
        elif key == 'M+': 
            try: self.calc_memory += self.safe_eval(current); self.lbl_memory.configure(text="M")
            except: pass
        elif key == 'M-': 
            try: self.calc_memory -= self.safe_eval(current); self.lbl_memory.configure(text="M")
            except: pass
        elif key == '=':
            try: 
                open_p = current.count('('); close_p = current.count(')')
                if open_p > close_p: current += ')' * (open_p - close_p)
                
                # Regex Otomatik Çarpma Düzeltmeleri
                current = re.sub(r'(\d)(\()', r'\1*\2', current) # 5( -> 5*(
                current = re.sub(r'(\d)(sin|cos|tan|log|ln|asin|acos|atan|sqrt)', r'\1*\2', current) # 2sin -> 2*sin
                current = re.sub(r'(\))(\d)', r'\1*\2', current) # )5 -> )*5
                current = re.sub(r'(\))(\()', r'\1*\2', current) # )( -> )*(

                result = self.safe_eval(current)
                self.calc_display.delete(0, tk.END)
                res_str = str(round(result, 8))
                if res_str.endswith(".0"): res_str = res_str[:-2]
                self.calc_display.insert(0, res_str)
            except:
                self.calc_display.delete(0, tk.END); self.calc_display.insert(0, self.T("calc_err"))
        else: self.calc_display.insert(tk.END, key)

    def safe_eval(self, expression):
        def deg_sin(x): return math.sin(math.radians(x))
        def deg_cos(x): return math.cos(math.radians(x))
        def deg_tan(x): return math.tan(math.radians(x))
        def deg_asin(x): return math.degrees(math.asin(x))
        def deg_acos(x): return math.degrees(math.acos(x))
        def deg_atan(x): return math.degrees(math.atan(x))

        safe_dict = {
            "sin": deg_sin, "cos": deg_cos, "tan": deg_tan,
            "asin": deg_asin, "acos": deg_acos, "atan": deg_atan,
            "log": math.log10, "ln": math.log, "sqrt": math.sqrt,
            "pi": math.pi, "e": math.e, "pow": math.pow
        }
        return eval(expression, {"__builtins__": None}, safe_dict)

    # ==========================================
    # 10. SEKME: MANTIK KAPILARI
    # ==========================================
    def setup_logic_tab(self):
        frame = self.tab_logic
        ctk.CTkLabel(frame, text=self.T("log_gate"), font=("Roboto", 16)).pack(pady=(20, 5))
        self.combo_gate = ctk.CTkComboBox(frame, values=["AND", "OR", "NOT", "NAND", "NOR", "XOR", "XNOR"], command=self.update_logic)
        self.combo_gate.set("AND")
        self.combo_gate.pack(pady=5)
        self.cv_logic = tk.Canvas(frame, width=300, height=200, bg="#2b2b2b", highlightthickness=0)
        self.cv_logic.pack(pady=20)
        control_frame = ctk.CTkFrame(frame, fg_color="transparent")
        control_frame.pack(pady=10)
        self.switch_a = ctk.CTkSwitch(control_frame, text=self.T("log_inA"), command=self.update_logic)
        self.switch_a.grid(row=0, column=0, padx=20)
        self.switch_b = ctk.CTkSwitch(control_frame, text=self.T("log_inB"), command=self.update_logic)
        self.switch_b.grid(row=0, column=1, padx=20)
        self.lbl_logic_out = ctk.CTkLabel(frame, text=f"{self.T('log_out')} 0", font=("Roboto", 24, "bold"), text_color="gray")
        self.lbl_logic_out.pack(pady=20)
        self.update_logic()

    def update_logic(self, *args):
        gate = self.combo_gate.get()
        a = self.switch_a.get()
        b = self.switch_b.get()
        if gate == "NOT": self.switch_b.configure(state="disabled")
        else: self.switch_b.configure(state="normal")
        out = 0
        if gate == "AND": out = a and b
        elif gate == "OR": out = a or b
        elif gate == "NOT": out = not a
        elif gate == "NAND": out = not (a and b)
        elif gate == "NOR": out = not (a or b)
        elif gate == "XOR": out = a ^ b
        elif gate == "XNOR": out = not (a ^ b)
        out = 1 if out else 0
        color = "#2ecc71" if out == 1 else "gray"
        self.lbl_logic_out.configure(text=f"{self.T('log_out')} {out}", text_color=color)
        self.draw_logic_gate(gate, a, b, out)

    def draw_logic_gate(self, gate, a, b, out):
        c = self.cv_logic; c.delete("all")
        col_a = "#2ecc71" if a else "gray"
        col_b = "#2ecc71" if b else "gray"
        col_out = "#2ecc71" if out else "gray"
        if gate == "NOT": c.create_line(50, 100, 120, 100, fill=col_a, width=3); c.create_text(40, 100, text="A", fill="white")
        else: c.create_line(50, 70, 120, 70, fill=col_a, width=3); c.create_text(40, 70, text="A", fill="white"); c.create_line(50, 130, 120, 130, fill=col_b, width=3); c.create_text(40, 130, text="B", fill="white")
        c.create_rectangle(120, 50, 200, 150, outline="white", width=2, fill="#34495e")
        c.create_text(160, 100, text=gate, fill="white", font=("Arial", 16, "bold"))
        c.create_line(200, 100, 270, 100, fill=col_out, width=3); c.create_text(280, 100, text="Q", fill="white")
        c.create_oval(250, 90, 270, 110, fill=col_out, outline="white")

    # ==========================================
    # 11. SEKME: ISI EMİCİ HESAPLAYICI
    # ==========================================
    def setup_heat_tab(self):
        frame = self.tab_heat
        self.cv_heat = tk.Canvas(frame, width=300, height=200, bg="#2b2b2b", highlightthickness=0); self.cv_heat.pack(pady=20); self.draw_heatsink()
        input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text=self.T("heat_tj")).grid(row=0, column=0, padx=10, pady=5); self.ent_tj = ctk.CTkEntry(input_frame, placeholder_text="125"); self.ent_tj.grid(row=0, column=1)
        ctk.CTkLabel(input_frame, text=self.T("heat_ta")).grid(row=1, column=0, padx=10, pady=5); self.ent_ta = ctk.CTkEntry(input_frame, placeholder_text="25"); self.ent_ta.grid(row=1, column=1); self.ent_ta.insert(0, "25")
        ctk.CTkLabel(input_frame, text=self.T("heat_p")).grid(row=2, column=0, padx=10, pady=5); self.ent_p = ctk.CTkEntry(input_frame, placeholder_text="5"); self.ent_p.grid(row=2, column=1)
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_heat, fg_color="#e74c3c").pack(pady=20)
        self.lbl_heat_res = ctk.CTkLabel(frame, text="Rth: ---", font=("Roboto", 24, "bold"), text_color="#f1c40f"); self.lbl_heat_res.pack()

    def draw_heatsink(self):
        c = self.cv_heat; c.delete("all")
        for i in range(5): x = 80 + i*30; c.create_rectangle(x, 50, x+10, 120, fill="#95a5a6", outline="black")
        c.create_rectangle(70, 120, 230, 140, fill="#7f8c8d", outline="black")
        c.create_rectangle(130, 140, 170, 160, fill="#2c3e50", outline="black"); c.create_text(150, 150, text="CHIP", fill="white", font=("Arial", 8))
        c.create_line(150, 140, 150, 100, fill="red", width=2, arrow=tk.LAST); c.create_text(180, 80, text="Heat", fill="red")

    def hesapla_heat(self):
        try:
            tj = float(self.ent_tj.get()); ta = float(self.ent_ta.get()); p = float(self.ent_p.get())
            if p <= 0: self.lbl_heat_res.configure(text=self.T("calc_err")); return
            rth = (tj - ta) / p; self.lbl_heat_res.configure(text=f"Max Rth: {rth:.2f} °C/W")
        except: self.lbl_heat_res.configure(text=self.T("calc_err"))

    # ==========================================
    # MEVCUT SEKMELER (Korunanlar)
    # ==========================================
    def setup_cap_tab(self):
        frame = self.tab_cap
        ctk.CTkLabel(frame, text=self.T("cap_code"), font=("Roboto", 16)).pack(pady=20)
        self.cv_cap = tk.Canvas(frame, width=200, height=150, bg="#2b2b2b", highlightthickness=0); self.cv_cap.pack(pady=10)
        self.draw_capacitor("104")
        self.ent_cap = ctk.CTkEntry(frame, font=("Arial", 16)); self.ent_cap.pack(pady=10)
        self.ent_cap.bind("<Return>", lambda e: self.calc_cap())
        ctk.CTkButton(frame, text=self.T("smd_solve"), command=self.calc_cap, fg_color="#e67e22").pack(pady=10)
        self.lbl_cap_res = ctk.CTkLabel(frame, text="---", font=("Roboto", 20, "bold"), text_color="#f39c12"); self.lbl_cap_res.pack(pady=20)
    def draw_capacitor(self, code):
        c = self.cv_cap; c.delete("all")
        c.create_line(70, 100, 70, 140, fill="#bdc3c7", width=3); c.create_line(130, 100, 130, 140, fill="#bdc3c7", width=3)
        c.create_oval(40, 20, 160, 110, fill="#d35400", outline="#e67e22", width=2); c.create_text(100, 65, text=code, fill="black", font=("Arial", 22, "bold"))
    def calc_cap(self):
        code = self.ent_cap.get().strip().upper(); self.draw_capacitor(code)
        try:
            if len(code) == 3 and code.isdigit():
                val_pf = int(code[:2]) * (10 ** int(code[2])); val_nf = val_pf / 1000; val_uf = val_nf / 1000
                if val_uf >= 1: res = f"{val_uf:.2f} µF"
                elif val_nf >= 1: res = f"{val_nf:.2f} nF"
                else: res = f"{val_pf} pF"
                self.lbl_cap_res.configure(text=f"{self.T('cap_val')} {res}")
            elif "P" in code or "N" in code or "U" in code: self.lbl_cap_res.configure(text="Sadece sayı (104)")
            else: self.lbl_cap_res.configure(text=self.T("calc_err"))
        except: self.lbl_cap_res.configure(text=self.T("calc_err"))
    def setup_awg_tab(self):
        frame = self.tab_awg
        self.cv_awg = tk.Canvas(frame, width=200, height=200, bg="#2b2b2b", highlightthickness=0); self.cv_awg.pack(pady=20)
        input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text=self.T("awg_no")).grid(row=0, column=0, padx=10)
        self.ent_awg = ctk.CTkEntry(input_frame, width=80, placeholder_text="24"); self.ent_awg.grid(row=0, column=1)
        ctk.CTkButton(frame, text=self.T("base_conv"), command=self.calc_awg, fg_color="#2980b9").pack(pady=10)
        self.lbl_awg_dia = ctk.CTkLabel(frame, text=f"{self.T('awg_dia')} ---", font=("Roboto", 16)); self.lbl_awg_dia.pack()
        self.lbl_awg_area = ctk.CTkLabel(frame, text=f"{self.T('awg_area')} ---", font=("Roboto", 16)); self.lbl_awg_area.pack()
        self.lbl_awg_amp = ctk.CTkLabel(frame, text=f"{self.T('awg_amp')} ---", font=("Roboto", 18, "bold"), text_color="#2ecc71"); self.lbl_awg_amp.pack(pady=10)
        self.draw_awg_circle(0.5)
    def draw_awg_circle(self, diameter_mm):
        c = self.cv_awg; c.delete("all"); size = min(180, max(5, diameter_mm * 20)); offset = (200 - size) / 2
        c.create_oval(offset, offset, offset+size, offset+size, fill="#d35400", outline="#e67e22", width=2)
        c.create_text(100, 190, text=f"Ø {diameter_mm:.3f} mm", fill="white")
    def calc_awg(self):
        try:
            awg = int(self.ent_awg.get()); dia_mm = 0.127 * (92 ** ((36 - awg) / 39)); area_mm2 = math.pi * ((dia_mm / 2) ** 2)
            amp_transmission = area_mm2 * 4; amp_chassis = area_mm2 * 15
            self.lbl_awg_dia.configure(text=f"{self.T('awg_dia')} {dia_mm:.3f} mm"); self.lbl_awg_area.configure(text=f"{self.T('awg_area')} {area_mm2:.3f} mm²")
            self.lbl_awg_amp.configure(text=f"{self.T('awg_amp')} ~{amp_transmission:.1f}A / ~{amp_chassis:.1f}A"); self.draw_awg_circle(dia_mm)
        except: self.lbl_awg_amp.configure(text=self.T("calc_err"))
    def setup_filter_tab(self):
        frame = self.tab_filter; self.filt_type = tk.IntVar(value=0)
        radio_frame = ctk.CTkFrame(frame, fg_color="transparent"); radio_frame.pack(pady=10)
        ctk.CTkRadioButton(radio_frame, text=self.T("filt_lp"), variable=self.filt_type, value=0, command=self.draw_filter).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text=self.T("filt_hp"), variable=self.filt_type, value=1, command=self.draw_filter).pack(side="left", padx=10)
        self.cv_filt = tk.Canvas(frame, width=300, height=180, bg="#2b2b2b", highlightthickness=0); self.cv_filt.pack(pady=10); self.draw_filter()
        input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text="R (kΩ):").grid(row=0, column=0, padx=5); self.ent_filt_r = ctk.CTkEntry(input_frame, width=100); self.ent_filt_r.grid(row=0, column=1)
        ctk.CTkLabel(input_frame, text="C (µF):").grid(row=1, column=0, padx=5); self.ent_filt_c = ctk.CTkEntry(input_frame, width=100); self.ent_filt_c.grid(row=1, column=1)
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_filtre, fg_color="#8e44ad").pack(pady=15)
        self.lbl_filt_res = ctk.CTkLabel(frame, text="fc: ---", font=("Roboto", 24, "bold"), text_color="#1abc9c"); self.lbl_filt_res.pack()
    def draw_filter(self):
        c = self.cv_filt; c.delete("all")
        c.create_line(50, 50, 100, 50, fill="white", width=2); c.create_text(30, 50, text="Vin", fill="white")
        c.create_line(200, 50, 250, 50, fill="white", width=2); c.create_text(270, 50, text="Vout", fill="white")
        c.create_line(50, 130, 250, 130, fill="white", width=2); c.create_text(150, 140, text="GND", fill="gray")
        if self.filt_type.get() == 0:
            c.create_rectangle(100, 40, 140, 60, fill="#f5deb3", outline="white"); c.create_text(120, 30, text="R", fill="white"); c.create_line(140, 50, 200, 50, fill="white", width=2)
            c.create_line(200, 50, 200, 80, fill="white", width=2); c.create_line(190, 80, 210, 80, fill="white", width=2); c.create_line(190, 90, 210, 90, fill="white", width=2); c.create_line(200, 90, 200, 130, fill="white", width=2); c.create_text(220, 85, text="C", fill="white")
        else:
            c.create_line(100, 50, 110, 50, fill="white", width=2); c.create_line(110, 40, 110, 60, fill="white", width=2); c.create_line(120, 40, 120, 60, fill="white", width=2); c.create_line(120, 50, 200, 50, fill="white", width=2); c.create_text(115, 30, text="C", fill="white")
            c.create_line(200, 50, 200, 70, fill="white", width=2); c.create_rectangle(190, 70, 210, 110, fill="#f5deb3", outline="white"); c.create_line(200, 110, 200, 130, fill="white", width=2); c.create_text(220, 90, text="R", fill="white")
    def hesapla_filtre(self):
        try:
            R = float(self.ent_filt_r.get()) * 1000; C = float(self.ent_filt_c.get()) / 1e6; fc = 1 / (2 * math.pi * R * C)
            self.lbl_filt_res.configure(text=f"fc: {fc:.2f} Hz")
        except: self.lbl_filt_res.configure(text=self.T("calc_err"))
    def setup_rf_tab(self):
        frame = self.tab_rf; self.rf_mode = tk.IntVar(value=0)
        radio_frame = ctk.CTkFrame(frame, fg_color="transparent"); radio_frame.pack(pady=10)
        ctk.CTkRadioButton(radio_frame, text="mW -> dBm", variable=self.rf_mode, value=0, command=self.update_rf_lbl).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="dBm -> mW", variable=self.rf_mode, value=1, command=self.update_rf_lbl).pack(side="left", padx=10)
        self.lbl_rf_input = ctk.CTkLabel(frame, text=self.T("rf_val")); self.lbl_rf_input.pack(pady=5)
        self.ent_rf = ctk.CTkEntry(frame, width=150, font=("Arial", 16)); self.ent_rf.pack(pady=5)
        ctk.CTkButton(frame, text=self.T("base_conv"), command=self.hesapla_rf, fg_color="#34495e").pack(pady=15)
        self.lbl_rf_res = ctk.CTkLabel(frame, text="---", font=("Roboto", 24, "bold"), text_color="#3498db"); self.lbl_rf_res.pack(); self.update_rf_lbl()
    def update_rf_lbl(self): txt = "MilliWatt (mW):" if self.rf_mode.get() == 0 else "dBm:"; self.lbl_rf_input.configure(text=txt)
    def hesapla_rf(self):
        try:
            val = float(self.ent_rf.get())
            if self.rf_mode.get() == 0: res = "-inf" if val <= 0 else f"{10 * math.log10(val):.2f} dBm"
            else: res = f"{10 ** (val / 10):.4f} mW"
            self.lbl_rf_res.configure(text=res)
        except: self.lbl_rf_res.configure(text=self.T("calc_err"))
    def setup_pcb_tab(self):
        frame = self.tab_pcb; self.cv_pcb = tk.Canvas(frame, width=300, height=150, bg="#2b2b2b", highlightthickness=0); self.cv_pcb.pack(pady=20); self.draw_pcb_trace(5)
        input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text=self.T("pcb_current")).grid(row=0, column=0, padx=10, pady=5); self.ent_pcb_amp = ctk.CTkEntry(input_frame, placeholder_text="1.0"); self.ent_pcb_amp.grid(row=0, column=1)
        ctk.CTkLabel(input_frame, text=self.T("pcb_temp")).grid(row=1, column=0, padx=10, pady=5); self.ent_pcb_temp = ctk.CTkEntry(input_frame, placeholder_text="10"); self.ent_pcb_temp.grid(row=1, column=1); self.ent_pcb_temp.insert(0, "10")
        ctk.CTkLabel(input_frame, text=self.T("pcb_thick")).grid(row=2, column=0, padx=10, pady=5); self.combo_pcb_oz = ctk.CTkComboBox(input_frame, values=["0.5 oz", "1.0 oz", "2.0 oz"]); self.combo_pcb_oz.grid(row=2, column=1); self.combo_pcb_oz.set("1.0 oz")
        ctk.CTkLabel(input_frame, text=self.T("pcb_layer")).grid(row=3, column=0, padx=10, pady=5); self.combo_pcb_layer = ctk.CTkComboBox(input_frame, values=[self.T("pcb_ext"), self.T("pcb_int")]); self.combo_pcb_layer.grid(row=3, column=1)
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_pcb, fg_color="#d35400").pack(pady=20)
        self.lbl_pcb_res = ctk.CTkLabel(frame, text="---", font=("Roboto", 24, "bold"), text_color="#f39c12"); self.lbl_pcb_res.pack()
    def draw_pcb_trace(self, width_factor):
        self.cv_pcb.delete("all"); self.cv_pcb.create_rectangle(10, 10, 290, 140, fill="#27ae60", outline=""); y1 = 75 - width_factor; y2 = 75 + width_factor; self.cv_pcb.create_line(10, 75, 290, 75, width=width_factor*2, fill="#e67e22"); self.cv_pcb.create_text(150, 20, text="PCB TRACE", fill="#ecf0f1", font=("Arial", 10))
    def hesapla_pcb(self):
        try:
            I = float(self.ent_pcb_amp.get()); dT = float(self.ent_pcb_temp.get()); oz = float(self.combo_pcb_oz.get().split()[0]); is_external = self.combo_pcb_layer.get() == self.T("pcb_ext"); k = 0.048 if is_external else 0.024
            area_mils2 = (I / (k * (dT ** 0.44))) ** (1/0.725); thick_mils = oz * 1.378; width_mils = area_mils2 / thick_mils; width_mm = width_mils * 0.0254
            self.lbl_pcb_res.configure(text=f"{width_mm:.3f} mm\n({width_mils:.1f} mil)"); vis_width = max(2, min(40, width_mm * 5)); self.draw_pcb_trace(vis_width)
        except: self.lbl_pcb_res.configure(text=self.T("calc_err"))
    def setup_battery_tab(self):
        frame = self.tab_batt; self.cv_batt = tk.Canvas(frame, width=200, height=100, bg="#2b2b2b", highlightthickness=0); self.cv_batt.pack(pady=20); self.draw_battery(100)
        ctk.CTkLabel(frame, text=self.T("batt_cap")).pack(pady=5); self.ent_mah = ctk.CTkEntry(frame, placeholder_text="2500"); self.ent_mah.pack(pady=5)
        ctk.CTkLabel(frame, text=self.T("batt_cons")).pack(pady=5); self.ent_ma = ctk.CTkEntry(frame, placeholder_text="50"); self.ent_ma.pack(pady=5)
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_batarya, fg_color="#27ae60").pack(pady=20); self.lbl_batt_life = ctk.CTkLabel(frame, text="---", font=("Roboto", 24, "bold"), text_color="#f1c40f"); self.lbl_batt_life.pack()
    def draw_battery(self, level): self.cv_batt.delete("all"); self.cv_batt.create_rectangle(20, 20, 160, 80, outline="white", width=3); self.cv_batt.create_rectangle(160, 35, 170, 65, fill="white"); fill_width = 25 + (130 * (level/100)); color = "#2ecc71" if level > 20 else "#e74c3c"; self.cv_batt.create_rectangle(25, 25, fill_width, 75, fill=color, outline=""); self.cv_batt.create_text(90, 50, text=f"%{level}", fill="white", font=("Arial", 16, "bold"))
    def hesapla_batarya(self):
        try: mah = float(self.ent_mah.get()); ma = float(self.ent_ma.get()); saat = (mah / ma) * 0.8; gun = saat / 24; self.lbl_batt_life.configure(text=f"{saat:.1f} {self.T('batt_hours')}\n({gun:.1f} {self.T('batt_days')})")
        except: self.lbl_batt_life.configure(text=self.T("calc_err"))
    def setup_direnc_tab(self):
        frame = self.tab_direnc; self.canvas = tk.Canvas(frame, width=400, height=120, bg="#2b2b2b", highlightthickness=0); self.canvas.pack(pady=10); self.draw_resistor_body()
        self.create_combobox(frame, self.T("res_band1"), list(self.renk_kodlari.keys()), self.update_band1); self.create_combobox(frame, self.T("res_band2"), list(self.renk_kodlari.keys()), self.update_band2)
        self.create_combobox(frame, self.T("res_band3"), list(self.carpanlar.keys()), self.update_band3); self.create_combobox(frame, self.T("res_band4"), list(self.toleranslar.keys()), self.update_band4)
        self.lbl_sonuc = ctk.CTkLabel(frame, text=f"{self.T('res_result')} ---", font=("Roboto", 20, "bold"), text_color="#3498db"); self.lbl_sonuc.pack(pady=20); self.secimler = [None, None, None, None]
    def draw_resistor_body(self):
        self.canvas.create_line(20, 60, 80, 60, width=5, fill="#A9A9A9"); self.canvas.create_line(320, 60, 380, 60, width=5, fill="#A9A9A9")
        self.canvas.create_rectangle(80, 25, 320, 95, fill="#f5deb3", outline="#d2b48c", width=2)
        self.band1_id = self.canvas.create_rectangle(100, 25, 120, 95, fill="#f5deb3", outline=""); self.band2_id = self.canvas.create_rectangle(140, 25, 160, 95, fill="#f5deb3", outline="")
        self.band3_id = self.canvas.create_rectangle(180, 25, 200, 95, fill="#f5deb3", outline=""); self.band4_id = self.canvas.create_rectangle(280, 25, 300, 95, fill="#f5deb3", outline="")
    def create_combobox(self, parent, text, values, command): container = ctk.CTkFrame(parent, fg_color="transparent"); container.pack(pady=5); ctk.CTkLabel(container, text=text, width=100, anchor="e").pack(side="left", padx=10); ctk.CTkComboBox(container, values=values, command=command, state="readonly", width=200).pack(side="left")
    def update_band1(self, c): self.secimler[0]=c; self.canvas.itemconfig(self.band1_id, fill=self.renk_to_hex[c]); self.hesapla_direnc()
    def update_band2(self, c): self.secimler[1]=c; self.canvas.itemconfig(self.band2_id, fill=self.renk_to_hex[c]); self.hesapla_direnc()
    def update_band3(self, c): self.secimler[2]=c; self.canvas.itemconfig(self.band3_id, fill=self.renk_to_hex[c]); self.hesapla_direnc()
    def update_band4(self, c): self.secimler[3]=c; self.canvas.itemconfig(self.band4_id, fill=self.renk_to_hex[c]); self.hesapla_direnc()
    def hesapla_direnc(self):
        if None in self.secimler: return
        r1, r2, r3, r4 = self.secimler; ohm = (self.renk_kodlari[r1]*10 + self.renk_kodlari[r2]) * self.carpanlar[r3]
        if ohm >= 1e6: yazi = f"{ohm/1e6:.2f} MΩ"
        elif ohm >= 1e3: yazi = f"{ohm/1e3:.2f} kΩ"
        else: yazi = f"{ohm:.2f} Ω"
        self.lbl_sonuc.configure(text=f"{self.T('res_result')} {yazi} ±%{self.toleranslar[r4]}")
    def setup_led_tab(self):
        frame = self.tab_led; ctk.CTkLabel(frame, text=self.T("led_supply")).pack(pady=(10,0)); self.entry_voltaj = ctk.CTkEntry(frame, placeholder_text="9"); self.entry_voltaj.pack()
        self.led_vals = {"Kırmızı": 2.0, "Sarı": 2.1, "Yeşil": 2.2, "Mavi": 3.2, "Beyaz": 3.2}; ctk.CTkLabel(frame, text=self.T("led_color")).pack(pady=(10,0)); self.combo_led = ctk.CTkComboBox(frame, values=list(self.led_vals.keys()), command=self.upd_led_vis); self.combo_led.pack()
        ctk.CTkLabel(frame, text=self.T("led_current")).pack(pady=(10,0)); self.combo_ak = ctk.CTkComboBox(frame, values=["20 mA", "10 mA", "2 mA"]); self.combo_ak.set("20 mA"); self.combo_ak.pack()
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_led, fg_color="green").pack(pady=15); self.cv_led = tk.Canvas(frame, width=60, height=60, bg="#2b2b2b", highlightthickness=0); self.cv_led.pack()
        self.led_shp = self.cv_led.create_oval(10,10,50,50, fill="#444", outline="#888", width=2); self.lbl_led_res = ctk.CTkLabel(frame, text=f"{self.T('led_res')} ---", font=("Roboto", 18, "bold")); self.lbl_led_res.pack(pady=5); self.lbl_led_wat = ctk.CTkLabel(frame, text="", text_color="orange"); self.lbl_led_wat.pack()
    def upd_led_vis(self, c): colors = {"Kırmızı":"red", "Sarı":"yellow", "Yeşil":"green", "Mavi":"#00BFFF", "Beyaz":"white"}; self.cv_led.itemconfig(self.led_shp, fill=colors.get(c, "gray"), outline=colors.get(c, "gray"))
    def hesapla_led(self):
        try:
            Vs = float(self.entry_voltaj.get().replace(',','.')); Vled = self.led_vals[self.combo_led.get()]; I = int(self.combo_ak.get().split()[0]) / 1000
            if Vs <= Vled: self.lbl_led_res.configure(text=self.T("led_err_v"), text_color="red"); return
            R = (Vs - Vled) / I; P = (Vs - Vled) * I
            self.lbl_led_res.configure(text=f"{self.T('led_res')} {R:.1f} Ω", text_color="#3498db"); self.lbl_led_wat.configure(text=f"{self.T('led_pwr')} {P:.3f} W")
        except: self.lbl_led_res.configure(text=self.T("calc_err"), text_color="red")
    def setup_smd_tab(self):
        frame = self.tab_smd; ctk.CTkLabel(frame, text=self.T("smd_title"), font=("Roboto", 16)).pack(pady=20); self.cv_smd = tk.Canvas(frame, width=200, height=100, bg="#2b2b2b", highlightthickness=0); self.cv_smd.pack(); self.draw_smd("---")
        self.ent_smd = ctk.CTkEntry(frame, font=("Arial", 16)); self.ent_smd.pack(pady=10); self.ent_smd.bind("<Return>", lambda e: self.calc_smd()); ctk.CTkButton(frame, text=self.T("smd_solve"), command=self.calc_smd, fg_color="purple").pack(); self.lbl_smd_res = ctk.CTkLabel(frame, text=f"{self.T('smd_val')} ---", font=("Roboto", 20, "bold"), text_color="#3498db"); self.lbl_smd_res.pack(pady=20)
    def draw_smd(self, txt): self.cv_smd.delete("all"); self.cv_smd.create_rectangle(10,20,40,80, fill="#bdc3c7", outline=""); self.cv_smd.create_rectangle(160,20,190,80, fill="#bdc3c7", outline=""); self.cv_smd.create_rectangle(40,20,160,80, fill="#111", outline=""); self.cv_smd.create_text(100,50, text=txt, fill="white", font=("Arial", 20, "bold"))
    def calc_smd(self):
        code = self.ent_smd.get().strip().upper(); self.draw_smd(code)
        try:
            if 'R' in code: val = float(code.replace('R','.'))
            elif len(code) in [3,4] and code.isdigit(): val = int(code[:-1]) * (10 ** int(code[-1]))
            else: self.lbl_smd_res.configure(text=self.T("calc_err")); return
            if val>=1e6: txt=f"{val/1e6} MΩ"
            elif val>=1e3: txt=f"{val/1e3} kΩ"
            else: txt=f"{val} Ω"
            self.lbl_smd_res.configure(text=f"{self.T('smd_val')} {txt}")
        except: self.lbl_smd_res.configure(text=self.T("calc_err"))
    def setup_bolucu_tab(self):
        frame = self.tab_div; self.cv_div = tk.Canvas(frame, width=300, height=200, bg="#2b2b2b", highlightthickness=0); self.cv_div.pack(pady=10); self.draw_voltage_divider(); input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text=self.T("div_vin")).grid(row=0, column=0, padx=5); self.ent_vin = ctk.CTkEntry(input_frame, width=80); self.ent_vin.grid(row=0, column=1)
        ctk.CTkLabel(input_frame, text="R1 (Ω):").grid(row=1, column=0, padx=5); self.ent_r1 = ctk.CTkEntry(input_frame, width=80); self.ent_r1.grid(row=1, column=1)
        ctk.CTkLabel(input_frame, text="R2 (Ω):").grid(row=2, column=0, padx=5); self.ent_r2 = ctk.CTkEntry(input_frame, width=80); self.ent_r2.grid(row=2, column=1)
        ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_bolucu, fg_color="#e67e22").pack(pady=10); self.lbl_vout = ctk.CTkLabel(frame, text=f"{self.T('div_vout')} ---", font=("Roboto", 24, "bold"), text_color="#2ecc71"); self.lbl_vout.pack()
    def draw_voltage_divider(self): c = self.cv_div; c.delete("all"); c.create_line(150, 20, 150, 180, fill="white", width=2); c.create_line(100, 20, 150, 20, fill="white", width=2); c.create_line(150, 100, 200, 100, fill="white", width=2); c.create_rectangle(140, 40, 160, 80, fill="#f5deb3", outline="white"); c.create_rectangle(140, 120, 160, 160, fill="#f5deb3", outline="white"); c.create_text(110, 35, text="Vin", fill="white"); c.create_text(180, 60, text="R1", fill="white"); c.create_text(180, 140, text="R2", fill="white"); c.create_text(220, 100, text="Vout", fill="#2ecc71", font=("Arial", 12, "bold"))
    def hesapla_bolucu(self):
        try: vin = float(self.ent_vin.get()); r1 = float(self.ent_r1.get()); r2 = float(self.ent_r2.get()); vout = vin * (r2 / (r1 + r2)); self.lbl_vout.configure(text=f"{self.T('div_vout')} {vout:.2f} V")
        except: self.lbl_vout.configure(text=self.T("calc_err"))
    def setup_opamp_tab(self):
        frame = self.tab_opamp; self.opamp_tur = tk.IntVar(value=0); radio_frame = ctk.CTkFrame(frame, fg_color="transparent"); radio_frame.pack(pady=10); ctk.CTkRadioButton(radio_frame, text=self.T("op_inv"), variable=self.opamp_tur, value=0, command=self.draw_opamp).pack(side="left", padx=10); ctk.CTkRadioButton(radio_frame, text=self.T("op_noninv"), variable=self.opamp_tur, value=1, command=self.draw_opamp).pack(side="left", padx=10); self.cv_opamp = tk.Canvas(frame, width=300, height=200, bg="#2b2b2b", highlightthickness=0); self.cv_opamp.pack(pady=10); self.draw_opamp(); input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=10)
        ctk.CTkLabel(input_frame, text="Vin:").grid(row=0, column=0); self.ent_op_vin = ctk.CTkEntry(input_frame, width=80); self.ent_op_vin.grid(row=0, column=1); ctk.CTkLabel(input_frame, text="R1:").grid(row=1, column=0); self.ent_op_r1 = ctk.CTkEntry(input_frame, width=80); self.ent_op_r1.grid(row=1, column=1); ctk.CTkLabel(input_frame, text="Rf:").grid(row=2, column=0); self.ent_op_rf = ctk.CTkEntry(input_frame, width=80); self.ent_op_rf.grid(row=2, column=1); ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_opamp, fg_color="#c0392b").pack(pady=15); self.lbl_opamp_gain = ctk.CTkLabel(frame, text=f"{self.T('op_gain')} ---", font=("Roboto", 18)); self.lbl_opamp_gain.pack(); self.lbl_opamp_vout = ctk.CTkLabel(frame, text="Vout: ---", font=("Roboto", 20, "bold"), text_color="#e74c3c"); self.lbl_opamp_vout.pack()
    def draw_opamp(self):
        c = self.cv_opamp; c.delete("all"); c.create_polygon(100, 50, 100, 150, 220, 100, fill="#ecf0f1", outline="white", width=2); c.create_text(115, 80, text="-", font=("Arial", 20)); c.create_text(115, 120, text="+", font=("Arial", 20)); c.create_line(220, 100, 260, 100, fill="white", width=2); c.create_text(280, 100, text="Vout", fill="white"); tur = self.opamp_tur.get()
        if tur == 0: c.create_line(20, 80, 100, 80, fill="white", width=2); c.create_rectangle(40, 70, 70, 90, fill="#f5deb3"); c.create_text(55, 60, text="R1", fill="white"); c.create_text(10, 80, text="Vin", fill="white", anchor="e"); c.create_line(80, 80, 80, 30, 240, 30, 240, 100, fill="white", width=2); c.create_rectangle(140, 20, 180, 40, fill="#f5deb3"); c.create_text(160, 10, text="Rf", fill="white"); c.create_line(80, 120, 100, 120, fill="white", width=2); c.create_text(70, 120, text="GND", fill="gray")
        else: c.create_line(20, 120, 100, 120, fill="white", width=2); c.create_text(10, 120, text="Vin", fill="white", anchor="e"); c.create_line(80, 80, 100, 80, fill="white", width=2); c.create_line(80, 80, 80, 180); c.create_rectangle(70, 140, 90, 170, fill="#f5deb3"); c.create_text(60, 155, text="R1", fill="white"); c.create_line(80, 80, 80, 30, 240, 30, 240, 100, fill="white", width=2); c.create_rectangle(140, 20, 180, 40, fill="#f5deb3"); c.create_text(160, 10, text="Rf", fill="white")
    def hesapla_opamp(self):
        try: vin=float(self.ent_op_vin.get()); r1=float(self.ent_op_r1.get()); rf=float(self.ent_op_rf.get()); kazanc = -(rf/r1) if self.opamp_tur.get()==0 else 1+(rf/r1); vout = vin * kazanc; self.lbl_opamp_gain.configure(text=f"{self.T('op_gain')} {kazanc:.2f}"); self.lbl_opamp_vout.configure(text=f"Vout: {vout:.2f} V")
        except: self.lbl_opamp_vout.configure(text=self.T("calc_err"))
    def setup_555_tab(self):
        frame = self.tab_555; self.cv_555 = tk.Canvas(frame, width=300, height=180, bg="#2b2b2b", highlightthickness=0); self.cv_555.pack(pady=10); self.draw_555(); input_frame = ctk.CTkFrame(frame, fg_color="transparent"); input_frame.pack(pady=5); ctk.CTkLabel(input_frame, text="R1 (kΩ):").grid(row=0, column=0); self.ent_555_r1 = ctk.CTkEntry(input_frame, width=80); self.ent_555_r1.grid(row=0, column=1); ctk.CTkLabel(input_frame, text="R2 (kΩ):").grid(row=1, column=0); self.ent_555_r2 = ctk.CTkEntry(input_frame, width=80); self.ent_555_r2.grid(row=1, column=1); ctk.CTkLabel(input_frame, text="C (µF):").grid(row=2, column=0); self.ent_555_c = ctk.CTkEntry(input_frame, width=80); self.ent_555_c.grid(row=2, column=1); ctk.CTkButton(frame, text=self.T("led_calc"), command=self.hesapla_555, fg_color="#2980b9").pack(pady=10); self.lbl_555_freq = ctk.CTkLabel(frame, text=f"{self.T('555_freq')} --- Hz", font=("Roboto", 20, "bold"), text_color="#1abc9c"); self.lbl_555_freq.pack(); self.lbl_555_duty = ctk.CTkLabel(frame, text=f"{self.T('555_duty')} %---", font=("Roboto", 16)); self.lbl_555_duty.pack()
    def draw_555(self): c = self.cv_555; c.delete("all"); c.create_rectangle(100, 30, 200, 150, fill="#333", outline="white"); c.create_text(150, 90, text="NE555", fill="white", font=("Arial", 16, "bold")); c.create_line(100, 50, 60, 50, fill="white", width=2); c.create_text(50, 50, text="Disch", fill="gray", font=("Arial", 8)); c.create_line(100, 100, 60, 100, fill="white", width=2); c.create_text(50, 100, text="Trig", fill="gray", font=("Arial", 8)); c.create_line(200, 90, 240, 90, fill="white", width=2); c.create_text(250, 90, text="Out", fill="#1abc9c")
    def hesapla_555(self):
        try: r1=float(self.ent_555_r1.get())*1000; r2=float(self.ent_555_r2.get())*1000; c=float(self.ent_555_c.get())/1e6; frekans = 1.44 / ((r1 + 2*r2) * c); duty = ((r1 + r2) / (r1 + 2*r2)) * 100; self.lbl_555_freq.configure(text=f"{self.T('555_freq')} {frekans:.2f} Hz"); self.lbl_555_duty.configure(text=f"{self.T('555_duty')} %{duty:.1f}")
        except: self.lbl_555_freq.configure(text=self.T("calc_err"))
    def setup_taban_tab(self):
        frame = self.tab_taban; ctk.CTkLabel(frame, text=self.T("base_input"), font=("Roboto", 16)).pack(pady=20); self.ent_sayi = ctk.CTkEntry(frame, width=200, font=("Arial", 18)); self.ent_sayi.pack(pady=10); self.var_tur = tk.IntVar(value=0); radio_frame = ctk.CTkFrame(frame, fg_color="transparent"); radio_frame.pack(pady=10); ctk.CTkRadioButton(radio_frame, text="Dec", variable=self.var_tur, value=0).pack(side="left", padx=10); ctk.CTkRadioButton(radio_frame, text="Hex", variable=self.var_tur, value=1).pack(side="left", padx=10); ctk.CTkRadioButton(radio_frame, text="Bin", variable=self.var_tur, value=2).pack(side="left", padx=10); ctk.CTkButton(frame, text=self.T("base_conv"), command=self.cevir_taban, fg_color="#34495e").pack(pady=10); result_frame = ctk.CTkFrame(frame); result_frame.pack(pady=20, padx=20, fill="x"); self.out_dec = ctk.CTkEntry(result_frame, font=("Arial", 14)); self.out_dec.pack(pady=5, padx=10, fill="x"); self.out_hex = ctk.CTkEntry(result_frame, font=("Arial", 14)); self.out_hex.pack(pady=5, padx=10, fill="x"); self.out_bin = ctk.CTkEntry(result_frame, font=("Arial", 14)); self.out_bin.pack(pady=5, padx=10, fill="x"); self.out_dec.insert(0, "Dec"); self.out_hex.insert(0, "Hex"); self.out_bin.insert(0, "Bin")
    def cevir_taban(self):
        girdi = self.ent_sayi.get().strip(); tur = self.var_tur.get()
        try:
            val=0; 
            if tur==0: val=int(girdi)
            elif tur==1: val=int(girdi, 16)
            elif tur==2: val=int(girdi, 2)
            self.out_dec.delete(0, tk.END); self.out_hex.delete(0, tk.END); self.out_bin.delete(0, tk.END); self.out_dec.insert(0, f"DEC: {val}"); self.out_hex.insert(0, f"HEX: {hex(val)[2:].upper()}"); self.out_bin.insert(0, f"BIN: {bin(val)[2:]}")
        except: self.out_dec.delete(0, tk.END); self.out_dec.insert(0, self.T("calc_err"))

if __name__ == "__main__":
    app = MuhendisApp()
    app.mainloop()