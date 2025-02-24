######################################################################
#Trabaho elaborado no âmbito das atividades desenvolvida da formação #
#Programação de alto nível - Python e integração com SQL             #
#  Programa para registo de cliente da empresa Mim'Arte              #
#--------------------------------------------------------------------#
#Formador: Júlio Magalhães                                           #
#Fromando: José Armando Marques                                      #
######################################################################

#bibliotecas de apoio ao programa
from tkinter import *
from tkinter.ttk import Treeview
from tkinter.messagebox import showinfo, showwarning
from bibconnect import conectar

#####Funções do splash inicial para criação do programa
#Criação da tabela "Mimarte"
def criartb():
    conn = conectar()  ##verificar a ligação
    if not conn:
        showinfo("Falha de ligação!", "Verifique a ligação à base de dados.")
        return
    ##abertura de cursor de comunicação com a base de dados
    cur = conn.cursor()

#Verificar se existe a tabela mimarte
    sql = "SELECT name FROM sys.tables WHERE name LIKE 'mimarte';"
    cur.execute(sql)
    listatab = cur.fetchall()

    if any(name[0] == 'mimarte' for name in listatab): #reposta se já  existe tabela
        showinfo("Programa já criado!", "Programa Mimarte já criado anteriormente.")
    else:   #criação da tabela, na eventualidade de não existir
        sql_create = """
            CREATE TABLE mimarte (
                id INT PRIMARY KEY IDENTITY(1,1),
                nome VARCHAR(50),
                rua VARCHAR(300),
                localidade VARCHAR(300),
                zona VARCHAR(300)
            );
        """
        cur.execute(sql_create)
        showinfo("Sucesso!", "Programa Mimarte criado com sucesso\nQueira carregar os dados dos clientes.")
##fecho da ligação à base de dados
    cur.close()
    conn.close()

#Função para importação dos dados do ficheiro .CSV para o nosso programa
def importar():
    conn = conectar()  ##verificar a ligação
    if not conn:
        showinfo("Falha de ligação!", "Verifique a ligação à base de dados.")
        return
    cur = conn.cursor()

#Apagar todos os dados existentes na tabela "mimarte" para evitar replicar indefinidamente
    cur.execute("truncate table mimarte;")
    conn.commit()

#Processo para importação dos dados existentes no ficheiro clientes.csv, para a tabela sql
    with open("clientes.csv", "r", encoding="UTF-8-SIG") as fp:
        cont = fp.readlines()
        for linha in cont:
            dados = linha.strip().split(";")
            nome, rua, localidade, zona = dados
            sql = f"""
                INSERT INTO mimarte (nome, rua, localidade, zona) VALUES
                ('{nome}', '{rua}', '{localidade}', '{zona}');
            """
            cur.execute(sql)
        conn.commit()
    showinfo("Sucesso!", "Dados dos clientes carregados com sucesso.")

    cur.close()
    conn.close()


#####Funções do programa principal com a BD dos clientes
##Função para obter os dados contidos na BDsql
def obter():
    conn = conectar()  ##verificar a ligação
    if not conn:
        showwarning("Conexão...", "Verifique credenciais de acesso à BD")
        return
#consulta os dados do sql para a ser usados na treeview
    cur = conn.cursor()
    sql = "SELECT * FROM mimarte;"
    cur.execute(sql)
    dados = cur.fetchall()
#limpa os dados, antes de carregar, para evitar replicar indefinidamente a nossa lista
    limpar()
# importa os dados do sql para a nossa treeview
    for linha in dados:
        tree.insert("", "end", values=tuple(linha))

#fecha as ligações do cursor e da base de dados
    cur.close()
    conn.close()

##função para limpar a TreeView
def limpar():
    tree.delete(*tree.get_children())

##função para remover 1 registo da TreeView e da base de dados
def remover():
    registo = tree.selection()

#mensagem ao utilizador, na eventualidade de não ter selecionado nenhuma linha
    if not registo:
        showwarning("Sem seleção!", "Tem que selecionar um registo para apagar")
        return
