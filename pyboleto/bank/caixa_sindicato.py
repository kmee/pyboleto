#-*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

from ..data import BoletoData, custom_property

from pybrasil.inscricao import formata_codigo_sindical, limpa_formatacao


class BoletoCaixaSindicato(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal
    '''

    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 14)
    nosso_numero = custom_property('nosso_numero', 12)
    cnae = ''
    codigo_sindical = ''

    total_empregados = ''
    qtd_contribuintes = ''
    total_remuneracao_contribuintes = ''


    def __init__(self):
        super(BoletoCaixaSindicato, self).__init__()

        self.codigo_banco = "104"
        self.local_pagamento = (u"Preferencialmente nas Casas Lotéricas e "
                                u"Agências da Caixa")
        self.logo_image = "logo_bancocaixa.jpg"

    @property
    def campo_livre(self):  # 24 digits
        campo_livre = '97{codigo_sindical}{cnae_1}177{nosso_numero}{cnae_2}'
        cnae = limpa_formatacao(self.cnae)
        filtro = {
            'codigo_sindical': self.conta_cedente[-5:],
            'nosso_numero': self.nosso_numero[:12],
            'cnae_1': cnae[0],
            'cnae_2': cnae[1:3],
        }
        campo_livre = campo_livre.format(**filtro)
        return campo_livre

    def format_nosso_numero(self):
        return self.nosso_numero

    @property
    def agencia_conta_cedente(self):
        return "%s / %s" % (self.agencia_cedente,
                               self.codigo_sindical_formatado)

    @property
    def codigo_sindical_formatado(self):
        return formata_codigo_sindical(self.codigo_sindical)
