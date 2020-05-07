#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:46:36 2020

@author: itamar
"""

from selenium import webdriver
import time

class B3:
    def __init__(self):
        self.bot = webdriver.Firefox()

    def start(self):
        bot = self.bot
        bot.get('http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm')
        time.sleep(2)

        iframe = bot.find_element_by_xpath('//iframe[@id="bvmf_iframe"]')
        bot.switch_to.frame(iframe)
        bot.implicitly_wait(30)

        tab = bot.find_element_by_xpath('//a[@id="ctl00_contentPlaceHolderConteudo_tabMenuEmpresaListada_tabSetor"]')
        time.sleep(3)
        tab.click()
        time.sleep(2)
        
        links = []
        elems = bot.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                links.append(href)
        link1 = elems[7]
        link1.click()
        bot.find_element_by_link_text('Material de Transporte')

if __name__ == "__main__":
    worker = B3()
    worker.start()