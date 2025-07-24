menu = """
Sistema Bancário

[1] Depositar
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[6] Listar Contas
[7] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"
numero_conta = 0
usuarios = []
contas = []


def depositar(saldo,valor,extrato,/):
  
    if valor <= 0:
        print("Valor Inválido! Por favor, entre com um valor válido")
        return saldo, extrato
    else:
        print(f"O valor de R$ {valor:.2f} foi depositado com sucesso ")
        saldo += valor
        extrato += f"Depósito (+): R$ {valor:.2f}\n"
         
        return saldo, extrato


def sacar(*,saldo,valor,limite,numero_saques,limite_saques,extrato):
    
    if numero_saques < limite_saques: 
        if valor <= 0:
            print("\nValor Inválido!\nPor favor, entre com um valor válido.")
            return saldo,extrato,numero_saques
    
        elif valor > limite and valor <= saldo:
            print("\nOperação Inválida!\nValor do saque maior do que o limite permitido, por favor,tente novamente.")
            return saldo,extrato,numero_saques
        
        elif valor > saldo:
            print("\nOperação Inválida!\nValor do saque maior do que o disponível em conta, por favor,tente novamente com um valor dentro do saldo disponível")
            return saldo,extrato,numero_saques
        
        else:
            print(f"O valor de R$ {valor:.2f} foi sacado com sucesso. ") 
            numero_saques += 1
            saldo -= valor
            extrato += f"Saque (-): R$ {valor:.2f}\n"
            return saldo,extrato,numero_saques
    else:
        print("\nVocê ultrapassou o seu limite diário de saques,tente novamente amanhã.")
        return saldo,extrato,numero_saques


def mostrar_extrato(saldo,/,*,extrato):
        print(f"EXTRATO".center(41,"="))
        print("\nNão houve movimentações nesta conta" if extrato == "" else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("".center(41,"="))
        
        
def criar_usuario(lista_de_usuarios):
    cpf = input("\nDigite um CPF: ")
    
    if lista_de_usuarios:
        
        for i in lista_de_usuarios:
            if i["cpf"] == cpf:
                print("\nJá existe um usuário para este cpf")
                return
        
        else:
            pass
        
    nome = input("\nInforme o nome completo: ")
    data_nascimento= input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("\nInforme o endereço (logradouro,numero do imovel - bairro - cidade/sigla do estado): ")
  
  
    print("\nUsuário criado com sucesso \n")
    return {"cpf":cpf, "nome":nome, "data_nascimento":data_nascimento, "endereco":endereco}
 
            
def criar_conta (agencia,numero_de_conta,lista_de_usuarios):
    cpf = input("\nDigite um CPF: ")
    
    for i in lista_de_usuarios:
        if i["cpf"] == cpf:
            numero_de_conta += 1
            print("\nConta criada com sucesso !")
            return {"agencia":agencia, "numero_da_conta": numero_de_conta, "usuario": i}, numero_de_conta
        
        else:    
            continue              
        
    print("\nUsuário não existe, tente novamente\n")
    return None,numero_de_conta

    
def listar_contas(lista_de_contas):
    if lista_de_contas:
        for i in lista_de_contas:
            texto = f'''
            Agência: {i["agencia"]}
            Conta Corrente: {i["numero_da_conta"]}
            Titular: {i["usuario"]["nome"]}
            '''
            print("=" * 50)
            print(texto)    
    else:
        print("\nNão existem contas cadastradas")
  
        
while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("\nDigite o valor a ser depositado: "))
        saldo, extrato = depositar(saldo,valor,extrato)
         
    elif opcao == "2":
        valor = float(input("\nDigite o valor a ser sacado: "))
        saldo,extrato,numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
            extrato=extrato
        )


    elif opcao == "3":
        mostrar_extrato(saldo,extrato=extrato)
        
    elif opcao == "4":
        novo_usuario = criar_usuario(usuarios)
        
        if novo_usuario:
            usuarios.append(novo_usuario)
            
    elif opcao == "5":
        conta, numero_conta = criar_conta(AGENCIA,numero_conta,usuarios)
        
        if conta:
            contas.append(conta)

    elif opcao == "6":
        listar_contas(contas)
        
    elif opcao == "7":
        print("\nSistema Encerrado\n")
        break

        
    else:
        print("Opção digitada inválida ! Por favor escolha novamente.\n")
