from dlist import DList
from dlist import DNode

import csv
import os.path


class Patient:
    """Class to represent a Patient"""
    def __init__(self,name,year,covid,vaccine):
        self.name=name
        self.year=year
        self.covid=covid
        self.vaccine=vaccine
        
    def __str__(self):
        return self.name+'\t'+str(self.year)+'\t'+str(self.covid)+'\t'+str(self.vaccine)


class HealthCenter(DList):
    """Class to represent a Health Center"""
    def __init__(self,filetsv=None):
        super(HealthCenter, self).__init__()

        if filetsv is None or not os.path.isfile(filetsv):
            self.name=''

        else: 
            print('loading the data for the health center from the file ',filetsv)
    
            self.name=filetsv.replace('.tsv','')
            tsv_file = open(filetsv)
            read_tsv = csv.reader(tsv_file, delimiter="\t")
        
        
            for row in read_tsv:
                name=row[0]
                year=int(row[1])
                covid=False
                
                if int(row[2])==1:
                    covid=True

                vaccine=int(row[3])
                self.addLast(Patient(name,year,covid,vaccine))


    def addPatient(self,patient):

        #add a new patient in alphabetic order
        #complexity must be linear
        #patient cannot be duplicated
        #patients must be sorted alphabetically

        #first we check if the patient if a duplicate and, if it is, we don't go any further

        found = False
        current = self._head
        pname = patient.name.lower()
        i = 0
        while current != None and not found and current.elem.name.lower() <= pname:
            if current.elem.name.lower() == pname:
                found = True 
                break
            current = current.next
            i = i+1

        #If not, we add it in the proper position for the list to stay sorted

        if not found:
            self.insertAt(i,patient)


    def searchPatients(self,year,covid=None,vaccine=None):

        #Steps we used to come up with an efficient (linear complexity) solution:
        #1. Restriction that is always speified: YEAR -> we check that first
        #2. Check whether the covid and vaccine conditions are specified and, in case they are, whether they are met
        #3. If all previously stated conditions are fullfilled, then the patient is added
        #3. Advance until the whole center has been evaluated

        newcenter = HealthCenter()
        current = self._head
        while current != None:     #although a for loop could be less costly when knowing the number of iterations, a while loop is more robust against errors such as modifications in the list
            if current.elem.year<=year and (covid==None or current.elem.covid==covid) and (vaccine==None or current.elem.vaccine==vaccine):
                newcenter.addLast(current.elem)
            current = current.next
        return newcenter
       
    
    def statistics(self):

        total = len(self)
        total70 = 0
        totalcovid = 0
        totalcovid70 = 0
        totalnodose = 0
        totalnodose70 = 0
        total1dose = 0
        total2dose = 0

        current = self._head
        while current != None:              #an alternative way is 'for _ in range(total):' but we keep the while loop since we want to keep the code simple and mantain the same style througout the code

            if current.elem.covid == True:
                totalcovid += 1

            if current.elem.vaccine == 0:
                totalnodose += 1
            elif current.elem.vaccine == 1:
                total1dose += 1
            else:
                total2dose += 1

            if current.elem.year <= 1950:
                total70 += 1
                if current.elem.covid == True:
                    totalcovid70 += 1
                if current.elem.vaccine == 0:
                    totalnodose70 += 1

            current = current.next

        percovid = round(totalcovid/total,2)
        percovid70 = round(totalcovid70/total70,2)
        pernodose = round(totalnodose/total,2)
        pernodose70 = round(totalnodose70/total70,2)
        per1dose = round(total1dose/total,2)
        per2dose = round(total2dose/total,2)
        return (percovid,percovid70,pernodose,pernodose70,per1dose,per2dose)


    def merge(self,other):

        newcenter = HealthCenter()
        currentself = self._head
        currentother = other._head
        while currentself is not None or currentother is not None:
            if currentself is not None and currentother is not None:
                if currentself.elem.name < currentother.elem.name:
                    newcenter.addLast(currentself.elem)
                    currentself = currentself.next
                elif currentself.elem.name > currentother.elem.name:
                    newcenter.addLast(currentother.elem)
                    currentother = currentother.next
                else:
                    newcenter.addLast(currentself.elem)
                    currentself = currentself.next
                currentselfurrentother = currentother.next
            elif currentself is None:
                newcenter.addLast(currentother.elem)
                currentother = currentother.next
            else:
                newcenter.addLast(currentself.elem)
                currentself = currentself.next
        return newcenter

        #linear complecity (o(n)) CHECKED
    
    
    def minus(self,other):

        #Here we will use the skeleton of the merge function, with a few changes in order to make it more efficient
        #For example, once the whole 'other' centered has been traversed, we add every element left from the 'self' center
        #We can do this because, since we are gradually comparing the lists in an alphabetically sorted way, once a list is 
        #finished, no element of that list could be in other one that is yet to be concluded

        newcenter = HealthCenter()
        currentself = self._head
        currentother = other._head
        while currentself is not None:
            if currentother is not None:
                if currentself.elem.name < currentother.elem.name:
                    newcenter.addLast(currentself.elem)
                    currentself = currentself.next
                elif currentself.elem.name > currentother.elem.name:
                    currentother = currentother.next
                else:
                    currentself = currentself.next
                    currentselfurrentother = currentother.next
            else:
                newcenter.addLast(currentself.elem)
                currentself = currentself.next
        return newcenter

    
    def inter(self,other):

        #Again, we use the skeleton of the merge function when it comes to comparing.
        #However, here we are interested in adding the patients only when they exist in both centers
        #That is, the first two conditionals allow for the lists of patients to be visited in a sorted (ordered) way
        #so that we can find those occurences which exist in both, then add them to the new center.
        #In order to make the solution even MORE EFFICIENT, we stop whenever any of the 2 centers has been completely
        #explored. It is easy to see how at that point, taking the advantage of sorted traversing, no new patient
        #of the center still unfinished could have been also in the finished center.

        newcenter = HealthCenter()
        currentself = self._head
        currentother = other._head
        while currentself is not None and currentother is not None:
            if currentself.elem.name < currentother.elem.name:
                currentself = currentself.next
            elif currentself.elem.name > currentother.elem.name:
                currentother = currentother.next
            else:
                newcenter.addLast(currentself.elem)
                currentself = currentself.next
                currentselfurrentother = currentother.next
        return newcenter


if __name__ == '__main__':
    
    gst=HealthCenter('data/LosFrailes.tsv')
    print(gst)

    #Puedes añadir más llamadas a funciones para probarlas