def xpf(expr, call_id):
    if call_id not in xpf.seen:
        xpf.seen.add(call_id)
        try:
            string = f'({len(expr)}) {repr(expr)}'
        except TypeError:
            string = repr(expr)
        print(f'XPF({call_id})XPF', string)
    return expr
xpf.seen = set()
