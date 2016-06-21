#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import datetime
import urllib
import sys
import hashlib
from google.appengine.ext import db
from google.appengine.api import users

class Usuario(db.Model):
    usuario=db.StringProperty(default='')
    senha=db.StringProperty(default='')

def UsuarioKey():
    return db.Key.from_path('Usuario','defaultusuario')

def UsuarioById(id):
    return Usuario.get_by_id(id,parent=UsuarioKey())


#PAGES#################################################
class LoginActivity(webapp2.RequestHandler):
    def get(self):
	self.response.write ("<html>"
                                    "<body>"
					'<body bgcolor="#B0F9EA">'
                                        '<font face="verdana" color="green">'
                                        '<center><p><img src="https://4.bp.blogspot.com/-Mb01oiIvCmQ/V2apaVRDxHI/AAAAAAAAACw/InWzrXaW_cY8IyEuUXy6Ak3Dbp05dTnDwCLcB/s1600/less%2Bwork.jpg" alt="logo" height="95" width="360"></p><center>'
                                        '<form action="/Home" method="POST">'
                                                            'Usuario:<input type=text name=usuario value=""/>'
                                                            'Senha<input type="password" name=senha value="">'
                                                            '<br><button >Login</button>'
                                                            

                                        '</form>'

                                        #'<button onclick="myFunction()">Try it</button>'
					'<p><a href="/AddUsuario">Sing in</a></p>'

                                        #'<p id="demo"></p>'

                                        #'<script>'
                                        #'function myFunction() {'
                                            #'var x = document.getElementById("myPsw").value;'
                                            #'document.getElementById("demo").innerHTML = x;'
                                        #'}'
										
                                        #'</script>'
										
				    '</body>'
				'</html>')								
	

        #Alunos = db.GqlQuery("select * from Usuario")

        #self.response.write('<ul>')

        #self.response.write('<p>Usuarios Cadastrados</p>')
        #self.response.write("")
        #for post in Alunos:
            #self.response.write('<li>{nome}</li>'
                #.format(nome=post.usuario,key=post.key().id()))

        #self.response.write('</ul>')
        #self.response.write('</body></html>')
    def post(self):
        usuario = self.request.get('usuario')
        senha =self.request.get('senha')
        if checkUsuario(usuario):
            self.response.write('<script>alert("Usuario nao cadastrado!");</script>')
        else:
            usuarios=db.GqlQuery("select * from Usuario")
            for post in usuarios:
                if post.usuario==usuario:
                    if post.senha==senha:
                        self.redirect('/Home')
                    else:
                        self.response.write('<script>alert("Senha incorreta!");</script>')

                
            
def checkUsuario(usuario):
    usuarios=db.GqlQuery("select * from Usuario")
    for post in usuarios:
        if post.usuario==usuario:
            return False
        else:
            continue
    else:
        return True

def criptografia(senha):
    m=hashlib.md5()
    m.update(str(senha))
    senha_criptografada=str(m.digest())
    return str(senha_criptografada)
    
class AddUsuario(webapp2.RequestHandler):
    def get(self):
        self.response.write(
            '<html>'
                '<body>'
                '<body bgcolor="#B0F9EA">'
                '<font face="verdana" color="green">'
				'<form action="/AddUsuario" method="POST">'
                    'Nome de usuario:<input type=text name=usuario value=""/>'
                    '<br>Senha:<input type="password" name=senha value=""/>'
                    '<br>Repita a senha:<input type="password" name=resenha value=""/>'
                    '<br><input type=submit text="Salvar"/>'
                '</form>'
                '</body>'
            '</html>')
    def post(self):
        usuario = self.request.get('usuario')
        senha =self.request.get('senha')
        resenha=self.request.get('resenha')
        newusuario = Usuario(parent=UsuarioKey())
        
	if senha!=resenha:
            self.response.write('<script>alert("Senhas nao conhecidem!");</script>')
        else:
            if checkUsuario(usuario):
                newusuario.usuario = usuario
                newusuario.senha = senha
                newusuario.put()
                self.redirect('/')
            else:
                self.response.write('<script>alert("Nome de usuario jah cadastrado!");</script>')
            
class Home(webapp2.RequestHandler):
    def get(self):
       self.response.write(
            '<html>'
                '<body>'
                '<body bgcolor="#B0F9EA">'
                '<font face="verdana" color="green">'
                '<p><h1>Bem Vindo!</h1><p>'
                '</body>'
            '</html>'
            )
    def post(self):
        usuario = self.request.get('usuario')
        senha =self.request.get('senha')
        if checkUsuario(usuario):
            self.response.write('<script>alert("Usuario nao cadastrado!");</script>')
        else:
            usuarios=db.GqlQuery("select * from Usuario")
            for post in usuarios:
                if post.usuario==usuario:
                    if post.senha==senha:
                        self.redirect('/Home')
                    else:
                        self.response.write('<script>alert("Senha incorreta!");</script>')


 

class DeleteAluno(webapp2.RequestHandler):
    def post(self):
        id = int(self.request.get('id'))
        newaluno = AlunoById(id)
        newaluno.delete()
        self.redirect('/')


            
app = webapp2.WSGIApplication([('/', LoginActivity),
                                ('/AddUsuario',AddUsuario),
                                ('/Home',Home),
                                ('/DeleteAluno',DeleteAluno)],
                              debug=True)
