#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlrd
import pprint
import numpy as np
import matplotlib.pyplot as plt

DATADIR = "TempD.xlsx" # TempD.xlsx是路网的连接图，里面存储着网络节点的道路连接情况
FAST_POINT = ['J01','J02','J03','J04','J05','J06','J07','J08','J09','J10','J11','J12','J13','J14','J15','J16','J17','J18','J19']

def parse_file(datafile):
	workbook = xlrd.open_workbook(datafile)
	# read the first sheet of the datafile
	sheet = workbook.sheet_by_index(0)

	# obtain the all value in sheet
	data = [[sheet.cell_value(r, col)
				for col in range(sheet.ncols)]
					for r in range(sheet.nrows)]
	return data

graphs_table = parse_file(DATADIR)

location = parse_file("location.xls") # location.xls 中记录着路网中各节点的位置信息

for index, point in enumerate(location):
	if point[0] == '' or index == 0:
		location.remove(point)

def table_to_diction(table):
	graph = {}
	for index, point in enumerate(table[:][0]):
		if index > 0:
			graph[table[index][0]] = []
	for index, pointx in enumerate(table[:][0]):
		if index == 0:
			continue
		for j, value in enumerate(table[index][index+1:]):
			if value != '':
				graph[table[index][0]].append(table[index+1+j][0])
				graph[table[index+1+j][0]].append(table[index][0])
	return graph

graphs = table_to_diction(graphs_table) # 将道路连接信息以字典形式记录


def compute_ranks_simple(graph):
	# RageRank算法，阻尼系数取为0.8，迭代20次

    d = 0.8 # damping factor
    numloops = 20
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages

            for point in graph[page]:
            	weight_page = len(graph[point])
            	newrank += 1.0 * d * ranks[point] / weight_page

            newranks[page] = newrank
        ranks = newranks
    return ranks


def compute_ranks(graph):
	# 考虑主干道路节点与其它道路节点的共别，而改进的RageRank算法，
	# 阻尼系数取为0.8，迭代20次。
    d = 0.8 # damping factor
    numloops = 20
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    # print ranks
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages

            for point in graph[page]:
            	weight_page = len(graph[point])
            	for p in graph[point]:
            		if p in FAST_POINT:
	            		weight_page += 1

            	if page in FAST_POINT:
            		newrank += 2.0 * d * ranks[point] / weight_page
            	else:
            		newrank += 1.0 * d * ranks[point] / weight_page
            newranks[page] = newrank
        ranks = newranks
    return ranks


def test_compute_ranks():
	"""测试函数，会以验证PageRank算法程序的正确性"""
	graph = {'a':['b','c'], 'b':['a','c','d','e'],'c':['a','d'],'d':['b'],'e':['b']}
	rank = compute_ranks_first_version(graph)
	print rank, sum([rank[i] for i in rank])

# test_compute_ranks()


def find_top_three(rank):
	"""已知各节点的重要性，找出重要性最高的三个"""
	top_three_important = [0, 0, 0]
	top_three_point = [0, 0, 0]
	for point in rank:
		if rank[point] > min(top_three_important):
			min_index = top_three_important.index(min(top_three_important))
			top_three_important[min_index] = rank[point]
			top_three_point[min_index] = point

	return top_three_point, top_three_important


def plot_importance(location, graphs, rank, top_three=0):
	location_x = []
	location_y = []
	size = []
	for point in location:
		location_x.append(point[1])
		location_y.append(point[2])
		size.append(rank[point[0]])

	min_size = min(size)
	for i in range(0,len(size)):
		size[i] = 2.5**(size[i]/min_size)
	plt.scatter(location_x, location_y, s=size)

	location_dic = {}
	for point in location:
		location_dic[point[0]] = point[1:]

	if top_three != 0:
		for top_point in top_three:
			plt.plot(location_dic[top_point][0], location_dic[top_point][1], 'ro',markersize=np.sqrt(200.))

	for point in graphs:
		plt.annotate(point, (location_dic[point][0], location_dic[point][1]))
		for another_point in graphs[point]:
			if point in FAST_POINT and another_point in FAST_POINT:
				plt.plot([location_dic[point][0], location_dic[another_point][0]],[location_dic[point][1], location_dic[another_point][1]], 'r')
			else:
				plt.plot([location_dic[point][0], location_dic[another_point][0]],[location_dic[point][1], location_dic[another_point][1]], 'b')
	plt.show()



def main(compute_ranks, graphs, location):
	rank = compute_ranks(graphs)
	top_three_point, top_three_important = find_top_three(rank)
	for x in rank:
		print x, rank[x]
	print top_three_point, top_three_important
	plot_importance(location, graphs, rank, top_three_point)

# 利用PageRank算法计算道路节点的重要性，并画出图形
main(compute_ranks_simple, graphs, location)
print 
# 利用改进的PageRank算法计算道路节点的重要性，并画出图形
main(compute_ranks, graphs, location)
