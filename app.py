from flask import Flask, render_template, send_file, send_from_directory, abort
import os
from igbo_words import word_lists

app = Flask(__name__)


@app.route('/bootstrap/<path:filename>')
def bootstrap_files(filename):
	"""Serve files from the bundled Bootstrap distribution folder."""
	base = os.path.join(app.root_path, 'bootstrap-4.4.1-dist')
	return send_from_directory(base, filename)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files with proper headers for PDFs to display inline."""
    response = send_from_directory(os.path.join(app.root_path, 'static'), filename)
    if filename.endswith('.pdf'):
        response.headers['Content-Disposition'] = 'inline; filename=' + filename
    return response

PDF_DIR = "static/presentations"   # e.g., static/presentations/file1.pdf

@app.route("/pdf/<name>")
def pdf(name):
    filename = f"{name}.pdf"

    # Security check: don't allow path traversal
    if not filename.endswith(".pdf") or "/" in name or "\\" in name:
        abort(404)

    full_path = os.path.join(PDF_DIR, filename)
    if not os.path.exists(full_path):
        abort(404)

    return send_from_directory(
        PDF_DIR,
        filename,
        mimetype="application/pdf",
        as_attachment=False
    )

@app.route('/')
def index():
	return render_template('index.html')

slide_titles = {
	'default': 'Default Slide Deck',
	'ahụike': 'Ahụ Ike',
	'akụkụ_ahụ': 'Akụkụ Ahụ',
	'ezinaulo': 'Ezi N\'Ulọ',
	'mmemme': 'Mmemme Igbo',
    'anụmanụ': 'Anụmanụ'
}

@app.route('/slides')
@app.route('/slides/<pdf_name>')
def slides(pdf_name='default'):
    return render_template('slides.html', pdf_name=pdf_name, slide_title=slide_titles.get(pdf_name, pdf_name), word_list=word_lists[pdf_name] if pdf_name in word_lists else {})

@app.route('/flash_cards')
@app.route('/flash_cards/<pdf_name>')
def flash_cards(pdf_name='default'):
    return render_template('flash_cards.html', pdf_name=pdf_name, slide_title=slide_titles.get(pdf_name, pdf_name), word_list=word_lists[pdf_name] if pdf_name in word_lists else {})

@app.route('/quiz')
@app.route('/quiz/<pdf_name>')
def quiz(pdf_name=None):
    print(word_lists[pdf_name])
    return render_template('quiz.html', pdf_name=pdf_name, word_list=word_lists[pdf_name] if pdf_name in word_lists else {})

if __name__ == '__main__':
	app.run(debug=True)

