#@TODO find an efficient way to implement a tree. [DONE]
#@TODO write First function: calculate_price(part_list). [DONE]
#@TODO write Second function: required_parts(part_list). [DONE]
#@TODO write The third function: stock_check(part_list, stock_list). [DONE]

# Functions in order to exhaust partlist by Queue
def CreateQueue():
    """ Creates an empty Queue """
    return []

def Enqueue(item, Queue):
    """ Add item to the end (back) of the Queue """
    Queue.append(item)

def Dequeue(Queue):
    """ Remove and return the item at the front of the Queue """
    return Queue.pop(0)

def IsEmptyQueue(Queue):
    """ Check whether the Queue is empty """
    return Queue == []

# helper functions for creating an effective tree that will meet our needs.
# shows the children nodes of the tree
def children(tree): return tree[1:]

# gives the datum of the node
def datum(tree): return tree[0]

# shows the expected nodes of a node
def expected_nodes(node): return [x[1] for x in children(node)] if type(node[1]) == tuple else []

# creates node by covering square brackets
def createNode(datm): return [datm]


# Root is unique and one for every list and is distinguishable
def findRoot(lst):
    returnlist = lst[:]
    nodes = []
    for i in range(len(lst)):
        nodes.extend(expected_nodes(lst[i]))
    for i in range(len(lst)):
        if lst[i][0] not in nodes:
            root = lst[i]
            returnlist.pop(returnlist.index(lst[i]))
    return root,returnlist


# insert nodes
def insertNode(tree,val):
    """
    insert nodes recursively by taking values and comparing it to the parent.
    :param tree: stock tree
    :param val: node to appended to the tree
    :return: updated tree
    """
    if tree == []:
        tree.append(val)
    elif expected_nodes(val) and datum(tree)[0] in expected_nodes(val):
        val = createNode(val)
        val.append(tree)
        tree = val
        return tree
    elif expected_nodes(datum(tree)):
        if datum(val) in expected_nodes(datum(tree)):
            tree.append(createNode(val))
            return tree
        elif children(tree) != []:
            for c_index in range(len(children(tree))):
                children(tree)[c_index] = insertNode(children(tree)[c_index],val)
            return tree
    return tree


# in order to seek the expected nodes
def seek(tree,val):
    if  expected_nodes(datum(tree)) != False:
        current_expecting = expected_nodes(datum(tree))
    else:
        current_expecting = []
    #print(expected_nodes(datum(tree)))
    for child in children(tree):
        if expected_nodes(datum(child)) != False:
            current_expecting.extend(seek(child,val))
    return current_expecting


# make tree out of raw data
def treeify(partlist):
    """
    Makes tree out of at most 2 level depth of nested list.
    :param partlist: part-list to be entered
    :return: stock-tree
    """
    root,arranged = findRoot(partlist)
    treeQ = CreateQueue()
    for i in arranged:
        Enqueue(i,treeQ)
    tree = []
    tree = insertNode(tree,root)
    while not IsEmptyQueue(treeQ):
        item = Dequeue(treeQ)
        candidate = seek(tree,item)
        if datum(item) in candidate:
            #print("c",candidate == False)
            tree = insertNode(tree,item)
        elif datum(tree)[0] in seek(item,datum(tree)):
            tree = insertNode(item,tree)
        else:
            Enqueue(item,treeQ)
    return tree


# ancient_multiplier and count are initally zero due to " n * 0 = 0 "
def traverseTreeCost(tree,count = 1,requireds = []):
    """
    This function traverses the tree recursively by taking numbers of parts from ancestor,
    simultaneously working with count variable to obtain the final count number of leaf.
    :param tree: Part-list that is to be entered to programme
    :param count: increases by ancient_multiplier. Helper for the leaf count foundation.
    :param requireds: returns the required parts.
    :return: sum of all the prices according to the count numbers of their stocks
    """
    # empty list for required parts
    requireds = []
    # check if it is a leaf
    if type(datum(tree)[1]) == float:
        # return both count of required and the cost
        requireds.append((count,datum(tree)[0]))
        return (datum(tree)[1]*count,requireds)
    # initiate cost
    cost = 0
    # iterate over children recursively
    for child_index in range(len(children(tree))):
        for i in datum(tree)[1:]:
            # get the multiplier
            if datum(children(tree)[child_index])[0] == i[1]: ncount = i[0]*count
        # simply traverse the children with multiplier
        traverse = traverseTreeCost(children(tree)[child_index],ncount,requireds)
        # cumulatively add cost
        cost += traverse[0]
        # meanwhile append required parts
        requireds.extend(traverse[1])
    return (cost,requireds)


