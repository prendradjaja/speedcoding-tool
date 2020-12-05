def xpf(expr, call_id):
    if call_id not in xpf.seen:
        xpf.seen.add(call_id)
        print(f'XPF(${call_id})', repr(expr))
    return expr
xpf.seen = set()
