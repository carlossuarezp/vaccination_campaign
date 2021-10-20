# @author: carlossuarezp
from binarysearchtree import BinarySearchTree
from dlist import DList
import csv      #read files csv, tsv
import os.path  #to work with files and directory https://docs.python.org/3/library/os.path.html
import queue    #package implementes a queueu, https://docs.python.org/3/library/queue.html
import re       #working with regular expressions


def checkFormatHour(time):
    """checks if the time follows the format hh:dd"""
    pattern = re.compile(r'\d{2}:\d{2}')  # busca la palabra foo
    
    if pattern.match(time):
        data=time.split(':')
        hour=int(data[0])
        minute=int(data[1])
        if hour in range(8,20) and minute in range(0,60,5):
            return True
    
    return False


#number of all possible appointments for one day
NUM_APPOINTMENTS=144


class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine,appointment=None):

        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        self.appointment=appointment     #string with format hour:minute

    def setAppointment(self,time):
        """gets a string with format hour:minute"""
        self.appointment=time
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)+'\t appointment:'+str(self.appointment)

    def __eq__(self,other):
        return  other!=None and self.name == other.name 



class HealthCenter2(BinarySearchTree):
    """Class to represent a Health Center. This class is a subclass of a binary search tree to 
    achive a better temporal complexity of its algorithms for 
    searching, inserting o removing a patient (or an appointment)"""


    def __init__(self,filetsv=None,orderByName=True):
        """
        This constructor allows to create an object instance of HealthCenter2. 
        It takes two parameters:
        - filetsv: a file csv with the information about the patients whe belong to this health center
        - orderByName: if it is True, it means that the patients should be sorted by their name in the binary search tree,
        however, if is is False, it means that the patients should be sorted according their appointments
        """

        #Call to the constructor of the super class, BinarySearchTree.
        #This constructor only define the root to None
        super(HealthCenter2, self).__init__()
        
        #Now we 
        if filetsv is None or not os.path.isfile(filetsv):
            #If the file does not exist, we create an empty tree (health center without patients)
            self.name=''
            #print('File does not exist ',filetsv)
        else: 
            order='by appointment'
            if orderByName:
                order='by name'

            #print('\n\nloading patients from {}. The order is {}\n\n'.format(filetsv,order))
            
            self.name=filetsv[filetsv.rindex('/')+1:].replace('.tsv','')
            #print('The name of the health center is {}\n\n'.format(self.name))
            #self.name='LosFrailes'

            fichero = open(filetsv)
            lines = csv.reader(fichero, delimiter="\t")
    
            for row in lines:
                #print(row)
                name=row[0] #nombre
                year=int(row[1]) #año nacimiento
                covid=False
                if int(row[2])==1:          #covid:0 o 1
                    covid=True
                vaccine=int(row[3])         #número de dosis
                try:
                    appointment=row[4]
                    if checkFormatHour(appointment)==False:
                        #print(appointment, ' is not a right time (hh:minute)')
                        appointment=None
                        
                except:
                    appointment=None    

                objPatient=Patient(name,year,covid,vaccine,appointment)
                #name is the key, and objPatient the eleme
                if orderByName:
                    self.insert(name,objPatient)
                else:
                    if appointment:
                        self.insert(appointment,objPatient)
                    else:
                        print(objPatient, " was not added because appointment was not valid!!!")
    
            fichero.close()


    def searchPatients(self,year=2021,covid=None,vaccine=None):
        """return a new object of type HealthCenter2 with the patients who
        satisfy the criteria of the search (parameters). 
        The function has to visit all patients, so the search must follow a level traverse of the tree.
        If you use a inorder traverse, the resulting tree should be a list!!!"""
        result=HealthCenter2()
        l = DList()          # We will store in a list all elements of the tree, one by one, in order to check whether they meet the criteria and act according to it
        l.addLast(self._root)
        while l.isEmpty()==False:
            current = l.removeFirst()
            if current.elem.year<=year and (covid==None or current.elem.covid==covid) and (vaccine==None or current.elem.vaccine==vaccine):
                result.insert(current.elem.name,current.elem)
            if current.left!=None:
                l.addLast(current.left)
            if current.right!=None:
                l.addLast(current.right)
        return result
        '''
        Algorithms analysis:
        What is the time complexity of the function? Explain best and worst cases

                With the help of a DList (we could have used a queue instead but it is not allowed), we have 
            implemented an algorithm based on level order traversing, introducing only 3 noticeable differences 
            from the levelorder() method itself, which has linear complexity: first creating and returning a result 
            (adds 2), then removing the line that prints each element of the queue (subtracts 1 each iteration), 
            and also checking whether the patient meets the criteria and, if so, adding it to the result center 
            (adds at most 2 each iteration). 
            The complexity is therefore LINEARITHMIC: O(nlog2(n)). That is easy to see, since we will iterate until 
            the list is empty, and only one element is removed per iteration. Inside the loop, the DList 
            methods only have complexity O(1), but the result.insert() method has complexity O(log2(n))

                Best case: this is trivial. Whenever there are no patients in the center, the invoking
            tree will be empty. Therefore self._root will be None and None will be put in the list, which 
            is the same as the list being empty. Therefore, the while loop will not be entered. Thus,
            the complexity for the best case is [4]

                Worst case: if the invoking center is not empty, then the complexity will highly depend
            on the size of the tree (number of patients), butwe cannot control that. 
            What we do know is that the more patients meet the criteria, the more iterations in which an extra 
            action must be performed (result.insert()). On top of that, in the case of a tree degenerated into a list, 
            the complexity of insert() is O(n). Thus, the worst case happens when all patients meet the criteria and 
            the result is a degenerate tree: [4+n+n(6+n)] = [4+7n+n^2]
        '''


    def vaccine(self,name,vaccinated):
        """This functions simulates the vaccination of a patient whose
        name is name. It returns True is the patient is vaccinated and False if not"""
        cnode = self.findlower(name)                     # We know that in this case the trees are alphabetically ordered so key = name
        if cnode is None:                           # if patient does not exist in the Health Center:
            print('Patient does not exist')
            return False
        elif (cnode.elem.vaccine == 2):             # if patient has already had two doses:
            print('This patient has already been vaccinated previously')
            self._remove(cnode)                     # remove from self
            vaccinated.insert(name,cnode.elem)      # store in vaccinated (alphabetical order, so key=name)
            return False
        elif (cnode.elem.vaccine == 1):             # if patient has had one dose:
            cnode.elem.vaccine = 2
            self._remove(cnode)                     # remove from self
            vaccinated.insert(name,cnode.elem)      # store in vaccinated (alphabetical order, so key=name)
            return True
        else:                                       # if patient has not had any dose:
            cnode.elem.vaccine = 1
            return True
        '''
        Algorithms analysis:
        What is the time complexity of the function? Explain best and worst cases

                Since we have been able to implement an efficient solution that does not rely on loops
            (only conditionals), we just need to study the complexity of the other methods of the 
            class that we make use of, and find the largest one.
            All find(), insert() and remove() have logarithmic complexity when working over a binary 
            search tree, and the Health Center is a data structure of such type.
            So, the complexity of this method itself is logarithmic: O(log2(n))

                Best case: is cnode is None, only the first conditional branch is entered. Inside it,
            the complexity is just [2] (one print and one return). Same thing goes for the 'else' case.
            However, then it would have to check 2 extra conditions ('elif'). Being more specific,
            cnode can be None when the tree is empty, which is indeed the best case, since it is the
            best case for the find() function, which is always executed, as well as for our conditional 
            structure. The complexity would be: 2(find with root=None) + 1(check 1st condition) + 2 = [5]

                Worst case: we will considering the possibility of the three degenerating into a list, in
            which case find(), remove() and insert() would all have O(n) complexity. On top of that,
            the function would need to enter the third conditional. That is, if the patient has had one dose
            we must perform one assignment, call 2 methods of (at worst) linear complexity and return a value:
            [2+2n]. More specifically, if the patient is at the 'bottom' of the three (the maximum depth), 
            this will be the worst case for the find() and remove() methods.
            The complexity would be: n(find) + 1(first condition) + 1(second condition) + [2+2n] = [4 + 3n]
        '''


    def makeAppointment(self,name,time,schedule):
        """This functions makes an appointment 
        for the patient whose name is name. It functions returns True is the appointment 
        is created and False eoc """

        if not checkFormatHour(time):               #Check format
            print("time parameter is invalid or malformed")
            return False

        cnode = self.findlower(name)
        if cnode is None:                           #if patient does not exist in the Health Center:
            print('Patient does not exist')
            return False
        elif (cnode.elem.vaccine == 2):             # if patient has already had two doses:
            print('This patient has already been vaccinated previously')
            return False

        else:
            if schedule.find(time) is None:
                cnode.elem.appointment = time
                schedule.insert(time,cnode.elem)
                return True
            else:
                time1 = time
                time2 = time
                while time1 is not False or time2 is not False:
                    time1 = auxCalcTime(time1, -5)              #Custom functions to compute next schedule time in a clean fashion
                    time2 = auxCalcTime(time2, 5)
                    if time1:                                   #Custom checks to see if we are in time range
                        if schedule.find(time1) is None:
                            cnode.elem.appointment = time1
                            schedule.insert(time1,cnode.elem)
                            return True
                    if time2:
                        if schedule.find(time2) is None:
                            cnode.elem.appointment = time2
                            schedule.insert(time2,cnode.elem)
                            return True
                print("no time slots available")
                return False

        '''
        Algorithms analysis:
        What is the time complexity of the function? Explain best and worst cases

                In this implementation we rely mostly on the search calls of the binary search tree, firstly 
            to check wether the patient exists and if he/she is vacinated, but later to search in the vacination 
            schedule. Both search and insert have logarithmic complexity, so our calls are logarithmic. We also call 
            checkFormatHour which has O(1) complexity (no loops nor recursive calls), and so does auxCalcTime, 
            so these method calls do not increase complexity. The only loop used is a while loop that iterates over 
            the possible times for vacination when the exact time is taken. It has a maximum number of iterations of n, 
            n being the number of potential time slots, which go from 08:00 to 20:00 in 5 minute jumps (so a total of 144 slots max). 
            This makes, in theory, the complexity linearithmic [O(n*log2(n))], although in most cases the iterations 
            will be very few, if not none.

                Best case: note that inside each of the first 3 conditional statements, only two primitive operations
            are performed (print and return). However it is clear that it is best when the time format is not correct
            (1st conditional), as it performs the return before even calling find(), which has, at best, logarithmic
            complexity. Therefore, the complexity for the best case would be [3]

                Worst case: we want to assign the patient (who is indeed found in the tree) a (format-wise corret) time
            slot which is either 08:00 or 19:55, into a schedule in which all slots are filled. We reach the while loop,
            which is forced to conduct the maximum number of iterations, as it iterates throughout the whole structure for 
            an empty slot that does not exist. On top of that, if we consider that either the invoking or the schedule tree
            gets degenerated into a list, which would make the complexity of the binary search calls linear, then we are 
            talking about a complexity of [O(n^2)] for the worst case
        '''

    def findlower(self,key):
        """Variation of the find method that does not discriminate between upper and lower case, for a correct search of patient names"""
        return self._findlower(self._root,key)

    def _findlower(self,node,key):
        if node==None:
            return None
        if node.key.lower()==key.lower():
            return node
        if key.lower()<node.key.lower():
            return self._findlower(node.left,key)
        if key.lower()>node.key.lower():
            return self._findlower(node.right,key)
                
