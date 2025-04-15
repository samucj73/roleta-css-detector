import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

st.set_page_config(page_title="Roleta CSS Detector", layout="centered")
st.title("Detector de Números e Selectores CSS da Roleta")

url = st.text_input("Cole o link da página da roleta")

@st.cache_resource


def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    
    service = Service(executable_path="/usr/local/bin/chromedriver")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def descobrir_numeros_com_selectores(url):
    driver = iniciar_driver()
    driver.get(url)
    time.sleep(10)

    resultados = []

    elements = driver.find_elements(By.CSS_SELECTOR, "*")
    for el in elements:
        try:
            texto = el.text.strip()
            if texto.isdigit() and 0 <= int(texto) <= 36:
                selector = driver.execute_script("""
                    function cssPath(el) {
                        if (!(el instanceof Element)) return;
                        var path = [];
                        while (el.nodeType === Node.ELEMENT_NODE) {
                            var selector = el.nodeName.toLowerCase();
                            if (el.id) {
                                selector += '#' + el.id;
                                path.unshift(selector);
                                break;
                            } else {
                                var sib = el, nth = 1;
                                while (sib = sib.previousElementSibling) {
                                    if (sib.nodeName.toLowerCase() == selector)
                                        nth++;
                                }
                                if (nth != 1)
                                    selector += ":nth-of-type(" + nth + ")";
                            }
                            path.unshift(selector);
                            el = el.parentNode;
                        }
                        return path.join(" > ");
                    }
                    return cssPath(arguments[0]);
                """, el)
                resultados.append((int(texto), selector))
        except:
            pass

    driver.quit()
    return resultados

if st.button("Descobrir números e seletores"):
    if url:
        resultados = descobrir_numeros_com_selectores(url)
        if resultados:
            st.success(f"{len(resultados)} número(s) encontrado(s).")
            df = pd.DataFrame(resultados, columns=["Número", "Seletor CSS"])
            st.dataframe(df)

            # Salvar histórico
            if os.path.exists("historico.csv"):
                hist = pd.read_csv("historico.csv")
                df = pd.concat([hist, df], ignore_index=True)

            df.to_csv("historico.csv", index=False)
        else:
            st.warning("Nenhum número encontrado.")
    else:
        st.warning("Cole um link válido.")

if os.path.exists("historico.csv"):
    st.subheader("Histórico salvo")
    st.dataframe(pd.read_csv("historico.csv"))

if st.button("Limpar histórico"):
    if os.path.exists("historico.csv"):
        os.remove("historico.csv")
        st.success("Histórico removido com sucesso.")
