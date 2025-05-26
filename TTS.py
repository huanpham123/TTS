from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import io

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('TTS.html')

@app.route('/api/tts', methods=['POST', 'GET'])
def api_tts():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text','') if data else ''
    else:
        text = request.args.get('text','')
    if not text:
        return jsonify({'error':'Thiếu tham số text'}),400

    tts = gTTS(text=text, lang='vi')
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)

    return send_file(buf,
                     mimetype='audio/mpeg',
                     as_attachment=False,
                     download_name='speech.mp3')

if __name__=='__main__':
    app.run(debug=True)