#obter os dados da treeview que se pretende eliminar da base de dados
    dados = tree.item(registo)["values"]
    codigo = dados[0]

    conn = conectar()  ##verificar a ligação
    if not conn:
        showwarning("Conexão...", "Verifique credenciais de acesso à BD")
        return
    cur = conn.cursor()
#comando para eliminar o registo selecionado da base de dados
    sql = "DELETE FROM mimarte WHERE id = ?;"
    cur.execute(sql, (codigo,))
    conn.commit()
    cur.close()
    conn.close()
# comando para eliminar o registo selecionado da treeview, e mensagem de alerta
    tree.delete(registo)
    showinfo("Sucesso", f"Cliente «{dados[1]}», removido com sucesso da BD!")

##função para editar 1 registo da TreeView
def editar():
    registo = tree.selection()
# mensagem ao utilizador, na eventualidade de não ter selecionado nenhuma linha
    if not registo:
        showwarning("Selecionar?!", "Terá que selecionar algum registo para poder editar")
        return

#Aumento do tamanho da janela, para comportar os campos para alteração ao registo
    jan.geometry("900x380")
    f3.pack()

#bloqueio dos botões superiores(com exceção do sair)
    bobter["state"] = "disabled"
    blimpar["state"] = "disabled"
    bremover["state"] = "disabled"
    beditar["state"] = "disabled"

    dados = tree.item(registo)["values"]
    eid["state"] = "normal"
    eid.delete(0, END)
    eid.insert(0, dados[0])
    eid["state"] = "disabled"
    enome.delete(0, END)
    enome.insert(0, dados[1])
    erua.delete(0, END)
    erua.insert(0, dados[2])
    elocal.delete(0, END)
    elocal.insert(0, dados[3])
    ezona.delete(0, END)
    ezona.insert(0, dados[4])

##função para replicar as alterações efetuadas na TreeView para a base de dados
def gravar():
    conn = conectar()  ##verificar a ligação
    if not conn:
        showwarning("Conexão...", "Verifique credenciais de acesso a BD")
        return
    cur = conn.cursor()
#comando para updade do registo selecionado, na nossa base de dados
    sql = """
        UPDATE mimarte 
        SET nome = ?, rua = ?, localidade = ?, zona = ? 
        WHERE id = ?;
    """
    cur.execute(sql, (enome.get(), erua.get(), elocal.get(), ezona.get(), int(eid.get())))
    conn.commit()

    cur.close()
    conn.close()

#chamada da função obter(), para atualização da treeview com os novos  dados da base de dados
    obter()

#redimencionamento da janela para o formato original, e reativação dos botões
    f3.pack_forget()
    jan.geometry("900x300")
    bobter["state"] = "normal"
    blimpar["state"] = "normal"
    bremover["state"] = "normal"
    beditar["state"] = "normal"

#função para abandonar o nosso programa
def sair():
    showwarning("A encerrar!", "Obrigado pela utilização!\nAté breve!")
    jan.destroy()

#####Configuração da GUI
###Criação da janela referente ao splash inicial, que nos permite criar a tabela na base de dados | carregar dados apartir de um csv
splash = Tk()
splash.title("Mim'Arte fotografia!")
splash.geometry("500x220")

# Carrega uma imagem
gfg_picture = PhotoImage(file="imagem.png")

# Exibe a imagem num Label
image_label = Label(splash, image=gfg_picture)
image_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche a janela com a imagem

# Cria o Label para o texto
splash_label = Label(splash, text="Seja bem vindo à Mim'Arte.\nEscolha uma das seguintes opções:",
                     font='times 20 bold')
splash_label.place(relx=0.5, rely=0.2, anchor="center")

# Cria os botões
bfechar = Button(splash, text="  Navegar para programa  ", command=splash.destroy)
bfechar.place(relx=0.5, rely=0.9, anchor="center")

bcarregar = Button(splash, text="Importar base de dados de cliente", command=importar)
bcarregar.place(relx=0.5, rely=0.7, anchor="center")

