from pathlib import Path

from trabalho1.armazenamento import carregar, salvar
from trabalho1.validacoes import TIPOS


BASE = Path(__file__).with_name("ativos.json")


def pedir(campo, atual=None, obrigatorio=True):
    mensagem = campo
    if atual is not None:
        mensagem += f" [{atual}]"
    valor = input(f"{mensagem}: ").strip()
    if not valor and atual is not None:
        return atual
    if not valor and obrigatorio:
        raise ValueError(f"{campo} não pode ficar vazio.")
    return valor


def mostrar_ativo(ativo):
    print(f"\nID: {ativo.id} | Nome: {ativo.nome} | Tipo: {TIPOS[ativo.tipo]} ({ativo.tipo})")
    print(f"Responsável: {ativo.responsavel} | Setor: {ativo.setor}")
    print(f"Criticidade: {ativo.criticidade} | Status: {ativo.status}")
    if ativo.descricao:
        print(f"Descrição: {ativo.descricao}")
    print(f"Vulnerabilidades: {len(ativo.vulnerabilidades)}")


def mostrar_vulnerabilidades(itens):
    if not itens:
        print("Ativo sem vulnerabilidades registradas ou nenhum resultado para os filtros.")
        return
    for ativo, vulnerabilidade in itens:
        print(f"\nID: {vulnerabilidade.id} | Ativo: {ativo.id} - {ativo.nome}")
        print(f"Descrição: {vulnerabilidade.descricao}")
        print(f"Categoria: {vulnerabilidade.categoria} | Severidade: {vulnerabilidade.severidade} | Status: {vulnerabilidade.status}")
        if vulnerabilidade.cve:
            print(f"CVE: {vulnerabilidade.cve} | CVSS: {vulnerabilidade.cvss}")
        if vulnerabilidade.referencia:
            print(f"Referência: {vulnerabilidade.referencia}")
        if vulnerabilidade.recomendacao:
            print(f"Recomendação: {vulnerabilidade.recomendacao}")


def cadastrar_ativo(inventario):
    print("\nTipos:", ", ".join(f"{codigo} - {nome}" for codigo, nome in TIPOS.items()))
    ativo = inventario.cadastrar_ativo(
        pedir("ID numérico"), pedir("Nome ou hostname"), pedir("Responsável"),
        pedir("Setor ou localização"), pedir("Código do tipo"),
        pedir("Criticidade (BAIXA/MEDIA/ALTA/CRITICA)", "MEDIA"),
        pedir("Status (ATIVO/INATIVO/MANUTENCAO)", "ATIVO"),
        pedir("Descrição", obrigatorio=False),
    )
    print(f"Ativo {ativo.id} cadastrado.")
    if input("Cadastrar vulnerabilidade inicial? (s/N): ").strip().lower() == "s":
        try:
            cadastrar_vulnerabilidade(inventario, ativo.id)
        except ValueError as erro:
            print(f"Vulnerabilidade não cadastrada: {erro}")


def buscar_ativo(inventario):
    escolha = pedir("Buscar por 1 - ID ou 2 - nome")
    if escolha == "1":
        ativo = inventario.buscar_ativo(id=pedir("ID"))
    elif escolha == "2":
        ativo = inventario.buscar_ativo(nome=pedir("Nome ou hostname"))
    else:
        raise ValueError("Escolha 1 ou 2.")
    if ativo is None:
        print("Ativo não encontrado.")
    else:
        mostrar_ativo(ativo)


def listar_ativos(inventario):
    itens = inventario.listar_ativos(
        nome=pedir("Parte do nome", obrigatorio=False),
        tipo=pedir("Código do tipo", obrigatorio=False) or None,
        status=pedir("Status", obrigatorio=False) or None,
    )
    if not itens:
        print("Nenhum ativo encontrado.")
    for ativo in itens:
        mostrar_ativo(ativo)


def atualizar_ativo(inventario):
    id = pedir("ID do ativo")
    ativo = inventario.buscar_ativo(id=id)
    if ativo is None:
        raise ValueError("Ativo não encontrado.")
    print("Pressione Enter para manter o valor atual.")
    campos = {
        "nome": pedir("Nome", ativo.nome),
        "responsavel": pedir("Responsável", ativo.responsavel),
        "setor": pedir("Setor", ativo.setor),
        "tipo": pedir("Código do tipo", ativo.tipo),
        "criticidade": pedir("Criticidade", ativo.criticidade),
        "status": pedir("Status", ativo.status),
        "descricao": pedir("Descrição", ativo.descricao),
    }
    inventario.atualizar_ativo(id, **campos)
    print("Ativo atualizado.")


