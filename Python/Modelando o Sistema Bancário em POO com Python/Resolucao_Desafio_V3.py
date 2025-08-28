#Importando bibliotecas
#Agora com Iterador e Log em txt
import textwrap
from abc import ABC, abstractclassmethod,abstractproperty
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent

#Criando classes
class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""
            Agência: {conta.agencia}
            Número: {conta.numero}
            Titular: {conta.cliente.nome}
            Saldo: {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index +=1

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0
        
    def realizar_transacao(self,conta,transacao):
        limite_transacoes = 10
        if len(conta.historico.transacoes_do_dia()) >= limite_transacoes:
            print(f"\n Você excedeu as {limite_transacoes} transações permitidas por dia")
            return
        
        transacao.registrar(conta)
        
    def adicionar_conta(self,conta):
        self.contas.append(conta)        
    
class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self,valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        
        if excedeu_saldo:
            print("\nOperação Inválida!\nValor do saque maior do que o disponível em conta, por favor,tente novamente com um valor dentro do saldo disponível")
       
        elif valor > 0:
            self._saldo -= valor
            print(f"O valor de R$ {valor:.2f} foi sacado com sucesso.") 
            return True
        
        else:
            print("\nValor Inválido!\nPor favor, entre com um valor válido.")    
        
        return False
        
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print(f"O valor de R$ {valor:.2f} foi depositado com sucesso ")
        
        else:
            print("Valor Inválido! Por favor, entre com um valor válido")
            return False
        
        return True          
   
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar (self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("\nOperação Inválida!\nValor do saque maior do que o limite permitido, por favor,tente novamente.")
        
        elif excedeu_saques:
            print("\nVocê ultrapassou o seu limite diário de saques,tente novamente amanhã.")
            
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""
            Agência:{self.agencia}
            C/C:{self.numero}
            Titular:{self.cliente.nome} 
        """        
        
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        data_atual = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": data_atual,
            }
        )        
    def gerar_relatorio(self,tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao
                
    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes
    
class Transacao(ABC):
    @property
    @abstractproperty
    def valor (self):
        pass
        
    @abstractclassmethod
    def registrar(self,conta):
        pass
    
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
        
class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

#Função de Log
def log_transacao(func):
    def envelope(*args, **kwargs):
        operacao_executada = func(*args, **kwargs)
        data_hora = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{datetime.now()}: {func.__name__.upper()}")
        
        with open(ROOT_PATH / "log.txt","a") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com argumento {args} e {kwargs}."
                f"Retornou {operacao_executada}\n"
            )
        
        return operacao_executada

    return envelope
    
#Criando demais funções
def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta !")
        return

    for conta in cliente.contas:
        i = cliente.contas.index(conta) + 1
        print(f"Conta Numero {i}\n",conta)
        
        
    indice = int(input("Escolha o numero da conta: "))
    if type(indice) == int and indice <= len(cliente.contas) and indice > 0:
        indice -= 1
        return cliente.contas[indice]
    else:
        print("Este numero de conta não existe ! Por favor tentar novamente")
        return

@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente:  ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("\nCliente não encontrado no sistema !")
        return
    
    valor = float(input("Informe o valor do depósito em R$: "))
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

@log_transacao    
def sacar(clientes):
    cpf = input("Informe o CPF do cliente:  ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("\nCliente não encontrado no sistema !")
        return
    
    valor = float(input("Informe o valor do saque em R$: "))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:  ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("\nCliente não encontrado no sistema !")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(f"EXTRATO".center(41,"="))
    transacoes = conta.historico.transacoes
    
    extrato = ""
    if not transacoes:
        extrato = "Não houve movimentações nesta conta"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\nR$ {transacao['valor']:.2f}\n\n"
            
    print(extrato)
    print(f"\nSaldo:\nR$ {conta.saldo:.2f}")
    print("".center(41,"="))

@log_transacao    
def criar_cliente(clientes):
    cpf = input("Informe o CPF do cliente:  ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if cliente:
        print("\nCliente já cadastrado com este CPF !")
        return
    
    nome = input("\nInforme o nome completo: ")
    data_nascimento = input("\nInforme a data de nascimento (dd-mm-aaaa): ")
    endereco = input("\nInforme o endereço completo(logradouro,numero - bairro - cidade/sigla do estado):  ")
    
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    
    clientes.append(cliente)
    
    print("\nUsuário criado com sucesso \n")

@log_transacao    
def criar_conta(numero_conta,clientes,contas):
    cpf = input("Informe o CPF do cliente:  ")
    cliente = filtrar_cliente(cpf,clientes)
    
    if not cliente:
        print("\nCliente não encontrado no sistema !\nCriação de conta encerrada")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\nConta criada com sucesso !")
    
def listar_contas(contas):
    for conta in ContaIterador(contas):
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
        
#Menu
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
def main():
    clientes = []
    contas = []

    while True:

        opcao = input(menu)

        if opcao == "1":
            depositar(clientes)
            
        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
           exibir_extrato(clientes)
            
        elif opcao == "4":
            criar_cliente(clientes)
                
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,clientes,contas)

        elif opcao == "6":
            listar_contas(contas)
            
        elif opcao == "7":
            print("\nSistema Encerrado\n")
            break
            
        else:
            print("Opção digitada inválida ! Por favor escolha novamente.\n")

main()