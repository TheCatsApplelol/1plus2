def O0O0O0O0000OO0OOO():
    ZERO = len("")
    ONE = len("x")
    TWO = len("xy")
    p = lambda: (lambda: ONE)
    q = lambda: (lambda: TWO)
    def make_layer(fn):
        return (lambda f=fn: (lambda: (lambda: f() ) ) )
    layered_a = make_layer(p)()
    layered_b = make_layer(q)()
    producers = [layered_a, layered_b]
    swapped = [producers[1], producers[0]]
    def pipeline(p0, p1):
        stage_raw = (lambda: (lambda: (p0()(), p1()()) ) )
        stage_bits = (lambda tup_fn=stage_raw: (lambda: (lambda: ( (tup_fn()())[ZERO]() | (tup_fn()())[ONE](),
                                                                     (tup_fn()())[ZERO]() & (tup_fn()())[ONE]() ) ) ) )
        stage_combine = (lambda bits_fn=stage_bits: (lambda: (lambda: ( (bits_fn()()())[ZERO] + (bits_fn()()())[ONE] ) ) ) )
        return stage_raw, stage_bits, stage_combine
    stage_raw, stage_bits, stage_combine = pipeline(swapped[ZERO], swapped[ONE])
    def encode_decode(combine_stage):
        to_bin = (lambda cstg=combine_stage: (lambda: (lambda: bin(cstg()()())[TWO:])))
        bin_callable = to_bin()
        def digits_from_bin(bfn):
            s = bfn()()
            bits = [(lambda ch=ch: (lambda: ord(ch)-ord("0"))) for ch in s]
            return bits
        bits_callables = digits_from_bin(bin_callable)
        def rebuild(bits):
            weights = []
            for i in range(len(bits)):
                weight = (ONE << i) * TWO // TWO
                weights.append(weight)
            weights = weights[::-1]
            total = ZERO
            for w, bcall in zip(weights, bits):
                total = total + (w * bcall()())
            return total
        rebuilt = rebuild(bits_callables)
        return (lambda r=rebuilt: (lambda: (lambda: r)))
    reconstructed_stage = encode_decode(stage_combine)
    def final_result():
        combined = stage_combine()()()
        reconstructed = reconstructed_stage()()()
        or_part = combined | reconstructed
        and_part = combined & reconstructed
        final = (or_part + and_part) // TWO * ONE
        return final
    return final_result()

if __name__ == "__main__":
    print(O0O0O0O0000OO0OOO())


    