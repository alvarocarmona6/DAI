from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,session,url_for, escape, jsonify,request
from pymongo import MongoClient
import re
import shelve
app = Flask(__name__)
app.secret_key = 'alvaro'

pag=1
@app.after_request
def save_history(response):
        if 'usuario' in session and request.method == "GET" and response.mimetype == "text/html":
                        session['urls'].append(request.path)
                        session.modified = True
                        if(len(session['urls'])) > 3:
                                session['urls'].pop(0)
        return response

@app.route('/')
def plantilla():
        return render_template('plantilla_padre.html')

@app.route('/hijo1')
def plantilla_hijo1():
        return render_template('hijo1.html')

@app.route('/hijo2')
def plantilla_hijo2():
        return render_template('hijo2.html')
@app.route('/hijo3')
def plantilla_hijo3():
        return render_template('hijo3.html')
@app.route('/hijo4')
def plantilla_hijo4():
        return render_template('hijo4.html')


@app.route('/crearusuario',  methods = ['GET', 'POST'])
def plantilla_crear():
        if request.method == 'POST':
               
                
                db = shelve.open('datos.db')
                db[request.form['usuario']] = {'nombre':request.form['usuario'],'clave':request.form['pwd'],'direccion':request.form['direccion']}
                
                
                db.close()
        
        return render_template('crearusuario.html')



@app.route('/verusuario',  methods = ['GET', 'POST'])
def ver():
        db = shelve.open('datos.db')
        datos = db[session['usuario']]
        db.close()
        return render_template('visualizarusuarios.html', title = 'Nombre: ' + datos['nombre'], dire =  'Direccion: ' + datos['direccion'])

@app.route("/login", methods = ['GET', 'POST'])
def login():

        db = shelve.open('datos.db')
        username = request.form['usuario']
        
        if request.method == 'POST' and username in db and db[username]['clave'] == request.form['pwd'] :
                session['usuario'] = request.form['usuario']
                session['urls'] = []

        db.close()  
        return render_template('plantilla_padre.html')

@app.route('/logout')
def logout():
   session.pop('usuario', 'pwd')
   session['urls'] = []
   return render_template('plantilla_padre.html')


@app.route('/editarusuario', methods = ['GET', 'POST'])
def editar():
        db = shelve.open('datos.db',writeback=True)
        datos = db[session['usuario']]
        if request.method == 'POST' :
                datos['nombre']=request.form['usuario']
                datos['clave']=request.form['pwd']
                datos['direccion']=request.form['direccion']
        db.close()
        return render_template('editarusuario.html')

@app.route('/busquedarestaurante', methods = ['GET', 'POST'])
def busqueda():

        numero_restaurante_pagina = 100
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test']
        if request.method == 'POST':

                
                resultado = db.restaurants.find_one( {"borough": request.form["barrio"]}  )
                restaurante = str(resultado)
                if restaurante =="None":
                        restaurante = "No hay restaurante"
                        nada =1
                else:
                        patron = re.compile("'name':\s'(.*?)'")
                        #patron = re.compile("u'name':\su'(.*?)'")
                        filtro = patron.findall(str(resultado))
                        restaurante = str(filtro)
                      
                return render_template('busquedarestaurante.html', error=restaurante)
 
        else:
               
                offset = (1-1)*numero_restaurante_pagina
                resultado = db.restaurants.find().skip(offset).limit(numero_restaurante_pagina)
                
                restaurante = ""
                while(resultado.alive):
                        try:
                                restaurante=restaurante +str(resultado.next())
                        except StopIteration:
                                restaurante = "No hay resultado"
                                return render_template('busquedarestaurante.html',error=restaurante)

                patron = re.compile("'name':\s'(.*?)'")
                #patron = re.compile("u'name':\su'(.*?)'")
                filtro = patron.findall(str(restaurante))
              
                return render_template('busquedarestaurante.html', Restaurante=filtro)


@app.route('/get_mas')
def responde():
        paginas = 100
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test']
        global pag
        pag=pag+1
		        
        offset = (pag-1)*paginas
        resultado=db.restaurants.find().skip(offset).limit(paginas)
        restaurante=""
        while(resultado.alive):
                try:
                        restaurante=restaurante+str(resultado.next())
                except StopIteration:
                        restaurante="No hay resultados"
                        return render_template('busquedarestaurante.html',error = restaurante)

        patron = re.compile("'name':\s'(.*?)'")
        filtro=patron.findall(str(restaurante))

        return jsonify({'filtro':filtro})    # podría ser string o HTML


@app.route('/get_menos')
def responde2():
        paginas = 100
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test']
        global pag
        if pag >1:
                pag=pag-1
		        
        offset = (pag-1)*paginas
        resultado=db.restaurants.find().skip(offset).limit(paginas)
        restaurante=""
        while(resultado.alive):
                try:
                        restaurante=restaurante+str(resultado.next())
                except StopIteration:
                        restaurante="No hay resultados"
                        return render_template('busquedarestaurante.html',error = restaurante)

        patron = re.compile("'name':\s'(.*?)'")
        filtro=patron.findall(str(restaurante))

        return jsonify({'filtro':filtro})    # podría ser string o HTML



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
