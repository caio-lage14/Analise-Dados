
import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Vendas de Carros",
    page_icon="🚗",
    layout="wide"
)


CATALOGO = {
    "Fiat Argo 1.0": {
        "marca": "Fiat",
        "ano": 2024,
        "categoria": "Hatch",
        "preco": 75000.00
    },
    "Chevrolet Onix 1.0": {
        "marca": "Chevrolet",
        "ano": 2025,
        "categoria": "Hatch",
        "preco": 85000.00
    },
    "Hyundai HB20": {
        "marca": "Hyundai",
        "ano": 2025,
        "categoria": "Hatch",
        "preco": 89000.00
    },
    "Toyota Corolla": {
        "marca": "Toyota",
        "ano": 2024,
        "categoria": "Sedan",
        "preco": 145000.00
    },
    "Honda Civic": {
        "marca": "Honda",
        "ano": 2023,
        "categoria": "Sedan",
        "preco": 135000.00
    },
    "Jeep Compass": {
        "marca": "Jeep",
        "ano": 2025,
        "categoria": "SUV",
        "preco": 180000.00
    },
    "Volkswagen T-Cross": {
        "marca": "Volkswagen",
        "ano": 2025,
        "categoria": "SUV",
        "preco": 145000.00
    },
    "BMW 320i": {
        "marca": "BMW",
        "ano": 2024,
        "categoria": "Premium",
        "preco": 320000.00
    }
}


if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "vendas" not in st.session_state:
    st.session_state.vendas = []

if "ultimo_comprovante" not in st.session_state:
    st.session_state.ultimo_comprovante = None


st.title("Dashboard de Vendas de Carros")
st.markdown("Sistema de vendas de veículos de uma concessionária.")
st.markdown("---")


total_vendido = sum(
    venda["Total (R$)"] for venda in st.session_state.vendas
)

quantidade_vendida = sum(
    venda["Qtd"] for venda in st.session_state.vendas
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Faturamento Total",
    f"R$ {total_vendido:,.2f}"
)

col2.metric(
    "Carros Vendidos",
    quantidade_vendida
)

col3.metric(
    "Vendas Realizadas",
    len(st.session_state.vendas)
)

st.markdown("---")


col_esquerda, col_direita = st.columns(
    [1, 1],
    gap="large"
)


with col_esquerda:

    st.subheader("🚘 Seleção de Veículos")

    with st.form("form_veiculo"):

        veiculo = st.selectbox(
            "Escolha o veículo",
            list(CATALOGO.keys())
        )

        dados = CATALOGO[veiculo]

        st.write(f"**Marca:** {dados['marca']}")
        st.write(f"**Ano:** {dados['ano']}")
        st.write(f"**Categoria:** {dados['categoria']}")

        st.caption(
            f"Preço unitário: R$ {dados['preco']:,.2f}"
        )

        quantidade = st.number_input(
            "Quantidade de veículos",
            min_value=1,
            max_value=10,
            value=1,
            step=1
        )

        adicionar = st.form_submit_button(
            "Adicionar ao Carrinho",
            use_container_width=True
        )

        if adicionar:

            subtotal = dados["preco"] * quantidade

            st.session_state.carrinho.append({
                "Veículo": veiculo,
                "Marca": dados["marca"],
                "Ano": dados["ano"],
                "Preço Unit. (R$)": dados["preco"],
                "Qtd": quantidade,
                "Subtotal (R$)": subtotal
            })

            st.success(
                f"{veiculo} adicionado ao carrinho!"
            )


    st.subheader("🛒 Carrinho de Vendas")

    if st.session_state.carrinho:

        df_carrinho = pd.DataFrame(
            st.session_state.carrinho
        )

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço Unit. (R$)": st.column_config.NumberColumn(
                    "Preço Unitário",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )

        total_compra = sum(
            item["Subtotal (R$)"]
            for item in st.session_state.carrinho
        )

        st.metric(
            "TOTAL DA VENDA",
            f"R$ {total_compra:,.2f}"
        )

        if st.button(
            "Limpar Carrinho",
            use_container_width=True
        ):
            st.session_state.carrinho = []
            st.rerun()

    else:

        st.info(
            "O carrinho está vazio. "
            "Selecione um veículo acima."
        )


with col_direita:

    st.subheader("💳 Pagamento e Fechamento")

    total_compra = sum(
        item["Subtotal (R$)"]
        for item in st.session_state.carrinho
    )

    st.metric(
        "TOTAL A PAGAR",
        f"R$ {total_compra:,.2f}"
    )

    st.markdown("---")

    valor_recebido = st.number_input(
        "Valor recebido do cliente (R$)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )

    if st.button(
        "Finalizar Venda",
        type="primary",
        use_container_width=True
    ):

        if not st.session_state.carrinho:

            st.warning(
                "Adicione um veículo antes de finalizar a venda."
            )

        elif valor_recebido < total_compra:

            falta = total_compra - valor_recebido

            st.error(
                f"Dinheiro insuficiente! "
                f"Faltam R$ {falta:,.2f}."
            )

        else:

            troco = valor_recebido - total_compra

            comprovante = {
                "Itens": [
                    item.copy()
                    for item in st.session_state.carrinho
                ],
                "Total (R$)": total_compra,
                "Recebido (R$)": valor_recebido,
                "Troco (R$)": troco
            }

            for item in st.session_state.carrinho:

                st.session_state.vendas.append({
                    "Veículo": item["Veículo"],
                    "Marca": item["Marca"],
                    "Ano": item["Ano"],
                    "Qtd": item["Qtd"],
                    "Total (R$)": item["Subtotal (R$)"]
                })

            st.session_state.ultimo_comprovante = comprovante
            st.session_state.carrinho = []

            st.rerun()



    if st.session_state.ultimo_comprovante:

        comprovante = st.session_state.ultimo_comprovante

        st.success("Pagamento concluído com sucesso!")

        st.metric(
            "TROCO A DEVOLVER",
            f"R$ {comprovante['Troco (R$)']:,.2f}"
        )

        with st.expander("Ver Comprovante da Venda"):

            st.write("### Comprovante da Concessionária")

            for item in comprovante["Itens"]:

                st.write(
                    f"**{item['Veículo']}** — "
                    f"{item['Qtd']} unidade(s)"
                )

                st.write(
                    f"Subtotal: R$ {item['Subtotal (R$)']:,.2f}"
                )

            st.markdown("---")

            st.write(
                f"**Total:** R$ {comprovante['Total (R$)']:,.2f}"
            )

            st.write(
                f"**Valor recebido:** "
                f"R$ {comprovante['Recebido (R$)']:,.2f}"
            )

            st.write(
                f"**Troco:** R$ {comprovante['Troco (R$)']:,.2f}"
            )

        if st.button(
            "Novo Atendimento",
            use_container_width=True
        ):

            st.session_state.ultimo_comprovante = None
            st.rerun()



st.markdown("---")
st.subheader("Histórico de Vendas")

if st.session_state.vendas:

    df_vendas = pd.DataFrame(
        st.session_state.vendas
    )

    st.dataframe(
        df_vendas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total (R$)": st.column_config.NumberColumn(
                "Total da Venda",
                format="R$ %.2f"
            )
        }
    )

else:

    st.info(
        "Nenhuma venda realizada até o momento."
    )
