from manimlib import *
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class PreferentialAttachmentDynamicGraph(Scene):
    def construct(self):
        # Initialize the graph
        initial_nodes = 5
        total_nodes = 100
        m_edges = 2  # New edges per node

        G = nx.empty_graph(initial_nodes)
        pos = nx.kamada_kawai_layout(G)  # More organic layout

        # Draw initial nodes and edges
        node_circles = {}
        edge_lines = {}

        for node in G.nodes():
            x, y = pos[node]
            circle = Circle(radius=0.1).move_to([x * 3, y * 3, 0])
            circle.set_fill(BLUE, opacity=0.8)
            node_circles[node] = circle
            self.add(circle)

        self.wait(1)

        # Add new nodes dynamically
        for new_node in range(initial_nodes, total_nodes):
            G.add_node(new_node)

            # Connect preferentially based on degree
            targets = list(G.nodes())[:-1]
            degrees = np.array([G.degree(t) for t in targets])
            probabilities = degrees / degrees.sum() if degrees.sum() > 0 else np.ones(len(degrees)) / len(degrees)

            connected_nodes = np.random.choice(targets, size=m_edges, replace=False, p=probabilities)

            for target in connected_nodes:
                G.add_edge(new_node, target)

            # Update node positions using Kamada-Kawai layout for a more natural spread
            pos = nx.kamada_kawai_layout(G)

            # Add and animate new node
            x, y = pos[new_node]
            node_size = 0.1 + 0.02 * G.degree(new_node)
            new_circle = Circle(radius=node_size).move_to([x * 3, y * 3, 0])
            new_circle.set_fill(RED, opacity=0.8)
            node_circles[new_node] = new_circle
            self.play(GrowFromCenter(new_circle), run_time=0.3)

            # Add dynamically updating edges
            for target in connected_nodes:
                def create_edge_func(source_circle, target_circle):
                    return lambda: Line(
                        source_circle.get_center(),
                        target_circle.get_center(),
                        color=WHITE,
                        stroke_width=1.5
                    )

                edge = always_redraw(create_edge_func(node_circles[new_node], node_circles[target]))
                edge_lines[(new_node, target)] = edge
                self.add(edge)

            # Animate node movements based on updated positions
            animations = []
            for node in G.nodes():
                x, y = pos[node]
                new_position = np.array([x * 3, y * 3, 0])
                node_size = 0.1 + 0.02 * G.degree(node)
                animations.append(
                    node_circles[node].animate.move_to(new_position).scale(node_size / node_circles[node].get_width())
                )

            # Play animation for node and edges together
            self.play(*animations, run_time=0.5)

        self.wait(2)

        # Plot the power-law degree distribution using matplotlib
        self.plot_degree_distribution(G)

    def plot_degree_distribution(self, G):
        # Calculate degree frequency
        degrees = [G.degree(n) for n in G.nodes()]
        degree_count = Counter(degrees)
        deg, cnt = zip(*sorted(degree_count.items()))  # Sort by degree for a proper line plot

        # Plot degree distribution on a log-log scale as a line graph
        plt.figure(figsize=(8, 6))
        plt.plot(deg, cnt, color='blue', marker='o', linestyle='-', linewidth=2)
        plt.xscale('log')
        plt.yscale('log')
        plt.title("Power-Law Degree Distribution (Line Plot)")
        plt.xlabel("Degree (log scale)")
        plt.ylabel("Frequency (log scale)")
        plt.grid(True, which="both", linestyle='--', linewidth=0.5)
        plt.show()