def auxCalcTime(time, delta):
    if not time:
        return False
    timed = [int(x) for x in time.split(":")]
    timed[1] += delta
    if timed[1]>=60:
        timed[1]-=60
        timed[0]+=1
    if timed[1]<0:
        timed[1]+=60
        timed[0]-=1

    #We dont include the following to avoid overlapping as we want all schedule times to be of the same day
    if timed[0]>=20 or timed[0]<8:
        return False

    timed = [str(x) for x in timed]
    return "{}{}:{}{}".format("0"*(2-len(timed[0])),timed[0],"0"*(2-len(timed[1])),timed[1])

'''
if __name__ == '__main__':
    ###Testing the constructor. Creating a health center where patients are sorted by name
    o=HealthCenter2('data/LosFrailes2.tsv')
    o.draw()
    print()

    print('Patients who were born in or before than 1990, had covid and did not get any vaccine')
    result=o.searchPatients(1990, True,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990, did not have covid and did not get any vaccine')
    result=o.searchPatients(1990, False,0)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and got one dosage')
    result=o.searchPatients(1990, None,1)
    result.draw()
    print()

    print('Patients who were born in or before than 1990 and had covid')
    result=o.searchPatients(1990, True)
    result.draw()
    print()

    ###Testing the constructor. Creating a health center where patients are sorted by name
    schedule=HealthCenter2('data/LosFrailesCitas.tsv',False)
    schedule.draw(False)
    print()

    o.makeAppointment("Perez","08:00",schedule)
    o.makeAppointment("Losada","19:55",schedule)
    o.makeAppointment("Jaen","16:00",schedule)
    o.makeAppointment("Perez","16:00",schedule)
    o.makeAppointment("Jaen","16:00",schedule)

    o.makeAppointment("Losada","15:45",schedule)
    o.makeAppointment("Jaen","08:00",schedule)

    o.makeAppointment("Abad","08:00",schedule)
    o.makeAppointment("Omar","15:45",schedule)
    
    schedule.draw(False)

    vaccinated=HealthCenter2('data/vaccinated.tsv')
    vaccinated.draw(False)

    name='Ainoza'  #doest no exist
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Abad'   #0 dosages
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)

    name='Font' #with one dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
    
    name='Omar' #with two dosage
    result=o.vaccine(name,vaccinated)
    print("was patient vaccined?:", name,result)
    print('center:')
    o.draw(False)
    print('vaccinated:')
    vaccinated.draw(False)
'''