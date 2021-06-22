import requests
import bs4
import re
from decimal import Decimal


def replace_dot_price(price):
    price = list(str(price).replace(".", ""))
    price.reverse()
    new_number = ""
    j = 0
    for s_number in enumerate(price):
        if j == 3:
            new_number += ","
            j = 0
        elif j < 3:
            new_number += s_number[1]
            j += 1
        if j == 0 and s_number[0] != 0:
            new_number += s_number[1]
            j += 1
    return new_number[::-1]


def Calc_Price(Product_Cost, Postage_Cost):
    Total = Product_Cost if ".0" not in str(Product_Cost) else int(
        str(Product_Cost)[0:str(Product_Cost).find(".")]) + Postage_Cost
    return Total


def Calculate__Postage(from_city, to_city, price, weight, post_method):
    form_data = {
        "from_id": from_city,
        "to_id": to_city,
        "inputWeight": weight,
        "inputPrice": price,
        "PayType": 1,
    }
    Response_Html = requests.post("https://payegan.ir/page/post/", data=form_data).content
    Bs_Object = bs4.BeautifulSoup(Response_Html, "html.parser")
    result_list = list(
        Bs_Object.find("div", attrs={"id": "getresponse"}).find("div", attrs={"class": "form-group"}).children)
    new_result_list = list(item for item in result_list if item != "\n")
    if int(post_method) == 1 and re.search("([\d]+,[\d]+)", new_result_list[1].text).group():
        Str_Postal_Cost = str(new_result_list[1].text).replace(",", ".")
        Postal_Cost = int(str(round(float(Str_Postal_Cost))) + "00")
        Total_Cost = Calc_Price(Product_Cost=price, Postage_Cost=Postal_Cost)
        context = {
            "Total_Cost": Total_Cost,
            "Total_Cost_Show": replace_dot_price(Total_Cost),
            "Postal_Cost": Postal_Cost,
            "to_city_code": to_city,
        }
        return context
    elif int(post_method) == 0 and re.search("([\d]+,[\d]+)", new_result_list[3].text).group():
        Str_Postal_Cost = str(new_result_list[3].text).replace(",", ".")
        Postal_Cost = int(str(round(float(Str_Postal_Cost))) + "00")
        Total_Cost = Calc_Price(Product_Cost=price, Postage_Cost=Postal_Cost)
        context = {
            "Total_Cost": Total_Cost,
            "Total_Cost_Show": replace_dot_price(Total_Cost),
            "Postal_Cost": Postal_Cost,
            "to_city_code": to_city,
        }
        return context
