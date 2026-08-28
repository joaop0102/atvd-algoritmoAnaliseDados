import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PASTA_DADOS = "dados"
PASTA_RESULTADOS = "resultados"

ARQUIVO_ORIGINAL = os.path.join(
    PASTA_DADOS,
    "pacientes_sinteticos.csv"
)

ARQUIVO_PROTEGIDO = os.path.join(
    PASTA_RESULTADOS,
    "dados_protegidos.csv"
)

ARQUIVO_RELATORIO = os.path.join(
    PASTA_RESULTADOS,
    "relatorio.txt"
)

# Semente para tornar os resultados reproduzíveis.
SEED = 42

# Parâmetro didático de privacidade diferencial.
# Quanto menor o epsilon, maior o ruído.
EPSILON = 1.0

np.random.seed(SEED)


# ============================================================
# PREPARAÇÃO DAS PASTAS
# ============================================================

def preparar_pastas():
    os.makedirs(PASTA_DADOS, exist_ok=True)
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)


# ============================================================
# 1. GERAÇÃO DE DADOS SINTÉTICOS
# ============================================================

def gerar_dados_sinteticos(n=1000):

    rng = np.random.default_rng(SEED)

    ids = [
        f"P{i:04d}"
        for i in range(1, n + 1)
    ]

    idade = rng.integers(
        18,
        90,
        size=n
    )

    sexo = rng.choice(
        ["F", "M"],
        size=n
    )

    diagnosticos = rng.choice(
        [
            "Nenhum",
            "Hipertensão",
            "Diabetes tipo 2",
            "Asma",
            "Hipotireoidismo"
        ],
        size=n,
        p=[
            0.30,
            0.28,
            0.20,
            0.12,
            0.10
        ]
    )

    # IMC sintético
    imc = np.clip(
        rng.normal(
            loc=28,
            scale=5,
            size=n
        ),
        17,
        45
    )

    # Glicemia sintética
    glicemia = rng.normal(
        loc=115,
        scale=35,
        size=n
    )

    # Aumenta artificialmente a glicemia em pessoas
    # classificadas como diabetes.
    glicemia = np.where(
        diagnosticos == "Diabetes tipo 2",
        glicemia + 55,
        glicemia
    )

    glicemia = np.clip(
        glicemia,
        60,
        300
    )

    # Pressão sistólica
    pressao_sistolica = rng.normal(
        loc=125,
        scale=18,
        size=n
    )

    pressao_sistolica = np.where(
        diagnosticos == "Hipertensão",
        pressao_sistolica + 25,
        pressao_sistolica
    )

    pressao_sistolica = np.clip(
        pressao_sistolica,
        90,
        220
    )

    # Pressão diastólica
    pressao_diastolica = (
        pressao_sistolica * 0.60
        + rng.normal(0, 7, n)
    )

    pressao_diastolica = np.clip(
        pressao_diastolica,
        50,
        140
    )

    # Internações
    internacoes = rng.poisson(
        0.5,
        size=n
    )

    # Pessoas com diabetes e hipertensão
    # possuem uma frequência sintética maior.
    internacoes += np.where(
        diagnosticos == "Diabetes tipo 2",
        rng.binomial(2, 0.30, n),
        0
    )

    internacoes += np.where(
        diagnosticos == "Hipertensão",
        rng.binomial(1, 0.25, n),
        0
    )

    # Classificação sintética de risco
    risco = []

    for i in range(n):

        pontos = 0

        if idade[i] >= 60:
            pontos += 1

        if glicemia[i] >= 180:
            pontos += 2

        if pressao_sistolica[i] >= 160:
            pontos += 2

        if imc[i] >= 30:
            pontos += 1

        if internacoes[i] >= 2:
            pontos += 1

        if pontos >= 4:
            risco.append("Alto")

        elif pontos >= 2:
            risco.append("Médio")

        else:
            risco.append("Baixo")

    df = pd.DataFrame({
        "ID": ids,
        "Idade": idade,
        "Sexo": sexo,
        "Diagnostico": diagnosticos,
        "Pressao_Sistolica": np.round(
            pressao_sistolica,
            1
        ),
        "Pressao_Diastolica": np.round(
            pressao_diastolica,
            1
        ),
        "Glicemia": np.round(
            glicemia,
            1
        ),
        "IMC": np.round(
            imc,
            1
        ),
        "Internacoes": internacoes,
        "Risco": risco
    })

    return df


