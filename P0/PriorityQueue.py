import heapq
'''Oi dieukriniseis vriskontai sto PDF.'''

class PriorityQueue:
   
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):        
        heapq.heappush(self.heap, (priority, item))	
        self.count += 1

    def pop(self):
		if  len(self.heap) == 0:
		   return "Empty Heap"
		return heapq.heappop(self.heap)[1]	#Returns the item with lowest priority.
       
    def isEmpty(self):
        return len(self.heap) == 0
		
    def update(self, item, priority):
        for p,it in self.heap:
          #it=self.heap
          #print it, p		   
          if it == item:
            index = [y[1] for y in self.heap].index(it)		   
            #print "index= ", index
            if p<= priority:
               break
            #else: 
            			 
            del self.heap[index]			
            self.heap.append((priority, item))
            heapq.heapify(self.heap)		 
            break  
        else:
           #print "push called!"		
           self.push(item,priority)		
        		   
  
def PQSort(intList):
  
  if len(intList) == 0:
    print "Empty List"
    return None
  
  q = PriorityQueue()
  inorder = []
  
  for i in intList:
    q.push(i,i)
    
  for j in intList:	
    t=q.pop()
    inorder.append(t)
    #print t
  #print 'inorder :', inorder
  return inorder


if __name__ == "__main__":
	q = PriorityQueue()
	q.push("task1", 3)
	q.push("task0", 1)
	q.push("task2", 4)
	q.push("task2", 5)
	
	q.update("task2",2)
	
	t=q.pop()
	print t
	t=q.pop()	
	print t
	t=q.pop()
	print t
	t=q.pop()
	print t
	t=q.pop()
	print t
	
	print q.isEmpty()
	
	print "---SORT---"
	lista = [1000, 20, 12, 43, 05, 126, 437, -12, 20 ];
	lis = [];	
	print PQSort(lista)