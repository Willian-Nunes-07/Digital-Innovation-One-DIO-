menu = """
Sistema Bancário

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3



def depositar():
    valor_deposito = float(input("\nDigite o valor a ser depositado: "))
    if valor_deposito <= 0:
        print("Valor Inválido! Por favor, entre com um valor válido")
        return 0
    else:
        print(f"O valor de R$ {valor_deposito:.2f} foi depositado com sucesso ") 
        return float(valor_deposito)

def sacar():
    global saldo
    global limite
    global numero_saques 
    valor_saque = float(input("\nDigite o valor a ser sacado: "))
    if valor_saque <= 0:
        print("\nValor Inválido!\nPor favor, entre com um valor válido.")
        return 0
    
    elif valor_saque > limite and valor_saque <= saldo:
        print("\nOperação Inválida!\nValor do saque maior do que o limite permitido, por favor,tente novamente.")
        return 0
    
    elif valor_saque > saldo:
        print("\nOperação Inválida!\nValor do saque maior do que o disponível em conta, por favor,tente novamente com um valor dentro do saldo disponível")
        return 0
    else:
        print(f"O valor de R$ {valor_saque:.2f} foi sacado com sucesso. ") 
        numero_saques += 1
        return float(valor_saque)

        
while True:

    opcao = input(menu)

    if opcao == "1":
        valor = depositar()
        saldo += valor
        extrato += f"Depósito (+): R$ {valor:.2f}\n"
         
    elif opcao == "2":
        if numero_saques < LIMITE_SAQUES:   
            valor = sacar()
            if valor > 0:
                saldo -= valor
                extrato += f"Saque (-): R$ {valor:.2f}\n"
        else:
            print("\nVocê ultrapassou o seu limite diário de saques,tente novamente amanhã.")


    elif opcao == "3":
        print(f"EXTRATO".center(41,"="))
        print("\nNão houve movimentações nesta conta" if extrato == "" else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("".center(41,"="))
        
        

    elif opcao == "4":
        print("\nSistema Encerrado\n")
        break

    else:
        print("Opção digitada inválida ! Por favor escolha novamente.\n")
