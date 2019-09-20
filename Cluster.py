#Importing libs
import random
from mpi4py import MPI
import time
#

#Defining funcs
def selectionSort(alist):

   for i in range(len(alist)):

      # Find the minimum element in remaining
       minPosition = i
       #

       for j in range(i+1, len(alist)):
           if alist[minPosition] > alist[j]:
               minPosition = j
                
       # Swap the found minimum element with minPosition       
       temp = alist[i]
       alist[i] = alist[minPosition]
       alist[minPosition] = temp
       #

   return alist

def sortCluster():
    if rank == 0: 
        #Create list
        data = random.sample(range(0,100000000),100000000)
        print ('Scattering data',data)
        #
    else:
        data = None
    
    #Broadcast data to every node
    data = comm.bcast(data,root=0)
    print ('Rank',rank,'has data: ', data)
    #
    
    #Define pivots
    increment = data.length/4
    pivot1 = increment
    pivot2 = pivot1 + increment
    pivot3 = pivot2 + increment
    #
    
    #Creating prepared lists for selectionSort, each node will have a part of
    #the data
    if rank ==0:
        data = [x for x in data if x < pivot1]
    if rank ==1:
        data = [x for x in data if pivot1 <= x and x<= pivot2]
    if rank == 2:
        data = [x for x in data if pivot2 <= x and x<= pivot3]
    if rank == 3:
        data = [x for x in data if x > pivot3]
    #
    
    #Now each node has a part of data and its ordered with the pivots

    #Start the time for sorting
    start_time = time.time()
    #
    
    #Sort the data
    data = selectionSort(data) 
    print ('rank',rank,'has sorted data: ',data)
    #
    
    #Gather all data into a new array
    new_data = comm.gather(data, root=0)
    if rank == 0:
        print  ('master collected: ', new_data)
    print("--- %s elapsed time ---" % (time.time() - start_time))
    #
    

def present():
    if rank == 0:
        print("I'm the master e o node ",rank)
    elif rank ==1:
        print("I'm the node",rank)
    elif rank == 2:
        print("I'm the node ",rank)
    elif rank == 3:
        print("I'm the node ",rank)

def sortOne():
    if rank == 0: 
        data = np.random.randint(1,20001,20000)
        print ('Rank: ',rank,'has the array: ',data)
        startTimeSolo = time.time()
        data = selectionSort(data)  
        print ('Rank: ',rank,'has the sorted: ',data)
        tempoSolo = (time.time() - startTimeSolo)
        print("--- %s elapsed time ---" % tempoSolo)
        
def TimeCompare():
    print("Sorting with one raspberry")
    sortOne()
    print("Sort using the cluster")
    sortCluster()
    comp = tempoCluster/tempoSolo
    print ("Has a gain of {:.1%}".format(comp))
    
    
    
def menu():
    print("")
    print("--------------MENU--------------")
    print('''Hello, what would you like to do?
      1 - Meet the cluster
      2 - Sort using the cluster
      3 - Sort using only one raspberry
      4 - Time comparison
      5 - Leave
      ''')
    op = int(input("Choice: "))
    if op == 1:
        present()
        menu()
    if op ==2:
        sortCluster()
        menu()
    if op ==3:
        sortOne()
        menu()
    if op ==4:
        TimeCompare()
        menu()
    if op == 5:
        print("Thanks for the attention")
#      
        
#Global variables        
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
tempoSolo = 0
tempoCluster = 0
#
  
menu()























        
    
    

    
