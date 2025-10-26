import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math # Importação movida para o topo, boa prática

# ---- dicionário global para guardar os widgets de entrada ----
entradas = {}

# --- TEXTO DA AJUDA (ATUALIZADO) ---
TEXTO_EXPLICACAO = """
## Algoritmo de Pontuação (VSM) ##

Este cálculo atribui pontos às suas métricas corporais com pesos por categoria.
Agora há cálculo para MASCULINO e FEMININO (seletor na aba).

Masculino (pesos):
- Altura: 2
- % Gordura: 3
- IMMF: 3
- Proporção Ombro/Cintura: 2

Feminino (pesos):
- Altura: 2
- Proporção Cintura/Quadril: 2  # <--- ALTERAÇÃO (Nome corrigido)
- IMMLG (Índice de Massa Muscular Livre de Gordura): 2
- % Gordura: 4
"""

def formatar_float(entrada_str):
    """Converte string com vírgula ou ponto para float."""
    return float(entrada_str.replace(',', '.'))

# ----------------------------
# <--- NOVA FUNÇÃO (Para Task 2) --->
# ----------------------------

def atualizar_campos_vsm(event=None):
    """Esconde/mostra campos de Ombro/Quadril baseado no sexo VSM."""
    global entradas
    try:
        sexo = entradas['sexo_vsm'].get()
        
        if sexo == "Masculino":
            # Mostra Ombro
            entradas['label_ombro'].grid()
            entradas['ombro'].grid()
            # Esconde Quadril
            entradas['label_quadril'].grid_remove()
            entradas['quadril'].grid_remove()
            # Limpa o campo escondido para evitar erros de cálculo
            entradas['quadril'].delete(0, tk.END) 
        
        elif sexo == "Feminino":
            # Esconde Ombro
            entradas['label_ombro'].grid_remove()
            entradas['ombro'].grid_remove()
            # Limpa o campo escondido
            entradas['ombro'].delete(0, tk.END)
            # Mostra Quadril
            entradas['label_quadril'].grid()
            entradas['quadril'].grid()
            
    except KeyError:
        # Widgets ainda não foram criados, ignora.
        pass 
    except Exception as e:
        print(f"Erro ao atualizar campos VSM: {e}")

# ----------------------------
# CLASSIFICAÇÕES
# ----------------------------

def classificar_potencial_masc(pct):
    if pct == 100.0:
        return "Parabéns, você é um Deus Grego!"
    elif pct >= 90.0:
        return "Parabéns, você é um Chad!"
    elif pct >= 80.0:
        return "Parabéns, você é um Chad Light!"
    elif pct >= 65.0: 
        return "Legal, você é melhor que um Normie."
    elif pct >= 50.0: 
        return "Você é um Normie."
    else:
        return "Que pena, você é um subfive."

def classificar_potencial_fem(pct):
    if pct == 100.0:
        return "100% Legal, você é uma Deusa rara!"
    elif pct >= 90.0:
        return "Legal você é uma Stacy!"
    elif pct >= 75.0:
        return "Legal você é uma Stacylite!"
    elif pct >= 60.0:
        return "Legal, você é uma Beckie."
    elif pct >= 50.0:
        return "Você é uma Normie."
    elif pct >= 40.0:
        return "Que pena, você é uma subfive."
    else:
        return "Que pena, você é uma Femcel."

# ----------------------------
#  VSM - MASCULINO (SEU ORIGINAL)
# ----------------------------

