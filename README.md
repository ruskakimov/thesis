Compile /cpp

```
g++ -std=c++17 -I/usr/local/or-tools/include \
    -L/usr/local/or-tools/lib \
    -lortools -o sample sample.cpp
```

To run SAT solver, execute the following command with the CNF of your choice:

```
time ./solvers/kissat --quiet [path_to_cnf_file]
```

---

Benchmark files are `.csv` files with the following columns:

- `graph` - name of the graph (type and number of nodes separated by an underscrore)
- `fang_projection` - is a real performance of [Fang's algorithm (2018)](https://arxiv.org/pdf/1003.3045) or a calculated projection
  - The paper only works with trees, therefore only tree graphs receive a projection
- `[solver_name]` - column for a particular solver

> Fang's algorithm projected time is calculated using this formula:
> `seconds = 1.16^n * k / 1000`
> Where: `k = 0.0583 / (1.16 ** 30)` and `n` is a number of nodes.
>
> _The projection calculated for known `n` closely matches the recorded timings in the paper._

All timings are recorded in seconds. If the graph was not solved in a reasonable amount of time, a descriptive string can be given instead.

---

`.graph` file example:

```
3
1 2
3 2
```

First line is `n`, the number of nodes/vertices. Following lines are edges `u v` where `u` and `v` fall in the range `[0, n-1]`.

---

Run `sat_encode_graphs.py` script with PyPy for a significant speed boost.

Run it as a module for imports to work:
`pypy3 -m scripts.sat_encode_graphs`