bcriartb = Button(splash, text="  Criar programa registo  ", command=criartb)
bcriartb.place(relx=0.5, rely=0.5, anchor="center")

splash.mainloop()

###Criação o programa baseado nos dados previamente carregados
jan = Tk()
jan.title("Mim'Arte fotografia | Lista de clientes")
jan.geometry("900x300")
jan.resizable(0, 0)

#Divisão em 3 frames, uma para os dados, outra para os botões e a última para os campos e botões usados para alteração dos registos
f1 = Frame(jan)
f2 = Frame(jan)
f3 = Frame(jan)

#Criação da treeview para organizar a apresentação de dados da base de dados, permitindo apenas seleção unitária de registos
tree = Treeview(f1, columns=("A", "B", "C", "D", "E"), show="headings", selectmode="browse")

#configuração dos cabeçalhos da treeview
tree.heading("A", text="Código")
tree.heading("B", text="Nome Cliente")
tree.heading("C", text="Rua")
tree.heading("D", text="Localidade")
tree.heading("E", text="Zona do país")

#configuração das colunas da treeview
tree.column("A", width=60, anchor="center")
tree.column("B", width=200)
tree.column("C", width=300)
tree.column("D", width=200)
tree.column("E", width=100, anchor="center")
tree.pack()

#Scrollbar da treeview
scrollbar = Scrollbar(f1, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)

#Posicionando a Treeview e a Scrollbar lado a lado
tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

#função chamada para evitar que a treeview arranque sem dados
obter()

##Botões da treeview para interação com a nossa base de dados
#Botão para consultar a BD e carregar para a treeview
bobter = Button(f2, text="Obter dados BD", command=obter)
bobter.pack(side="left", padx=10, pady=25)

#Botão para limpar os dados da treeview
blimpar = Button(f2, text="Limpar Treeview", command=limpar)
blimpar.pack(side="left", padx=10)

#Botão para remover um registo na BD e na treeview
bremover = Button(f2, text="Remover Cliente", command=remover)
bremover.pack(side="left", padx=10)

#Botão para editar um registo na BD e na treeview
beditar = Button(f2, text="Editar dados", command=editar)
beditar.pack(side="left", padx=10)

#Botão para sair do programa
bsair = Button(f2, text="Sair", command=sair)
bsair.pack(side="left", padx=10)

#Cabeçalhos das colunas de suporte à edição de dados da treeview
Label(f3, text="Id:").grid(row=0, column=0)#, sticky=N)
Label(f3, text="Nome:").grid(row=0, column=1)#, sticky=N)
Label(f3, text="Rua:").grid(row=0, column=2)#, sticky=N)
Label(f3, text="Localidade:").grid(row=0, column=3)#, sticky=N)
Label(f3, text="Zona:").grid(row=0, column=4)#, sticky=N)

#Campos de introdução dos dados a alterar no registo selecionado da treeview
eid = Entry(f3, width=5)
eid["state"] = "disabled"
eid.grid(row=1, column=0, sticky="w")
enome = Entry(f3, width=30)
enome.grid(row=1, column=1)
erua = Entry(f3, width=50)
erua.grid(row=1, column=2)
elocal = Entry(f3, width=30)
elocal.grid(row=1, column=3)
ezona = Entry(f3, width=10)
ezona.grid(row=1, column=4, sticky="w")

#botão para gravar as alterações no registo selecionado da treeview
bgravar = Button(f3, text="Gravar", command=gravar)
bgravar.grid(row=2, column=3, sticky=E)

#botão para para cancelar as alterações ao registo selecionado da treeview
bcancelar = Button(f3, text="Cancelar",
                   command=lambda: [f3.pack_forget(), jan.geometry("900x300"),
                                    bobter.configure(state="normal"),
                                    blimpar.configure(state="normal"),
                                    bremover.configure(state="normal"),
                                    beditar.configure(state="normal")])
bcancelar.grid(row=2, column=4, sticky=W)

#mostrar as frames 1 e 2
f1.pack()
f2.pack()

jan.mainloop()
