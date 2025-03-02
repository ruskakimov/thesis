int: n; % nodes
int: k; % obstacles
int: s; % start
int: t; % goal

array[1..n, 1..n] of bool: adj;
array[1..n, 1..k] of bool: cover;

% Decision variables
array[1..n] of var 0..n: visited_at; % visit time
array[1..k] of var bool: removed; % removed obstacles

constraint visited_at[s] = 1;
constraint visited_at[t] > 1;

% Has neighbour with earlier visit time (except the start)
constraint forall (vi in 1..n diff {s}) (
  visited_at[vi] > 0 -> exists(vj in 1..n where adj[vi, vj]) (visited_at[vj] = visited_at[vi] - 1 /\ visited_at[vj] > 0)
);

% Activate touched obstacles
constraint forall (v in 1..n) (
  visited_at[v] > 0 -> forall(o in 1..k where cover[v, o] = true) (removed[o] = true)
);

solve minimize sum(removed);