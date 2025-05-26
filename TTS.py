from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import io
from flask_cors import CORS

app = Flask(__name__, template_folder='../templates')
CORS(app)

@app.route('/', methods=['GET'])
def index():
    # Khi truy cập root, redirect về trang HTML
    return render_template('TTS.html')

@app.route('/api/tts', methods=['GET', 'POST'])
def tts():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        text = data.get('text') or request.form.get('text', '')
    else:
        text = request.args.get('text', '')
    if not text:
        return jsonify({'error': 'Missing text parameter'}), 400

    # Sinh MP3
    buf = io.BytesIO()
    tts = gTTS(text=text, lang='vi', slow=False)
    tts.write_to_fp(buf)
    buf.seek(0)
    return send_file(
        buf,
        mimetype='audio/mpeg',
        as_attachment=False,
        download_name='speech.mp3'
    )

# Entry point cho Vercel
def handler(request, context):
    return app(request.environ, start_response=context.start_response)
