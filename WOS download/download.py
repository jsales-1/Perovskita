import re
from playwright.sync_api import Playwright, sync_playwright  # type: ignore
from config import (
    LOGIN,
    SENHA,
    PESQUISA,
    SIGLA,
    NOME_UNIVERSIDADE,
    NOME_PASTA,
    CAFE,
    PESQUISA_AVANCADA,
)
import os
from tqdm import tqdm  # type: ignore
import time
import random


def slow_type(element, text):
    """Digita um texto letra por letra com um pequeno atraso."""
    element.fill("")
    for char in text:
        element.press(char)
        delay = random.random() / 10
        time.sleep(delay)


def dowload_data(page1, nome_arquivo, NOME_PASTA, inicio, fim):
    page1.get_by_role("button", name="Export", exact=True).click()
    time.sleep(2)
    page1.get_by_label("Tab delimited file").click()
    time.sleep(2)
    page1.locator("label[for='radio3-input']").click()
    time.sleep(2)
    page1.get_by_label("Input starting record range").click()
    slow_type(page1.get_by_label("Input starting record range"), f"{inicio}")
    time.sleep(2)
    page1.get_by_label("Input ending record range. A").click()
    slow_type(page1.get_by_label("Input ending record range. A"), f"{fim}")
    time.sleep(2)
    page1.get_by_label("Author, Title, Source").click()
    time.sleep(2)
    page1.get_by_label("Custom selection (29)").click()
    time.sleep(2)
    page1.get_by_role("button", name="Save selections").click()

    # Manipular o download
    with page1.expect_download(timeout=240000) as download_info:  # Timeout aumentado para 60 segundos
        page1.locator("app-export-out-details").get_by_role(
            "button", name="Export"
        ).click()
    download = download_info.value

    # Salvar o arquivo no disco
    download_path = os.path.join(
        NOME_PASTA, nome_arquivo
    )  # Substituir pelo caminho desejado
    download.save_as(download_path)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    if CAFE:
        page = context.new_page()
        page.goto("https://www.periodicos.capes.gov.br/index.php/acesso-cafe.html")
        page.get_by_placeholder("Digite a sigla ou o nome da").click()
        slow_type(page.get_by_placeholder("Digite a sigla ou o nome da"), SIGLA)
        time.sleep(2)
        page.get_by_text(NOME_UNIVERSIDADE).click()
        time.sleep(2)
        page.get_by_role("button", name="Enviar").click()
        time.sleep(2)
        page.locator("#username").click()
        slow_type(page.locator("#username"), LOGIN)

        time.sleep(2)
        page.get_by_label("Senha").click()
        slow_type(page.get_by_label("Senha"), SENHA)
        time.sleep(2)
        page.locator("button[name='_eventId_proceed']").click()

        page.wait_for_timeout(5000)

    page1 = context.new_page()
    page1.goto(
        "https://www-webofscience-com.ez42.periodicos.capes.gov.br/wos/woscc/basic-search"
    )
    page1.locator("#onetrust-accept-btn-handler").click()
    time.sleep(2)
    if PESQUISA_AVANCADA:
        page1.get_by_role("link", name="Advanced search").click()
        time.sleep(2)
        slow_type(page1.get_by_placeholder("Enter or edit your query here"), PESQUISA)
        time.sleep(2)
        page1.get_by_label("Query editor").locator("button").filter(has_text="Search").click()
    else:
        page1.locator("div").filter(
            has_text=re.compile(r"^Example: liver disease india singh$")
        ).nth(3).click()
        time.sleep(2)
        page1.get_by_label("Search box").click()
        slow_type(page1.get_by_label("Search box"), PESQUISA)
        time.sleep(2)
        page1.get_by_role("button", name="Search", exact=True).click()
        time.sleep(2)

    # Localiza o elemento do cabeçalho e obtém o texto
    results_heading = page1.get_by_role(
        "heading", name=re.compile(r"results from Web of")
    )
    results_text = results_heading.inner_text()

    match = re.search(r"([\d,]+)", results_text)
    if match:
        number_of_results = match.group(1).replace(",", "")
        print(f"Número de resultados: {number_of_results}")
    else:
        raise Exception("Número de resultados não encontrado.")
    
    # Aumento no tempo de espera
    page1.get_by_role("button", name="Export", exact=True).click()
    time.sleep(2)
    page1.get_by_label("Tab delimited file").click()
    time.sleep(2)
    page1.get_by_role("button", name="Author, Title, Source").click()
    time.sleep(15)

    inicio = 1
    fim = 1000
    total_results = int(number_of_results)
    while True:
        if inicio > total_results:
            break
        nome_arquivo = f"arquivo_{inicio}_{fim}.txt"
        download_path = os.path.join(NOME_PASTA, nome_arquivo)
        start_time = time.time()
        if not os.path.exists(download_path):
            dowload_data(page1, nome_arquivo, NOME_PASTA, inicio, fim)
        end_time = time.time()
        elapsed_time = end_time - start_time
        inicio = fim + 1
        fim = min(inicio + 999, total_results)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    os.makedirs(NOME_PASTA, exist_ok=True)
    run(playwright)
