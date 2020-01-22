from pattern.graph import Graph
g = Graph()
g.add_edge('doll', 'toy', type='is-a')
g.add_edge('silent', 'doll', type='is-property-of')
g.add_edge('doll', 'girl', type='is-related-to')
node = g['doll']
print(node.id)
print(node.links)
