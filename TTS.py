from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import io
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, template_folder='templates')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fix for Vercel proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# CORS middleware
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tts', methods=['GET'])
def text_to_speech():
    try:
        text = request.args.get('text', '').strip()
        
        if not text:
            logger.warning("Empty text request")
            return jsonify({'error': 'Missing text parameter'}), 400
        
        if len(text) > 500:
            text = text[:500]  # Limit to 500 characters
            logger.warning("Text truncated to 500 chars")

        logger.info(f"Processing TTS for text: {text[:50]}...")
        
        # Generate speech
        tts = gTTS(text=text, lang='vi', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        logger.info("Audio generated successfully")
        
        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='speech.mp3'
        )
        
    except Exception as e:
        logger.error(f"Error in TTS generation: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Required for Vercel
application = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
