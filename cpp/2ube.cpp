#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include "ortools/sat/cp_model.h"

using namespace operations_research;
using namespace operations_research::sat;

std::pair<std::vector<int>, std::vector<int>> solve(int n, const std::vector<std::pair<int, int>>& edges) {
    // Create the model
    CpModelBuilder model;
    int m = edges.size();

    // Variables
    std::vector<IntVar> pos_of_node;
    std::vector<BoolVar> page_of_edge;

    for (int i = 0; i < n; i++) {
        pos_of_node.push_back(model.NewIntVar(Domain(0, n - 1))); // Fix: Use Domain
    }

    for (int i = 0; i < m; i++) {
        page_of_edge.push_back(model.NewBoolVar());
    }

    // All-Different constraint for positions
    model.AddAllDifferent(pos_of_node);

    // Constraints for directed edges
    for (const auto& edge : edges) {
        model.AddLessThan(pos_of_node[edge.first], pos_of_node[edge.second]);
    }

    const CpSolverResponse response = Solve(model.Build());

    if (response.status() == CpSolverStatus::OPTIMAL || response.status() == CpSolverStatus::FEASIBLE) {
        std::cout << "Solution found:" << std::endl;
        std::vector<std::pair<int, int>> node_positions;
        for (int i = 0; i < n; i++) {
            node_positions.emplace_back(i, SolutionIntegerValue(response, pos_of_node[i]));
        }

        std::sort(node_positions.begin(), node_positions.end(), [](const auto& a, const auto& b) {
            return a.second < b.second;
        });

        std::vector<int> order;
        std::vector<int> pages;
        for (const auto& node : node_positions) {
            order.push_back(node.first);
        }

        for (const auto& page : page_of_edge) {
            pages.push_back(SolutionIntegerValue(response, page));
        }

        return {order, pages};
    } else {
        std::cout << "No solution found." << std::endl;
        return {{}, {}};
    }
}

int main() {
    int n = 10;  // Grid size
    std::vector<std::pair<int, int>> edges;

    // Generate edges for a 10x10 directed grid graph
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int node = i * n + j; // Convert (i, j) to a node index

            if (j + 1 < n) { // Edge pointing right
                edges.emplace_back(node, node + 1);
            }
            if (i + 1 < n) { // Edge pointing down
                edges.emplace_back(node, node + n);
            }
        }
    }

    auto result = solve(n * n, edges);

    std::cout << "Order: ";
    for (int node : result.first) {
        std::cout << node << " ";
    }
    std::cout << std::endl;

    std::cout << "Pages: ";
    for (int page : result.second) {
        std::cout << page << " ";
    }
    std::cout << std::endl;

    return 0;
}