# ============================================================
# 2. ANONIMIZAÇÃO / GENERALIZAÇÃO
# ============================================================

def anonimizar_dados(df):

    protegido = df.copy()

    # --------------------------------------------------------
    # Remove o identificador individual
    # --------------------------------------------------------

    protegido = protegido.drop(
        columns=["ID"]
    )

    # --------------------------------------------------------
    # Generaliza a idade
    # --------------------------------------------------------

    bins = [
        0,
        29,
        39,
        49,
        59,
        69,
        79,
        120
    ]

    labels = [
        "0-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
        "70-79",
        "80+"
    ]

    protegido["Faixa_Idade"] = pd.cut(
        protegido["Idade"],
        bins=bins,
        labels=labels,
        right=True
    )

    protegido = protegido.drop(
        columns=["Idade"]
    )

    # --------------------------------------------------------
    # Arredondamento/generalização
    # --------------------------------------------------------

    protegido["Glicemia"] = (
        np.round(
            protegido["Glicemia"] / 10
        ) * 10
    )

    protegido["IMC"] = (
        np.round(
            protegido["IMC"]
        )
    )

    protegido["Pressao_Sistolica"] = (
        np.round(
            protegido["Pressao_Sistolica"] / 5
        ) * 5
    )

    protegido["Pressao_Diastolica"] = (
        np.round(
            protegido["Pressao_Diastolica"] / 5
        ) * 5
    )

    return protegido


# ============================================================
# 3. RUÍDO LAPLACE
# ============================================================

def ruido_laplace(
    valor,
    sensibilidade,
    epsilon=EPSILON
):

    escala = sensibilidade / epsilon

    ruido = np.random.laplace(
        0,
        escala
    )

    return valor + ruido


# ============================================================
# 4. ESTATÍSTICAS
# ============================================================

def calcular_estatisticas(df):

    numericas = [
        "Pressao_Sistolica",
        "Pressao_Diastolica",
        "Glicemia",
        "IMC",
        "Internacoes"
    ]

    estatisticas = df[numericas].describe().T

    estatisticas[
        "mediana"
    ] = df[numericas].median()

    estatisticas[
        "variancia"
    ] = df[numericas].var()

    return estatisticas.round(2)


# ============================================================
# 5. ESTATÍSTICAS PROTEGIDAS
# ============================================================

def calcular_estatisticas_privadas(df):

    resultado = {}

    resultado["Quantidade"] = ruido_laplace(
        len(df),
        1
    )

    resultado["Media_Glicemia"] = ruido_laplace(
        df["Glicemia"].mean(),
        100
    )

    resultado["Media_IMC"] = ruido_laplace(
        df["IMC"].mean(),
        10
    )

    resultado["Media_Pressao_Sistolica"] = ruido_laplace(
        df["Pressao_Sistolica"].mean(),
        100
    )

    resultado["Media_Pressao_Diastolica"] = ruido_laplace(
        df["Pressao_Diastolica"].mean(),
        100
    )

    resultado["Media_Internacoes"] = ruido_laplace(
        df["Internacoes"].mean(),
        5
    )

    return {
        chave: round(valor, 2)
        for chave, valor in resultado.items()
    }


# ============================================================
# 6. PERCENTUAIS
# ============================================================

def distribuicoes(df):

    diagnosticos = (
        df["Diagnostico"]
        .value_counts(
            normalize=True
        )
        .mul(100)
        .round(2)
    )

    riscos = (
        df["Risco"]
        .value_counts(
            normalize=True
        )
        .mul(100)
        .round(2)
    )

    sexo = (
        df["Sexo"]
        .value_counts(
            normalize=True
        )
        .mul(100)
        .round(2)
    )

    return diagnosticos, riscos, sexo


# ============================================================
# 7. CORRELAÇÃO
# ============================================================

def calcular_correlacao(df):

    variaveis = [
        "Pressao_Sistolica",
        "Pressao_Diastolica",
        "Glicemia",
        "IMC",
        "Internacoes"
    ]

    return df[variaveis].corr().round(2)


