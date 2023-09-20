from tkinter import *
from tkinter import ttk
import sqlite3
root = Tk()
class Func():
    def limpa_tela(self):
        self.cod_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        print('Conectando ao Banco de Dados...')
    def desconecta_bd(self):
        self.conn.close(); 
        print("Desconectando do Banco de Dados.")
    def montaTabelas(self): # cria tabelas dentro do banco de dados
        self.conecta_bd()
        # Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente CHARVAR(40) NOT NULL, 
                telefone INTEGER(20),
                cidade CHARVAR(40)
            );        
        """)
        self.conn.commit(); #Para validar as informações no db
        print("Banco de Dados criado!")
        self.desconecta_bd()
    def variaveis(self):#funcao criada para armazenar variaveis, em cada função chamo a funcao variaveis e não precia repetir código. Evitar redundancia de código.
        self.cod = self.cod_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        self.conecta_bd() # conecta ao banco de dados
        self.cursor.execute(""" INSERT INTO clientes(nome_cliente, telefone, cidade)
         VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit() # validar os dados
        self.desconecta_bd()
        self.select_lista()#sempre que ocorrer qq alteração na lista, esta sera atualizada
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes 
        ORDER BY nome_cliente ASC; """) # cod, nome_cliente, telefone, cidade
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):#funcao duplo clique, seleciona as informações.Sempre que tiver uma interação coloca event
        self.limpa_tela() #Caso tenha algo digitado lá em cima irá ser apagado
        self.listaCli.selection() #pega as informações da lista
        for n in self.listaCli.selection():# extrai os dados
            col1, col2, col3, col4 = self.listaCli.item(n, "values") #extrai os itens
            self.cod_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.cod,)),
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()#limpa registro das entrys
        self.select_lista()#atualiza informação da treeview
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(''' UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ? WHERE cod = ? ''',
		(self.nome, self.telefone, self.cidade, self.cod ))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
        
class Application(Func):
    def __init__(self):
        self.root = root
        self.tela()
        self.frame_de_tela()
        self.widgets_frame1()
        self.Lista_frame2()   # módulo para mostrar os clientes cadastrados no Banco de Dados
        self.montaTabelas()
        self.select_lista()
        self.add_cliente()
        root.mainloop()

    def tela(self):
        self.root.title('Cadastro de Clientes')
        self.root.configure(background='#997EC6')
        self.root.geometry('700x500+700+200')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=600)
        self.root.minsize(width=520, height=400)
    def frame_de_tela(self):
        self.frame1 = Frame(self.root, bd=10, bg='#E0E3EF',
                            highlightbackground='#775EA3', highlightthickness=6)
        # relative (rel) se refere a posição relativa dos objetos na tela
        # o valores váo de 0 a 1 - 0 é esquerda e 1 a direita
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2 = Frame(self.root, bd=10, bg='#E0E3EF',
                            highlightbackground='#775EA3', highlightthickness=6)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        # cria botão limpar
        self.bt_limpar = Button(self.frame1, text='Limpar', bd=2 ,bg='#4E9DE5',fg='white',
                                font=('Ubuntu',11), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão buscar
        self.bt_buscar = Button(self.frame1, text='Buscar', bd=2 ,bg='#4E9DE5',fg='white',
                                font=('Ubuntu',11))
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão novo
        self.bt_novo = Button(self.frame1, text='Novo', bd=2, bg='#4E9DE5',fg='white'
                              ,font=('Ubuntu',11), command=self.add_cliente)
        self.bt_novo.place(relx=0.55, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão alterar
        self.bt_alterar = Button(self.frame1, text='Alterar', bd=2, bg='#4E9DE5',fg='white',font=('Ubuntu',11), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão apagar
        self.bt_apagar = Button(self.frame1, text='Apagar', bd=2, bg='#4E9DE5',fg='white'
                                ,font=('Ubuntu',11), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        # criação dos Labels e  Entrada do Código
        self.lb_codigo = Label(self.frame1, text='Código',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_codigo.place(relx=0.05, rely=0.05)
        self.cod_entry = Entry(self.frame1, relief='groove')
        self.cod_entry.place(relx=0.05, rely=0.15, relwidth=0.085)
        # criação dos label e Entrada do Nome
        self.lb_nome = Label(self.frame1, text='Nome',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_nome.place(relx=0.05, rely=0.35)
        self.nome_entry = Entry(self.frame1, relief='groove')
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.85)
        # criação dos Labels e Entrada do Telefone
        self.lb_telefone = Label(self.frame1, text='Telefone',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_telefone.place(relx=0.05, rely=0.65)
        self.telefone_entry = Entry(self.frame1, relief='groove')
        self.telefone_entry.place(relx=0.05, rely=0.75, relwidth=0.4)
        # criação das Labels e Entrada de Cidade
        self.lb_cidade = Label(self.frame1, text='Cidade',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_cidade.place(relx=0.5, rely=0.65)
        self.cidade_entry = Entry(self.frame1, relief='groove')
        self.cidade_entry.place(relx=0.5, rely=0.75, relwidth=0.4)
    def Lista_frame2(self):
        # criação das colunas no Treeview
        self.listaCli = ttk.Treeview(self.frame2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        # criação dos cabeçalhos das colunas - "#" número da coluna
        self.listaCli.heading("#0", text="")   # coluna "#0" deve ficar vazia
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=200)

        # barra de rolagem
        self.scroolLista = Scrollbar(self.frame2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaCli.bind('<Double-1>', self.OnDoubleClick)#bind tipo de interação que será feito com a lista
Application()