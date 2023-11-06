from bs4 import BeautifulSoup as BS
from requests.exceptions import HTTPError
from dataclasses import dataclass
from lxml import html
import requests
import json
import csv
import os


@dataclass
class RowsTable:
    column_name: str
    column_item: str

@dataclass
class StorageTable:
    data: RowsTable

class ExpectedValueHigher(Exception):
    def __init__(self, key, value, expected_value):
        self.key = key
        self.value = value
        self.expected_value = expected_value

    def __str__(self):
        return f"{self.key} (Frontend:JavaScript|Backend:PHP) has {self.value} unique visitors per month. (Expected more than {self.expected_value})"
    
    
class WikiArticleTable:

    __INSTANCE = None
    __URL = "https://en.wikipedia.org/w/api.php"
    __PARAMS = {
        "action": "parse",
        "page": "Programming_languages_used_in_most_popular_websites",
        "format": "json"
    }

    def __new__(cls, *args, **kwargs):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = super().__new__(cls)
        return cls.__INSTANCE
    
    def __del__(self):
        self.__INSTANCE = None

    def __init__(self, section: str = "all", range_from: int = 0, range_to: int = 6) -> None:
        """
        Params: Table
        Section: [all, head, value]
        Min range: 0
        Max range: 6
        """
        self.section = section
        self.range_from = range_from
        self.range_to = range_to

    @classmethod
    def __get_request_session(cls):
        session = requests.Session()
        response = session.get(url=cls.__URL, params=cls.__PARAMS)
        if response.status_code == 200:
            return response
        else:
            raise HTTPError(response.status_code)
        
    def __get_html(self):
        response = self.__get_request_session()
        data = response.json()
        body_html = data["parse"]["text"]["*"]
        return body_html

    
    def __get_table(self):
        body_html = self.__get_html()
        soup = BS(body_html, "html.parser")
        table_html = soup.find("table").find('tbody').find_all("tr")
        return table_html

    def get_content_table(self):
        table_html = self.__get_table()
        try:
            rows = []
            for row in table_html:
                category_getters = {
                    "all": row.find_all(["th", "td"]),
                    "head": row.find_all("th"),
                    "value": row.find_all("td"),
                }
                if not (headers := category_getters[self.section]):
                    pass
                if len(headers) > 0:
                    row = [line.rstrip() for line in [headers[i].text for i in range(self.range_from, self.range_to)]]
                    rows.append(row)
            return rows  
        except KeyError:
            raise KeyError("Choose the one of correct type from [all, head, value] data.")

    def __get_items_table(self):
        table_html = self.__get_table()
        rows = []
        for row in table_html:
            headers = row.find_all(["th", "td"])
            if len(headers) > 0:
                row = [line.rstrip() for line in [headers[i].text for i in range(self.range_from, self.range_to)]]
                rows.append(row)
        return rows  

    def __get_massive_table(self) -> StorageTable:
        table = self.__get_items_table()
        massive = []
        for j in range(len(table)):
            item = []
            for i in range(self.range_from, self.range_to):
                item.append(RowsTable(column_name=table[0][i], column_item=table[j][i]))
            massive.append(item)
        return StorageTable(data=massive)
    
    def get_classobject(self, column_number: int = None):
        """
        params:: range[0,5]
        """
        table = self.__get_massive_table()
        if column_number is not None:
            if column_number in range(1,6) and isinstance(column_number, int):
                for item in table.data:
                    yield item[column_number]
            else:
                raise ValueError("Only integer value in range [1,5]")
        else: 
            yield table.data

    def get_populatiry(self):
        content = self.get_content_table()[1:]
        popularity_list = []
        for row in content:
            popularity = int(str(row[1]).split()[0].split('[')[0].replace(',', "").replace('.', ""))
            popularity_list.append(popularity)
        return popularity_list
    
    def get_websites_with_popularity(self):
        content = self.get_content_table()[1:]
        websites_with_popularity_dict = {}
        for row in content:
            popularity = int(str(row[1]).split()[0].split('[')[0].replace(',', "").replace('.', ""))
            websites = str(row[0]).split('[')[0]
            websites_with_popularity_dict[websites] = popularity
        return websites_with_popularity_dict
    
    def compare_numbers(self, websites_with_popularity_dict: dict, compare_number: int):
        for website, popularity in websites_with_popularity_dict.items():
            if not isinstance(popularity, (int, float)) or not isinstance(compare_number, (int, float)):
                raise TypeError("Both arguments should be numeric")
            if popularity < compare_number:
                raise ExpectedValueHigher(website, popularity, compare_number)
                
    def save_table_to_csv(self, name: str = "default") -> None:
        rows = self.get_content_table()
        filename = f"wikipedia/csv/{name}.csv"
        absolute_path = os.path.dirname(filename)
        os.makedirs(absolute_path, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in rows:
                writer.writerow(row)  

    def save_page_to_json(self, name: str = "default") -> None:
        response = self.__get_request_session()
        data = response.json()
        filename = f"wikipedia/json/{name}.json"
        absolute_path = os.path.dirname(filename)
        os.makedirs(absolute_path, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
           
                