# ============================================================
# 8. ANÁLISE POR DIAGNÓSTICO
# ============================================================

def analise_por_diagnostico(df):

    resultado = (
        df
        .groupby("Diagnostico")
        .agg(
            Quantidade=(
                "Diagnostico",
                "count"
            ),

            Glicemia_Media=(
                "Glicemia",
                "mean"
            ),

            IMC_Medio=(
                "IMC",
                "mean"
            ),

            Pressao_Sistolica_Media=(
                "Pressao_Sistolica",
                "mean"
            ),

            Internacoes_Media=(
                "Internacoes",
                "mean"
            )
        )
    )

    return resultado.round(2)


# ============================================================
# 9. PSEUDOANÁLISE
# ============================================================

def gerar_pseudoanalise(df):

    texto = []

    texto.append(
        "PSEUDOANÁLISE DOS DADOS"
    )

    texto.append(
        "=" * 60
    )

    texto.append(
        "ATENÇÃO: esta seção identifica padrões "
        "observados e formula hipóteses."
    )

    texto.append(
        "Não representa diagnóstico médico nem "
        "prova de causalidade."
    )

    texto.append("")

    # --------------------------------------------------------
    # Padrão 1
    # --------------------------------------------------------

    diabetes = df[
        df["Diagnostico"]
        == "Diabetes tipo 2"
    ]

    outros = df[
        df["Diagnostico"]
        != "Diabetes tipo 2"
    ]

    if len(diabetes) > 0:

        media_diabetes = diabetes[
            "Glicemia"
        ].mean()

        media_outros = outros[
            "Glicemia"
        ].mean()

        texto.append(
            "OBSERVAÇÃO 1:"
        )

        texto.append(
            f"A glicemia média do grupo com "
            f"diabetes foi {media_diabetes:.2f}, "
            f"enquanto nos demais grupos foi "
            f"{media_outros:.2f}."
        )

        texto.append(
            "HIPÓTESE:"
        )

        texto.append(
            "Neste conjunto sintético, existe uma "
            "associação aparente entre diabetes "
            "e valores maiores de glicemia."
        )

        texto.append("")

    # --------------------------------------------------------
    # Padrão 2
    # --------------------------------------------------------

    alto = df[
        df["Risco"] == "Alto"
    ]

    baixo = df[
        df["Risco"] == "Baixo"
    ]

    if len(alto) > 0 and len(baixo) > 0:

        media_internacoes_alto = alto[
            "Internacoes"
        ].mean()

        media_internacoes_baixo = baixo[
            "Internacoes"
        ].mean()

        texto.append(
            "OBSERVAÇÃO 2:"
        )

        texto.append(
            f"O grupo de alto risco apresentou "
            f"média de {media_internacoes_alto:.2f} "
            f"internações, contra "
            f"{media_internacoes_baixo:.2f} "
            f"no grupo de baixo risco."
        )

        texto.append(
            "HIPÓTESE:"
        )

        texto.append(
            "Pode existir uma associação entre "
            "maior quantidade de internações e "
            "classificação de risco elevada."
        )

        texto.append("")

    # --------------------------------------------------------
    # Padrão 3
    # --------------------------------------------------------

    hipertensao = df[
        df["Diagnostico"]
        == "Hipertensão"
    ]

    if len(hipertensao) > 0:

        media_pressao = hipertensao[
            "Pressao_Sistolica"
        ].mean()

        media_geral = df[
            "Pressao_Sistolica"
        ].mean()

        texto.append(
            "OBSERVAÇÃO 3:"
        )

        texto.append(
            f"A pressão sistólica média do grupo "
            f"com hipertensão foi {media_pressao:.2f}, "
            f"enquanto a média geral foi "
            f"{media_geral:.2f}."
        )

        texto.append(
            "HIPÓTESE:"
        )

        texto.append(
            "Os dados apresentam uma associação "
            "aparente entre o diagnóstico de "
            "hipertensão e pressão sistólica "
            "mais elevada."
        )

        texto.append("")

    # --------------------------------------------------------
    # Conclusão
    # --------------------------------------------------------

    texto.append(
        "CONCLUSÃO DA PSEUDOANÁLISE:"
    )

    texto.append(
        "Foram encontrados padrões estatísticos "
        "no conjunto de dados sintéticos."
    )

    texto.append(
        "Esses padrões devem ser considerados "
        "hipóteses para investigação posterior."
    )

    texto.append(
        "Eles não demonstram relação causal."
    )

    return "\n".join(texto)


