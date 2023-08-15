# bot/utils.py:
import requests
from bs4 import BeautifulSoup
from database.models import Car
from database.db_session import SessionLocal

def check_publications():
    BASE_URL = "https://auto.ria.com/search/?indexName=auto,order_auto,newauto_search&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=-1&dealer.id=135&page={}&size=50"
    page_num = 0
    links = []

    while True:
        URL = BASE_URL.format(page_num)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Получение списка ссылок на текущей странице
        current_links = [a['href'] for a in soup.find_all('a', href=True) if "/auto_" in a['href']]
        
        # Если на странице нет ссылок, прерываем цикл
        if not current_links:
            break
        
        links.extend(current_links)
        page_num += 1

    # Удаление дубликатов
    links = list(set(links))
    print(len(links))
    
    session = SessionLocal()
    db_links = session.query(Car.link).all()
    db_links = [link[0] for link in db_links]
    
    new_links = [link for link in links if link not in db_links]
    removed_links = [link for link in db_links if link not in links]
    
    added_links = set()  # Для отслеживания уже добавленных ссылок

    for link in new_links:
        # Проверка на существование записи перед добавлением
        exists = session.query(Car.link).filter_by(link=link).first() is not None
        if not exists and link not in added_links:
            new_car = Car(link=link)
            session.add(new_car)
            added_links.add(link)
    
    for link in removed_links:
        removed_car = session.query(Car).filter(Car.link == link).first()
        session.delete(removed_car)
    
    session.commit()
    session.close()
    
    return new_links, removed_links
