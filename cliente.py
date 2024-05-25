from concurrent.futures import thread
import socket
import threading
from turtle import width
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import simpledialog

from sqlalchemy import column

ctk.set_appearance_mode("dark")

class Chat:
    def __init__(self):
        
        HOST = '127.0.0.1'
        PORT = 55555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        login = Tk()
        login.withdraw()
        
        self.janela_carregada = False
        self.ativo = True
        
        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)
        
        thread = threading.Thread(target=self.conecta)
        thread.start()
        self.janela(self.nome, self.sala)

    def janela(self, nome, sala):
        self.root = ctk.CTk()
        self.root.geometry("800x800")
        self.root.title("Chat")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.labelTitle = ctk.CTkLabel(self.root, text=f'{nome} está conectado na sala {sala}.', anchor='center')
        self.labelTitle.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), columnspan=2, sticky=ctk.W+ctk.E)

        self.boxMessages = ctk.CTkTextbox(self.root)
        self.boxMessages.grid(row=1, column=0, padx=(20, 20), pady=(10, 10), columnspan=2, sticky=ctk.W+ctk.E+ctk.S+ctk.N)

        self.sendMessage = ctk.CTkEntry(self.root)
        self.sendMessage.grid(row=2, column=0, padx=(20, 10), pady=(10, 30), sticky=ctk.W+ctk.E)

        self.bntEnviar = ctk.CTkButton(self.root, text="Enviar", font=("Arial", 16, 'bold'), command=lambda: self.enviarMensagem())
        self.bntEnviar.grid(row=2, column=1, padx=(0, 20), pady=(10, 30), sticky=ctk.W+ctk.E)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

        self.root.mainloop()

    
    def fechar(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.boxMessages.insert('end', recebido.decode())
                except:
                    pass

    def enviarMensagem(self):
        mensagem = self.sendMessage.get()
        self.client.send(mensagem.encode())


chat = Chat()