def calcular_pontos_vsm_masc(altura_m, peso, percentual_gordura, largura_ombro, largura_cintura):
    """Lógica do VSM masculino (mantida)."""
    P_ALT = 2.0
    P_GORD = 3.0
    P_IMMF = 3.0
    P_PROP = 2.0
    FAIXA_PROP_GORD = 35.0 - 12.0

    try:
        # <--- ALTERAÇÃO (adicionado ombro na verificação)
        if altura_m <= 0 or largura_cintura <= 0 or largura_ombro <= 0:
            raise ZeroDivisionError

        massa_magra = peso * (100 - percentual_gordura) / 100
        immf = massa_magra / (altura_m ** 2)
        proporcao_oc = largura_ombro / largura_cintura

    except ZeroDivisionError:
        # <--- ALTERAÇÃO (mensagem de erro atualizada)
        return None, "Erro: Altura, cintura e ombro devem ser maiores que zero."

    # Altura
    pa = 0.0
    if altura_m < 1.65:
        pa = 0.0
    elif 1.65 <= altura_m <= 1.80:
        faixa = 1.80 - 1.65
        pa = P_ALT * ((altura_m - 1.65) / faixa)
    elif 1.80 < altura_m <= 1.95:
        pa = P_ALT
    elif 1.95 < altura_m <= 2.10:
        faixa_queda = 2.10 - 1.95
        pa = P_ALT * (1.0 - ((altura_m - 1.95) / faixa_queda))
    else:
        pa = 0.0

    # % Gordura
    pg = 0.0
    if percentual_gordura > 30.0:
        pg = 0.0
    elif 12.0 < percentual_gordura <= 30.0:
        pg = P_GORD * (1.0 - ((percentual_gordura - 12.0) / FAIXA_PROP_GORD))
    else:  # <= 12
        pg = P_GORD

    # Proporção Ombro/Cintura
    p = proporcao_oc
    pp = 0.0
    if p >= 1.6:
        pp = P_PROP
    elif 1.0 <= p < 1.6:
        pp = P_PROP * ((p - 1.0) / (1.6 - 1.0))
    else:
        pp = 0.0

    # IMMF
    pi = 0.0
    if immf >= 23.0:
        pi = P_IMMF
    elif 16.0 <= immf < 23.0:
        pi = P_IMMF * ((immf - 16.0) / (23.0 - 16.0))
    else:
        pi = 0.0

    # Clamp
    pa = max(0.0, min(P_ALT, pa))
    pg = max(0.0, min(P_GORD, pg))
    pi = max(0.0, min(P_IMMF, pi))
    pp = max(0.0, min(P_PROP, pp))

    pt = pa + pg + pi + pp
    pm = P_ALT + P_GORD + P_IMMF + P_PROP
    pct = (pt / pm) * 100.0

    dados = {
        'immf': immf,
        'proporcao': proporcao_oc,
        'pa': pa, 'pg': pg, 'pi': pi, 'pp': pp,
        'pt': pt, 'pm': pm, 'percentual': pct
    }
    return dados, None

# ----------------------------
#  VSM - FEMININO (NOVO)
# ----------------------------

