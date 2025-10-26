📏 Calculadora de VSM + % Gordura (Tkinter)

App simples em Python + Tkinter com duas abas:

VSM (pontuação de estética/shape) para Masculino e Feminino

Percentual de Gordura pelos protocolos Jackson & Pollock (4 ou 7 dobras) com fórmula de Siri

🧩 Funcionalidades

Seletor de sexo (VSM) com campos dinâmicos:

Masculino: usa Ombro/Cintura (O/C)

Feminino: usa Cintura/Quadril (C/Q)

Pontuação VSM:

Masculino (pesos): Altura (2), % Gordura (3), IMMF (3), O/C (2)

Feminino (pesos): Altura (2), C/Q (2), IMMLG (2), % Gordura (4)

Classificação automática por percentual final (mensagens típicas “Chad/Stacy” etc.)

Jackson & Pollock:

4 dobras (sem idade) e 7 dobras (solicita idade)

Cálculo de densidade corporal e % Gordura (Siri)

Validações e mensagens de erro amigáveis

🚀 Como usar

Tenha Python 3 instalado (Tkinter já vem no Python “full”).

Salve o arquivo como calculadora_vsm.py.

Rode:

python calculadora_vsm.py


Aba VSM: escolha o sexo, preencha altura, peso, % gordura e as larguras pedidas (Ombro/Cintura ou Cintura/Quadril). Clique CALCULADORA DE VSM.

Aba Percentual de Gordura: selecione sexo e protocolo (4/7 dobras), preencha as dobras (e idade se 7 dobras). Clique CALCULAR % GORDURA.

📐 Detalhes de cálculo (resumo)

IMMF/IMMLG = massa magra / altura² (kg/m²)

Proporções:

Masc: O/C = ombro ÷ cintura

Fem: C/Q = cintura ÷ quadril (menor é melhor até ~0,71)

Siri: %G = (495 / densidade) − 450

Regras de pontuação seguem faixas lineares e clamps conforme comentários no código.

🧠 Tecnologias

Python 3

Tkinter (GUI nativa)

math (log10 para fórmulas J&P)

📄 Licença

Uso livre para fins pessoais e educacionais.
