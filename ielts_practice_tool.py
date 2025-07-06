import os
import pyaudio
import wave
import google.generativeai as genai
from google.cloud import speech
from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

# --- GÜVENLİ YAPI: Ortam Değişkenlerinden Ayarları Okuma ---

# Proje klasöründeki .env dosyasını bulur ve içindeki değişkenleri yükler
load_dotenv()

# Ortam değişkenlerinden API anahtarını ve kimlik bilgisi dosya yolunu okur
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# Google Cloud kütüphaneleri 'GOOGLE_APPLICATION_CREDENTIALS' değişkenini otomatik olarak tanır
# Bu yüzden script içinde tekrar ayarlamamıza gerek yok.

# Anahtarların ve yolların ayarlanıp ayarlanmadığını kontrol edelim.
# Bu, başkalarının projenizi kullanmasını kolaylaştırır.
if not GEMINI_API_KEY or not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    print("HATA: Lütfen `.env` dosyasını oluşturup içine gerekli API anahtarını ve dosya yolunu ekleyin.")
    print("Gerekli değişkenler: GEMINI_API_KEY, GOOGLE_APPLICATION_CREDENTIALS")
    exit()  # Değişkenler yoksa programdan çık


def record_audio(file_path="recording.wav", duration=5, rate=16000):
    """Mikrofondan ses kaydeder ve bir WAV dosyasına kaydeder."""
    print(">>> Kayıt başlıyor... 5 saniye konuşun.")
    try:
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=1024)
        frames = [stream.read(1024) for _ in range(0, int(rate / 1024 * duration))]
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print(f">>> Kayıt tamamlandı ve '{file_path}' olarak kaydedildi.")
        return True
    except Exception as e:
        print(f"HATA: Ses kaydı sırasında bir sorun oluştu: {e}")
        return False


def transcribe_audio(file_path="recording.wav"):
    """Bir ses dosyasını metne çevirir."""
    print(">>> Ses metne çevriliyor...")
    try:
        client = speech.SpeechClient()
        with open(file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        response = client.recognize(config=config, audio=audio)

        if not response.results or not response.results[0].alternatives:
            print(">>> Üzgünüm, ses anlaşılamadı.")
            return None

        transcript = response.results[0].alternatives[0].transcript
        print(f">>> Söylediğiniz: '{transcript}'")
        return transcript
    except Exception as e:
        print(f"HATA: Google Speech-to-Text API çağrısında sorun oluştu: {e}")
        return None


def get_gemini_response(prompt):
    """Gemini'ye bir prompt gönderir ve cevabını alır."""
    if not prompt:
        return "Sorry, I didn't catch that. Could you please repeat?"

    print(">>> Gemini cevap düşünüyor...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = f"You are a friendly IELTS examiner. The candidate just said: '{prompt}'. Ask a simple follow-up question."
        response = model.generate_content(full_prompt)

        ai_response = response.text
        print(f">>> Gemini'nin Cevabı: '{ai_response}'")
        return ai_response
    except ValueError:
        print(">>> Gemini Güvenlik Engeli: Cevap üretilemedi. Muhtemelen uygunsuz içerik.")
        return "I'm sorry, I cannot respond to that. Let's try another topic."
    except Exception as e:
        print(f"HATA: Gemini API çağrısında sorun oluştu: {e}")
        return "I'm having trouble connecting right now. Let's pause for a moment."


def synthesize_speech(text, output_file="response.mp3"):
    """Metni ses dosyasına çevirir."""
    print(">>> Cevap seslendiriliyor...")
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code="en-GB", name="en-GB-News-M")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        print(f">>> Seslendirme tamamlandı ve '{output_file}' olarak kaydedildi.")
        return output_file
    except Exception as e:
        print(f"HATA: Google Text-to-Speech API çağrısında sorun oluştu: {e}")
        return None


def main():
    """Ana iş akışını yönetir."""
    audio_file = "user_recording.wav"

    if record_audio(audio_file):
        user_text = transcribe_audio(audio_file)
        ai_text = get_gemini_response(user_text)
        ai_audio_file = synthesize_speech(ai_text)

        if ai_audio_file:
            print(">>> AI'nin cevabı çalınıyor...")
            try:
                sound = AudioSegment.from_mp3(ai_audio_file)
                play(sound)
                print(">>> Pratik döngüsü tamamlandı.")
            except Exception as e:
                print(f"HATA: Ses dosyası çalınamadı: {e}")


if __name__ == "__main__":
    main()