def calcular_pontos_vsm_fem(altura_m, peso, percentual_gordura, largura_quadril, largura_cintura):
    """
    Parâmetros Femininos:
    - Altura (2 pts): máx entre 1,65–1,75; 0 <1,50 e >1,80; linear nas transições.
    # <--- ALTERAÇÃO (Nome da proporção corrigido de Q/C para C/Q)
    - Proporção Cintura/Quadril (2 pts): máx para <0,71; 0 para >=1; linear entre.
    - IMMLG (2 pts): máx >=21; 0 <=16; linear entre 16–21.
    - % Gordura (4 pts): máx entre 12–20; regressão linear 20–35 até 0; >35 => 0.
                       <12: desconta proporcional (linear até 0% → 0).
    """
    P_ALT = 2.0
    P_QC  = 2.0
    P_IMM = 2.0
    P_PG  = 4.0

    try:
        # <--- ALTERAÇÃO (Adicionado 'largura_quadril' à verificação de ZeroDivisionError)
        if altura_m <= 0 or largura_cintura <= 0 or largura_quadril <= 0:
            raise ZeroDivisionError

        massa_magra = peso * (1 - percentual_gordura / 100.0)
        immlg = massa_magra / (altura_m ** 2)  # kg/m²
        
        # <--- ALTERAÇÃO (Cálculo invertido para Cintura/Quadril conforme solicitado)
        proporcao_qc = largura_cintura / largura_quadril

    except ZeroDivisionError:
        # <--- ALTERAÇÃO (Mensagem de erro atualizada)
        return None, "Erro: Altura, cintura e quadril devem ser maiores que zero."

    # Altura (2 pts)
    if altura_m <= 1.50 or altura_m >= 1.80:
        pa = 0.0
    elif 1.50 < altura_m < 1.65:
        pa = P_ALT * ((altura_m - 1.50) / (1.65 - 1.50))
    elif 1.65 <= altura_m <= 1.75:
        pa = P_ALT
    else:  # 1.75 < h < 1.80
        pa = P_ALT * (1.0 - ((altura_m - 1.75) / (1.80 - 1.75)))

    # Proporção Cintura/Quadril (2 pts) – menor é melhor até 0,71
    # (A lógica original já estava correta para C/Q, só o cálculo estava invertido)
    if proporcao_qc >= 1.0:
        pqc = 0.0
    elif proporcao_qc < 0.71:
        pqc = P_QC
    else:  # 0.71 <= r < 1.0 → decresce linearmente até 0
        pqc = P_QC * (1.0 - ((proporcao_qc - 0.71) / (1.0 - 0.71)))

    # IMMLG (2 pts) – >=21 máximo, <=16 zero, linear entre
    if immlg >= 21.0:
        pim = P_IMM
    elif immlg <= 16.0:
        pim = 0.0
    else:
        pim = P_IMM * ((immlg - 16.0) / (21.0 - 16.0))

    # % Gordura (4 pts)
    pg = percentual_gordura
    if pg > 35.0:
        ppg = 0.0
    elif 20.0 < pg <= 35.0:
        ppg = P_PG * (1.0 - ((pg - 20.0) / (35.0 - 20.0)))
    elif 12.0 <= pg <= 20.0:
        ppg = P_PG
    elif 0.0 <= pg < 12.0:
        # “desconte apenas a pontuação proporcional de regressão linear”
        # Redução linear de 12% (cheio) até 0% (zero).
        ppg = P_PG * (pg / 12.0)
    else:
        ppg = 0.0  # guarda para negativos

    # Clamp
    pa  = max(0.0, min(P_ALT, pa))
    pqc = max(0.0, min(P_QC,  pqc))
    pim = max(0.0, min(P_IMM, pim))
    ppg = max(0.0, min(P_PG,  ppg))

    pt = pa + pqc + pim + ppg
    pm = P_ALT + P_QC + P_IMM + P_PG  # 10 pontos
    pct_total = (pt / pm) * 100.0

    dados = {
        'immlg': immlg,
        'proporcao_qc': proporcao_qc,
        'pa': pa, 'pqc': pqc, 'pim': pim, 'ppg': ppg,
        'pt': pt, 'pm': pm, 'percentual': pct_total
    }
    return dados, None

# ----------------------------
#  JACKSON & POLLOCK FUNCTIONS (2ª aba)
# ----------------------------

def densidade_4dobras(sexo: str, soma_mm: float) -> float:
    # import math (movido para o topo)
    if soma_mm <= 0:
        raise ValueError("A soma das dobras deve ser > 0.")
    if sexo.lower().startswith('m'):
        return 1.1620 - 0.0630 * math.log10(soma_mm)
    else:
        return 1.1549 - 0.0678 * math.log10(soma_mm)

def densidade_7dobras(sexo: str, soma_mm: float, idade: int) -> float:
    if soma_mm <= 0:
        raise ValueError("A soma das dobras deve ser > 0.")
    if idade <= 0:
        raise ValueError("Idade inválida.")
    if sexo.lower().startswith('m'):
        return 1.112 - 0.00043499 * soma_mm + 0.00000055 * (soma_mm ** 2) - 0.00028826 * idade
    else:
        return 1.097 - 0.00046971 * soma_mm + 0.00000056 * (soma_mm ** 2) - 0.00012828 * idade