# ============================================================
# 10. GRÁFICOS
# ============================================================

def gerar_graficos(df):

    # --------------------------------------------------------
    # Diagnósticos
    # --------------------------------------------------------

    plt.figure(
        figsize=(9, 5)
    )

    df[
        "Diagnostico"
    ].value_counts().plot(
        kind="bar"
    )

    plt.title(
        "Distribuição dos Diagnósticos"
    )

    plt.xlabel(
        "Diagnóstico"
    )

    plt.ylabel(
        "Quantidade"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_RESULTADOS,
            "diagnosticos.png"
        )
    )

    plt.close()

    # --------------------------------------------------------
    # Risco
    # --------------------------------------------------------

    plt.figure(
        figsize=(7, 5)
    )

    df[
        "Risco"
    ].value_counts().plot(
        kind="bar",
        color=[
            "green",
            "orange",
            "red"
        ]
    )

    plt.title(
        "Distribuição de Risco"
    )

    plt.xlabel(
        "Risco"
    )

    plt.ylabel(
        "Quantidade"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_RESULTADOS,
            "risco.png"
        )
    )

    plt.close()

    # --------------------------------------------------------
    # Glicemia
    # --------------------------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    plt.hist(
        df["Glicemia"],
        bins=20,
        color="steelblue",
        edgecolor="black"
    )

    plt.title(
        "Distribuição da Glicemia"
    )

    plt.xlabel(
        "Glicemia"
    )

    plt.ylabel(
        "Frequência"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_RESULTADOS,
            "glicemia.png"
        )
    )

    plt.close()

    # --------------------------------------------------------
    # IMC
    # --------------------------------------------------------

    plt.figure(
        figsize=(8, 5)
    )

    plt.hist(
        df["IMC"],
        bins=20,
        color="purple",
        edgecolor="black"
    )

    plt.title(
        "Distribuição do IMC"
    )

    plt.xlabel(
        "IMC"
    )

    plt.ylabel(
        "Frequência"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            PASTA_RESULTADOS,
            "imc.png"
        )
    )

    plt.close()


# ============================================================
# 11. RELATÓRIO
# ============================================================

def gerar_relatorio(
    df,
    df_protegido,
    estatisticas,
    privadas,
    diagnosticos,
    riscos,
    sexo,
    correlacao,
    por_diagnostico,
    pseudo
):

    with open(
        ARQUIVO_RELATORIO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "==================================================\n"
        )

        arquivo.write(
            "RELATÓRIO DE ANÁLISE DE DADOS DE SAÚDE\n"
        )

        arquivo.write(
            "==================================================\n\n"
        )

        arquivo.write(
            "IMPORTANTE:\n"
        )

        arquivo.write(
            "Os dados utilizados neste projeto são "
            "totalmente sintéticos e fictícios.\n"
        )

        arquivo.write(
            "Não representam pacientes reais.\n\n"
        )

        arquivo.write(
            "1. RESUMO\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            f"Quantidade de registros: {len(df)}\n"
        )

        arquivo.write(
            f"Quantidade de registros protegidos: "
            f"{len(df_protegido)}\n\n"
        )

        arquivo.write(
            "2. ESTATÍSTICAS DESCRITIVAS\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            estatisticas.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "3. DISTRIBUIÇÃO DOS DIAGNÓSTICOS (%)\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            diagnosticos.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "4. DISTRIBUIÇÃO DE RISCO (%)\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            riscos.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "5. DISTRIBUIÇÃO POR SEXO (%)\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            sexo.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "6. ESTATÍSTICAS POR DIAGNÓSTICO\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            por_diagnostico.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "7. MATRIZ DE CORRELAÇÃO\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            correlacao.to_string()
        )

        arquivo.write("\n\n")

        arquivo.write(
            "8. ESTATÍSTICAS COM PRIVACIDADE\n"
        )

        arquivo.write(
            "--------------------------------------------------\n"
        )

        arquivo.write(
            f"Epsilon utilizado: {EPSILON}\n\n"
        )

        for chave, valor in privadas.items():

            arquivo.write(
                f"{chave}: {valor}\n"
            )

        arquivo.write("\n\n")

        arquivo.write(
            pseudo
        )

        arquivo.write("\n\n")

        arquivo.write(
            "==================================================\n"
        )

        arquivo.write(
            "FIM DO RELATÓRIO\n"
        )

        arquivo.write(
            "==================================================\n"
        )


