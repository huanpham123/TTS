# app.py
from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import io
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, template_folder='templates')

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix for Vercel proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

@app.route('/')
def index():
    return render_template('TTS.html')

@app.route('/api/tts', methods=['GET', 'POST'])
def text_to_speech():
    try:
        # Nhận văn bản từ cả GET và POST
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                text = data.get('text', '')
            else:
                text = request.form.get('text', '')
        else:
            text = request.args.get('text', '')

        if not text:
            logger.warning("Empty text request")
            return jsonify({'error': 'Missing text parameter'}), 400

        logger.info(f"Processing text: {text[:100]}...")  # Log first 100 chars

        # Tạo file âm thanh với gTTS
        tts = gTTS(text=text, lang='vi', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Trả về file âm thanh
        response = send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )
        
        # Thêm headers cho CORS nếu cần
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        logger.error(f"Error processing TTS request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