def siri_percentual_gordura(densidade: float) -> float:
    if densidade <= 0:
        raise ValueError("Densidade inválida.")
    return (495.0 / densidade) - 450.0

# ----------------------------
#  UI: ABA PERCENTUAL DE GORDURA (Jackson & Pollock)
# ----------------------------

class AbaJacksonPollock:
    def __init__(self, master):
        self.master = master
        self.entradas = {}
        self._build_ui()

    def _build_ui(self):
        padx_val, pady_val = 8, 5

        tk.Label(self.master, text="Percentual de Gordura (Jackson & Pollock)", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, columnspan=4, pady=(5,8)
        )

        tk.Label(self.master, text="Sexo:").grid(row=1, column=0, sticky='w', padx=padx_val, pady=pady_val)
        self.sexo_var = tk.StringVar(value="Masculino")
        sexo_cb = ttk.Combobox(self.master, textvariable=self.sexo_var, state="readonly",
                               values=["Masculino", "Feminino"], width=14)
        sexo_cb.grid(row=1, column=1, sticky='w', padx=padx_val, pady=pady_val)
        sexo_cb.bind("<<ComboboxSelected>>", lambda e: self._montar_campos())

        tk.Label(self.master, text="Protocolo:").grid(row=1, column=2, sticky='w', padx=padx_val, pady=pady_val)
        self.protocolo_var = tk.StringVar(value="4 Dobras")
        prot_cb = ttk.Combobox(self.master, textvariable=self.protocolo_var, state="readonly",
                               values=["4 Dobras", "7 Dobras"], width=14)
        prot_cb.grid(row=1, column=3, sticky='w', padx=padx_val, pady=pady_val)
        prot_cb.bind("<<ComboboxSelected>>", lambda e: self._montar_campos())

        tk.Label(self.master, text="Idade (anos):").grid(row=2, column=0, sticky='w', padx=padx_val, pady=pady_val)
        self.entradas['idade'] = tk.Entry(self.master, width=10)
        self.entradas['idade'].grid(row=2, column=1, sticky='w', padx=padx_val, pady=pady_val)

        self.frame_campos = tk.Frame(self.master, borderwidth=1, relief='groove')
        self.frame_campos.grid(row=3, column=0, columnspan=4, sticky='we', padx=padx_val, pady=(pady_val, 8))

        tk.Button(self.master, text="CALCULAR % GORDURA", command=self._calcular, bg="#4CAF50", fg="white").grid(
            row=4, column=0, columnspan=4, pady=(6,10)
        )

        self.resultado = tk.Label(self.master, text="Aguardando dados...", justify='left', fg='blue', font=('Courier', 10))
        self.resultado.grid(row=5, column=0, columnspan=4, sticky='w', padx=padx_val, pady=pady_val)

        self._montar_campos()

    def _limpar_frame_campos(self):
        for w in self.frame_campos.winfo_children():
            w.destroy()
        self.entradas = {k:v for k,v in self.entradas.items() if k == 'idade'}

    def _montar_campos(self):
        self._limpar_frame_campos()
        sexo = self.sexo_var.get()
        protocolo = self.protocolo_var.get()

        padx_val, pady_val = 6, 4

        if protocolo == "4 Dobras":
            if sexo == "Masculino":
                pontos = ["Tríceps (mm)", "Subescapular (mm)", "Suprailíaca (mm)", "Abdômen (mm)"]
            else:
                pontos = ["Tríceps (mm)", "Suprailíaca (mm)", "Abdômen (mm)", "Coxa (mm)"]
        else:
            pontos = [
                "Peitoral (mm)", "Axilar média (mm)", "Tríceps (mm)", "Subescapular (mm)",
                "Abdômen (mm)", "Suprailíaca (mm)", "Coxa (mm)"
            ]

        tk.Label(self.frame_campos, text="Informe as dobras (mm):", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky='w', padx=padx_val, pady=(6,6)
        )

        r = 1
        for p in pontos:
            tk.Label(self.frame_campos, text=p).grid(row=r, column=0, sticky='w', padx=padx_val, pady=pady_val)
            ent = tk.Entry(self.frame_campos, width=12)
            ent.grid(row=r, column=1, sticky='w', padx=padx_val, pady=pady_val)
            self.entradas[p] = ent
            r += 1

        dica = (
            "Dicas:\n"
            "- Meça no lado direito do corpo.\n"
            "- Segure a prega com polegar e indicador; posicione o adipômetro ~1 cm abaixo dos dedos.\n"
            "- Leia após ~2s; faça 2–3 medidas por ponto e use a média."
        )
        tk.Label(self.frame_campos, text=dica, justify='left', fg='gray').grid(
            row=r, column=0, columnspan=2, sticky='w', padx=padx_val, pady=(6,8)
        )

        if self.protocolo_var.get() == "7 Dobras":
            self.entradas['idade'].config(state='normal')
        else:
            self.entradas['idade'].delete(0, tk.END)
            self.entradas['idade'].config(state='disabled')

    def _somar_dobras(self):
        soma = 0.0
        for k, widget in self.entradas.items():
            if k == 'idade':
                continue
            val_str = widget.get().strip()
            if not val_str:
                raise ValueError("Preencha todas as dobras.")
            v = formatar_float(val_str)
            if v < 0:
                raise ValueError("Dobras não podem ser negativas.")
            soma += v
        return soma

    def _calcular(self):
        try:
            sexo = self.sexo_var.get()
            protocolo = self.protocolo_var.get()
            soma = self._somar_dobras()

            if protocolo == "4 Dobras":
                dens = densidade_4dobras(sexo, soma)
                pct = siri_percentual_gordura(dens)
                detalhe = f"Protocolo 4 dobras | Sexo: {sexo} | Soma: {soma:.1f} mm\n"
            else:
                idade_str = self.entradas['idade'].get().strip()
                if not idade_str:
                    messagebox.showerror("Erro", "Informe a idade para o protocolo de 7 dobras.")
                    return
                idade = int(formatar_float(idade_str))
                dens = densidade_7dobras(sexo, soma, idade)
                pct = siri_percentual_gordura(dens)
                detalhe = f"Protocolo 7 dobras | Sexo: {sexo} | Soma: {soma:.1f} mm | Idade: {idade}\n"

            texto = (
                "##### RESULTADO - JACKSON & POLLOCK #####\n\n"
                f"{detalhe}"
                f"Densidade corporal: {dens:.4f} g/mL\n"
                f"% Gordura (Siri): {pct:.2f}%"
            )
            self.resultado.config(text=texto)

        except ValueError as ve:
            messagebox.showerror("Erro de Entrada", str(ve))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

