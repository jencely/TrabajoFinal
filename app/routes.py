from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Meme, Etiqueta
from app.utils import upload_to_s3, get_imagga_tags, generate_filename

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded', 400
            
        file = request.files['file']
        descripcion = request.form.get('descripcion', '')
        usuario = request.form.get('usuario', 'anonymous')
        etiquetas_manual = request.form.get('etiquetas', '').split(',')
        
        # Subir archivo a S3
        filename = generate_filename(file.filename)
        s3_url = upload_to_s3(file, filename)
        
        if not s3_url:
            return 'Error uploading to S3', 500
            
        # Crear registro del meme
        meme_id = Meme.create(descripcion, s3_url, usuario)
        
        # Guardar etiquetas manuales
        for etiqueta in etiquetas_manual:
            if etiqueta.strip():
                Etiqueta.create(meme_id, etiqueta.strip())
        
        # Obtener y guardar etiquetas de Imagga
        imagga_tags = get_imagga_tags(s3_url)
        for tag, confidence in imagga_tags:
            Etiqueta.create(meme_id, tag, confidence)
        
        return redirect(url_for('main.index'))
        
    return render_template('upload.html')

@main.route('/search')
def search():
    query = request.args.get('q', '')
    
    if query:
        memes = Meme.search(query)
        resultados = []
        for meme in memes:
            meme_dict = {
                'id': meme[0],
                'descripcion': meme[1],
                'ruta': meme[2],
                'usuario': meme[3],
                'cargada': meme[4],
                'etiquetas': Etiqueta.get_by_meme_id(meme[0])
            }
            resultados.append(meme_dict)
    else:
        resultados = []
    
    return render_template('search.html', query=query, resultados=resultados)