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
    
if __name__ == '__main__':

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
print "Content-Type:text/html; charset=UTF-8\n"
print "<!doctype html>"
print "<html>"
print "<body>"
print "<h1>Sistema de calculo de menor rota</h1>"
print "Bem vindo ao sistema de calculo de melhor rota de uma sala para a outra!!\n"
print 'Dado o grafo(mapa):<p><img src="https://2.bp.blogspot.com/-UovahJGzt-E/VwqXEvQMaoI/AAAAAAAAAAk/xfN5xEh8yBo1OGrV03patbf-uzcN1G-CQ/s1600/grafo.jpg" alt="grafo" height="196" width="332"></p>'
print "Cadastre seu nome e sua sala e calcule qual a melhor rota da sua sala para as outras onde os outros aulos estão."
import os
def qs(x):
    if os.environ['QUERY_STRING']:
        for t in os.environ['QUERY_STRING'].split("&"):
            if t.split("=")[0]==x:return t.split("=")[1]
    return ''
import cgi
POST=cgi.FieldStorage()
def pv(x):
    if(POST.getvalue(x)):return POST.getvalue(x)
    return ''
from google.appengine.ext import db
class Aluno(db.Model):
    nome=db.ByteStringProperty(default='')
    sala=db.ByteStringProperty(default='')
if pv('nome'):
    if qs('id'):
        reg=db.get(qs('id'))
        reg.nome=pv('nome')
        reg.sala=pv('sala')
        reg.put()
    else:
        Aluno(nome=pv('nome'),sala=pv('sala')).put()
if qs('del'):
    db.delete(qs('del'))
if qs('cal'):
    reg=db.get(qs('cal'))
    print "<hr><form action=index.py?cal="+qs('cal')+" method=post>"
    print "<p>Insira o nome de algum aluno que esta na sala onde voce quer chegar</p>"
    print "De <input name=saida value='"+str(reg.nome)+"'><br>"
    print "Ate <input name=chegada><br>"
    print "<input type=submit value=calcular> <input type=button value=Voltar onclick=\"location.href='index.py';\">"

if pv('saida'):
    if qs('cal'):
        reg=db.get(qs('cal'))
        for obj in Aluno.all():
            if str(obj.nome)==pv('chegada'):
                print "<hr><form method=post>"
                print '<font size="3" color="red">Melhor caminho eh :'+ melhor(str(reg.sala),str(obj.sala))+'</font>'
                break
        else:
            print "<hr><form method=post>"
            print "Aluno de chegada nÃ£o cadastrado"
        print "<input type=button value=Voltar onclick=\"location.href='index.py';\">"


if (pv('nome')or qs('del')):
    print "<a href=index.py>voltar pra listagem</a>"
else:
    print "<table border=1>";
    print "<tr><td>Cadastro de Alunos</td></tr>";
    print "<tr><td>Alunos</td><td>Salas</td></tr>";
    for reg in Aluno.all().order('nome'):
        print "<tr><td>"+str(reg.nome)+"</td><td>"+str(reg.sala)+"</td><td><input type=button value=Alterar onclick=\"location.href='index.py?id="+str(reg.key())+"';\"><input type=button value=Melhor onclick=\"location.href='index.py?cal="+str(reg.key())+"';\"> <input type=button value=Excuir onclick=\"if(confirm('Tem Certeza que deseja excluir esse aluno?'))location.href='index.py?del="+str(reg.key())+"';\"></td></tr>"
    print "</table>";
if (qs('id') and not pv('nome')):
    reg=db.get(qs('id'))
    print "<hr><form action=index.py?id="+qs('id')+" method=post>"
    print "Nome <input name=nome value='"+str(reg.nome)+"'><br>"
    print "Sala <input name=sala value='"+str(reg.sala)+"'><br>"
    print "<input type=submit value=Salvar> <input type=button value=Novo onclick=\"location.href='index.py';\">"
else:
    print "<hr><form method=post>"
    print "Nome <input name=nome><br>"
    print "Sala <input name=sala><br>"
    print "<input type=submit value=Salvar>"
    
    
print "</form><hr>"
print "</body>"
print "</html>"
