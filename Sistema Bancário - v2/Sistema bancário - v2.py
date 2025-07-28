saldo = 0
extrato_deposito = ""
extrato_saque = ""
numero_saques = 0
limite = 500
LIMITE_SAQUES = 3
usuarios = []
contas_corrente = []

menu = """

Seja bem-vindo(a) ao Sistema Bancário!

Escolha a operação desejada:

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """

menu_incial = """

Seja bem-vindo(a) {nome_usuario}
Conta: {numero_conta}

Selecione a operação desejada
    
[1] Ir para o Sistema
[2] Cadastrar Conta Bancária
[0] Sair

=> """

def cadastrar_usuarios():
    print("\n>>>>> CADASTRO DE USUÁRIOS <<<<<")
    nome = input("\nDigite seu Nome Completo: ")
    data_nascimento = input("Digite sua Data de Nascimento (dd/mm/aaaa): ")
    cpf = input("Digite seu CPF (SOMENTE NÚMEROS): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("\nJá existe um usuário cadastrado neste CPF!")
            return

    endereco = input("Digite seu endereço (logradouro, número - bairro - cidade/sigla do estado): ")

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print("\nUsuário cadastrado com sucesso!")
    return usuario

def cadastrar_conta_bancaria(usuario):
    print("\n>>>>> CADASTRO DE CONTA BANCÁRIA <<<<<")
    agencia = "0001"
    numero_conta = len(contas_corrente) + 1
    numero_conta_formatado = f"{numero_conta:08d}"
    numero_conta = f"{numero_conta_formatado}-0"

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato_deposito": "",
        "extrato_saque": "",
        "numero_saques": 0
    }

    contas_corrente.append(conta)
    print(f"\nConta Bancária cadastrada com sucesso!\n\nAgência: {conta["agencia"]}\nNº: {conta["numero_conta"]}")
    return conta

def continuar():
    while True:
        print('\nDeseja Continuar?\n\n[s]: sim\n[n]: não')
        decisao = input('\n=> ')
        if decisao == 's':
            return True
        elif decisao == 'n':
            return False
        else:
            print('Operação Inválida! Escolha uma das opções acima.')

def deposito(saldo, valor_deposito, extrato_deposito, /):    
    print("\n>>>>> DEPOSITAR <<<<<")
    while True:
        valor_deposito = float(input("\nInsira o valor a ser depositado: "))

        if valor_deposito > 0:
            print('\nDepósito realizado!')
            saldo += valor_deposito
            print(f'\nValor depositado: {valor_deposito}')
            print(f'Saldo disponível: {saldo}')
            extrato_deposito += f"Depósito: R$ {valor_deposito:.2f}\n"
            if not continuar():
                break
        else:
            print("Operação inválida! Insira um valor válido.")

    return saldo, extrato_deposito

def saque(*, saldo, valor_saque, extrato_saque, limite, numero_saques, LIMITE_SAQUES):
    while True:
        valor_saque = float(input("\nInsira o valor a ser sacado: "))

        if valor_saque <= saldo:
            if numero_saques < LIMITE_SAQUES:
                if valor_saque > 0:
                    if valor_saque <= limite:
                        print('\nSaque realizado!')
                        numero_saques += 1
                        print(f'N° saques: {numero_saques}')
                        saldo -= valor_saque
                        print(f'Saldo disponível: {saldo}')
                        extrato_saque += f"Saque: R$ {valor_saque:.2f}\n"
                    else:
                        print('Limite excedido! Insira um valor dentro do limite.')
                    if not continuar():
                        break
                else:
                    print("Operação inválida! Insira um valor válido.")
            else:
                print('Limite de saque diários excedido! Tente novamente no dia seguinte.')
                break
        else:
            print('Operação inválida! Saldo insuficiente.')
            break
    
    return saldo, extrato_saque, numero_saques