# ============================================================
# 12. PROGRAMA PRINCIPAL
# ============================================================

def main():

    preparar_pastas()

    print()
    print("=" * 60)
    print(
        "SISTEMA DE ANÁLISE E PROTEÇÃO "
        "DE DADOS DE SAÚDE"
    )
    print("=" * 60)

    print(
        "\n[1/8] Gerando dados sintéticos..."
    )

    df = gerar_dados_sinteticos(
        n=1000
    )

    df.to_csv(
        ARQUIVO_ORIGINAL,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"      {len(df)} registros gerados."
    )

    print(
        "\n[2/8] Aplicando anonimização/generalização..."
    )

    df_protegido = anonimizar_dados(
        df
    )

    df_protegido.to_csv(
        ARQUIVO_PROTEGIDO,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        "      Identificador removido."
    )

    print(
        "      Idade generalizada."
    )

    print(
        "      Variáveis numéricas generalizadas."
    )

    print(
        "\n[3/8] Calculando estatísticas..."
    )

    estatisticas = calcular_estatisticas(
        df_protegido
    )

    print(
        estatisticas
    )

    print(
        "\n[4/8] Calculando distribuições..."
    )

    diagnosticos, riscos, sexo = distribuicoes(
        df
    )

    print(
        "\nDiagnósticos:"
    )

    print(
        diagnosticos
    )

    print(
        "\nRisco:"
    )

    print(
        riscos
    )

    print(
        "\n[5/8] Calculando correlações..."
    )

    correlacao = calcular_correlacao(
        df_protegido
    )

    print(
        correlacao
    )

    print(
        "\n[6/8] Analisando por diagnóstico..."
    )

    por_diagnostico = analise_por_diagnostico(
        df_protegido
    )

    print(
        por_diagnostico
    )

    print(
        "\n[7/8] Aplicando proteção estatística..."
    )

    privadas = calcular_estatisticas_privadas(
        df_protegido
    )

    for chave, valor in privadas.items():

        print(
            f"      {chave}: {valor}"
        )

    print(
        "\n[8/8] Executando pseudoanálise..."
    )

    pseudo = gerar_pseudoanalise(
        df_protegido
    )

    print()
    print(pseudo)

    print(
        "\nGerando gráficos..."
    )

    gerar_graficos(
        df_protegido
    )

    print(
        "\nGerando relatório..."
    )

    gerar_relatorio(
        df,
        df_protegido,
        estatisticas,
        privadas,
        diagnosticos,
        riscos,
        sexo,
        correlacao,
        por_diagnostico,
        pseudo
    )

    print()
    print("=" * 60)
    print("PROCESSAMENTO CONCLUÍDO")
    print("=" * 60)

    print(
        "\nArquivos gerados:"
    )

    print(
        f"  - {ARQUIVO_ORIGINAL}"
    )

    print(
        f"  - {ARQUIVO_PROTEGIDO}"
    )

    print(
        f"  - {ARQUIVO_RELATORIO}"
    )

    print(
        f"  - {PASTA_RESULTADOS}\\diagnosticos.png"
    )

    print(
        f"  - {PASTA_RESULTADOS}\\risco.png"
    )

    print(
        f"  - {PASTA_RESULTADOS}\\glicemia.png"
    )

    print(
        f"  - {PASTA_RESULTADOS}\\imc.png"
    )

    print(
        "\nIMPORTANTE:"
    )

    print(
        "Os dados são sintéticos e não correspondem "
        "a pacientes reais."
    )


if __name__ == "__main__":
    main()