def excluir_ativo(inventario):
    id = pedir("ID do ativo")
    ativo = inventario.buscar_ativo(id=id)
    if ativo is None:
        raise ValueError("Ativo não encontrado.")
    mostrar_ativo(ativo)
    confirmar = input("Excluir o ativo e todas as vulnerabilidades? Digite EXCLUIR: ").strip() == "EXCLUIR"
    print("Ativo excluído." if inventario.excluir_ativo(id, confirmar) else "Exclusão cancelada.")
    return confirmar


def cadastrar_vulnerabilidade(inventario, ativo_id=None):
    ativo_id = ativo_id or pedir("ID do ativo")
    vulnerabilidade = inventario.cadastrar_vulnerabilidade(
        ativo_id, pedir("ID numérico da vulnerabilidade"), pedir("Descrição"),
        pedir("Categoria ou tipo"), pedir("Severidade (BAIXA/MEDIA/ALTA/CRITICA)"),
        pedir("Status (ABERTA/EM_TRATAMENTO/CORRIGIDA/RISCO_ACEITO)", "ABERTA"),
        pedir("CVE, se houver", obrigatorio=False),
        pedir("CVSS de 0 a 10, se houver", obrigatorio=False),
        pedir("Referência, se houver", obrigatorio=False),
        pedir("Recomendação, se houver", obrigatorio=False),
    )
    print(f"Vulnerabilidade {vulnerabilidade.id} cadastrada.")


def consultar_vulnerabilidades(inventario):
    ativo_id = pedir("ID do ativo (vazio para todos)", obrigatorio=False) or None
    mostrar_vulnerabilidades(inventario.listar_vulnerabilidades(
        ativo_id=ativo_id,
        cve_codigo=pedir("CVE exata (opcional)", obrigatorio=False),
        severidade=pedir("Severidade (opcional)", obrigatorio=False) or None,
        status=pedir("Status (opcional)", obrigatorio=False) or None,
    ))


def atualizar_vulnerabilidade(inventario):
    id = pedir("ID da vulnerabilidade")
    encontrado = inventario.localizar_vulnerabilidade(id)
    if encontrado is None:
        raise ValueError("Vulnerabilidade não encontrada.")
    vuln = encontrado[1]
    print("Pressione Enter para manter o valor atual.")
    inventario.atualizar_vulnerabilidade(
        id, descricao=pedir("Descrição", vuln.descricao),
        categoria=pedir("Categoria", vuln.categoria),
        severidade=pedir("Severidade", vuln.severidade),
        status=pedir("Status", vuln.status),
        cve=pedir("CVE", vuln.cve), cvss=pedir("CVSS", vuln.cvss or ""),
        referencia=pedir("Referência", vuln.referencia),
        recomendacao=pedir("Recomendação", vuln.recomendacao),
    )
    print("Vulnerabilidade atualizada.")


def excluir_vulnerabilidade(inventario):
    id = pedir("ID da vulnerabilidade")
    encontrado = inventario.localizar_vulnerabilidade(id)
    if encontrado is None:
        raise ValueError("Vulnerabilidade não encontrada.")
    mostrar_vulnerabilidades([encontrado])
    confirmar = input("Digite EXCLUIR para confirmar: ").strip() == "EXCLUIR"
    print("Vulnerabilidade excluída." if inventario.excluir_vulnerabilidade(id, confirmar) else "Exclusão cancelada.")
    return confirmar


def main(caminho=BASE):
    try:
        inventario = carregar(caminho)
    except ValueError as erro:
        print(f"Erro: {erro}")
        return
    operacoes = {
        "1": cadastrar_ativo, "2": buscar_ativo, "3": listar_ativos,
        "4": atualizar_ativo, "5": excluir_ativo,
        "6": cadastrar_vulnerabilidade, "7": consultar_vulnerabilidades,
        "8": atualizar_vulnerabilidade, "9": excluir_vulnerabilidade,
    }
    alteracoes = {"1", "4", "5", "6", "8", "9"}
    while True:
        print("\nINVENTÁRIO DE SEGURANÇA")
        print("1 Cadastrar ativo | 2 Buscar ativo | 3 Listar ativos")
        print("4 Atualizar ativo | 5 Excluir ativo | 6 Cadastrar vulnerabilidade")
        print("7 Consultar vulnerabilidades | 8 Atualizar vulnerabilidade | 9 Excluir vulnerabilidade | 0 Sair")
        try:
            escolha = input("Opção: ").strip()
            if escolha == "0":
                print("Encerrado.")
                break
            if escolha not in operacoes:
                print("Opção inválida.")
                continue
            resultado = operacoes[escolha](inventario)
            if escolha in alteracoes and resultado is not False:
                salvar(caminho, inventario)
        except (ValueError, EOFError, KeyboardInterrupt) as erro:
            if isinstance(erro, (EOFError, KeyboardInterrupt)):
                print("\nEncerrado.")
                break
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
