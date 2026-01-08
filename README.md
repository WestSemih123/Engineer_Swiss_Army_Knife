# 🛠️ Mühendislik Asistanı (Engineering Assistant)

Python ve CustomTkinter kullanılarak geliştirilmiş, Elektrik-Elektronik ve Bilgisayar Mühendisliği öğrencileri ile profesyonelleri için kapsamlı, hepsi bir arada hesaplama ve simülasyon aracı.

---

## 🌟 Özellikler

Bu proje, mühendislik hesaplamalarını tek bir arayüzde toplayan **15 farklı modül** içerir:

- **Akıllı Bilimsel Hesap Makinesi**: Otomatik parantez tamamlama, derece/radyan dönüşümü, trigonometrik ve logaritmik fonksiyonlar.  
- **Direnç Renk Hesaplayıcı**: 4 ve 5 bantlı dirençlerin değerini ve toleransını okur.  
- **SMD Kod Çözücü**: 103, 4R7, 222 gibi SMD direnç kodlarını çözer.  
- **Kapasitör Kod Çözücü**: 104, 22p gibi mercimek kondansatör kodlarını pF, nF, µF cinsine çevirir.  
- **LED Direnç Hesaplayıcı**: LED'i güvenle çalıştırmak için gereken ön direnci ve harcanan gücü (Watt) hesaplar.  
- **Gerilim Bölücü (Voltage Divider)**: İki direnç ile oluşturulan devrenin çıkış voltajını hesaplar.  
- **Op-Amp Hesaplayıcı**: Eviren (Inverting) ve Evirmeyen (Non-Inverting) yükselteçlerin kazancını ve çıkış voltajını hesaplar.  
- **NE555 Zamanlayıcı**: Astable modda çalışan 555 entegresinin frekansını ve görev döngüsü (duty cycle) oranını hesaplar.  
- **Pasif Filtre Tasarımcısı**: RC (Alçak Geçiren) ve CR (Yüksek Geçiren) filtrelerin kesim frekansını (Cut-off Frequency) bulur.  
- **RF Güç Dönüştürücü**: Watt, Miliwatt ve dBm birimleri arasında dönüşüm yapar.  
- **PCB Yol Genişliği (Trace Width)**: IPC-2221 standartlarına göre, belirli bir akımı taşımak için gereken bakır yol genişliğini hesaplar.  
- **Mantık Kapıları (Logic Gates)**: AND, OR, NOT, NAND, NOR, XOR, XNOR kapılarının doğruluk tablosunu interaktif olarak simüle eder.  
- **Isı Emici (Heatsink) Hesaplayıcı**: Güç elektroniği bileşenleri için gereken termal direnci (Rth) hesaplar.  
- **Batarya Ömrü Hesaplayıcı**: Bir cihazın pil kapasitesine ve çektiği akıma göre ne kadar süre çalışacağını tahmin eder.  
- **AWG Kablo Çevirici**: AWG (American Wire Gauge) kablo numaralarını mm çapına ve kesit alanına çevirir, taşıyabileceği tahmini akımı gösterir.

---

## 🚀 Kurulum

Projeyi bilgisayarınıza indirin:

```bash
git clone https://github.com/KULLANICI_ADINIZ/Muhendislik-Asistani.git
cd Muhendislik-Asistani
Gerekli kütüphaneyi yükleyin:

bash
Copy code
pip install customtkinter
Uygulamayı çalıştırın:

bash
Copy code
python muhendis_proje.py
📦 .EXE Olarak Derleme (Windows)
Python yüklü olmayan bilgisayarlarda çalıştırmak için projeyi tek bir .exe dosyasına dönüştürebilirsiniz:

PyInstaller'ı yükleyin:

bash
Copy code
pip install pyinstaller
Derleme komutunu çalıştırın:

bash
Copy code
pyinstaller --noconsole --onefile muhendis_proje.py
dist klasöründe oluşan .exe dosyasını kullanabilirsiniz.

🤝 Katkıda Bulunma
Bu depoyu Fork'layın.

Yeni bir özellik dalı (branch) oluşturun:

bash
Copy code
git checkout -b yeni-ozellik
Değişikliklerinizi yapın ve commit’leyin:

bash
Copy code
git commit -m "Yeni özellik eklendi"
Dalınızı Push’layın:

bash
Copy code
git push origin yeni-ozellik
Bir Pull Request oluşturun.

📄 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için LICENSE dosyasına bakabilirsiniz.
