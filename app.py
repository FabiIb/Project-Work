from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')

# Connessione al db SqLite
def init_db():
    conn = sqlite3.connect('prenotazioni.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS prenotazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        number INTEGER NOT NULL,
        location TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# All'avvio controllo se ci sono prenotazioni
@app.route('/')
def index():
    conn = sqlite3.connect('prenotazioni.db')
    c = conn.cursor()
    c.execute('SELECT * FROM prenotazioni')
    prenotazioni = c.fetchall()
    conn.close()

    if not prenotazioni:
        prenotazione_esistente = False
    else:
        prenotazione_esistente = True

    # Passo il risultato del controllo come argomento
    return render_template('index.html', prenotazione_esistente=prenotazione_esistente)

# Salvataggio della prenotazione
@app.route('/prenotazione', methods=['GET', 'POST'])
def prenotazione():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        number = request.form['number']
        location = request.form['location']

        conn = sqlite3.connect('prenotazioni.db')
        c = conn.cursor()
        c.execute('''
        INSERT INTO prenotazioni (name, email, date, time, number, location)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, date, time, number, location))
        conn.commit()
        conn.close()

        return redirect(url_for('success'))
    return render_template('prenotazione.html')

# In caso di buon fine, renderizza schermata di successo
@app.route('/success')
def success():
    return render_template('success.html')

# Get di tutte le prenotazioni
@app.route('/prenotazioni')
def lista_prenotazioni():
    conn = sqlite3.connect('prenotazioni.db')
    c = conn.cursor()
    c.execute('SELECT * FROM prenotazioni')
    prenotazioni = c.fetchall()
    conn.close()

    # Se non ci sono prenotazioni, lo popolo come lista vuota
    if not prenotazioni:
        prenotazioni = []

    return render_template('lista_prenotazioni.html', prenotazioni=prenotazioni)


# Modifica della prenotazione
@app.route('/modifica/<int:id>', methods=['GET', 'POST'])
def modifica(id):
    conn = sqlite3.connect('prenotazioni.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        number = request.form['number']
        location = request.form['location']
        
        c.execute('''
        UPDATE prenotazioni
        SET name = ?, email = ?, date = ?, time = ?, number = ?, location = ?
        WHERE id = ?
        ''', (name, email, date, time, number, location, id))
        conn.commit()
        conn.close()
        return redirect(url_for('lista_prenotazioni'))
    
    c.execute('SELECT * FROM prenotazioni WHERE id = ?', (id,))
    prenotazione = c.fetchone()
    conn.close()
    
    return render_template('modifica.html', prenotazione=prenotazione)

# Cancellazione prenotazione
@app.route('/cancella/<int:id>', methods=['GET'])
def cancella(id):
    conn = sqlite3.connect('prenotazioni.db')
    c = conn.cursor()
    c.execute('DELETE FROM prenotazioni WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_prenotazioni'))

if __name__ == '__main__':
    init_db()  # Inizializza il db
    app.run(debug=True)
