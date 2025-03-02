int: n; % nodes
int: k; % obstacles
int: s; % start
int: t; % goal

% array[1..m, 1..2] of 1..n: edges = [| 1, 2 | 1, 3 | 2, 4 | 3, 4 |];

array[1..n, 1..n] of bool: adj;
array[1..n, 1..k] of bool: cover;

% Decision variables
array[1..n] of var 0..n: visited_at; % visit time
array[1..k] of var bool: removed; % removed obstacles

constraint visited_at[s] = 1;
constraint visited_at[t] > 1;

% Visit previous node
constraint forall (vi in 1..n diff {s}) (
  visited_at[vi] > 0 -> exists(vj in 1..n where adj[vi, vj]) (visited_at[vj] = visited_at[vi] - 1)
);

% constraint (visited_at[4] > 0) -> ((visited_at[3] == visited_at[4] - 1) \/ (visited_at[2] == visited_at[4] - 1));
% constraint (visited_at[3] > 0) -> ((visited_at[4] == visited_at[3] - 1) \/ (visited_at[1] == visited_at[3] - 1));
% constraint (visited_at[2] > 0) -> ((visited_at[4] == visited_at[2] - 1) \/ (visited_at[1] == visited_at[2] - 1));

% Activate touched obstacles
constraint forall (v in 1..n) (
  visited_at[v] > 0 -> forall(o in 1..k where cover[v, o] = true) (removed[o] = true)
);
% constraint (visited_at[1] > 0) -> removed[1];
% constraint (visited_at[2] > 0) -> (removed[1] /\ removed[2]);
% constraint (visited_at[3] > 0) -> removed[1];
% constraint (visited_at[4] > 0) -> removed[3];

solve minimize sum(removed);

% output ["visited: \(visited_at)\n", "removed: \(sum(removed))\n"];