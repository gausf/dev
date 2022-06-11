import imp
from django.shortcuts import render
from django.http import HttpResponse
from queue import PriorityQueue 


# Create your views here.

GRAPH = {'Arad':{'Zerind':75,'Timisoara':118,'Sibiu':140},
         'Zerind':{'Oradea':71,'Arad':75},
         'Oradea':{'Sibiu',151},
         'Sibiu':{'Rimniciu Vilcea':80,'Fagaras':99,'Arad':140},
         'Fagaras':{'Sibiu':99,'Bucharest':211},
         'Rimniciu Vilcea':{'Pitesti':97,'Craiova':146,'Sibiu':80},
         'Timisoara':{'Lugoj':111,'Arad':118},
         'Lugoj':{'Mehadia':70},
         'Mehadia':{'Lugoj':70,'Dorbeta':75},
         'Dorbeta':{'Mehadia':75,'Craiova':120},
         'Pitesti':{'Craiova':138,'Bucharest':101},
         'Craiova':{'Pitesti':138,'Dorbeta':120,'Rimniciu Vilcea':146},
         'Bucharest':{'Giurgiu':90,'Urziceni':85,'Fagaras':211,'Pitesti':101},
         'Giurgiu': {'Bucharest':90},
         'Urziceni':{'Vaslui':142,'Hirsova':98,'Bucharest':85},
         'Vaslui':{'Lasi':92,'Urziceni':142},
         'Lasi':{'Neamt':87,'Vaslui':92},
         'Neamt':{'Lasi':87},
         'Hirsova':{'Eforie':86,'Urziceni':98},
         'Eforie':{'Hirsova':86},
         }
straight_line = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Fagaras': 176,
        'Rimniciu Vilcea': 193,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Dorbeta': 242,
        'Pitesti': 100,
        'Craiova': 160,
        'Bucharest': 0,
        'Giurgiu': 77,
        'Urziceni': 80,
        'Vaslui': 199,
        'Lasi': 226,
        'Neamt': 234,
        'Hirsova': 151,
        'Eforie': 161
    }
def a_star(source, destination):
     
    p_q,visited = PriorityQueue(),{}
    p_q.put((straight_line[source], 0, source, [source]))
    visited[source] = straight_line[source]
    Queue =[0]*(100)
    e=0
    while not p_q.empty():
        (heuristic, cost, vertex, path) = p_q.get()
        Queue[e] = heuristic ,cost,vertex , path
        print('Queue Status:',heuristic, cost, vertex, path)
        if vertex == destination:
           return  Queue,heuristic, cost, path
        for next_node in GRAPH[vertex].keys():
            current_cost = cost + GRAPH[vertex][next_node]
            heuristic = current_cost + straight_line[next_node]
            if not next_node in visited or visited[next_node] >= heuristic:
                visited[next_node] = heuristic
                p_q.put((heuristic, current_cost, next_node,path + [next_node]))
        e+=1


   

def hot(request):
    cont = None
    Dist = None
    Queue = None
    if 'country'  in request.GET:
        cont = request.GET['country']
    if 'dest' in request.GET:
        Dist = request.GET['dest']
    if cont not in GRAPH or Dist not in GRAPH:       
        heuristic = ""
        cost = ""
        noexs="CITY DOES NOT EXIST."
        return render(request , 'pages/hot.html',{'exc':noexs ,'C':cont,'D':Dist})

    else:
        Queue = [0]*(100)
        Queue,heuristic, cost, optimal_path = a_star(cont,Dist)   
        return render(request , 'pages/hot.html',{'my':'test' ,'C':cont,'D':Dist,'HE':heuristic,'CO':cost,'Q':Queue})

def index(request):  

    newnode = None
    toldnode = None
    g = None
    h = None
    b = None
    c = None
    if 'newnode' in request.GET:
        newnode = request.GET['newnode']
    if 'g' in request.GET:
        g = request.GET['g']
        c=int(g)
    if 'toldnode' in request.GET:
        toldnode = request.GET['toldnode']
    if 'h' in request.GET:
        h = request.GET['h']
        b = int(h)
        if newnode in GRAPH: 
            GRAPH[newnode][toldnode] =b
        else:
            GRAPH[newnode] ={toldnode:b}
    straight_line[newnode]=c
    heuristic ="newnode"
    cost = "oldenode"

    return render(request , 'pages/index.html',{'my':'test' ,'HE':heuristic,'CO':cost,'Q':GRAPH, 'add':straight_line })