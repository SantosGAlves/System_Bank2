from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.conta.append(conta)        

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome= nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__ (self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("&& Operação inválida, seu saldo é menor que o valor &&")
    
        elif valor > 0:
            self._saldo -= valor
            print("== Saque concluido com sucesso ==")
            return True
        else:
            ("&& Operação falhou, valor inválido &&")
            return False
        
    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            print("== Depósito feito vom sucesso ==")

        else:
            ("&& Operação falhou, valor inválido &&")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, saques_limite=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.saques_limite = saques_limite

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes 
                             if transacao["tipo"] == Saque.__name__])
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.saques_limite

        if excedeu_limite:
            print("&& Operação falhou!! O valor limite para saques é de R$ 500,00 &&")

        elif excedeu_saques:
            print ("&& Falha!! Número de saques máximo atingido &&")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''\
                Agência: \t{self.agencia}
                Conta_Corrente:\t\t{self.numero}
                Titular\t{self.cliente.nome}'''
    
class Historico:
    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
            return self.transacoes
        
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo":transacao.__class__.__name__ ,
                "valor": transacao.valor ,
                "data": datetime.now().strftime
                ("%d-%m-%y %H:%M:%s"),
            }
        )
        
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


