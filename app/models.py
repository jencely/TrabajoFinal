import uuid
from datetime import datetime
import psycopg2
from config import Config
import requests

def get_db_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Crear tabla de memes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS memes (
            id UUID PRIMARY KEY,
            descripcion TEXT NOT NULL,
            ruta TEXT NOT NULL,
            usuario TEXT NOT NULL,
            cargada TIMESTAMP NOT NULL
        )
    ''')
    
    # Crear tabla de etiquetas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS etiquetas (
            id UUID PRIMARY KEY,
            meme_id UUID REFERENCES memes(id),
            etiqueta TEXT NOT NULL,
            confianza FLOAT
        )
    ''')
    
    conn.commit()
    cur.close()
    conn.close()

class Meme:
    @staticmethod
    def create(descripcion, ruta, usuario):
        conn = get_db_connection()
        cur = conn.cursor()
        
        id = str(uuid.uuid4())  
        cargada = datetime.now()
        
        cur.execute('''
            INSERT INTO memes (id, descripcion, ruta, usuario, cargada)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        ''', (id, descripcion, ruta, usuario, cargada))
        
        conn.commit()
        cur.close()
        conn.close()
        return str(id)
    
    @staticmethod
    def get_by_id(meme_id):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM memes WHERE id = %s', (meme_id,))
        meme = cur.fetchone()
        
        cur.close()
        conn.close()
        return meme

    @staticmethod
    def search(query):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('''
            SELECT DISTINCT m.* FROM memes m
            LEFT JOIN etiquetas e ON m.id = e.meme_id
            WHERE m.descripcion ILIKE %s
            OR e.etiqueta ILIKE %s
        ''', (f'%{query}%', f'%{query}%'))
        
        memes = cur.fetchall()
        cur.close()
        conn.close()
        return memes

class Etiqueta:
    @staticmethod
    def create(meme_id, etiqueta, confianza=None):
        conn = get_db_connection()
        cur = conn.cursor()
        
        id = str(uuid.uuid4())  
        
        cur.execute('''
            INSERT INTO etiquetas (id, meme_id, etiqueta, confianza)
            VALUES (%s, %s, %s, %s)
        ''', (id, meme_id, etiqueta, confianza))
        
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_meme_id(meme_id):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM etiquetas WHERE meme_id = %s', (meme_id,))
        etiquetas = cur.fetchall()
        
        cur.close()
        conn.close()
        return etiquetas