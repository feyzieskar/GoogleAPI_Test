# AI-Powered IELTS Speaking & Listening Practice Tool

Bu proje, IELTS sınavına hazırlanan kullanıcılar için yapay zeka destekli bir Konuşma ve Dinleme alıştırma aracıdır. Kullanıcılar, yapay zeka ile konuşma pratiği yapabilir ve dinamik olarak üretilen dinleme testlerini çözebilirler.

Bu script, projenin temel teknolojilerini test etmek için oluşturulmuş bir prototiptir.

## Kullanılan Teknolojiler
- **Python 3.9+**
- **Google Cloud Speech-to-Text:** Kullanıcı sesini metne çevirme.
- **Google Cloud Text-to-Speech:** Yapay zeka cevabını seslendirme.
- **Google Gemini API:** Diyalog yönetimi ve içerik üretme.
- **Pydub & PyAudio:** Ses kaydetme ve çalma.

## Kurulum ve Yapılandırma

1.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/SENIN_KULLANICI_ADIN/PROJE_ADIN.git](https://github.com/SENIN_KULLANICI_ADIN/PROJE_ADIN.git)
    cd PROJE_ADIN
    ```

2.  **Sanal Ortam Oluşturun ve Aktif Edin:**
    ```bash
    python -m venv venv
    # Windows için:
    # venv\Scripts\activate
    # macOS/Linux için:
    source venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Kimlik Bilgilerini Ayarlayın (En Önemli Adım):**

    Bu proje, Google Cloud ve Gemini API'lerini kullanır. Bu servisleri kullanabilmek için kimlik bilgilerinizi ayarlamanız gerekmektedir. **Bu dosyaları ve anahtarları asla public repolarda paylaşmayın!**

    * **Google Cloud için:**
        * Bir Google Cloud projesi oluşturun ve `Speech-to-Text` ile `Text-to-Speech` API'lerini etkinleştirin.
        * Bir hizmet hesabı (service account) oluşturun ve bir **JSON anahtar dosyası** indirin.
        * İndirdiğiniz bu dosyayı projenin ana klasörüne `gcp_credentials.json` adıyla kaydedin. (`.gitignore` dosyası bu dosyanın yüklenmesini engelleyecektir).
        * Aşağıdaki ortam değişkenini sisteminize ayarlayın:
            ```bash
            # macOS/Linux için .zshrc veya .bash_profile'a ekleyin:
            export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/gcp_credentials.json"

            # Windows için:
            # Sistem Özellikleri -> Ortam Değişkenleri bölümünden ayarlayın.
            ```

    * **Gemini için:**
        * [Google AI Studio](https://aistudio.google.com/)'dan bir API anahtarı oluşturun.
        * Proje ana klasöründe `.env` adında bir dosya oluşturun ve içine şunu yazın:
            ```
            GEMINI_API_KEY=BURAYA_GEMINI_ANAHTARINIZI_YAPISTIRIN
            ```

## Çalıştırma

Tüm kurulum ve yapılandırma adımlarını tamamladıktan sonra, script'i çalıştırabilirsiniz:
```bash
python ielts_practice_tool.py
```