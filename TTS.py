# app.py
from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import io
import logging
from flask_cors import CORS

app = Flask(__name__, template_folder='templates')
CORS(app)  # Mở CORS cho mọi nguồn

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('TTS.html')

@app.route('/api/tts', methods=['GET', 'POST'])
def text_to_speech():
    """
    Nhận text qua GET hoặc POST, trả về audio/mpeg.
    GET:  /api/tts?text=...
    POST: JSON {"text": "..."} hoặc form-data field "text"
    """
    try:
        # Lấy text đầu vào
        if request.method == 'POST':
            if request.is_json:
                text = request.get_json().get('text', '')
            else:
                text = request.form.get('text', '')
        else:
            text = request.args.get('text', '')

        if not text:
            return jsonify({'error': 'Missing text parameter'}), 400

        logger.info(f"TTS text: {text[:50]}...")

        # Tạo mp3 với gTTS
        tts = gTTS(text=text, lang='vi', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)

        # Trả về file MP3
        return send_file(
            buf,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )

    except Exception as e:
        logger.exception("Error in TTS")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Host 0.0.0.0 để ESP truy cập được, debug=False khi deploy
    app.run(host='0.0.0.0', port=5000, debug=False)
