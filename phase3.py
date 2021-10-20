"""
@author: carlossuarezp
"""
import sys


class HealthCenter():
    def __init__(self,name=None):
        self.name=name
    
    def __eq__(self,other):
        return  other!=None and self.name==other.name
    
    def __str__(self):
        return self.name


class AdjacentVertex:
  def __init__(self,vertex,weight):
    self.vertex=vertex
    self.weight=weight
  
  def __str__(self):
    return '('+str(self.vertex)+','+str(self.weight)+')'
 
class Map():
    def __init__(self):
        self.centers={}
        self.vertices={}
    
    def addHealthCenter(self,center):
        i=len(self.centers)
        self.centers[i]=center
        self.vertices[i]=[]
        
    def _getIndice(self,center):
        for index in self.centers.keys():
            if self.centers[index]==center:
                return index
        return -1
        
    def __str__(self):
        result=''
        for i in self.vertices.keys():
            result+=str(self.centers[i])+':\n'
            for adj in self.vertices[i]:
                result+='\t'+str(self.centers[adj.vertex])+', distance:'+str(adj.weight)+'\n'
        return result
    
       
    def addConnection(self,center1,center2,distance):
        #print('new conexion:',pto1,pto2)
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        self.vertices[index1].append(AdjacentVertex(index2,distance))
        #print('adding:',index2,index1,distancia)
        self.vertices[index2].append(AdjacentVertex(index1,distance))

        
    def areConnected(self,center1,center2):
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                return adj.weight
        #print(pto1,pto2," no están conectados")
        return 0
            
    def removeConnection(self,center1,center2):
        index1=self._getIndice(center1)
        index2=self._getIndice(center2)
        if index1==-1:
            print(center1,' not found!')
            return
        if index2==-1:
            print(center2,' not found!!')
            return 
        
        for adj in self.vertices[index1]:
            if adj.vertex==index2:
                self.vertices[index1].remove(adj)
                break
                
        for adj in self.vertices[index2]:
            if adj.vertex==index1:
                self.vertices[index2].remove(adj)
                break

    
        

    def createPath(self): 
        """This function prints the vertices by dfs algorithm"""
        #print('dfs traversal:')
        # Mark all the vertices as not visited 
        visited = [False] * len(self.vertices)

        paths=[]
        for v in  self.vertices:
            if visited[v]==False:
                self._dfs(v, visited,paths)
        
        print()
        return paths
        
    def _dfs(self, v, visited,paths): 
        # Mark the current node as visited and print it 
        visited[v] = True
        #print(self.centers[v], end = ' ') 
        paths.append(self.centers[v])
        # Recur for all the vertices  adjacent to this vertex 
        for adj in self.vertices[v]: 
          i=adj.vertex
          if visited[i] == False: 
            self._dfs(i, visited,paths) 
            
            
    
    def printSolution(self,distances,previous,v): 
        """imprime los caminos mínimos desde v"""
        for i in range(len(self.vertices)):
          if distances[i]==sys.maxsize:
            print("There is not path from ",v,' to ',i)
          else: 
            minimum_path=[]
            prev=previous[i]
            while prev!=-1:
              minimum_path.insert(0,self.centers[prev])
              prev=previous[prev]
            
            minimum_path.append(self.centers[i])  
    
            print('Ruta mínima de:',self.centers[v],'->',self.centers[i],", distance", distances[i], ', ruta: ',  end= ' ')
            for x in minimum_path:
                print(x,end= ' ')
            print()
    
    def minDistance(self, distances, visited): 
        """This functions returns the vertex (index) with the mininum distance. To do this, 
        we see in the list distances. We 
        only consider the set of vertices that have not been visited"""
        # Initilaize minimum distance for next node 
        min = sys.maxsize 
    
        #returns the vertex with minimum distance from the non-visited vertices
        for i in range(len(self.vertices)): 
          if distances[i] <= min and visited[i] == False: 
            min = distances[i] 
            min_index = i 
      
        return min_index 
    
    def dijkstra(self, v=0): 
        """"This function takes the index of a delivery point pto and calculates its mininum path 
        to the rest of vertices by using the Dijkstra algoritm. Devuelve una lista con las distancias
        y una lista con los vértices anteriores a uno dado en el camino mínimo"""  
        
        
        #we use a Python list of boolean to save those nodes that have already been visited  
        visited = [False] * len(self.vertices) 
    
        #this list will save the previous vertex 
        previous=[-1]*len(self.vertices) 
    
        #This array will save the accumulate distance from v to each node
        distances = [sys.maxsize]*len(self.vertices) 
        #The distance from v to itself is 0
        distances[v] = 0
    
        for i in range(len(self.vertices)): 
          # Pick the vertex with the minimum distance vertex.
          # u is always equal to v in first iteration 
          u = self.minDistance(distances, visited) 
          # Put the minimum distance vertex in the shotest path tree
          visited[u] = True
          
          # Update distance value of the u's adjacent vertices only if the current  
          # distance is greater than new distance and the vertex in not in the shotest path tree 
          for adj in self.vertices[u]:
            i=adj.vertex
            w=adj.weight
            if visited[i]==False and distances[i]>distances[u]+w:
              distances[i]=distances[u]+w   
              previous[i]=u       
              
        #finally, we print the minimum path from v to the other vertices
        #self.printSolution(distances,previous,v)
        return previous,distances
 
    def minimumPath(self, start, end):
        """calcula la ruta mínima entre dos puntos de entrega"""
        indexStart=self._getIndice(start)
        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end)  + " does not exist")
            return None
        
        previous,distances=self.dijkstra(indexStart)
        
        #construimos el camino mínimo
        minimum_path=[]
        prev=previous[indexEnd]
        while prev!=-1:
            minimum_path.insert(0,str(self.centers[prev]))
            prev=previous[prev]
            
        minimum_path.append(str(self.centers[indexEnd]))
        return minimum_path, distances[indexEnd]

    def Bellman_Ford(self, s=0):

    	'''Bellman-Ford algorithm solves the problem of graphs with negative weighed edges, over which
    	Dijkstra cannot operate properly. However, it does not work whenever there is a cycle for 
    	which its edges add up to a negative value. This is something we will check in the last step of
    	our implementation. This algorithm does not use the method of minimal distance combined with an updated
    	list of the already visited vertices. That is because instead of focusing on the vertices, it
    	focuses on the edges. It does as many iterations as vertices there are and, on each of them, it checks
    	the adjacent vertices for each vertex (the edge connections) and relaxes them, if necessary'''

    	# STEP 1: initialize
    	# d[v] stores the value of the minimum path from s to v. Set to infinity in initialization
    	d = [sys.maxsize]*len(self.vertices)
    	#The distance from the source to itself is 0
    	d[s]=0
    	# p is used to store the vertices previous to each vertex on the path from the s
    	p=[-1]*len(self.vertices)
    	accu = True

    	# STEP 2: iterate and potential vertex relaxation
    	for i in range(len(self.vertices)):
    		# for each v
    		for v in range(len(self.vertices)):
    			# for each connection (u,v)
    			for j in self.vertices[v]:
    				u = j.vertex
    				w = j.weight
    				if (d[u] > d[v]+w):
    					d[u] = d[v]+w
    					p[u] = v

    	# STEP 3: check for non-negative cycles for each connection (u,v)
    	for v in range(len(self.vertices)):
    		for j in self.vertices[v]:
    			u = j.vertex
    			w = j.weight
    			if (d[u] > d[v]+w):
    				accu = False          # the algorithm does not converge
    				break
    	return p,d,accu

    	'''
 		What is the temporal complexity of the function? Justify the best and worst case
		
				One can clearly check that the complexity is O(n^2) in the case of most graphs (sparse), while it would be 
			O(n^3) for dense graphs. 
				In step 1 we define a series of arrays and in step 2 we enter a 3-level nested loop, which defines 
			the complexity, as in step 3 the nested loop only has 2 levels.
				The number of iterations for the first and second loops in the nest is n(number of vertices of the graph),
			which that makes sense since we want to iterate as many times as vertices (O(n)), while checking all adjacency 
			connections inside every iteration (O(n) or O(n^2)). In order to check all connections, we need to iterate over 
			every vertex, and then iterate inside over every other vertex that is adjacent.
				This last iteration, if the graph is sparse, is O(1), but if dense, becomes O(n), so that is where the 
			difference comes from.

				Best case: since this algorithm needs a source vertex to calculate distances from, we cannot consider an
			empty graph. Given that, the best case happens when the graph is only composed by that source vertex.
			That means it has no edges and therefore it must perform only one iteration of the first loop and not
			enter the second one, as there are no adjacent edges: O(1)

				Worst case: several factors make complexity reach is highest. The worst combination would be a very
			dense graph (if each graph is adjacent to every other one, the number of iterations for the nested loops
			will be not close, but literally n^3) in which we constantly need to relax the vertices (which depends on the
			internal structure of the graph and values of the edges) such that the graph has no negative cycles (if it did,
			then the loop in step 3 would break and stop before reaching the maximum number of iterations): O(n^3)

 		'''
    
    def minimumPathBF(self,start,end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Bellman-Ford. Puedes implementar otras funciones auxiliares si lo consideras necesario """

        minimum_path=[]
        minimumDistance=0
        indexStart=self._getIndice(start)

        if indexStart==-1:
            print(str(start) + " does not exist")
            return None
        indexEnd=self._getIndice(end)
        if indexEnd==-1:
            print(str(end) + " does not exist")
            return None
        
        previous,distances,accu=self.Bellman_Ford(indexStart)
        if accu is False:
        	print('The algorithm does not converge')
        	return None
        minimumDistance = distances[indexEnd]
        prev=previous[indexEnd]
        while prev!=-1:
            minimum_path.insert(0,str(self.centers[prev]))
            prev=previous[prev]
        minimum_path.append(str(self.centers[indexEnd].name))

        return minimum_path, minimumDistance
        
        '''
        	The complexity of every statement in this method is smaller than that of the call to Bellman-Ford,
        which is explained above, so the complexity and the worst case analysis are the same.
        	However, we have a particular best case for which we would not even have to perform the call to 
        Bellman-Ford, achieving minimum complexity. This happens when either the start or end parameters do not
        exist within the graph.
        '''

    def Floyd_Warshall(self):

        l = len(self.vertices)
        M = [[float('inf') for _ in range(l)] for _ in range(l)]
        P = [[None for _ in range(l)] for _ in range(l)]
        
        for x in range(l):
            for y in range(l):
                if x == y:
                    M[x][y] = 0
                    P[x][y] = x
        
        for i in self.vertices:
            for vertice in self.vertices[i]:
                M[i][vertice.vertex] = vertice.weight
                P[i][vertice.vertex] = vertice.vertex


        #Find distances and store paths
        for k in range(l):
            for i in range(l):
                for j in range(l):
                    temp = M[i][k] + M[k][j]
                    if temp < M[i][j]:
                        M[i][j] = temp
                        P[i][j] = P[i][k]
        return M,P

    def minimumPathFW(self, start, end):
        """"calcula y devuelve la ruta mínima entre start y end, aplicando el algoritmo de 
         Floyd-Warshall. Puedes implementar otras funciones auxiliares si lo consideras necesario"""

        minimum_path=[]
        minimumDistance=0
        X=self._getIndice(start)
        if X==-1:
            print(str(start) + " does not exist")
            return None
        Y=self._getIndice(end)
        if Y==-1:
            print(str(end) + " does not exist")
            return None

        M,P = self.Floyd_Warshall()
        
        minimumDistance = M[X][Y]

        #Find path
        minimum_path.append(str(self.centers[X]))
        while X != Y:
            X = P[X][Y]
            minimum_path.append(str(self.centers[X].name))

        return minimum_path, minimumDistance

        '''
        What is the temporal complexity of the function? Justify the best and worst case
        
            We will explain the complexity for Floyd_Warshall, since the complexity for minimumpathFW is determined by it,
        as the algorithm is called inside the method and it has higher complexity: ignoring such call, the statement with
        the largest complexity for the function is either the while loop or the calls to _getIndice, which are both O(n).

        	Meanwhile, one can check that Floyd_Warshall complexity is O(n^3) in the case of all graphs, since the more 
        iteration dense part of the code involves iterating with 3 nested for loops iterating n times each where n in the
        number of vertices. The rest of the steps have a complexity of O(n^2) for the initialization of variables.

            Best case: The best case for this implemenation would be that the entered center does not belong to the graph, 
        that would exit the function with a complexity of O(n), as it would need to check whether the center was in the graph.
        In terms of the method minimumpathFW here is the only difference, as we have an even better case when either the
        starting point center or the endpoint center do not exist. In that case, the algorithm would not even be called and the
        complexity would still be O(n), due to the calling of _getIndice, but with less steps performed.

        	Worst case: The worst case is the same as the average case, their complexity is always O(n) for a successful 
        path search. But if the graph had lots of vertices, The time to compute the initializarion of variables would be grater, 
        but the maximum number of vertices per center is n-1, the maxiumun number ot total vertices is (n-1)^2: O(n^2),
        this complexity is still dwarfed by the main 3 nested loops, so it does not increase the overall complexity of O(n^3)
        '''

def test():
    #https://www.bogotobogo.com/python/images/Dijkstra/graph_diagram.png
   
    m=Map()
    for c in ['A','B','C','D','E','F']:
        m.addHealthCenter(HealthCenter(c))
    
    print(m)
    m.addConnection(m.centers[0],m.centers[1],7)#A,B,7
    m.addConnection(m.centers[0],m.centers[2],9)#A,C,9
    m.addConnection(m.centers[0],m.centers[5],14)#A,F,14
    
    m.addConnection(m.centers[1],m.centers[2],10)#B,C,10
    #m.addConnection(m.centers[1],m.centers[3],15)#B,D,15
    
    m.addConnection(m.centers[2],m.centers[3],55)#C,D,11
    m.addConnection(m.centers[2],m.centers[5],2)#C,F,2
    
    m.addConnection(m.centers[3],m.centers[4],6)#D,E,6
    
    m.addConnection(m.centers[4],m.centers[5],9)#E,F,9
    print(m)
    
    
    c1=m.centers[0]
    c2=m.centers[1]
    c3=m.centers[2]
    c4=m.centers[3]
    c5=m.centers[4]
    c6=m.centers[5]

    print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    print(c1,c2,' are connected?:',m.areConnected(c1,c2))
    
    #m.removeConnection(c1,c2)
    print(m)
    
    print('createPath:',end=' ')
    ruta=m.createPath()
    #print('Ruta:',ruta)
    for r in ruta:
        print(r, end=' ')
    print()
    
    minimum_path,d=m.minimumPath(c3,c6)
    for p in minimum_path:
        print(p,end=' ')
    print('total distance:',d)

    #añade más pruebas para probar los dos nuevos métodos minimumPathBF y minimumPathFW
    minimum_path,d=m.minimumPathBF(c3,c6)
    for p in minimum_path:
        print(p,end=' ')
    print('total distance:',d)

    M,P = m.Floyd_Warshall()
    print(M)
    print(P)
    
    minimum_path,d=m.minimumPathFW(c3,c6)
    for p in minimum_path:
        print(p,end=' ')
    print('total distance:',d)
    

#Descomenar para usarlo en Spyder
if __name__ == '__main__':
    test()
