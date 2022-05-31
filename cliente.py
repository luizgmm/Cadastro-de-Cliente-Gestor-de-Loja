import imp
import sqlite3
import webbrowser
from select import select
from tkinter import *
from tkinter import ttk

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
root = Tk()
class Relatorio():
    def printCliente(self):
        webbrowser.open("Cliente.pdf")
    def geraRelatorio(self):
        self.c = canvas.Canvas("Cliente.pdf")
        self.codigoRelatorio = self.codigo_entry.get()
        self.nomeRelatorio = self.nome_entry.get()
        self.produtoRelatorio = self.produto_entry.get()
        self.precoRelatorio = self.preco_entry.get()
        self.unidadeRelatorio = self.quantidade_entry.get()
        self.dataRelatorio = self.data_entry.get()
        self.funcionarioRelatorio = self.funcionario_entry.get()

        self.c.setFont("Helvetica-Bold", 28)
        self.c.drawString(200, 800, 'Ficha do Cliente')
        
        self.c.setFont("Helvetica-Bold",18)
        self.c.drawString(70,700, 'Codigo: ')
        self.c.drawString(70,650, 'Nome do Cliente: ')
        self.c.drawString(70,600, 'Produto: ')
        self.c.drawString(70,550, 'Preço: ')
        self.c.drawString(70,500, 'Unidades: ')
        self.c.drawString(70,450, 'Data: ')
        self.c.drawString(70,400, 'Funcionario: ')

        self.c.setFont("Helvetica",18)
        self.c.drawString(150,700, self.codigoRelatorio)
        self.c.drawString(220,650, self.nomeRelatorio)
        self.c.drawString(150,600, self.produtoRelatorio)
        self.c.drawString(130,550, self.precoRelatorio)
        self.c.drawString(170,500, self.unidadeRelatorio)
        self.c.drawString(130,450, self.dataRelatorio)
        self.c.drawString(190,400, self.funcionarioRelatorio)

        self.c.rect(20,720,550,200, fill=False , stroke=True)


        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.preco_entry.delete(0, END)
        self.quantidade_entry.delete(0, END)
        self.data_entry.delete(0, END)
        self.funcionario_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("Clientes.db")
        self.cursor = self.conn.cursor()
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando")
    def montarTabelas(self):
        self.conecta_bd(); print("Conectando no Banco de Dados")

        ### criar tabela
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(50) NOT NULL,
                produto CHAR(50) NOT NULL,
                preco CHAR(50) NOT NULL,
                unidades CHAR(50) NOT NULL,
                data CHAR(50),
                funcionario CHAR(50) NOT NULL
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.produto = self.produto_entry.get()
        self.preco = self.preco_entry.get()
        self.unidade = self.quantidade_entry.get()
        self.data = self.data_entry.get()
        self.funcionario = self.funcionario_entry.get()
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""INSERT INTO clientes (nome_cliente, produto, preco, unidades, data, funcionario)
            VALUES (?,?,?,?,?,?)""", (self.nome, self.produto, self.preco, self.unidade, self.data, self.funcionario))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT cod, nome_cliente, produto, preco, unidades, data, funcionario FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
            self.desconecta_bd
    def duploclick(self, event):
        self.limpar_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.produto_entry.insert(END, col3)
            self.preco_entry.insert(END, col4)
            self.quantidade_entry.insert(END, col5)
            self.data_entry.insert(END, col6)
            self.funcionario_entry.insert(END, col7)
    def deletar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """,(self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_lista()
    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, produto =?, preco = ?, unidades = ?, data = ?, funcionario = ?
            WHERE cod = ?""", (self.nome, self.produto, self.preco, self. unidade, self.data, self.funcionario, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpar_tela()
    def buscar_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """SELECT cod, nome_cliente, produto, preco, unidades, data, funcionario FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC"""%nome)
        buscarCliente = self.cursor.fetchall()
        for i in buscarCliente:
            self.listaCli.insert("", END, values =i)
        self.limpar_tela() 
        self.desconecta_bd()

class Aplication(Funcs, Relatorio):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.criando_botoes_frame1()
        self.lista_frame2()
        self.montarTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de Cliente")
        self.root.configure(background='#708090')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=600, height=500)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd='4',bg='#ADD8E6', highlightbackground='#00BFFF' , highlightthickness=3)
        self.frame_1.place(relx=0.03 , rely=0.03, relwidth= 0.95, relheight= 0.45  )

        self.frame_2 = Frame(self.root, bd='4',bg='#D3D3D3', highlightbackground='#00BFFF', highlightthickness=3)
        self.frame_2.place(relx=0.03 , rely=0.5, relwidth= 0.95, relheight= 0.45  )
    def criando_botoes_frame1(self):
        ###criando o botão novo 
        self.bt_novo = Button(self.frame_1, text="Novo", bd=3, bg='#008B8B', command= self.add_cliente)
        self.bt_novo.place(relx =0.2 , rely=0.1, relwidth=0.1, relheight=0.150)
        ###criando o botão Buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=3, bg='#20B2AA', command=self.buscar_cliente)
        self.bt_buscar.place(relx =0.36 , rely=0.1, relwidth=0.1, relheight=0.150)
        ###criando o botão Alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=3, bg='#20B2AA', command= self.alterar_cliente)
        self.bt_alterar.place(relx =0.47 , rely=0.1, relwidth=0.1, relheight=0.150)
        ###criando o botão Limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=3, bg='#20B2AA', command=self.limpar_tela)
        self.bt_limpar.place(relx =0.58 , rely=0.1, relwidth=0.1, relheight=0.150)
        ###criando o botão apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=3, bg='#FF6347', command=self.deletar_cliente)
        self.bt_apagar.place(relx =0.69 , rely=0.1, relwidth=0.1, relheight=0.150)

        ###Criando label e entrada do cod
        self.lb_codigo = Label(self.frame_1, text= "Código", fg='#182bd2', bg='#ADD8E6')
        self.lb_codigo.place(relx=0.05,rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05,rely=0.15, relwidth=0.07)

        ###Criando label e entrada do nome
        self.lb_nome = Label(self.frame_1, text= "Nome Cliente", fg='#182bd2', bg='#ADD8E6')
        self.lb_nome.place(relx=0.05,rely=0.27)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05,rely=0.37, relwidth=0.70)

         ###Criando label e entrada do Produto
        self.lb_produto= Label(self.frame_1, text= "Produto", fg='#182bd2', bg='#ADD8E6')
        self.lb_produto.place(relx=0.05,rely=0.47)

        self.produto_entry = Entry(self.frame_1)
        self.produto_entry.place(relx=0.05,rely=0.57, relwidth=0.2)

        ###Criando label e entrada do Preço
        self.lb_preco = Label(self.frame_1, text= "Preço", fg='#182bd2', bg='#ADD8E6')
        self.lb_preco.place(relx=0.30,rely=0.47)

        self.preco_entry = Entry(self.frame_1)
        self.preco_entry.place(relx=0.30,rely=0.57, relwidth=0.1)

        ###Criando label e entrada do Quantidade
        self.lb_quantidade = Label(self.frame_1, text= "Unidades", fg='#182bd2', bg='#ADD8E6')
        self.lb_quantidade.place(relx=0.45,rely=0.47)

        self.quantidade_entry = Entry(self.frame_1)
        self.quantidade_entry.place(relx=0.45,rely=0.57, relwidth=0.05)

        ###Criando label e entrada do Data
        self.lb_data= Label(self.frame_1, text= "Data", fg='#182bd2', bg='#ADD8E6')
        self.lb_data.place(relx=0.55,rely=0.47)

        self.data_entry = Entry(self.frame_1)
        self.data_entry.place(relx=0.55,rely=0.57, relwidth=0.2)

        ###Criando label e entrada do Funcionario 
        self.lb_funcionario= Label(self.frame_1, text= "Funcionario", fg='#182bd2', bg='#ADD8E6')
        self.lb_funcionario.place(relx=0.05,rely=0.67)

        self.funcionario_entry = Entry(self.frame_1)
        self.funcionario_entry.place(relx=0.05,rely=0.77, relwidth=0.70)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1','col2','col3','col4','col5','col6','col7',))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Cod")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Produto")
        self.listaCli.heading("#4", text="Preço")
        self.listaCli.heading("#5", text="Unid")
        self.listaCli.heading("#6", text="Data")
        self.listaCli.heading("#7", text="Funcionario")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=30)
        self.listaCli.column("#2", width=70)
        self.listaCli.column("#3", width=70)
        self.listaCli.column("#4", width=70)
        self.listaCli.column("#5", width=1)
        self.listaCli.column("#6", width=70)
        self.listaCli.column("#7", width=70)
       

        self.listaCli.place(relx=0.01, rely=0.1, relheight=0.85, relwidth=0.98)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96 , rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.duploclick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        def Quit(): self.root.destroy()
        menubar.add_cascade(label = "Opções", menu= filemenu)
        menubar.add_cascade(label= "Relatorio", menu= filemenu2)

        filemenu.add_cascade(label="Sair", command= Quit)
        filemenu.add_command(label="Limpar tela", command=self.limpar_tela)
        
        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelatorio)


Aplication()