def traverseTreeStock(tree,stock,count = 1,requireds = []):
    """
    This function traverses the tree recursively by taking numbers of parts from ancestor,
    simultaneously working with count variable to obtain the final count number of leaf.
    :param stock:
    :param tree: Part-list that is to be entered to programme
    :param count: increases by ancient_multiplier. Helper for the leaf count foundation.
    :param requireds: returns the required parts.
    :return: sum of all the prices according to the count numbers of their stocks
    """
    # empty list for required parts
    requireds = []
    # check if it is a leaf
    if type(datum(tree)[1]) == float:
        # return both count of required and the cost
        #requireds.append((count,datum(tree)[0]))

        for item in stock:
            item_name = item[1]
            M = item[0]
            if item_name == datum(tree)[0]:
                req_name = datum(tree)[0]
                N = count
                if N > M:
                    requireds.append((req_name,N-M))
                    return (datum(tree)[1]*count,requireds)
                else:
                    return (datum(tree)[1]*count,requireds)
        else:
            requireds.append((datum(tree)[0],count))
        return (datum(tree)[1]*count,requireds)
    # initiate cost
    cost = 0
    # iterate over children recursively
    for child_index in range(len(children(tree))):
        for i in datum(tree)[1:]:
            # get the multiplier
            if datum(children(tree)[child_index])[0] == i[1]: ncount = i[0]*count
        # simply traverse the children with multiplier
        traverse = traverseTreeStock(children(tree)[child_index],stock,ncount,requireds)
        # cumulatively add cost
        cost += traverse[0]
        # meanwhile append required parts
        requireds.extend(traverse[1])
    return (cost,requireds)


# FIRST FUNCTION
############################## CALCULATE PRICE ################################
def calculate_price(part_list):
    # @TODO first make it tree: treeify() [DONE]
    tree = treeify(part_list)
    # @TODO second make traverse tree: calculate_price() -> actually traverses the tree [DONE]
    calculated_price = traverseTreeCost(tree)[0]
    # return calculated_price
    return calculated_price


# SECOND FUNCTION
############################# REQUIRED PARTS ################################
def required_parts(part_list):
    """
    In order to understand this function, we need to understand traverse function.
    Traverse function returns 2 values:
        1: calculated_price
        2: nested list of tuples containing required_parts
    However, this nested list must be flattened,therefore it undergoes a function called 'flatten' [recursive]

    :param part_list: part-list that is to be entered.
    :return: list of all the required parts.
    """
    # @TODO first make it tree: treeify() [DONE]
    tree = treeify(part_list)
    # @TODO second make traverse tree: required_parts() [DONE]
    # this returns a nested list like this :
    # [[(2, 'rim'), (2, 'spoke'), [(4, 'gear'), [(10, 'bolt'), (14, 'nut')]]], [(1, 'rearframe'), [(1, 'fork'), (2, 'handle')]]]
    requireds = traverseTreeCost(tree)[1] # raw state
    #print(required_parts_raw)
    # it undergoes a process of flattening
    # returning the value
    return requireds

# THIRD FUNCTION
############################# STOCK CHECK ################################
"""
def stock_check(part_list, stock_list):
    required = required_parts(part_list)
    check_result = []
    for req in required:
        N = req[0]
        req_name = req[1]
        for stock in stock_list:
            M = stock[0]
            stock_name = stock[1]
            if req_name == stock_name:
                if N > M:
                    check_result.append((req_name,N-M))
                    break
                else:
                    break
        else:
            check_result.append((req_name, req[0]))
    return check_result
"""

def stock_check(part_list, stock_list):
    tree = treeify(part_list)
    r = traverseTreeStock(tree,stock_list)[1]
    return r

