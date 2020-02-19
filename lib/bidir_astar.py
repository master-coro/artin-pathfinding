# -*- coding: utf-8 -*-

'''
@author : Erwin Lejeune <erwin.lejeune15@gmail.com>
@date : 28/01/2020
@brief : astar implementation
'''


from lib.world import World
from lib.node import Node
from lib.astar import AStar
from sys import stdout


class TwoWayAStar(AStar):
    def __init__(self, start, target, allow_diagonals, World):
        self.first_dir = AStar(start, target, allow_diagonals, World)
        self.second_dir = AStar(target, start, allow_diagonals, World)

        self.reached = False
        self.path = []

    def shortest_path(self):
        while self.first_dir.open_nodes and self.second_dir.open_nodes:
            self.first_dir.open_nodes.sort()
            self.second_dir.open_nodes.sort()
            first_dir_node = self.first_dir.open_nodes[0]
            second_dir_node = self.second_dir.open_nodes[0]

            if first_dir_node.tile_pos == second_dir_node.tile_pos:
                self.reached = True
                self.meeting = first_dir_node
                self.path = self.reconstruct_path(first_dir_node)
                break

            else:
                self.first_dir.closed_nodes.append(
                    self.first_dir.open_nodes.pop(0))
                self.second_dir.closed_nodes.append(
                    self.second_dir.open_nodes.pop(0))

                first_successors = first_dir_node.successors()
                second_successors = second_dir_node.successors()

                for first_s_node in first_successors:
                    if first_s_node in self.first_dir.open_nodes:
                        first_chosen_one = self.first_dir.open_nodes.pop(
                            self.first_dir.open_nodes.index(first_s_node))

                        if first_s_node.g_cost < first_chosen_one.g_cost:
                            self.first_dir.open_nodes.append(first_s_node)
                        else:
                            self.first_dir.open_nodes.append(first_chosen_one)

                    elif first_s_node not in self.first_dir.closed_nodes:
                        self.first_dir.open_nodes.append(first_s_node)

                for second_s_node in second_successors:
                    if second_s_node in self.second_dir.open_nodes:
                        second_chosen_one = self.second_dir.open_nodes.pop(
                            self.second_dir.open_nodes.index(second_s_node))

                        if second_s_node.g_cost < second_chosen_one.g_cost:
                            self.second_dir.open_nodes.append(second_s_node)
                        else:
                            self.second_dir.open_nodes.append(
                                second_chosen_one)

                    elif second_s_node not in self.second_dir.closed_nodes:
                        self.second_dir.open_nodes.append(second_s_node)

        if not(self.reached):
            stdout.write("\033[;1m" + "\033[1;31m")
            stdout.write(
                '========================! NO PATH FOUND !=========================')
            stdout.write("\033[0;0m")

    def reconstruct_path(self, node):
        first_path = self.first_dir.reconstruct_path(node)
        print(first_path)
        second_path = self.second_dir.reconstruct_path(node)
        print(second_path)
        second_path.reverse()
        path = first_path + second_path

        return(path)

    def path_info(self):
        if self.reached:
            print("\nGoal reached.")

            stdout.write("Using Bidirectional A*, the shortest path between < TILE = " +
                         str(self.first_dir.start.tile_pos) + " > and < TILE = " +
                         str(self.first_dir.target.tile_pos) + " > is ")
            stdout.write("\033[1;31m")
            stdout.write("|| " + str(len(self.path)) + " ||\n\n")
            stdout.write("\033[0;0m")

        else:
            print("\n\nNo path info...\n")