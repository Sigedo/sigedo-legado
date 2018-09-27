# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- index page ----

def index():
    return dict()

# ---- index2 page ----
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

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

# ---- CRUD ALUNO -----

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

    grid = SQLFORM.grid(Aluno, create=False, advanced_search = False,
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

# @auth.requires_login()
def aluno_editar():
    # db.aluno.cpf.writable = False
    # db.aluno.cpf.readable = True
    form = SQLFORM(Aluno, request.args(0, cast=str),)
    if form.process().accepted:
        session.flash = 'Aluno atualizado: %s' % form.vars.nome
        redirect(URL('aluno_detalhe/' + form.vars.cpf))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Atualização de dados'
    return dict(form=form)


def aluno_detalhe():
    '''
    Aqui o request.arg (0) pega o parametro URL e executa o select no banco de
    dados
    '''
    aluno_detalhe = db(Aluno.cpf == request.args(0)).select()
    return dict(aluno_detalhe=aluno_detalhe)
