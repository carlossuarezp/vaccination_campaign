"""BinarySearchTree.ipynb
@author: carlossuarezp
# Binary Search Trees
Firstly, we should import the classes BinaryNode and Node.
"""


from binarytree import BinaryTree
from binarytree import Node


class BSTNode(Node):
    def __init__(self, key, elem,left=None,right=None,parent=None):
        self.key=key
        
        #we call the constructor of Node
        super(BSTNode,self).__init__(elem,left,right,parent)



    def __eq__(self,other):
        #if other:
        #    print(self.key,other.key)
        #return other!=None and self.key==other.key and self.elem==other.elem
        return other!=None and self.key==other.key  and self.left==other.left and self.right==other.right

class BinarySearchTree(BinaryTree):
    
    
    def search(self,key):
        """Returns True if the key exists into the True, eoc False"""
        return self._searchNode(self._root,key)

    def _searchNode(self,node,key):
        """Recursive function"""

        if node==None:
            return False

        if node.key==key:
            return True
        
        if key<node.key:
            return self._searchNode(node.left,key)

        if key>node.key:
            return self._searchNode(node.right,key)


    def searchIt(self,key):
        node=self._root
        while node:
            if node.key==key:
                return True
            elif key<node.key:
                node=node.left
            else:
                node=node.right
        
        return False


    def find(self,key):
        """Returns the node whose key is key, and None if key does not exist"""
        return self._find(self._root,key)

    def _find(self,node,key):
        """Recursive function that returns the node whose key is key"""
        if node==None:
            return None
        if node.key==key:
            return node
        if key<node.key:
            return self._find(node.left,key)
        if key>node.key:
            return self._find(node.right,key)
    

    def _numChildren(self,node):
        """returns the number of children of node"""
        if node==None or (node.left==None and node.right==None):
            return 0
        if node.left!=None and node.right!=None:
            return 2
        return 1

        
    def insert(self,key,elem):
        """inserts a new node, with key and element elem, into the tree"""
        if self._root == None:
            self._root=BSTNode(key,elem)
        else:
            self._insertNode(self._root,key,elem)

    def _insertNode(self,node,key,elem):
        """recursive funtion to insert a new node"""
        if node.key==key:
            print('Error: {} already exist into the tree.'.format(key))
        elif key<node.key:
            if node.left!=None:
                self._insertNode(node.left,key,elem)
            else: #node.left==None
                newNode=BSTNode(key,elem)
                node.left=newNode
                newNode.parent=node
        else: #key>node.key
            if node.right!=None:
                self._insertNode(node.right,key,elem)
            else: #node.right==None
                #ya he encontrado la posición
                newNode=BSTNode(key,elem)
                node.right=newNode
                newNode.parent=node

    def remove(self,key):
        """Searches and removes the node whose key is key"""
        node=self.find(key)
        if node == None:
            print('{} does not exist!!!'.format(key))
            return None
        
        print('removing ', key, node.elem)
        self._remove(node)
    
    
    def _remove(self,node):    
        """Recursive function to remove node.
        Three posible scenarios:
        1) node is a leaf
        2) node only has a child
        3) node has two children"""

        numChildren=self._numChildren(node)
        #First case: no children
        if numChildren==0:
            #print(node.elem , 'is a leave')
            if node.parent!=None: 
                if node is node.parent.right: #hijo izquierdo del padre:
                    node.parent.right=None
                elif node is node.parent.left: 
                    node.parent.left=None
            else:
                self._root=None
            
        
        #Second case: only one child, the left child
        elif numChildren==1:
            grandP=node.parent #grand parent
            
            #we get the grandchild
            if node.left is not None:
                grandC=node.left   
            elif node.right is not None:
                grandC=node.right
            
            #link the grandparent to the grandchild    
            if grandP==None:
                self._root=grandC
            else:
                if node is grandP.left:
                    grandP.left=grandC
                elif node is grandP.right: 
                    grandP.right=grandC
                
            grandC.parent=grandP
            
        
        #Third case: two children
        else:
            successor=node.right
            while successor.left!=None:
                successor=successor.left
                        
            #we replace the node's elem by the successor's elem
            node.key=successor.key
            node.elem=successor.elem
            #we remove the succesor from the tree
            self._remove(successor)

        
        
    def draw(self,extend=True):
        """Fucntion to draw a tree. It extend is True,
        for each node, its key and element are printed
        If extend is False, it only prints its key"""
        if self._root:
            self._draw('', self._root, False, extend)
        else:
            print('tree is empty')
        print('\n\n')
        
    def _draw(self,prefix, node, isLeft,extend):
        if node !=None:
            self._draw(prefix + "     ", node.right, False, extend)
            #You can replace the elem with key
            if extend:
                print(prefix + ("|-- ") + 'key:'+str(node.key) +'\telem:('+ str(node.elem)+')')
            else:
                print(prefix + ("|-- ") + str(node.key))
                
            self._draw(prefix + "     ", node.left, True, extend)


    def __eq__(self,other):
        return other!=None and self._root==other._root

if __name__=='__main__':
 	tree=BinarySearchTree()
 	for x in [18,11,23,5,15,20,24,9,15,22,21,6,8,7]:
 	    tree.insert(x,x)
 	print()

 	tree.draw(False)
 	print('size:',tree.size())
 	print('height:',tree.height())

 	for x in [5,10,17,20,22,23,25]:
 	    print("search({})={}".format(x,tree.search(x)))

 	"""Remove the root"""

 	tree.remove(18)
 	tree.draw(False)

 	#remove a leave
 	tree.remove(7)
 	tree.draw(False)

 	#remove a leave
 	tree.remove(8)
 	tree.draw(False)
#
#	#remove a node with only right child
 	tree.remove(5)
 	tree.draw(False)

 	#remove a node with only left child
 	tree.remove(9)
 	tree.draw(False)
#
#	#remove a node with two children
 	tree.remove(11)
 	tree.draw()
#
#	#remove a node with two children root
 	tree.remove(20)
 	tree.draw()
#
 	tree.remove(15)
 	tree.draw()
 	tree.remove(6)
 	tree.draw()
 	tree.remove(8)
 	tree.draw()
#
#	#remove a root, with only the right child
 	tree.remove(24)
 	tree.draw()
 	print()
#
 	for x in [5,10,15,20]:
 	    tree.insert(x,x)
 	tree.draw()
#
#	#remove a root, with only the left child
 	tree.remove(23)
 	tree.draw()
#
#	#remove a root, with only the left child
 	tree.remove(22)
 	tree.draw()
#
#	#remove a root, with only the right child
 	tree.remove(5)
 	tree.draw()
         