# ----------------------------
#  ABA VSM (com seletor de sexo)
# ----------------------------

def mostrar_explicacao():
    messagebox.showinfo("Algoritmo de Pontuação", TEXTO_EXPLICACAO)

def calcular_e_exibir():
    """Botão da aba VSM: escolhe cálculo masculino ou feminino pelo seletor."""
    try:
        sexo_vsm = entradas['sexo_vsm'].get()  # "Masculino" ou "Feminino"

        # --- <--- ALTERAÇÃO (Campos comuns lidos primeiro) ---
        altura_cm = formatar_float(entradas['altura'].get())
        peso = formatar_float(entradas['peso'].get())
        percentual_gordura = formatar_float(entradas['gordura'].get())
        largura_cintura = formatar_float(entradas['cintura'].get())

        altura_m = altura_cm / 100.0

        if sexo_vsm == "Masculino":
            # --- <--- ALTERAÇÃO (Leitura do campo específico movida para cá) ---
            largura_ombro = formatar_float(entradas['ombro'].get())

            # --- <--- ALTERAÇÃO (Validação apenas dos campos usados) ---
            if any(v < 0 for v in [altura_cm, peso, percentual_gordura, largura_ombro, largura_cintura]):
                messagebox.showerror("Erro de Entrada", "Valores não podem ser negativos.")
                return

            dados, erro = calcular_pontos_vsm_masc(
                altura_m, peso, percentual_gordura, largura_ombro, largura_cintura
            )
            if erro:
                messagebox.showerror("Erro de Cálculo", erro)
                return

            classificacao = classificar_potencial_masc(dados['percentual'])
            resultado_formatado = (
                f"##### RESULTADO - CALCULADORA DE VSM (MASC) #####\n\n"
                f"IMMF: {dados['immf']:.2f} | Proporção O/C: {dados['proporcao']:.2f}\n\n"
                f"Pontuação Altura: {dados['pa']:.2f} / 2.00\n"
                f"Pontuação Gordura: {dados['pg']:.2f} / 3.00\n"
                f"Pontuação IMMF: {dados['pi']:.2f} / 3.00\n"
                f"Pontuação Proporção: {dados['pp']:.2f} / 2.00\n\n"
                f"Pontuação Total VSM: {dados['percentual']:.2f}% ({dados['pt']:.2f} / {dados['pm']:.2f})\n\n"
                f"CLASSIFICAÇÃO: {classificacao}"
            )
        else:
            # --- <--- ALTERAÇÃO (Leitura do campo específico movida para cá) ---
            largura_quadril = formatar_float(entradas['quadril'].get())

            # --- <--- ALTERAÇÃO (Validação apenas dos campos usados) ---
            if any(v < 0 for v in [altura_cm, peso, percentual_gordura, largura_quadril, largura_cintura]):
                messagebox.showerror("Erro de Entrada", "Valores não podem ser negativos.")
                return

            dados, erro = calcular_pontos_vsm_fem(
                altura_m, peso, percentual_gordura, largura_quadril, largura_cintura
            )
            if erro:
                messagebox.showerror("Erro de Cálculo", erro)
                return

            classificacao = classificar_potencial_fem(dados['percentual'])
            # --- <--- ALTERAÇÃO (Rótulos corrigidos para C/Q) ---
            resultado_formatado = (
                f"##### RESULTADO - CALCULADORA DE VSM (FEM) #####\n\n"
                f"IMMLG: {dados['immlg']:.2f} kg/m² | Proporção C/Q: {dados['proporcao_qc']:.2f}\n\n"
                f"Pontuação Altura: {dados['pa']:.2f} / 2.00\n"
                f"Pontuação % Gordura: {dados['ppg']:.2f} / 4.00\n"
                f"Pontuação IMMLG: {dados['pim']:.2f} / 2.00\n"
                f"Pontuação C/Q: {dados['pqc']:.2f} / 2.00\n\n"
                f"Pontuação Total VSM: {dados['percentual']:.2f}% ({dados['pt']:.2f} / {dados['pm']:.2f})\n\n"
                f"CLASSIFICAÇÃO: {classificacao}"
            )

        entradas['resultado_label'].config(text=resultado_formatado)

    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira números válidos em todos os campos obrigatórios.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# ----------------------------
