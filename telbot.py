import telebot
import requests

# Fungsi untuk menangani perintah /infografis
# @bot.message_handler(commands=['infografis'])
def send_infografis(message):
    args = message.text.split()[1:]

    # Pastikan input setidaknya memiliki keyword
    if len(args) == 0:
        bot.send_message(message.chat.id, "Silakan masukkan keyword untuk mencari infografis.")
        return
    
    # Keyword: ambil semua argumen sebelum dua argumen terakhir sebagai keyword
    if len(args) >= 3:
        keyword = ' '.join(args[:-2])  # Ambil keyword
        try:
            page = int(args[-2])  # Ambil page dari argumen kedua terakhir
            jumlah_infografis = int(args[-1])  # Ambil jumlah dari argumen terakhir
        except ValueError:
            bot.send_message(message.chat.id, "Pastikan halaman dan jumlah infografis yang dimasukkan berupa angka.")
            return
    elif len(args) == 2:
        keyword = args[0]  # Jika hanya ada satu keyword dan satu angka, ambil keyword dan halaman
        try:
            page = int(args[1])
            jumlah_infografis = 5  # Default jumlah infografis
        except ValueError:
            bot.send_message(message.chat.id, "Pastikan halaman yang dimasukkan berupa angka.")
            return
    else:
        keyword = args[0]  # Jika hanya ada keyword
        page = 1  # Default halaman
        jumlah_infografis = 5  # Default jumlah infografis

    jumlah_infografis = min(jumlah_infografis, 10)  # Batas maksimum 10

    # Set up parameters for the API request
    params = {
        'model': 'infographic',
        'lang': 'ind',
        'domain': '3320',
        'page': page,
        'keyword': keyword,
        'key': API_KEY
    }

    # Make the API request
    response = requests.get(API_URL, params=params)

    # Print the raw response for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

    # Cek status code sebelum memproses
    if response.status_code != 200:
        bot.send_message(message.chat.id, f"Error: Received status code {response.status_code}. Please try again later.")
        return

    # Try parsing the response as JSON
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        bot.send_message(message.chat.id, "Error: Unable to process the response. Please try again later.")
        return

    # Check if data is available and process it
    if data['status'] == 'OK' and 'data' in data and len(data['data']) > 1:
        infografis_list = data['data'][1][:jumlah_infografis]  # Ambil sesuai jumlah yang diminta atau default

        if infografis_list:
            # Untuk setiap infografis, kirim gambar dan link download
            for infografis in infografis_list:
                title = infografis['title']
                img_url = infografis['img']
                download_url = infografis['dl']

                # Kirim thumbnail sebagai gambar dengan HTML
                bot.send_photo(
                    message.chat.id,
                    img_url,
                    caption=f"<b>{title}</b>",
                    parse_mode='HTML'
                )
        else:
            bot.send_message(message.chat.id, 'Tidak ada infografis yang ditemukan.')
    else:
        bot.send_message(message.chat.id, 'Terjadi kesalahan atau tidak ada data yang ditemukan.')

# Fungsi untuk menangani perintah /start
# @bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, (
        "Selamat datang di Bot Infografis!\n"
        "Bot ini menyediakan akses cepat untuk mendapatkan infografis dari berbagai topik.\n"
        "Anda dapat menggunakan perintah berikut:\n"
        "- /infografis <keyword> <halaman> <jumlah>: Mencari infografis berdasarkan keyword.\n"
        "  Jumlah default infografis yang ditampilkan adalah 5, maksimal 10 per permintaan.\n"
        "Untuk bantuan lebih lanjut, Anda bisa menggunakan perintah /help."
    ))

# Fungsi untuk menangani perintah /help
# @bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, (
        "Bantuan Bot Infografis:\n"
        "Bot ini dirancang untuk membantu Anda mencari dan mengakses infografis dengan mudah.\n\n"
        "Cara menggunakan:\n"
        "/infografis <keyword> <halaman> <jumlah>\n"
        "Contoh: /infografis transportasi 1 3\n"
        "Ini akan menampilkan 3 infografis tentang 'transportasi' dari halaman 1.\n\n"
        "Perintah lainnya:\n"
        "/start - Menampilkan pesan sambutan dan informasi dasar tentang bot.\n"
        "/help - Menampilkan informasi bantuan tentang cara menggunakan bot.\n\n"
        "Jika Anda memiliki pertanyaan lebih lanjut, jangan ragu untuk bertanya!"
    ))

# Jalankan bot
bot.polling()