def extrato(saldo, /, *, extrato_saque, extrato_deposito):
    while True:
            print("\n>>>>> EXTRATO DE MOVIMENTAÇÕES <<<<<")
            if not (extrato_saque or extrato_deposito or (extrato_saque and extrato_deposito)):
                print('\nNão foram realizadas movimentações.')
                break
            if extrato_deposito or (extrato_saque and extrato_deposito):
                print('\n• Depósitos realizados:')
                print(f'\n{extrato_deposito}')
            if extrato_saque or (extrato_saque and extrato_deposito):
                print('\n• Saques realizados:')
                print(f'\n{extrato_saque}')
            print(f'\nSaldo atual: {saldo}')
            break

while True:
    login_usuario = input("\n\n>>>>> LOGIN <<<<<\n\nCaso deseje encerrar o sistema, digite '0'\n\nInsira seu CPF: ")
    if login_usuario == "0":
        break
    usuario_encontrado = None

    for usuario in usuarios:
        if usuario["cpf"] == login_usuario:
            usuario_encontrado = usuario
            break
    
    if usuario_encontrado:
        nome_usuario = usuario_encontrado["nome"]

        contas_usuario = []
        for conta in contas_corrente:
            if conta["usuario"]["cpf"] == login_usuario:
                contas_usuario.append(conta)

        if len(contas_usuario) == 1:
            conta_selecionada = contas_usuario[0]
        else:
            print("\nQual conta deseja utilizar?\n")
            for i, conta in enumerate(contas_usuario, start=1):
                print(f"[{i}] {conta["numero_conta"]}")

            while True:
                escolha_conta = int(input("\nDigite a opção desejada: "))
                
                if 1 <= escolha_conta <= len(contas_usuario):
                    conta_selecionada = contas_usuario[escolha_conta - 1]
                    break
                else:
                    print("Operação inválida. Tente novamente.")

        numero_conta = conta_selecionada["numero_conta"]
        menu_formatado = menu_incial.format(nome_usuario=nome_usuario, numero_conta=numero_conta)

        while True:           
            escolha = input(menu_formatado)

            if escolha == "1":
                saldo = conta_selecionada.get("saldo", 0)
                extrato_deposito = conta_selecionada.get("extrato_deposito", "")
                extrato_saque = conta_selecionada.get("extrato_saque", "")
                numero_saques = conta_selecionada.get("numero_saques", 0)

                while True:
                    opcao = input(menu)
                    if opcao == "1":
                        saldo, extrato_deposito = deposito(saldo, 0, extrato_deposito)
                    elif opcao == "2":
                        saldo, extrato_saque, numero_saques = saque(saldo = saldo, valor_saque = 0, extrato_saque = extrato_saque, limite = limite, numero_saques = numero_saques, LIMITE_SAQUES = LIMITE_SAQUES)
                    elif opcao == "3":
                        extrato(saldo, extrato_saque = extrato_saque, extrato_deposito = extrato_deposito)
                    elif opcao == "0":
                        break
                    else:
                        print("Operação inválida, por favor selecione novamente a operação desejada.")
                
                conta_selecionada["saldo"] = saldo
                conta_selecionada["extrato_deposito"] = extrato_deposito
                conta_selecionada["extrato_saque"] = extrato_saque
                conta_selecionada["numero_saques"] = numero_saques
                break
            elif escolha == "2":
                cadastrar_conta_bancaria(usuario_encontrado)
                break
            elif escolha == "0":
                break
            else:
                print("Operação inválida. Tente novamente.")
    else:
        while True:
            print("\nUsuário não encontrado. O que deseja fazer?\n\n[1] Cadastrar Usuário\n[2] Tentar Novamente")
            select = input("\nDigite a opção desejada: ")
            if select == "1":
                novo_usuario = cadastrar_usuarios()
                if novo_usuario:
                    cadastrar_conta_bancaria(novo_usuario)
                    break
                else:
                    break
            elif select == "2":
                break
            else:
                print("Operação inválida. Tente novamente.")