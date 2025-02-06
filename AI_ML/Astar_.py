graph={
    "S":[('A',3),('D',4)],
    "A":[('S',3),('D',5),('B',4)],
    "D":[('S',4),('A',5),('E',2)],
    "E":[('D',2),('B',5),('F',4)],
    "B":[('A',4),('E',5),('C',4)],
    "C":[('B',4)],
    "F":[('E',4),('G',3.5)],
    "G":[('F',3.5)]
}

heuristics={
    "S":11.5,
    "A":10.1,
    "D":9.2,
    "B":5.8,
    "E":7.1,
    "F":3.5,
    "C":3.4,
    "G":0
}

start_node="S"
goal_node="G"
goal_reached=0
frontier=[(heuristics[start_node]),0,[start_node]]
cost_so_far={start_node:0}

while frontier:
    estimated_cost,current_cost,path=heapq.heappop(frontier)
    current_node=path[-1]
    if current_node==goal_node:
        print("path ",path)
        print("total cost",current_cost)
        goal_reached=1
        break
    for neighbor,cost in graph[current_cost]:
        new_cost=current_cost+cost
        if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
            new_cost=cost_so_far[neighbor]
            priority=new_cost+heuristics[neighbor]