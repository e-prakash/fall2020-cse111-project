from .Graph import Graph
from .Manage import Manage
from .Options import Options
from .Report import Report

class QueryBuilder(object):

        Graph = Graph
        Manage = Manage
        Options = Options
        Report = Report

if __name__ == "__main__":

        print(QueryBuilder.Graph.getEarthquakeNuclear([1900, 2030], ['nuclear explosion', 'earthquake'], [0, 10.0], None, [1, 6255147], [1814991, 1168579], [0, 50000], ['H', 'N'], 0, 0));