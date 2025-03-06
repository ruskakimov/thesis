%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% MiniZinc model: Topological Order with Non-Overlapping Edges
%
% Decision Variables:
%   - pos[i] : The position (from 1 to n) of node i.
%   - page[j] : A Boolean for edge j.
%
% Instance parameters (in a .dzn file):
%   - n : number of nodes.
%   - m : number of edges.
%   - edge_from[1..m] : For each edge j, the source node.
%   - edge_to[1..m]   : For each edge j, the target node.
%
% Constraints:
%   1. All positions are different.
%   2. Topological order: For every edge (u,v), pos[u] < pos[v].
%   3. Non-overlapping edges: For any two edges (u,v) and (w,x) 
%      with all four endpoints distinct, if they are on the same page,
%      then they may not “cross” (i.e., it cannot be that
%         pos[u] < pos[w] < pos[v] < pos[x]  OR
%         pos[w] < pos[u] < pos[x] < pos[v]).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
include "globals.mzn";

% Instance parameters (provided in a .dzn file)
int: n;
int: m;
array[1..m] of int: edge_from;
array[1..m] of int: edge_to;

% Decision variables
array[1..n] of var 1..n: pos;
array[1..m] of var bool: page;

% Constraint 1: All positions must be different.
constraint all_different(pos);

% Constraint 2: Topological order for every edge.
constraint forall(i in 1..m)(
    pos[ edge_from[i] + 1 ] < pos[ edge_to[i] + 1 ]
);

% Constraint 3: Non-overlapping edges.
% For any two distinct edges (i, j) with all endpoints distinct, 
% if they are on the same page, then they must not "overlap".
%
% Overlap is defined as either:
%   (pos[u] < pos[w] < pos[v] < pos[x])  OR
%   (pos[w] < pos[u] < pos[x] < pos[v]),
% where for edge i: u = edge_from[i], v = edge_to[i],
% and for edge j: w = edge_from[j], x = edge_to[j].
constraint forall(i, j in 1..m where i < j)(
  if ( edge_from[i] != edge_from[j] /\ edge_from[i] != edge_to[j] /\
       edge_to[i]   != edge_from[j] /\ edge_to[i]   != edge_to[j] )
  then
    ( page[i] = page[j] ) ->
      not(
         ( pos[ edge_from[i]+1 ] < pos[ edge_from[j]+1 ] /\
           pos[ edge_from[j]+1 ] < pos[ edge_to[i]+1 ]   /\
           pos[ edge_to[i]+1 ]   < pos[ edge_to[j]+1 ] )
       \/
         ( pos[ edge_from[j]+1 ] < pos[ edge_from[i]+1 ] /\
           pos[ edge_from[i]+1 ] < pos[ edge_to[j]+1 ]   /\
           pos[ edge_to[j]+1 ]   < pos[ edge_to[i]+1 ] )
      )
  else
    true
  endif
);

solve satisfy;

output [
  "Node Positions (node -> pos):\n" ++ 
  concat([ "Node " ++ show(i) ++ " -> " ++ show(pos[i]) ++ "\n" | i in 1..n ]) ++
  "\nEdge Pages (edge: from -> to):\n" ++
  concat([ "Edge " ++ show(i) ++ " (" ++ show(edge_from[i]) ++ " -> " ++ show(edge_to[i]) ++ "): " ++ show(page[i]) ++ "\n" | i in 1..m ])
];
