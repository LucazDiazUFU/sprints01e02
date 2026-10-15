from itertools import product
import json


def implica(p, q):
    return not p or q


def tabelas():
    return [
        {
            "p": p,
            "q": q,
            "p_e_q": p and q,
            "p_ou_q": p or q,
            "p_implica_q": implica(p, q),
            "de_morgan_esquerda": not (p and q),
            "de_morgan_direita": not p or not q,
            "tautologia": p or not p,
            "contradicao": p and not p,
            "modus_ponens": implica(p and implica(p, q), q),
            "afirmar_consequente": implica(q and implica(p, q), p),
        }
        for p, q in product([False, True], repeat=2)
    ]


if __name__ == "__main__":
    print(json.dumps(tabelas(), ensure_ascii=False, indent=2))
