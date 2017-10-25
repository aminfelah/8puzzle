# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 20:16:36 2017

@author: Mikhail Berezovskiy
"""

'''
input: search type,  board square 3x3 with numbers from 0-8
output: write txt file:
    path_to_goal: the sequence of moves taken to reach the goal
    cost_of_path: the number of moves taken to reach the goal
    nodes_expanded: the number of nodes that have been expanded
    search_depth: the depth within the search tree when the goal 
        node is found
    max_search_depth:  the maximum depth of the search tree in the 
    lifetime of the algorithm
    running_time: the total running time of the search instance, 
        reported in seconds
    max_ram_usage: the maximum RAM usage in the lifetime of the process 
        as measured by the ru_maxrss attribute in the resource module, 
        reported in megabytes

'''
import sys
import time
    
from collections import deque

class Node(object):
  def __init__(self, board, parentNode, action):
    self.boardId = ','.join(board)
    self.board = board
    self.h = 0
    if parentNode == False:
      self.parent = False
      self.depth = 0
      self.action = ''
    else:
      self.parent = parentNode
      self.depth = parentNode.depth + 1
      self.action = action
  def __str__(self):
    return self.boardId

class Frontier(object):
  def __init__(self, initNode, searchType):
    self.initNode = initNode
    self.searchType = searchType
    self.expSet = set([initNode.boardId])
    self.expNodes = [initNode]
    if searchType != 'ast':
        self.q = deque([initNode])
    else:
        self.q = [(initNode.h,initNode)]
    self.path_to_goal = []
    self.nodes_expanded = 0
    self.search_depth = 0
    self.max_search_depth = 0
    self.t0 = time.process_time()
    self.running_time = 0
    self.max_ram_usage = 0
    self.goal = '0,1,2,3,4,5,6,7,8'
    self.goalFound = False
    
  def run(self):
    #check initial state == goal
    if self.initNode.boardId == self.goal:
      return self.success(self.initNode)
    #run search
    while len(self.q)>0:
      #get node from queue and expand
      #bfs
      if self.searchType == 'bfs':
        node = self.q.popleft()
      #dfs
      elif self.searchType == 'dfs':
        node = self.q.pop()
      #ast
      elif self.searchType == 'ast':
        node = self.q.pop(0)[1]
      #check goal
      self.check(node)
      if self.goalFound:
        return
    #no solution?
    return print ('no solution')
  
  def check(self, node):
    if node.boardId == self.goal:
      self.goalFound = True
      return self.success(node)
    else:
      self.nodes_expanded = self.nodes_expanded + 1
      self.expNodes.append(node)
      return self.expandNodes(node)
    
  def expandNodes(self, node):
    b = node.board
    z = node.board.index('0')
    #check Up,Down,Left,Right neighbor nodes
    #bfs
    if self.searchType == 'bfs' or self.searchType == 'ast':
      if z-3 >= 0: self.addNewNode(Node(self.swap(b, z, z-3), node, 'Up'))
      if z+3 <= 8: self.addNewNode(Node(self.swap(b, z, z+3), node, 'Down'))
      if z%3-1 >= 0: self.addNewNode(Node(self.swap(b, z, z-1), node, 'Left'))
      if z%3+1 < 3: self.addNewNode(Node(self.swap(b, z, z+1), node, 'Right'))
    #dfs
    elif self.searchType == 'dfs':
      if z%3+1 < 3: self.addNewNode(Node(self.swap(b, z, z+1), node, 'Right'))
      if z%3-1 >= 0: self.addNewNode(Node(self.swap(b, z, z-1), node, 'Left'))
      if z+3 <= 8: self.addNewNode(Node(self.swap(b, z, z+3), node, 'Down'))
      if z-3 >= 0: self.addNewNode(Node(self.swap(b, z, z-3), node, 'Up'))
      
  def addNewNode(self, newNode):
    #check if node is explored
    if newNode.boardId not in self.expSet:
      self.expSet.add(newNode.boardId)
      if self.searchType != 'ast':
        self.q.append(newNode)
      else:
        if newNode.boardId == self.goal:
          self.goalFound = True
          return self.success(newNode)
        newNode = self.heuristic(newNode)
        self.q.append((newNode.h+newNode.depth, newNode))

        self.q.sort(key=lambda tup: tup[0])
      #check max depth condition
    if newNode.depth >= self.max_search_depth:
        self.max_search_depth = newNode.depth
  
  def heuristic(self, node):
    #heuristic function, Manhattan distance
    #return node with h(n) value
    for i in range(len(node.board)):
        dX = abs(int(i/3) - int(int(node.board[i])/3))
        dY = abs(i % 3 - int(node.board[i]) % 3)
        d = dX + dY
        node.h = d + node.h
    return node
  
  def swap(self, board, z, new):
    newBoard = board[:]
    newBoard[z] = board[new]
    newBoard[new] = '0'
    return newBoard

  def success(self, node):
    successfulPath = self.getPathToGoal(node)
    
    print ('path to goal:', successfulPath)
    print ('cost of path:', len(successfulPath))
    print ('nodes_expanded:', self.nodes_expanded)
    print ('depth:', node.depth)
    print ('max_search_depth', self.max_search_depth)
    print ('running_time', time.process_time() - self.t0)
    
    #file writing
    f = open('output.txt', 'w')
    f.write('path_to_goal: ' + str(successfulPath) + '\n')
    f.write('cost_of_path: ' + str(len(successfulPath)) + '\n')
    f.write('nodes_expanded: ' +  str(self.nodes_expanded) + '\n')
    f.write('search_depth: ' + str(node.depth) + '\n')
    f.write('max_search_depth: ' + str(self.max_search_depth) + '\n')
    f.write('running_time: ' + str(time.process_time() - self.t0) + '\n')
    
    #memory usage
    if sys.platform == "win32":
        import psutil
        self.max_ram_usage = psutil.Process().memory_info().rss/1024/1024
    else:
        # Note: if you execute Python from cygwin,
        # the sys.platform is "cygwin"
        # the grading system's sys.platform is "linux2"
        import resource
        self.max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024/1024
    print ('max_ram_usage:', self.max_ram_usage)
    f.write('max_ram_usage: ' + str(self.max_ram_usage))
    
    #f.write('running_time: ' + self.running_time)
    
    f.close
  
  def getPathToGoal(self,node):
    while node.parent:
      self.path_to_goal.append(node.action)
      node = node.parent
    self.path_to_goal.reverse()
    return self.path_to_goal


##initialize
if len(sys.argv)>1:
    myboard = sys.argv[2]
    searchType = sys.argv[1]
else:
    #myboard = '8,6,7,2,5,4,3,0,1'
    myboard = '1,2,5,3,4,0,6,7,8'
    #myboard = '0,1,2,3,4,5,6,7,8'
    #myboard = '0,2,1,3,4,5,6,7,8'
    #myboard = '6,1,8,4,0,2,7,3,5'
    #myboard = '6,1,8,4,0,2,7,3,5'
    #myboard =  '6,1,8,4,0,2,7,3,5'
    #myboard = '8,6,4,2,1,3,5,7,0'
    searchType = 'ast'

b = myboard.split(',')
initNode = Node(b, False, '')
myFrontier = Frontier(initNode, searchType)
myFrontier.run()

    