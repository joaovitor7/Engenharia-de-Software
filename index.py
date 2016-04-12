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
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited        
        self.visited = False  
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()  

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start, target):
    
    # Set the distance for the start node to zero 
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance 
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacet:n
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)
            
            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                
        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)
    
g = Graph()

g.add_vertex('a')
g.add_vertex('b')
g.add_vertex('c')
g.add_vertex('d')
g.add_vertex('e')
    

g.add_edge('a','b',1)
g.add_edge('a','c',2)
g.add_edge('a','e',5)
g.add_edge('b','d',4)
g.add_edge('c','e',2)
g.add_edge('d','e',1)

def melhor(a,e):
    dijkstra(g, g.get_vertex(a), g.get_vertex(e)) 

    target = g.get_vertex(e)
    path = [target.get_id()]
    shortest(target, path)
    result= path[::-1]
    melhor_caminho=''
    for i in result:
        melhor_caminho+=' '+i
    return melhor_caminho

from google.appengine.ext import db
from google.appengine.api import users

class Aluno(db.Model):
    nome=db.StringProperty(default='')
    sala=db.StringProperty(default='')

def AlunoKey():
    return db.Key.from_path('Aluno','defaultaluno')

def AlunoById(id):
    return Aluno.get_by_id(id,parent=AlunoKey())


#PAGES#################################################
class MainPage(webapp2.RequestHandler):
    def get(self):
	self.response.write ("<html>"
                                    "<body>"
					"<h1>Sistema de calculo de menor rota</h1>"
					"Bem vindo ao sistema de calculo de melhor rota de uma sala para a outra!!\n"
					'Dado o grafo(mapa):<p><img src="https://2.bp.blogspot.com/-UovahJGzt-E/VwqXEvQMaoI/AAAAAAAAAAk/xfN5xEh8yBo1OGrV03patbf-uzcN1G-CQ/s1600/grafo.jpg" alt="grafo" height="196" width="332"></p>'
					"<p>Cadastre seu nome e sua sala e calcule qual a melhor rota da sua sala para as outras onde os outros aulos estao</p>."
				    '</body>'
				'</html>')									
	self.response.write('<html>'
                                    '<body>'
                                        '<a href="/AddAluno">Adicionar Aluno</a>')

        Alunos = db.GqlQuery("select * from Aluno order by sala desc limit 10")

        self.response.write('<ul>')

        self.response.write('<p>Alunos Cadastrados</p>')
        self.response.write("")
        for post in Alunos:
            self.response.write('<li>{nome} da sala : {sala} ' \
            '<a href="/EditAluno?id={key}">Editar Aluno</a><a href="/CalcularMelhorCaminho?id={key}"> Calcular melhor rota</a></li>'
                .format(nome=post.nome,sala=post.sala,key=post.key().id()))

        self.response.write('</ul>')
        self.response.write('</body></html>')


class AddAluno(webapp2.RequestHandler):
    def get(self):
        self.response.write(
            '<html>'
                '<body>'
                '<form action="/AddAluno" method="POST">'
                    'Aluno:<input type=text name=aluno value=""/>'
                    '<br>Sala:<input type=text name=sala value=""/>'
                    '<br><input type=submit text="Salvar"/>'
                '</form>'
                '</body>'
            '</html>')
    def post(self):
        nome = self.request.get('aluno')
        sala = self.request.get('sala')
        newpost = Aluno(parent=AlunoKey())
        newpost.nome = nome
        newpost.sala = sala
        newpost.put()
        self.redirect('/')

class EditAluno(webapp2.RequestHandler):
    def get(self):
        id = int(self.request.get('id'))
        newaluno = AlunoById(id)
        self.response.write(
            '<html>'
                '<body>'
                '<form action="/EditAluno" method="POST">'
                    '<input type="hidden" value="{id}" name="id">'
                    'Aluno:<input type=text name=aluno value="{aluno}"/>'
                    '<br>Sala:<input type=text name=sala value="{sala}"/>'
                    '<br><input type=submit value="Salvar"/>'
                '</form>'
                '<form action="/DeleteAluno" method="POST">'
                    '<input type="hidden" value="{id}" name="id">'
                    '<br><input type=submit value="delete"/>'
                '</form>'
                '</body>'
            '</html>'
            .format(aluno=newaluno.nome,
                sala=newaluno.sala,id=newaluno.key().id()))
    def post(self):
        aluno = self.request.get('aluno')
        sala = self.request.get('sala')
        id = int(self.request.get('id'))
        newaluno = AlunoById(id)
        newaluno.nome = aluno
        newaluno.sala = sala
        newaluno.put()
        self.redirect('/')

class DeleteAluno(webapp2.RequestHandler):
    def post(self):
        id = int(self.request.get('id'))
        newaluno = AlunoById(id)
        newaluno.delete()
        self.redirect('/')

class CalcularMelhorCaminho(webapp2.RequestHandler):
    def get(self):
        id = long(self.request.get('id'))
        newaluno = AlunoById(id)
        self.response.write(
            '<html>'
                '<body>'
                '<form action="/CalcularMelhorCaminho" method="POST">'
                    '<input type="hidden" value="{id}" name="id">'
                    'Do Aluno:<input type=text name=saida value="{aluno}"/>'
                    '<br>Ate o Aluno:<input type=text name=chegada value=""/>'
                    '<br><input type=submit value="Calcular"/>'
                '</form>'
                
                '</body>'
            '</html>'
            .format(aluno=newaluno.nome,id=newaluno.key().id()))
    def post(self):
        id = int(self.request.get('id'))
        aluno=AlunoById(id)
        saida=aluno.sala
        aluno_2=self.request.get('chegada')
        for obj in Aluno.all():
            if str(obj.nome)==aluno_2:
                self.response.write('<font size="3" color="red">Melhor caminho eh :'+ melhor(str(saida),str(obj.sala))+'</font>')
                break
        else:
            self.response.write( "Aluno de chegada nao cadastrado")
            
app = webapp2.WSGIApplication([('/', MainPage),
                                ('/AddAluno',AddAluno),
                                ('/EditAluno',EditAluno),
                                ('/DeleteAluno',DeleteAluno),
                                ('/CalcularMelhorCaminho',CalcularMelhorCaminho)],
                              debug=True)
