from API import Urls as url
from Utils import Functions as fc
import requests
import pandas as pd
import streamlit as st
import DB.User as ft
from Utils import Constantes

def home():
    st.title("Página Inicial")
    st.write("Bem-vindo à página inicial!")

def segunda_pagina():
    try:

        st.title("Comentarios")
        nome = st.text_input('Nome:')
        comentario = st.text_area('Adicionar Comentário:')
        if len(nome) > 0 and len(comentario) > 0 and st.button('add'):
            ft.adicionar_comentario(nome=nome, comentario=comentario)
            st.success('Comentário salvo com sucesso!')
        comentarios = ft.obter_todos_comentarios()

        st.header('Comentários:')
        for comentario in reversed(comentarios):
            st.write(
                f"**{ft.user_name_by_id(comentario.id_usuario)}** {comentario.data_postagem.strftime(Constantes.FORMAT_DATE_TIME_DD_MM_YYYY__H_M_S)}:")
            st.write(f"**Comentário:** {comentario.comentario}")
            st.markdown("---")

    except Exception as e:
        fc.info(str(e))



def terceira_pagina():
    if __name__ == '__main__':
        st.title('Dados Financeiros IBM')
        fc.info("Iniciando busca")
        col1, col2, = st.columns(2)
        url_vendas = None
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button('Últimos 100 resultados'):
                url_vendas = url.url_last_100
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button('Últimos 30 dias'):
                pass
            url_vendas = url.url_30_days

        if url_vendas:
            json_data = requests.get(url=url_vendas).json()
            time_series_data = json_data["Time Series (5min)"]
            st.write(json_data['Meta Data'])
            data_list = [
                {
                    "timestamp": timestamp,
                    "open": float(data["1. open"]),
                    "high": float(data["2. high"]),
                    "low": float(data["3. low"]),
                    "close": float(data["4. close"]),
                    "volume": int(data["5. volume"])
                }
                for timestamp, data in time_series_data.items()
            ]
            df = pd.DataFrame(data_list)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            with col1:
                st.title('Gráfico de Volume de Vendas')
                st.line_chart(df['volume'])
            with col2:
                st.title('Base de dados')
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(df)
                st.write()


def quarta_pagina():
    tab1, tab2 = st.tabs(['Usuarios', 'Criar novo usuário'])
    with tab1:
        st.header('Usuários:')
        nome_pesquisado = st.text_input("Digite o nome para buscar usuários:")
        usuarios = ft.get_users()
        if nome_pesquisado:
            usuarios_encontrados = fc.buscar_usuarios_por_nome(nome_pesquisado, usuarios)
        else:
            usuarios_encontrados = usuarios

        for usuario in usuarios_encontrados:
            expander = st.expander(f"{usuario.nome} - {usuario.email}")

            with expander:
                st.write(f"Nome: {usuario.nome}")
                st.write(f"Email: {usuario.email}")

                key_nome = f"novo_nome_{usuario.id_usuario}"
                key_email = f"novo_email_{usuario.id_usuario}"

                novo_nome = st.text_input("Novo Nome:", key=key_nome, value=usuario.nome)
                novo_email = st.text_input("Novo Email:", key=key_email, value=usuario.email)

                if novo_nome and novo_email and st.button(f"Salvar Alterações para {usuario.nome}"):
                    ft.update_user(id_usuario=usuario.id_usuario, novo_nome=novo_nome, novo_email=novo_email)
                    st.success("Alterações salvas com sucesso!")
    with tab2:
        st.subheader("Formulário de Criação de Usuário")
        nome = st.text_input("Nome:")
        email = st.text_input("E-mail:")
        if st.button("Enviar"):
            if nome and email:
                fc.create_user(nome=nome, email=email)
                st.success(f"Usuário criado com sucesso!\nNome: {nome}\nE-mail: {email}")
            else:
                st.warning("Por favor, preencha todos os campos.")

pagina_selecionada = st.sidebar.radio("Selecione a Página", ("Home", "Comentários", "Consulta", 'Usuários'))

if pagina_selecionada == "Home":
    home()
elif pagina_selecionada == "Comentários":
    segunda_pagina()
elif pagina_selecionada == "Consulta":
    terceira_pagina()
elif pagina_selecionada == 'Usuários':
    quarta_pagina()





