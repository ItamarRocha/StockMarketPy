#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:46:36 2020

@author: itamar
"""

from selenium import webdriver
import time
import bs4 as bs
import requests

class B3:
    def __init__(self):
        self.bot = webdriver.Firefox() #initialize the browser

    def start(self):
        bot = self.bot
        bot.get('http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm')
        time.sleep(2)#goes to specified site and sleeps 

        iframe = bot.find_element_by_xpath('//iframe[@id="bvmf_iframe"]')
        bot.switch_to.frame(iframe)#change frame
        bot.implicitly_wait(30)

        tab = bot.find_element_by_xpath('//a[@id="ctl00_contentPlaceHolderConteudo_tabMenuEmpresaListada_tabSetor"]')
        time.sleep(3)#setor de atuação
        tab.click()
        time.sleep(2)
        
        links = []#pegas todos os links dos setores de atuação
        elems = bot.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None and 'cias-listadas' in href:
                links.append(href)
                
        time.sleep(1)
        bot.get(links[0])
        #link1 = elems[7]#pega o link 7 só pra testar
        #link1.click()#bora lá
        #bot.find_element_by_link_text('Material de Transporte')
        time.sleep(2)
        companyes_links = []#pega as companhias desse setor de atuação
        new_elems = bot.find_elements_by_tag_name('a')
        for elem in new_elems:
            href = elem.get_attribute('href')
            if href is not None and 'cias-listadas' in href:
                companyes_links.append(href)
        
        time.sleep(4)
        #company_link = new_elems[-1]#clica na ultima companhia
        #company_link.click()
        bot.get(companyes_links[-1])
        
        
        time.sleep(2)
        new_tab = bot.find_element_by_xpath('//a[@id="ctl00_contentPlaceHolderConteudo_MenuEmpresasListadas1_tabMenuEmpresa_tabRelatoriosFinanceiros"]')
        time.sleep(2)#vai pros relatórios financeiros da empresa
        new_tab.click()
        ### ver se tem como pegar pela lista de li com o classname , se pá funciona pra todas as páginas

        dfp = bot.find_element_by_id('ctl00_contentPlaceHolderConteudo_rptDocumentosDFP_ctl00_lnkDocumento')
        href = dfp.get_attribute('href')#pega o link de redirecionamento que ia abrir a janela pop up e redireciona o browser pra ela
        data_site = href.split("(\'")[1].split("\')")[0]
        time.sleep(2)
        #dfp.click()
        
        bot.get(data_site)
        
        
if __name__ == "__main__":
    worker = B3()
    worker.start()