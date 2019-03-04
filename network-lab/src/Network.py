
import json
import networkx as nx

class Network(object):
    
    def __init__(self,mdata,ndata):
        self.nodes = ndata['nodes']
        self.links = ndata['links']
        self.type = mdata['type']
        self.color_dict = mdata['color_dict']
        self.count = []
        self.G = nx.DiGraph()
        
   
    '''=========Get basic netywork========='''
    def get_network(self):
        for item in self.nodes:
            self.G.add_node(item['id'],typ = item['type'],\
                           name = item['name'],icolor = item['icolor'])
        for item in self.links:
            self.G.add_edge(item['source'],item['target'],\
                            weight = item['value']) 
    
         
    '''get types count of nodes for legend'''
    def get_type_count(self):
        for typ in self.type:
            typ_cnt = 0
            for nds in self.nodes:
                if nds["type"]==typ:
                    typ_cnt = typ_cnt+1
            if typ_cnt !=0:        
                self.count.append({"type":typ,\
                          "icolor":self.color_dict[typ],\
                          "icount":typ_cnt})
        return self.count
    
    def get_degree(self):
        self.get_network()
        new_nodes = []
        for node in self.nodes:
            if node['id'] =='C':
                node.update({'degree':25})
            else:
                node.update({'degree':self.G.degree(node['id'])+1})
            new_nodes.append(node)
        self.nodes = new_nodes
        
        
    '''=============== GET DATA ================='''
    
    '''basic data dumper'''            
    def data_dumper(self,file_name,data):
            with open(file_name, 'w') as fp:
                json.dump(data, fp)
                   
                    
    def get_network_data(self,fname,dump = False):
        self.get_type_count()
        self.get_degree()
        new_data = {'links': self.links, 'nodes': self.nodes, 'count': self.count}
        
        if dump:
            self.data_dumper(file_name = fname,data = new_data) 
        else:
            return new_data
    
    
    
    
    
    