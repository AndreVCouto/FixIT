import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Reexecuta o script com privilégios de administrador
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
    sys.exit()

# Função para criar botões com tamanho fixo
def create_fixed_button(root, text, font, command=None, state=tk.NORMAL):
    style = ttk.Style()
    style.configure('TButton', font=font, padding=6, relief="flat", background='#FFFFFF')
    style.map('TButton', background=[('active', '#D3D3D3')])

    button = ttk.Button(root, text=text, style='TButton', command=command, state=state)
    button.config(width=30)  # Ajuste intermediário baseado em tamanho de caracteres
    return button

# Função para executar os comandos do CMD e abrir uma janela de CMD
def run_command_in_cmd(command):
    subprocess.Popen(f'cmd.exe /k {command}', creationflags=subprocess.CREATE_NEW_CONSOLE)

def verificar_reparo_disco():
    disable_buttons()  # Desativa todos os botões durante a execução
    run_command_in_cmd("chkdsk /f")  # Executa o comando no CMD
    enable_buttons()  # Reativa os botões após a execução

def limpeza_disco():
    disable_buttons()  # Desativa todos os botões durante a execução
    run_command_in_cmd("cleanmgr")  # Executa o comando no CMD
    enable_buttons()  # Reativa os botões após a execução

def desfrag_disco():
    disable_buttons()  # Desativa todos os botões durante a execução
    run_command_in_cmd("defrag E: /O")  # Executa o comando no CMD
    enable_buttons()  # Reativa os botões após a execução

def ping_rede():
    disable_buttons()  # Desativa todos os botões durante a execução
    run_command_in_cmd("ping google.com")  # Executa o comando no CMD
    enable_buttons()  # Reativa os botões após a execução

def verifica_arquivos():
    disable_buttons()  # Desativa todos os botões durante a execução
    run_command_in_cmd("sfc /scannow")  # Executa o comando no CMD
    enable_buttons()  # Reativa os botões após a execução

def atualiza_drivers():
    # Pop-up de confirmação
    response = messagebox.askyesno("Atualizações de Drivers", "Deseja atualizar todos os Drivers?")
    if response:
        disable_buttons()  # Desativa todos os botões durante a execução
        run_command_in_cmd("winget upgrade --all")  # Executa o comando no CMD
        enable_buttons()  # Reativa os botões após a execução
    else:
        # Fechar CMD se o usuário clicar em "Não"
        enable_buttons()

def disable_buttons():
    for button in button_list:
        button.config(state=tk.DISABLED)

def enable_buttons():
    for button in button_list:
        button.config(state=tk.NORMAL)

# Configuração da janela principal
root = tk.Tk()
root.title("FixIT")
root.geometry("740x400")
root.resizable(False, False)  # Desabilita redimensionamento manual
root.configure(bg='#FFFFFF')

# Painel interno
panel_frame = tk.Frame(root, bg='#FFFFFF')
panel_frame.place(x=20, y=20, width=700, height=400)  # Espaçamento de 20px em cada lado

# Fonte Verdana
title_font = ('Verdana', 18)
button_font = ('Verdana', 10)

# Título
title = tk.Label(panel_frame, text="FixIT", font=title_font, bg='#FFFFFF', fg='#000000')
title.place(x=0, y=0)  # Posição ajustada à esquerda, dentro do painel

# Configuração dos botões
button_texts = [
    ("Verificação e Reparo de Disco", verificar_reparo_disco),
    ("Verificação de Rede", ping_rede),
    ("Limpeza de Disco", limpeza_disco),
    ("Verificação de Arquivos de Sistema", verifica_arquivos),
    ("Desfragmentação de Disco", desfrag_disco),
    ("Em Breve", None) #Atualizações de Drivers
]

# Frame para organizar os botões
button_frame = tk.Frame(panel_frame, bg='#FFFFFF')
button_frame.place(relx=0.5, rely=0.45, anchor="center")  # Centralizado no painel

# Espaçamento entre botões
padx = 20
pady = 15

button_list = []
for i, (text, command) in enumerate(button_texts):
    button = create_fixed_button(button_frame, text, button_font, command)
    button.grid(row=i//2, column=i%2, padx=padx, pady=pady, ipadx=20, ipady=8)  # Ajuste de espaçamento interno e externo
    button_list.append(button)

# Créditos
credit = tk.Label(panel_frame, text="By André Couto", font=('Verdana', 8), bg='#FFFFFF', fg='#000000')
credit.place(x=600, y=345)  # Posição ajustada para o canto inferior direito

# Loop da interface
root.mainloop()
