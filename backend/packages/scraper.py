import requests
from bs4 import BeautifulSoup


def scrap_data():
    response = requests.get("https://www.psoas.fi/en/apartments")
    soup = BeautifulSoup(response.text, "html.parser")
    divs = soup.find_all("div", class_="card-huoneisto__details")

    obj = []

    for div in divs:
        name = div.find(
            "span", class_="card-huoneisto__summary__nimi").get_text(strip=True)
        apartment_report = div.find(class_="card-huoneisto__summary__report")
        address = div.find(
            "span", class_="card-huoneisto__summary__osoite").get_text(strip=True)
        image_src = div.find("img", class_="attachment-haku")["src"]
        apartment_number = apartment_report.get_text(strip=True).split(" ")[
            0] if apartment_report else 0
        apartment_vacancy = apartment_report.get_text(
            strip=True).split(" ")[-2] if apartment_report else 0
        obj.append({
            "Name": name,
            "Address": address,
            "ImageUrl": image_src,
            "ApartmentAmount": int(apartment_number),
            "DormVacancy": int(apartment_vacancy),
        })
    return obj
