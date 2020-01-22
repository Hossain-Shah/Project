locs = [('Omnicom', 'IN', 'New York'),('DDB Needham', 'IN', 'New York'),('Kaplan Thaler Group', 'IN', 'New York'),('BBDO South', 'IN', 'Atlanta'),('Georgia-Pacific', 'IN', 'Atlanta')]
query = [e1 for (e1, rel, e2) in locs if e2=='Atlanta']
print(query)