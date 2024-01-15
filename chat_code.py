import flet as ft

# Passo 1 - Colocar o Titulo - um botão?
# Passo 2 - Adcionar o PopUp
# Passo 3 - Criar o chat
# passo 4 - Criar o Tunel / pubsub


def main(pagina):

    titulo = ft.Text("Chatzinho!")

    chat = ft.Column()

    def tunel(info):
        tipo = info['tipo']
        if tipo == 'mensagem':
            texto_msg = info['texto']
            usuario_msg = info['usuario']
            # adicionar mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_msg}: {texto_msg}"))
        else:
            usuario_msg = info['usuario']
            chat.controls.append(ft.Text(f"{usuario_msg} entrou no chat",
                                         size=14, italic=True, color=ft.colors.LIGHT_BLUE_ACCENT_700))
        pagina.update()

    pagina.pubsub.subscribe(tunel)

    def enviar_mensagem(evento):
        
        pagina.pubsub.send_all({'usuario': nome_usuario.value, 'texto': caixa_mensagem.value, 'tipo': 'mensagem'})

        #limpar barra de mensagem
        caixa_mensagem.value = ""
        pagina.update()
        
    caixa_mensagem = ft.TextField(label="Escreva sua mensagem", on_submit=enviar_mensagem)
    botao_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    
    def entrar_chat(evento):
        pagina.pubsub.send_all({'usuario': nome_usuario.value, 'tipo': 'entrada'})
        popup.open = False
        pagina.remove(titulo)
        pagina.remove(botao1)

        #adicionar novos elementos
        pagina.add(chat)
        pagina.add(ft.Row(
            [caixa_mensagem, botao_mensagem]
        ))
        pagina.update()


    nome_usuario = ft.TextField(label="Nome do usuário", on_submit=entrar_chat)

    def entrar(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()
    
    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Boas Vindas!"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_chat)]        
    )
        
    # Inicio!
    botao1 = ft.ElevatedButton("Iniciar chat", on_click=entrar)
    pagina.add(titulo)
    pagina.add(botao1)


ft.app(main, view=ft.WEB_BROWSER, port=8000)

