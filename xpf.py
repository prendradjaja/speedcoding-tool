def xpf(expr, call_id):
    if call_id not in xpf.seen:
        xpf.seen.add(call_id)
        if isinstance(expr, list):
            string = f'({len(expr)}) {repr(expr)}'
        else:
            string = repr(expr)
        print(f'XPF({call_id})XPF', string)
    return expr
xpf.seen = set()
