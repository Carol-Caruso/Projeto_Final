import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def conectar():
    return sqlite3.connect('clientes1.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
      CREATE TABLE IF NOT EXISTS clientes1 (
             id INTEGER PRIMARY KEY,
             nome TEXT NOT NULL,
             email TEXT NOT NULL,
             telefone INTEGER NOT NULL,
             endereco TEXT NOT NULL                                  
        )
    ''')
    conn.commit()
    conn.close()

def agregar_clientes1():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    email = entry_email.get()
    endereco = entry_endereco.get()

    if nome and telefone and email and endereco:
       conn = conectar()
       c = conn.cursor()
       c.execute('INSERT INTO clientes1(nome, telefone, email, endereco) VALUES(?, ?, ?, ?)', 
                 (nome, telefone, email, endereco))
       conn.commit()
       conn.close()
       messagebox.showinfo('Cliente cadastrado', 'O cliente foi adicionado no banco de dados') 
       mostrar_clientes1()
    else:
       messagebox.showerror('Erro', 'Ocorreu um erro o cliente não foi adicionado ao banco')
 
def mostrar_clientes1():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * from clientes1')
    clientes1 = c.fetchall()
    for cliente in clientes1:
        tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2],cliente[3], cliente[4]))
    conn.close()

def eliminar_cliente():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        conn = conectar() 
        c = conn.cursor()
        c.execute('DELETE FROM clientes1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Exito', 'CLIENTE DELETADO')
        mostrar_clientes1()
    else:
        messagebox.showerror('Erro', 'Cliente não deletados')

def atualizar_cliente():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        novo_nome = entry_nome.get()
        novo_telefone = entry_telefone.get()
        novo_email = entry_email.get()
        novo_endereco = entry_endereco.get()
        if (novo_nome and novo_telefone and novo_email and novo_endereco):
            conn = conectar() 
            c = conn.cursor()
            c.execute('UPDATE clientes1 SET nome = ?, telefone = ?, email = ?, endereco = ? WHERE id = ?', 
                     (novo_nome, novo_telefone, novo_email, novo_endereco, user_id)) 
            conn.commit()
            conn.close()
            messagebox.showinfo('Exito', 'Cliente alterado')
            mostrar_clientes1()
        else:
            messagebox.showerror('Erro', 'Clientes1 não inseridos')
    else:
        messagebox.showwarning('Atenção', 'O Cliente não foi selecionado')

def buscar():
    nome = entry_nome.get()

    if nome.isdigit():
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT * FROM clientes1 WHERE id = ?", (nome))
        pessoa = c.fetchone()
        conn.commit()
        conn.close()

        if nome:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(tk.END, pessoa[1])
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(tk.END, pessoa[2])
            entry_email.delete(0, tk.END)
            entry_email.insert(tk.END, pessoa[3])
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(tk.END, pessoa[4])
        else:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
    else:
        messagebox.showerror("Erro", "Nome não cadastrado.")

janela = tk.Tk()
janela.title('CADASTRO DE CLIENTES1 - EMPRESA XYZ COMERCIO')

label_nome = tk.Label(janela, text='NOME')
label_nome.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10, ipadx=10)

label_telefone = tk.Label(janela, text='TELEFONE')
label_telefone.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=1, column=1, padx=10, pady=10, ipadx=10)

label_email = tk.Label(janela, text='EMAIL')
label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_email = tk.Entry(janela)
entry_email.grid(row=2, column=1, padx=10, pady=10, ipadx=10)

label_endereco = tk.Label(janela, text='ENDEREÇO')
label_endereco.grid(row=3, column=0, padx=10, pady=10, sticky=tk.E)
entry_endereco = tk.Entry(janela)
entry_endereco.grid(row=3, column=1, padx=10, pady=10, ipadx=10)

btn_agregar = tk.Button(janela, text='INSERIR CLIENTE', command=agregar_clientes1)
btn_agregar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

btn_atualizar = tk.Button(janela, text='ATUALIZAR CLIENTE', command=atualizar_cliente)
btn_atualizar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

btn_deletar = tk.Button(janela, text='DELETAR CLIENTE', command=eliminar_cliente)
btn_deletar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

btn_procurar = tk.Button(janela, text='PROCURAR CLIENTE', command=buscar)
btn_procurar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

columns = ('ID','NOME','TELEFONE', 'EMAIL', 'ENDEREÇO')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
mostrar_clientes1()

janela.mainloop()