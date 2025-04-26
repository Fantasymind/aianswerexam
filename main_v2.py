import os
import sys
import requests
import fitz  # PyMuPDF
import argparse
import json


# Mengambil API key dari environment variable
API_KEY = os.getenv('OPENROUTER_API_KEY')


def read_pdf(file_path):
    """Membaca PDF dan mengekstrak teks."""
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None

    text = ""
    for page in doc:
        text += page.get_text()  # Ekstrak teks dari halaman
    return text


def send_to_openrouter(messages):
    """Mengirim pesan ke OpenRouter API dan mendapatkan respons."""
    if not API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"  # Ganti dengan endpoint yang sesuai
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-r1:free",  # Ganti dengan model yang sesuai
        "messages": messages
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

    return response.json()


def main():
    # Menggunakan argparse untuk menangani argumen input
    parser = argparse.ArgumentParser(description='Read a PDF file and chat with its content using OpenRouter API.')
    parser.add_argument('pdf_file', type=str, help='Path to the PDF file to be processed')
    parser.add_argument('-p', '--prompt', type=str, default='', help='Optional chat prompt to send along with the PDF content')
    args = parser.parse_args()

    pdf_file_path = args.pdf_file
    user_prompt = args.prompt.strip()

    if not os.path.isfile(pdf_file_path):
        print(f"Error: File '{pdf_file_path}' does not exist.")
        sys.exit(1)

    pdf_text = read_pdf(pdf_file_path)
    if pdf_text is None:
        sys.exit(1)

    # Prepare messages for chat API
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.append({"role": "user", "content": pdf_text})
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    # Kirim pesan ke OpenRouter
    response = send_to_openrouter(messages)
    if response is None:
        sys.exit(1)

    # Extract assistant message content and print nicely
    try:
        assistant_message = response['choices'][0]['message']['content']
    except (KeyError, IndexError):
        print("Unexpected response format:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        sys.exit(1)

    print("\n=== Jawaban dari OpenRouter ===\n")
    print(assistant_message)
    print("\n=== Selesai ===\n")


if __name__ == "__main__":
    main()
