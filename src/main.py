from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
from selenium import webdriver
from time import sleep
import pandas as pd
import openai


def converter_para_float(valor_str):
    # Remover caracteres não numéricos, exceto vírgula e ponto
    valor_str = re.sub(r'[^\d,\.]', '', valor_str)
    # Substituir vírgula por ponto
    valor_str = valor_str.replace(',', '.')
    # Converter para float
    return float(valor_str)


def resumir_conteudo(course_content):
    # Concatenar todos os itens de course_content em uma única string
    content_string = " ".join(course_content)

    # Chamar o GPT-3.5-turbo para gerar um resumo
    # Substitua 'YOUR_OPENAI_API_KEY' pela sua chave de API
    openai.api_key = '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'
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    messages=[
            {"role": "system", "content": "Reduza os conteúdos do curso: de maneira parafraseada em no máximo 4 linhas" + content_string}
        ]
    )
    return response.choices[0].message.content.strip()


urls = [
"https://hotmart.com/pt-br/marketplace/produtos/curso-de-logistica-industrial/M26971325P",
"https://hotmart.com/pt-br/marketplace/produtos/curso-basico-de-logistica-industrial/R71637174V",
"https://hotmart.com/pt-br/marketplace/produtos/logisticaindustrial/D66254571Y",

]


df_global = pd.DataFrame(columns=["Curso", "Horas", "Valor", "Classificação", "Inscritos", "Palavra-Chave", "Conteudo"], )
driver = webdriver.Chrome()
for url in urls:
    try:
        driver.get(url)
        sleep(2)
        html_page = driver.page_source
        soup = BeautifulSoup(html_page, 'html.parser')

        course_description = []
        course_content = []
        course_title = soup.find("h1").get_text()
        course_money = soup.find("span", {"class": "_text-md-5 _text-sm-2 _text-gray-900"}).get_text()


        for desc in soup.find_all("p", {"class": "_mb-5"}):
            course_description.append(desc.get_text())



        for content in soup.find_all("li", {"class": "accordion__text hover clickable"}):
            course_content.append(content.get_text())


        content_resumed = resumir_conteudo(course_content)
        print(f"O curso {course_title} que custa R${course_money} se resume em {content_resumed}")

        # Criar um 'single df'
        single_df = pd.DataFrame({"Curso": [course_title], "Horas": [0], "Valor": [course_money], "Classificação": [0], "Inscritos": [0], "Palavra-Chave": ["Logística Industrial"], "Conteudo": [content_resumed]})

        # Adicionar ao DataFrame global
        df_global = pd.concat([df_global, single_df], ignore_index=True)
        df_global.to_csv("Global_dataframe.csv", sep=";")
        sleep(10)

    except:
        print(f"Pulando {url}")
    

    