#  INTERFACE COM ABAS
# ----------------------------

def criar_interface():
    """Configura e exibe a janela principal com abas."""
    global entradas

    janela = tk.Tk()
    janela.title("Calculadora de VSM")
    janela.geometry("620x620")

    notebook = ttk.Notebook(janela)
    notebook.pack(fill='both', expand=True)

    # ===== ABA 1: VSM =====
    aba_vsm = tk.Frame(notebook)
    notebook.add(aba_vsm, text="VSM")

    padx_val, pady_val = 10, 6

    # Título + ajuda
    frame_titulo = tk.Frame(aba_vsm)
    frame_titulo.grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(frame_titulo, text="CALCULADORA DE VSM", font=("Arial", 11, "bold")).pack(side=tk.LEFT)
    tk.Button(frame_titulo, text="❓", command=mostrar_explicacao, width=2).pack(side=tk.LEFT, padx=5)

    # Seletor de sexo (para alternar cálculo MASC/FEM)
    tk.Label(aba_vsm, text="Sexo (VSM):").grid(row=1, column=0, padx=padx_val, pady=pady_val, sticky='w')
    sexo_vsm = ttk.Combobox(aba_vsm, state="readonly", values=["Masculino", "Feminino"], width=14)
    sexo_vsm.set("Masculino")
    sexo_vsm.grid(row=1, column=1, padx=padx_val, pady=pady_val, sticky='w')
    entradas['sexo_vsm'] = sexo_vsm
    # --- <--- ALTERAÇÃO (Adiciona o 'bind' para chamar a função de atualização) ---
    sexo_vsm.bind("<<ComboboxSelected>>", atualizar_campos_vsm)

    # Entradas comuns
    tk.Label(aba_vsm, text="Altura (cm):").grid(row=2, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['altura'] = tk.Entry(aba_vsm)
    entradas['altura'].grid(row=2, column=1, padx=padx_val, pady=pady_val)

    tk.Label(aba_vsm, text="Peso (kg):").grid(row=3, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['peso'] = tk.Entry(aba_vsm)
    entradas['peso'].grid(row=3, column=1, padx=padx_val, pady=pady_val)

    tk.Label(aba_vsm, text="% Gordura:").grid(row=4, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['gordura'] = tk.Entry(aba_vsm)
    entradas['gordura'].grid(row=4, column=1, padx=padx_val, pady=pady_val)

    # --- <--- ALTERAÇÃO (Salva os LABELS no dict 'entradas' para poder escondê-los) ---
    
    # Larguras / perímetros necessários
    entradas['label_ombro'] = tk.Label(aba_vsm, text="Largura do Ombro (cm):")
    entradas['label_ombro'].grid(row=5, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['ombro'] = tk.Entry(aba_vsm)
    entradas['ombro'].grid(row=5, column=1, padx=padx_val, pady=pady_val)

    tk.Label(aba_vsm, text="Largura da Cintura (cm):").grid(row=6, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['cintura'] = tk.Entry(aba_vsm)
    entradas['cintura'].grid(row=6, column=1, padx=padx_val, pady=pady_val)

    entradas['label_quadril'] = tk.Label(aba_vsm, text="Largura do Quadril (cm):")
    entradas['label_quadril'].grid(row=7, column=0, padx=padx_val, pady=pady_val, sticky='w')
    entradas['quadril'] = tk.Entry(aba_vsm)
    entradas['quadril'].grid(row=7, column=1, padx=padx_val, pady=pady_val)

    # Botão de cálculo
    tk.Button(aba_vsm, text="CALCULADORA DE VSM", command=calcular_e_exibir,
              bg='#4CAF50', fg='white').grid(row=8, column=0, columnspan=2, padx=padx_val, pady=15)

    entradas['resultado_label'] = tk.Label(
        aba_vsm, text="Aguardando dados...", justify=tk.LEFT, fg='blue', font=('Courier', 10)
    )
    entradas['resultado_label'].grid(row=9, column=0, columnspan=2, padx=padx_val, pady=pady_val)

    # ===== ABA 2: Percentual de Gordura =====
    aba_jp = tk.Frame(notebook)
    notebook.add(aba_jp, text="Percentual de Gordura")
    AbaJacksonPollock(aba_jp)

    # --- <--- ALTERAÇÃO (Chama a função 1 vez para esconder o campo 'quadril' inicialmente) ---
    atualizar_campos_vsm()

    janela.mainloop()

# iniciar
if __name__ == "__main__":
    criar_interface()
