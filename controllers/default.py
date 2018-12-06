# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------


# ---- index page ----

def index():
    return dict()

# ---- index2 page ----
@auth.requires_login()
def level():
    return dict()

def suporte():
    return dict()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# def ver_usuarios():
#     grid = SQLFORM.grid(db.auth_user)
#     return dict(grid=grid)


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# ---- CRUD ALUNO -----

@auth.requires_login()
def aluno_cadastro():
    form = SQLFORM(Aluno)
    if form.process().accepted:
        session.flash = 'Novo aluno: %s' % form.vars.nome
        redirect(URL('aluno_cadastro'))
    elif form.errors:
        response.flash = 'Corrija os erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

@auth.requires_login()
def aluno_ver():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'aluno_editar/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        # db.table.id.readable or writable = False
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'aluno_detalhe/' + str(parametro)
        redirect(URL(url))

    grid = SQLFORM.grid(Aluno, create=False, advanced_search = False, orderby=db.aluno.nome,
    fields=[
            db.aluno.nome,
            db.aluno.cpf,
            db.aluno.matricula,
            db.aluno.curso,
            db.aluno.periodo,
            db.aluno.email,
            ],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def aluno_rep():
    grid = SQLFORM.grid(Aluno, deletable=False, editable=False, details=False,
    create=False, advanced_search = True, orderby=db.aluno.nome,
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def aluno_editar():
    # db.aluno.cpf.writable = False
    # db.aluno.cpf.readable = True
    form = SQLFORM(Aluno, request.args(0, cast=int),)
    if form.process().accepted:
        session.flash = 'Aluno atualizado: %s' % form.vars.nome
        redirect(URL('aluno_detalhe/' + str(form.vars.id)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

@auth.requires_login()
def aluno_apagar():
    db(Aluno.id==request.args(0, cast=int)).delete()
    session.flash = 'Aluno apagado!'
    redirect(URL('aluno_ver'))

@auth.requires_login()
def aluno_detalhe():
    '''
    Aqui o request.arg (0) pega o parametro URL e executa o select no banco de
    dados
    '''
    aluno_detalhe = db(Aluno.id == request.args(0)).select()
    return dict(aluno_detalhe=aluno_detalhe)


# ---- CRUD PROFESSOR -----

@auth.requires_login()
def professor_cadastro():
    form = SQLFORM(Professor)
    if form.process().accepted:
        session.flash = 'Novo professor: %s' % form.vars.nome
        redirect(URL('professor_cadastro'))
    elif form.errors:
        response.flash = 'Corrija os erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

@auth.requires_login()
def professor_ver():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'professor_editar/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'professor_detalhe/' + str(parametro)
        redirect(URL(url))

    grid = SQLFORM.grid(Professor, create=False, advanced_search = False, orderby=db.professor.nome,
    fields=[
            db.professor.nome,
            db.professor.cpf,
            db.professor.telefone,
            db.professor.email,
            ],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def professor_editar():
    form = SQLFORM(Professor, request.args(0, cast=int),)
    if form.process().accepted:
        session.flash = 'Professor atualizado: %s' % form.vars.nome
        redirect(URL('professor_detalhe/' + str(form.vars.id)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

@auth.requires_login()
def professor_apagar():
    db(Professor.id==request.args(0, cast=str)).delete()
    session.flash = 'Professor apagado!'
    redirect(URL('professor_ver'))

@auth.requires_login()
def professor_detalhe():
    professor_detalhe = db(Professor.id == request.args(0)).select()
    return dict(professor_detalhe=professor_detalhe)


# ---- CRUD EMPRESA -----

@auth.requires_login()
def empresa_cadastro():
    form = SQLFORM(Empresa)
    if form.process().accepted:
        session.flash = 'Empresa %s cadastrada' % form.vars.nome
        redirect(URL('empresa_cadastro'))
    elif form.errors:
        response.flash = 'Corrija os erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

@auth.requires_login()
def empresa_ver():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'empresa_editar/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'empresa_detalhe/' + str(parametro)
        redirect(URL(url))

    grid = SQLFORM.grid(Empresa, create=False, advanced_search = False,
    fields=[
            db.empresa.nome,
            db.empresa.cnpj,
            db.empresa.telefone,
            db.empresa.email,
            ],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def empresa_rep():
    grid = SQLFORM.grid(Empresa, deletable=False, editable=False, details=False,
    create=False, advanced_search = True, maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)


@auth.requires_login()
def empresa_editar():
    form = SQLFORM(Empresa, request.args(0, cast=int),)
    if form.process().accepted:
        session.flash = 'Empresa atualizada: %s' % form.vars.nome
        redirect(URL('empresa_detalhe/' + str(form.vars.id)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

@auth.requires_login()
def empresa_apagar():
    db(Empresa.id==request.args(0, cast=int)).delete()
    session.flash = 'Empresa apagada!'
    redirect(URL('empresa_ver'))

@auth.requires_login()
def empresa_detalhe():
    empresa_detalhe = db(Empresa.id == request.args(0)).select()
    return dict(empresa_detalhe=empresa_detalhe)


# ---- CRUD ESTÁGIO -----

@auth.requires_login()
def estagio_cadastro():
    form = SQLFORM(Estagio)
    if form.process().accepted:
        session.flash = 'Estagio cadastrado'
        redirect(URL('estagio_cadastro'))
    elif form.errors:
        response.flash = 'Corrija os erros encontrados no formulário'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário'
    return dict(form=form)

@auth.requires_login()
def estagio_ver():
    if 'edit' in request.args:
        edit = request.args
        response.flash = edit
        parametro = edit[2]
        url = 'estagio_editar/' + parametro
        redirect(URL(url))
    if 'view' in request.args:
        view = request.args
        response.flash = view
        parametro = view[2]
        url = 'estagio_detalhe/' + str(parametro)
        redirect(URL(url))

    grid = SQLFORM.grid(Estagio, create=False, advanced_search = True,
    fields=[
            db.estagio.aluno,
            db.estagio.empresa,
            db.estagio.professor,
            db.estagio.situacao,
            db.estagio.data_inicio,
            db.estagio.data_fim
            ],
            maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def estagio_rep():
    grid = SQLFORM.grid(Estagio, deletable=False, editable=False, details=False,
    create=False, advanced_search = True, maxtextlength=30,
    exportclasses=dict(tsv_with_hidden_cols=False,
                       csv=False, xml=False, json=False))
    return dict(grid=grid)

@auth.requires_login()
def estagio_editar():
    form = SQLFORM(Estagio, request.args(0, cast=int),)
    if form.process().accepted:
        session.flash = 'Estagio atualizado'
        redirect(URL('estagio_detalhe/' + str(form.vars.id)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)

@auth.requires_login()
def estagio_apagar():
    db(Estagio.id==request.args(0, cast=int)).delete()
    session.flash = 'Estagio removido!'
    redirect(URL('estagio_ver'))

@auth.requires_login()
def estagio_detalhe():
    estagio_detalhe = db(Estagio.id == request.args(0)).select()
    return dict(estagio_detalhe=estagio_detalhe)

# ---- PÁGINA DE RELATÓRIO -----

@auth.requires_login()
def relatorio():
    return dict()
