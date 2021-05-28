import requests
import bs4
import re


def Calculate__Postage(from_city, to_city, price, weight, post_method):
    Destination_From_Request = requests.get(
        "https://payeganltd.com/backend/web/index.php?r=site%2Fcity_list&just_state=3&id=1&q=" + from_city)
    Destination_To_Request = requests.get(
        "https://payeganltd.com/backend/web/index.php?r=site%2Fcity_list&just_state=3&id=1&q=" + to_city)
    if Destination_From_Request.status_code == 200 and Destination_To_Request.status_code == 200:
        From_The_Destination_Json = Destination_From_Request.json()
        To_The_Destination_Json = Destination_To_Request.json()
        if len(From_The_Destination_Json.get("results")) > 0 and len(To_The_Destination_Json.get("results")) > 0:
            form_data = {
                "from_id": From_The_Destination_Json.get("results")[0].get("id"),
                "to_id": To_The_Destination_Json.get("results")[0].get("id"),
                "inputWeight": weight,
                "inputPrice": price,
                "PayType": 1,
            }
            Response_Html = requests.post("https://payegan.ir/page/post/", data=form_data).content
            Bs_Object = bs4.BeautifulSoup(Response_Html, "html.parser")
            result_list = list(
                Bs_Object.find("div", attrs={"id": "getresponse"}).find("div", attrs={"class": "form-group"}).children)
            new_result_list = list(item for item in result_list if item != "\n")
            if post_method == 1 and re.search("([\d,])", new_result_list[1].text):
                return float(str(new_result_list[1].text).replace(",", "."))
            elif post_method == 0 and re.search("([\d,])", new_result_list[3].text):
                return float(str(new_result_list[3].text).replace(",", "."))
