import io
from gtts import gTTS
from flask import Response, request, render_template

def handler(request, context):
    # Nếu GET không có text => trả về giao diện HTML đơn giản
    if request.method == 'GET' and not request.args.get('text'):
        return render_template("TTS.html")

    # Lấy nội dung text từ query hoặc JSON
    text = request.args.get('text', '')
    if not text and request.method == 'POST':
        data = request.get_json(silent=True) or {}
        text = data.get('text', '')

    if not text:
        return Response("Thiếu tham số 'text'", status=400)

    # Sinh ra MP3 từ văn bản
    buf = io.BytesIO()
    tts = gTTS(text=text, lang='vi')
    tts.write_to_fp(buf)
    buf.seek(0)

    return Response(buf.read(), mimetype='audio/mpeg')
