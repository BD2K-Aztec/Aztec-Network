

import json


#========================================================================
# This class helps to read data from 'sample.ann' files to create
# nodes and edges for network and graph analysis
# Verbose = 0 for no report,1 for print report, 2 for write out in file
# By: Sigdel D.                           Data-2018-Jan-10
#=========================================================================



class DataReader(object):
    
    
    def __init__(self,input_file,mdata):
        
        
        '''Input file shoulsd be provided'''
        self.input_file = input_file
        
        '''list of list of items in a line of .ann file'''
        self.Llist = []
        
        '''dictionary to hold t-id and a list a value including
        name and type'''
        self.t_dict = {}  
        
        
        '''dictionary to hold e-id and a list a value including
        name and type'''
        self.e_dict = {}
        
        
        '''dictionary to hold r-id and a list a value including
        name and type'''
        self.r_dict = {}
        
        
        '''dictionary to hold node-id and a list a value including
        name and type'''
        self.node_dict ={}
        
        
        '''Collection of all final nodes'''
        self.Nodes  =[]
        
        
        '''Collection of all final edges'''
        self.Edges = []
        
        '''entity type'''
        self.type = mdata["type"]
        
        '''effective entity type represent the kernel of network'''
        self.effective_type = mdata["imp_type"]
        
        '''relation of entity type'''
        self.relations = mdata["relations"]
        
        '''dictionary to assign diff. color to diff. entity'''
        self.color_dict =  mdata["color_dict"]
        
        '''counter to count types of nodes'''
        self.Count = []
        
        
        
        
        
    # =================== Helper Functions =============
    
    
    '''function to sum charcters in the list   ''' 
    def sum_chr_items(self, items):
        
        '''take a blank string'''
        st =""
        
        '''iterate over item to be joined'''
        for item in items:
            st = st+" "+item
        return st
    
    
    
    
    
    ''' Line of text is converted to list and collected in Llist'''
    def line_to_list(self):
        
        '''initiate file reader'''
        with open(self.input_file) as f:
            
            '''iterate over each line in file'''
            for line in f:
                
                '''fill up Llist'''
                self.Llist.append(line.split())
              
            
        
            
            
            
            
    '''edge value finder for given relation type'''            
    def find_edg_value(self,eg):
        
        '''iterate over relation'''
        for k,item in enumerate(self.relations):
            
            '''when supplied edge matches with one in list'''
            if item == eg:
                
                '''asign a value to edge'''
                return((k+1)/2)
            
            
    #============== T-data ========================================
    # T-data generally occurs as: T4 Disease_disorder 81 85 ADHD  #
    # we take them to => id:T4, type:Disease_disorder, group :3,  # 
    # name: ADHD, icolor:Chocolate etc                            #
    #==============================================================
    
    
    '''Peeling out T-data'''
    def set_tdata(self, verbose = 0):
        
        #-------------------------------------
        '''get ready a debug file'''
        if verbose == 2:
            out = open("./dbg/tdbg.txt", "w")
         #------------------------------------   
            
            
        '''iterate over lists in list collection: Llist'''
        for item in self.Llist:
            
            '''select onlly t-term lists'''
            if item[0][0] =="T":
                
                #-------------------------------------------------------------
                '''item look up'''
                if verbose==1:
                    print("item is : ", self.sum_chr_items(item),"===>")
                elif verbose ==2:
                    out.write("text is:" + self.sum_chr_items(item))
                    out.write("===>")
                #------------------------------------------------------------
                
                
                '''pick up T-ids as t-key'''
                t_key = item[0]
                
                '''pick up entity type as t_type'''
                t_type = item[1]
                
                '''pick up term as t_val'''
                t_val = self.sum_chr_items(item[4:])
                
                '''update t_dict with {t-id : [type, term]}'''
                self.t_dict.update({t_key:[t_type,t_val]})
                
                '''update node_dict with {t_id: [type,term]} '''
                self.node_dict.update({t_key:[t_type,t_val]})
                
                #-----------------------------------------------------
                if verbose !=0:
                    
                    '''t-node look up'''
                    result = ["id:", t_key,\
                              ", type:", t_type,\
                              ", name:",t_val,\
                              ", icolor:",self.color_dict[t_type]]
                
                
                if verbose == 1:
                    print(result)
                elif verbose == 2:
                    for itm in result:
                        out.write(str(itm))
                    out.write("\n") 
                    
                #-------------------------------------------------------   
                    
                '''collect nodes in Node list'''
               
                self.Nodes.append({"id":t_key,\
                              "type":t_type,\
                              "name":t_val,\
                              "icolor":self.color_dict[t_type]})
               
                
                
                
                
                
    #============== E-data ========================================
    # E-data generally occurs as: * OVERLAP E1 E3 E6 E4           #
    # and we take them to===>idST, name : OVERLAP, value : 3.0,   #
    # source : 2, source_id : E1, source_name :  attention-deficit#
    # hyperactivity disorder, target : 4, target_id : E3,         #
    # target_name :  2005                                         #
    #==============================================================  
    
    
    
                
    '''Peel out the e-data'''            
    def set_edata(self, verbose = 0):
        
        #-------------------------------------
        '''get ready a debug file'''
        if verbose == 2:
            out = open("./dbg/edbg.txt", "w")
         #------------------------------------  
        
        
        
        '''iterate over lists in Llist'''
        for item in self.Llist: 
            
            '''slsect only  e-terms lists'''
            if item[0][0] =="E":
                
                #-------------------------------------------------------------
                '''item look up'''
                if verbose==1:
                    print("item is : ", self.sum_chr_items(item),"===>")
                elif verbose ==2:
                    out.write("text is:" + self.sum_chr_items(item))
                    out.write("===>")
                #------------------------------------------------------------
                
                '''pick up t-key associated to e-key'''
                t_key = item[1].split(':')[1]
                
                '''pick up e-key '''
                e_key = item[0]
                
                '''pick up e-type'''
                e_type = item[1].split(':')[0]
                
                '''find type by attaching it to associated t-type'''
                e_val = self.t_dict[t_key][1]
                
                '''update e-dictionary'''
                self.e_dict.update({e_key:[e_type,e_val]})
                
                '''update node dictionary'''
                self.node_dict.update({e_key:[e_type,e_val]})  
                
                '''replace t-nodes by e-nodes when they overlap'''
                for item in self.Nodes:
                    if item["id"] ==  t_key :
                        self.Nodes.remove(item)
                        
                        
                #-----------------------------------------------------
                if verbose !=0:
                    
                    '''t-node look up'''
                    result = ["id:", e_key,\
                              ", type:", e_type,\
                              ", name:",e_val,\
                              ", icolor:",self.color_dict[e_type]]
                
                
                if verbose == 1:
                    print(result)
                elif verbose == 2:
                    for itm in result:
                        out.write(str(itm))
                    out.write("\n") 
                    
                #-------------------------------------------------------   
                
                
                '''collect nodes in node list'''
                self.Nodes.append({"id":e_key,\
                            "type":e_type,\
                            "name":e_val,\
                            "icolor":self.color_dict[e_type]})
                
                
    #============== R-data ========================================
    # R-data generally occurs as:R2 MODIFY Arg1:T8 Arg2:E4 and we  #
    # take them to ===>idR2, name : MODIFY, value : 1.0, source :  #
    # 7, source_id : T8, source_name :  40, target : 5, target_id  #
    # : E4, target_name :  body mass index                         #
    #==============================================================
    
    
    '''Peel out r-data'''            
    def set_rdata(self, verbose = 0):
        
        
        #-------------------------------------
        '''get ready a debug file'''
        if verbose == 2:
            out = open("./dbg/rdbg.txt", "w")
         #------------------------------------   
        
        
        '''iterate over lists of Llist'''
        for item in self.Llist:     
            
            '''select only r-term lists'''
            if item[0][0] =="R":
                
                #-------------------------------------------------------------
                '''item look up'''
                if verbose==1:
                    print("item is : ", self.sum_chr_items(item),"===>")
                elif verbose ==2:
                    out.write("text is:" + self.sum_chr_items(item))
                    out.write("===>")
                #------------------------------------------------------------
                
                
                '''pick up r-key'''
                r_key = item[0]
                
                '''pick up relation'''
                rln = item[1]
                
                '''pick up source node id'''
                fm_id = item[2].split(":")[1]
                
                '''pick up target node id'''
                to_id = item[3].split(":")[1]
                
                '''find source node type'''
                fm_type = self.node_dict[fm_id][0]
                
                '''find target node type'''
                to_type = self.node_dict[to_id][0]
                
                '''find source name'''
                fm_name = self.node_dict[fm_id][1]
                
                '''find target name'''
                to_name = self.node_dict[to_id][1]
                
                '''update r dictionary'''
                self.r_dict.update({r_key:[rln,fm_id,to_id]}) 
                
                #-----------------------------------------------------
                if verbose !=0:
                    
                    '''edge look up'''
                    result = ["id",r_key,\
                            ", name : ",rln,\
                            ", value : ",self.find_edg_value(rln),\
                            ", source : ",fm_id,\
                            ", source_name : ",fm_name,\
                            ", target : ",to_id,\
                            ", target_name : ",to_name]
                
                
                if verbose == 1:
                    print(result)
                elif verbose == 2:
                    for itm in result:
                        out.write(str(itm))
                    out.write("\n") 
                    
                #-------------------------------------------------------   
                
                    
                
                '''Collect edges in Edge list'''
                self.Edges.append({"id":r_key,\
                            "name":rln,\
                            "value":self.find_edg_value(rln),\
                            "source":fm_id,\
                            "source_name":fm_name,\
                            "target":to_id,\
                            "target_name":to_name})  
                           
                           
                
    
    #============== S-data ============================================
    # S-data generally occurs as: OVERLAP E1 E3 E6 E4===>idST, name   #
    #: OVERLAP, value : 3.0, source : 2, source_id : E1, source_name  #
    #: attention-deficit hyperactivity disorder, target : 4,          #
    # target_id : E3, target_name :  2005                             #
    #==================================================================             
                
                
                
    def set_sdata(self, verbose =0):
        
        
         #-------------------------------------
        '''get ready a debug file'''
        if verbose == 2:
            out = open("./dbg/sdbg.txt", "w")
         #------------------------------------   
        
        
        '''iterate over lists in LList'''
        for item in self.Llist: 
            '''when these are non of T,E,R-data'''
            if item[0][0] !="E":
                if item[0][0] !="R":
                    if item[0][0] !="T":
                        
                        '''when it is * data'''
                        if item[0][0] =="*":
                            
                             #-------------------------------------------------------------
                            '''item look up'''
                            if verbose==1:
                                print("item is : ", self.sum_chr_items(item),"===>")
                            elif verbose ==2:
                                out.write("text is:" + self.sum_chr_items(item))
                                out.write("===>")
                            #------------------------------------------------------------
                            
                            '''give a star key'''
                            r_key = "ST"
                            
                            '''find relation'''
                            rln = item[1]
                            
                            '''get collection of ids'''
                            ids = item[2:]
                            
                            '''find nonrepeated edges'''
                            for  i in range(len(ids)):
                                for j in range(i,len(ids)):
                                    if i != j:
                                        
                                        '''source id'''
                                        fm_id  = ids[i]
                                        '''target id'''
                                        to_id = ids[j]
                                        '''source type'''
                                        fm_type = self.node_dict[fm_id][0]
                                        '''target type'''
                                        to_type = self.node_dict[to_id][0]
                                        '''source name'''
                                        fm_name = self.node_dict[fm_id][1]
                                        '''target name'''
                                        to_name = self.node_dict[to_id][1]
                                        
                                        
                                         #-----------------------------------------------------
                                        if verbose !=0:
                    
                                            '''edge look up'''
                                            result = ["id",r_key,\
                                                ", name : ",rln,\
                                                ", value : ",self.find_edg_value(rln),\
                                                ", source : ",fm_id,\
                                                ", source_name : ",fm_name,\
                                                ", target : ",to_id,\
                                                ", target_name : ",to_name]
                
                
                                        if verbose == 1:
                                            print(result)
                                        elif verbose == 2:
                                            for itm in result:
                                                out.write(str(itm))
                                            out.write("\n") 
                    
                                        #-------------------------------------------------------   
                                        
                                        
                                        
                                        '''collect edges'''
                                        self.Edges.append({"id":r_key,\
                                                    "name":rln,\
                                                    "value": self.find_edg_value(rln),\
                                                    "source":fm_id,\
                                                    "source_name":fm_name,\
                                                    "target":to_id,\
                                                    "target_name":to_name})
                                                  
                                                  
        
        
    #============== Center =============================================
    # Centre of the network is name of the disease or any other most
    # relevant term. Central node is joined to all relevant imp nodes
    #===================================================================       
    def center(self):
        
        '''add a central node'''
        self.Nodes.append({"id":"C",\
                            "type":'Disease_disorder',\
                            "name":"Center",\
                            "icolor":self.color_dict['Disease_disorder']})
        
        
        '''connect imp-types node to center node'''
        for item in self.Nodes:
            if item['type'] in self.effective_type:
                self.Edges.append({"id":"C",\
                                    "name":"Center",\
                                    "value": 1,\
                                    "source_name":"cardiomyopathy",\
                                    "source": "C",\
                                    "target":item["id"],\
                                    "target_name":item['name']}) 
        
    
    
    
    # ================= Data Getters ===============
    
    
    '''basic data dumper'''            
    def data_dumper(self,file_name,data):
            with open(file_name, 'w') as fp:
                json.dump(data, fp)
                
    
    '''fill up Nodes''' 
    def get_nodes(self,dump=False):
        self.line_to_list()
        self.set_tdata()
        self.set_edata()
        
        if dump:
            self.data_dumper(file_name = 'nodes.json',data = self.Nodes)
        return self.Nodes
    
    
    '''fill up Edges'''
    def get_edges(self, dump=False):
        self.set_rdata()
        self.set_sdata()
        if dump:
            self.data_dumper(file_name = 'edges.json',data = self.Edges)
        return self.Edges
    
    
    '''get all data'''
    def get_data(self,fname,dump=False):
        all_data = {}
        nodes = self.get_nodes(dump=False)
        edges = self.get_edges(dump=False)
        self.center()
        all_data.update({'nodes':nodes,'links':edges })
        if dump:
            self.data_dumper(file_name = fname,data = all_data) 
        else:
            return all_data
    
    
    
    
    