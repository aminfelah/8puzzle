# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 21:15:42 2017

@author: Mikhail Berezovskiy
"""
  def __init__(self):
    #self.searchType = sys.argv[1]
    self.searchType = 'bfs'
    #self.initBoard = list(map(int, sys.argv[2].split(',')))
    self.initBoard = list(map(int, myboard.split(',')))
    self.frontier = Frontier(self.initBoard, self.searchType) 
  def __str__(self):
    return str(self.initBoard)

class Node(object):
  def __init__(self, board, parent):
    self.board = board
    self.nid = nodeid + 1
    if parent:
      self.depth = parent['depth'] + 1
      
    
class Frontier(object):
  def __init__(self, board, searchType):
    self.node = {
        "nid": 0,
        "board": board,
        "depth": 0,
        "zid": board.index(0),
        "parent": False
        }
    self.board = board
    self.q = deque([])
    self.path_to_goal = []
    self.nodes_expanded = 0
    self.search_depth = 0
    self.max_search_depth = 0
    self.running_time = 0
    self.max_ram_usage = 0
    self.initPosition = board.index(0)
    self.goal = [0,1,2,3,4,5,6,7,8]
    
  def check(self, node):
    print(node)
    if node['board'] == self.goal:
      return True
    else:
      return False

  def expand(self, node):
    '''
    input current state
    return updated Q
    '''
    parent = node
    depth = parent.depth+1
    z = node
    #up
    if 
    nid = self.nodeId + 1
    
  def run(self, node):
    if self.check(node):
      print('success')
      return self.success(node)
    elif len(self.q) == 0:
      return print('q is empty')
    else:
      self.expand(node)
      return self.run(self.q.pop(0))

  def success(self, node):
    return print('goal')

mySearch = SearchObj()
print(mySearch)
mySearch.frontier.run(mySearch.frontier.node)
