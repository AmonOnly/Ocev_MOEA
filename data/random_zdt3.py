
#!/usr/bin/env python3
"""Random Search for ZDT3 (Random Search)
Generates num_evals random candidate solutions and keeps all non-dominated solutions found.
Run: python3 random_zdt3.py --pop 100 --gen 250 --runs 10

This script follows the report spec: number of evaluations = pop_size * generations
"""

import argparse, random, math
random.seed(0)

def zdt1(x):
    n = len(x)
    x_real = [xi / 1000.0 for xi in x]
    f1 = x_real[0]
    g = 1.0 + 9.0 * sum(x_real[1:]) / (n - 1)
    h = 1.0 - math.sqrt(f1 / g)
    f2 = g * h
    return (f1,f2)

def zdt3(x):
    n = len(x)
    f1 = x[0]
    g = 1.0 + 9.0 * sum(x[1:]) / (n - 1)
    h = 1.0 - math.sqrt(f1 / g) - (f1 / g) * math.sin(10 * math.pi * f1)
    f2 = g * h
    return (f1,f2)

def dominates(a,b):
    return (a[0] <= b[0] and a[1] <= b[1]) and (a[0] < b[0] or a[1] < b[1])

def update_nondominated(nd_set, cand):
    non_dom = []
    dominated = False
    for p in nd_set:
        if dominates(p, cand):
            dominated = True
            break
        if not dominates(cand, p):
            non_dom.append(p)
    if not dominated:
        non_dom.append(cand)
    return non_dom

def random_search(problem, n_var, num_evals):
    nd = []
    for _ in range(num_evals):
        if problem=='zdt1':
            x = [random.randint(0,1000) for _ in range(n_var)]
            obj = zdt1(x)
        else:
            x = [random.random() for _ in range(n_var)]
            obj = zdt3(x)
        nd = update_nondominated(nd, obj)
    return nd

def hypervolume(front, ref_point):
    pts = sorted(front, key=lambda x: x[0], reverse=True)
    hv = 0.0
    last_f1 = ref_point[0]
    for f1,f2 in pts:
        width = last_f1 - f1
        if width > 0:
            height = ref_point[1] - f2
            hv += width * max(height, 0.0)
            last_f1 = f1
    return hv

def spacing(front):
    if len(front) <= 1:
        return 0.0
    d = []
    for i in range(len(front)):
        di = []
        for j in range(len(front)):
            if i==j: continue
            dist = sum(abs(front[i][k] - front[j][k]) for k in range(2))
            di.append(dist)
        d.append(min(di))
    mean_d = sum(d)/len(d)
    var = sum((di - mean_d)**2 for di in d) / (len(d)-1) if len(d)>1 else 0.0
    return math.sqrt(var)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pop', type=int, default=100)
    parser.add_argument('--gen', type=int, default=250)
    parser.add_argument('--nvar', type=int, default=50)
    parser.add_argument('--runs', type=int, default=10)
    parser.add_argument('--ref', type=float, nargs=2, default=None)
    return parser.parse_args()

def main(problem, filename):
    args = parse_args()
    num_evals = args.pop * args.gen
    hv_list = []
    sp_list = []
    for run in range(args.runs):
        nd = random_search(problem, args.nvar, num_evals)
        if args.ref is None:
            maxf1 = max(p[0] for p in nd) if nd else 1.0
            maxf2 = max(p[1] for p in nd) if nd else 1.0
            ref = (maxf1 * 1.2 + 1e-9, maxf2 * 1.2 + 1e-9)
        else:
            ref = (args.ref[0], args.ref[1])
        hv = hypervolume(nd, ref)
        sp = spacing(nd)
        hv_list.append(hv)
        sp_list.append(sp)
        if run==0:
            print(f'Run {run+1}: nd_size={len(nd)} hv={hv:.6g} spacing={sp:.6g}')
            for p in nd[:20]:
                print(f'{p[0]:.6g}, {p[1]:.6g}')
    def stats(lst):
        return (min(lst), sum(lst)/len(lst), max(lst))
    print('\\nHV stats (min, mean, max):', stats(hv_list))
    print('Spacing stats (min, mean, max):', stats(sp_list))

if __name__=='__main__':
    main(problem='zdt3', filename='random_zdt3.py')
