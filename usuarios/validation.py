def clean_name(valor_campo, nome_do_campo, lista_de_erros):
        if any(char.isdigit() for char in valor_campo):
            lista_de_erros[nome_do_campo] = 'Nome inválido: Não incluir número'

def compare_passwords(valor_campo_um, valor_campo_dois, nome_do_campo, lista_de_erros):
    if valor_campo_um != valor_campo_dois:
        lista_de_erros[nome_do_campo] = 'As senhas devem ser equivalentes!'

def field_not_strip(valor_campo, nome_do_campo, lista_de_erros):
    if not valor_campo.strip():
        lista_de_erros[nome_do_campo] = f'O campo {nome_do_campo} não pode ficar em branco!'