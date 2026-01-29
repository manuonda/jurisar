"""
Scraper para jurisprudencia de Jujuy
"""
from playwright.sync_api import sync_playwright
import time
from typing import List, Dict
from core.config import settings


def scrape_fallos_jujuy(max_pages: int = None) -> List[Dict]:
    """
    Scraper para jurisprudencia de Jujuy
    Extrae fallos de jurisprudencia.justiciajujuy.gov.ar
    """
    max_pages = max_pages or settings.SCRAPER_MAX_PAGES
    fallos = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        base_url = "https://jurisprudencia.justiciajujuy.gov.ar/public/buscador"
        
        for i in range(max_pages):
            try:
                page.goto(f"{base_url}?index={i}")
                page.wait_for_selector(".resultado-fallo", timeout=10000)
                
                # Extraer información de cada fallo
                items = page.query_selector_all(".resultado-fallo")
                
                for item in items:
                    try:
                        caratula_elem = item.query_selector('.caratula')
                        fecha_elem = item.query_selector('.fecha')
                        tribunal_elem = item.query_selector('.tribunal')
                        link_elem = item.query_selector('a')
                        
                        if not caratula_elem or not link_elem:
                            continue
                        
                        fallo = {
                            'caratula': caratula_elem.inner_text(),
                            'fecha': fecha_elem.inner_text() if fecha_elem else None,
                            'tribunal': tribunal_elem.inner_text() if tribunal_elem else None,
                            'url': link_elem.get_attribute('href')
                        }
                        
                        # Ir al detalle del fallo para obtener texto completo
                        if fallo['url']:
                            detail_page = browser.new_page()
                            detail_page.goto(fallo['url'])
                            detail_page.wait_for_selector('.texto-fallo', timeout=10000)
                            
                            texto_elem = detail_page.query_selector('.texto-fallo')
                            if texto_elem:
                                fallo['texto_completo'] = texto_elem.inner_text()
                            
                            detail_page.close()
                        
                        fallos.append(fallo)
                        
                    except Exception as e:
                        print(f"Error procesando fallo: {e}")
                        continue
                
                time.sleep(settings.SCRAPER_DELAY_SECONDS)
                
            except Exception as e:
                print(f"Error en página {i}: {e}")
                break
        
        browser.close()
    
    return fallos
