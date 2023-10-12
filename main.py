import networkx as nx
import matplotlib.pyplot as matplotlib
import heapq
import osmnx
import folium
import webbrowser
from math import radians, sin, cos, sqrt, atan2


def uniform_cost_search(inici, desti, graf):
    cua_de_prioritat = []
    heapq.heappush(cua_de_prioritat, (0, inici, []))
    explorats = set()

    while cua_de_prioritat:
        cost, node_actual, cami = heapq.heappop(cua_de_prioritat)

        if node_actual == desti:
            resultat = (cami + [node_actual], cost)
            return resultat

        if node_actual in explorats:
            continue
        explorats.add(node_actual)

        for node_adjacent, cost_node_adjacent in graf[node_actual].items():

            if node_adjacent not in explorats:
                heapq.heappush(cua_de_prioritat, (cost + cost_node_adjacent, node_adjacent, cami + [node_actual]))

    return


def imprimir_llista_adjacencia(graf):
    print("\nLlista d'adjacència del graf:\n ")

    for node in graf:
        print(str(node) + ": ", end="")

        for node_adjacent, distancia in graf[node].items():
            print(str(node_adjacent) + " (" + str(distancia) + ") ", end="")
        print()


def clicar_mapa_interactiu(graf_omsnx):
    gdf_nodes, gdf_arestes = osmnx.graph_to_gdfs(graf_omsnx)

    centre_graf_lon, centre_graf_lat = gdf_nodes.unary_union.centroid.coords[0]

    mapa = folium.Map(location=[centre_graf_lat, centre_graf_lon], zoom_start=13)
    mapa.add_child(folium.ClickForMarker(popup='Agregar marcador'))
    mapa.add_child(folium.LatLngPopup())

    mapa.save('m.html')
    webbrowser.open('m.html', new=2)


def calcular_distancia(coordenada1, coordenada2):
    radi_terra = 6371

    lat1, lon1 = coordenada1
    lat2, lon2 = coordenada2

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    diferencia_lon = lon2 - lon1
    diferencia_lat = lat2 - lat1

    a = sin(diferencia_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diferencia_lon / 2) ** 2
    b = 2 * atan2(sqrt(a), sqrt(1 - a))
    distancia = radi_terra * b

    return distancia


def trobar_coordenada_mes_propera(coordenada, llista):
    distancia_minima = float('inf')
    coordenada_mes_propera = None

    for tuples_coordenades in llista:
        distancia = calcular_distancia(coordenada, tuples_coordenades)
        if distancia < distancia_minima:
            distancia_minima = distancia
            coordenada_mes_propera = tuples_coordenades

    return coordenada_mes_propera


def trobar_node_per_coordenades(graf_osmnx, coordenades):
    latitud, longitud = coordenades
    for node, coordenades in graf_osmnx.nodes(data=True):
        if coordenades['y'] == latitud and coordenades['x'] == longitud:
            return node
    return None


def imprimir_mapa_interactiu(graf_omsnx, node_inici, node_desti, cami_nodes):
    gdf_nodes, gdf_arestes = osmnx.graph_to_gdfs(graf_omsnx)

    centre_graf_lon, centre_graf_lat = gdf_nodes.unary_union.centroid.coords[0]

    mapa = folium.Map(location=[centre_graf_lat, centre_graf_lon], zoom_start=13)

    lat_node_inici, lon_node_inici = graf_omsnx.nodes[node_inici]['y'], graf_omsnx.nodes[node_inici]['x']
    lat_node_desti, lon_node_desti = graf_omsnx.nodes[node_desti]['y'], graf_omsnx.nodes[node_desti]['x']
    folium.Marker(location=[round(lat_node_inici, 4), round(lon_node_inici, 4)],
                  icon=folium.Icon(color='green')).add_to(mapa)
    folium.Marker(location=[round(lat_node_desti, 4), round(lon_node_desti, 4)],
                  icon=folium.Icon(color='red')).add_to(mapa)

    cami_arestes = list(zip(cami_nodes, cami_nodes[1:]))

    for aresta in cami_arestes:
        node_actual, seguent_node = aresta
        lat_node_actual, lon_node_actual = graf_omsnx.nodes[node_actual]['y'], graf_omsnx.nodes[node_actual]['x']
        lat_node_seguent, lon_node_seguent = graf_omsnx.nodes[seguent_node]['y'], \
            graf_omsnx.nodes[seguent_node]['x']
        folium.PolyLine(locations=[(lat_node_actual, lon_node_actual), (lat_node_seguent, lon_node_seguent)],
                        color='blue').add_to(mapa)

    mapa.save('mapa.html')
    webbrowser.open('mapa.html', new=2)


def llista_tuples_coordenades(graf_omsnx):
    llista_coordenades = []
    for node, coordenades in graf_omsnx.nodes(data=True):
        latitud = coordenades['y']
        longitud = coordenades['x']
        tupla_coordenades = (latitud, longitud)
        llista_coordenades.append(tupla_coordenades)
    return llista_coordenades


def de_osmnx_a_diccionari(graf_osmnx):
    diccionari_adjacencia = {}

    for node in graf_osmnx.nodes():
        nodes_adjacents = {}

        for node_adjacent in graf_osmnx.neighbors(node):

            for node_x, node_y, data in graf_osmnx.edges(data=True):

                if (node_x == node and node_y == node_adjacent) or (
                        node_x == node_adjacent and node_y == node):
                    longitud = int(round(data['length']))
                    nodes_adjacents[node_adjacent] = longitud
                    break
        diccionari_adjacencia[node] = nodes_adjacents
    return diccionari_adjacencia


def de_diccionari_a_networkx(graf_diccionari):
    graf = nx.Graph()

    for node in graf_diccionari:
        graf.add_node(node)

    for node, nodes_adjacents in graf_diccionari.items():

        for node_adjacent in nodes_adjacents:

            if not graf.has_edge(node, node_adjacent):
                graf.add_edge(node, node_adjacent)
    return graf


def imprimir_imatge_graf_simple(graf_networkx):
    nx.draw(graf_networkx, with_labels=True)
    labels = nx.get_edge_attributes(graf_networkx, 'weight')
    nx.draw_networkx_edge_labels(graf_networkx, pos=nx.spring_layout(graf_networkx), edge_labels=labels)
    matplotlib.show()
