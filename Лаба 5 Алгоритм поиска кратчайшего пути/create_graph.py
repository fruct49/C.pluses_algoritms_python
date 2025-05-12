import osmnx as ox

# Загружаем дорожный граф для Алматы
G = ox.graph_from_place('Алматы, Казахстан', network_type='drive')
ox.save_graphml(G, 'almaty_road_network.graphml')
