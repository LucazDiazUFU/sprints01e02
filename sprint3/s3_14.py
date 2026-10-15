from itertools import product
import json


def meio_somador(a, b):
    return {"soma": a != b, "vai_um": a and b}


def multiplexador(a, b, seletor):
    return (a and not seletor) or (b and seletor)


if __name__ == "__main__":
    portas = [
        {
            "a": a,
            "b": b,
            "AND": a and b,
            "OR": a or b,
            "NAND": not (a and b),
            "NOR": not (a or b),
            "XOR": a != b,
            "XNOR": a == b,
            "NOT_a": not a,
            **meio_somador(a, b),
        }
        for a, b in product([False, True], repeat=2)
    ]
    print(
        json.dumps(
            {
                "portas": portas,
                "mux": [
                    {"a": a, "b": b, "seletor": s, "saida": multiplexador(a, b, s)}
                    for a, b, s in product([False, True], repeat=3)
                ],
            },
            indent=2,
        )
    )
