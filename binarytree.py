"""BinaryTree.ipynb
@author: carlossuarezp
# Binary Trees
"""

import queue #it is Python module to implement queues
#from queue import SQueue

class Node:
    def __init__(self,elem,left=None,right=None,parent=None):
        self.elem=elem
        self.left=left
        self.right=right
        self.parent=parent

    def __eq__(self,other):
        """checks if self is equal to other"""
        return other!=None and self.elem==other.elem
        #return other!=None and self.elem==other.elem and self.left==other.left and self.right==other.right
 
    
    
class BinaryTree:
  
    def __init__(self):
        """creates an empty binary tree"""
        self._root=None


   
    def size(self):
        """Returns the number of nodes"""
        return self._size(self._root)

    def _size(self,node):
        "return the size of the subtree from node"
        if node==None:
            return 0
        
        return 1 + self._size(node.left) + self._size(node.right)

    def height(self):
        """Returns the height of the tree"""
        return self._height(self._root)
    
    def _height(self,node):
        """return the height of node"""
        if node==None:
            return -1

        return 1 + max(self._height(node.left),self._height(node.right))

    
    def depth(self,node):
        """return the depth of node"""

        if node==None:
            return 0

        if node.parent==None: 
            #node==self._root
            return 0
        
        return 1 + self.depth(node.parent)

    def preorder(self):
        """prints the preorder (root, left, right) traversal of the tree"""
        self._preorder(self._root)
        
    def _preorder(self,node):
        """prints the preorder (root, left, right) traversal of the subtree
        than hangs from node"""

        if node!=None:
            print(node.elem)
            self._preorder(node.left)
            self._preorder(node.right)

        
    def postorder(self):
        """prints the postorder (left, right, root)  traversal of the tree"""
        self._postorder(self._root)
        
    def _postorder(self,node):
        """prints the postorder (left, right, root) traversal of the subtree
        than hangs from node"""
        if node!=None:
            self._postorder(node.left)
            self._postorder(node.right)
            print(node.elem)
        
    def inorder(self):
        """prints the inorder (left, root, right)  traversal of the tree"""
        self._inorder(self._root)

    def _inorder(self,node):
        """prints the inorder (left, root, right) traversal of the subtree
        than hangs from node"""
        if node!=None:
            self._inorder(node.left)
            print(node.elem)
            self._inorder(node.right)
        
    def levelorder(self):
        """prints the level order of the tree"""

        if self._root==None:
            print('tree is empty')
        else:
            
            q=queue.Queue()
            q.put(self._root) #enqueue: we save the root
            
            while q.empty()==False:
                current=q.get() #dequeue
                print(current.elem)
                if current.left!=None:
                    q.put(current.left)
                if current.right!=None:
                    q.put(current.right)
                
