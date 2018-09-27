# -*- coding: utf-8 -*-
# Author: Alzemand

# ----- Validador de aluno -----

Aluno.cpf.requires = [IS_CPF(), IS_NOT_IN_DB(db, 'aluno.cpf', error_message="CPF já cadastrado"),
IS_NOT_EMPTY(error_message='Informe o CPF'),
]
Aluno.telefone.requires = IS_PHONE(error_message="Telefone inválido")
Aluno.email.requires = IS_EMAIL(error_message="E-mail inválido")
Aluno.data_nascimento.requires = IS_DATE(format=T('%d/%m/%Y'), error_message='Data no formato dd/mm/aaaa')
Aluno.curso.requires = IS_IN_SET(["Administração",
                                  "Engenharia de Produção",
                                  "Sistemas de Informação",
                                  "Matemática"], error_message="Selecione um curso")

'''Falta desenvolver IS_RG()'''
# Aluno.identidade.requires = IS_RG()
