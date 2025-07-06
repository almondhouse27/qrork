from flask import Flask, render_template, request, url_for, send_file, flash
from app.qrork import generate


app = Flask(__name__)
app.secret_key = 'fiasco'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        file_name = request.form.get('file_name')
        file_format = request.form.get('file_format')
        theme = request.form.get('theme')
        buf, filename, ext = generate(url, file_name, file_format, theme)

        if buf:
            if ext == 'jpg':
                mimetype = 'image/jpeg'
            elif ext == 'svg':
                mimetype = 'image/svg+xml'
            else:
                mimetype = f'image/{ext}'
            return send_file(
                buf,
                as_attachment=True,
                download_name=filename,
                mimetype=mimetype
            )
        else:
            flash("Error generating QR code.")
            return render_template('index.html')

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, port=5005)