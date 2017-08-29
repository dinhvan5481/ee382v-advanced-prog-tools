import json
import sys
import re
import urllib
from bs4 import BeautifulSoup


def contractAsJson(filename):
  with open(filename) as f:
    html_doc = f.read()

  soup = BeautifulSoup(html_doc, 'html.parser')
  curr_prc = soup.find_all('span', class_="time_rtq_ticker")[0].get_text()

  opt_tables = soup.find_all('table', attrs={"border": 0, "cellpadding": 3, "cellspacing": 1, "width": "100%"})
  table_keys = ["Strike", "Symbol", "Last", "Change", "Bid", "Ask", "Vol", "Open"]
  table_rows = []
  for table in opt_tables:
    rows = table.find_all('tr')
    for row in rows:
      cells = (c.get_text() for c in row.find_all('td'))
      table_row = dict(zip(table_keys, cells))
      if table_row != {}:
        table_row_map = {}
        for k, cell in table_row.items():
          if k == 'Symbol':
            if 'C' in cell:
                table_row_map["Type"] = "C"
                type_idx = cell.rindex("C")
            else:
                table_row_map["Type"] = "P"
                type_idx = cell.rindex("P")

            table_row_map["Date"] = cell[type_idx - 6: type_idx]
            table_row_map["Symbol"] = cell[0: type_idx - 6]
          else:
            table_row_map[k] = cell

        table_rows.append({k: table_row_map[k] for k in sorted(table_row_map.keys())})

  optionQuotes = sorted(table_rows, key=lambda row: int(row['Open'].replace(',', '')), reverse= True)

  url_tags = soup.find_all('table', attrs={"id": "yfncsumtab"})[0].find_all('a', href=True)
  date_urls = []
  base_url = 'http://finance.yahoo.com'
  for url in url_tags:
    # print(url["href"])
    if re.search('(\d{4}-\d{2}(-\d{2})?)$', url["href"].strip()) is not None:
      date_urls.append('{}{}'.format(base_url, url["href"]).replace('&', '&amp;'))

  return json.dumps({"currPrice": float(curr_prc), "dateUrls": date_urls, "optionQuotes": optionQuotes})


if __name__ == '__main__':
  filename = 'aapl.dat'
  html_doc = ''
  # with open(filename) as f:
  #   html_doc = f.read()
  #
  # soup = BeautifulSoup(html_doc, 'html.parser')
  # curr_prc = soup.find_all('span', class_="time_rtq_ticker")[0].get_text()
  #
  # opt_tables = soup.find_all('table', attrs={"border": 0, "cellpadding": 3, "cellspacing": 1, "width": "100%"})
  # table_keys = ["Strike", "Symbol", "Last", "Change", "Bid", "Ask", "Vol", "Open"]
  # table_rows = []
  # for table in opt_tables:
  #   rows = table.find_all('tr')
  #   for row in rows:
  #     cells = (c.get_text() for c in row.find_all('td'))
  #     table_row = dict(zip(table_keys, cells))
  #     if table_row != {}:
  #       table_row_map = {}
  #       for k, cell in table_row.items():
  #         if k == 'Symbol':
  #           if 'C' in cell:
  #               table_row_map["Type"] = "C"
  #               type_idx = cell.rindex("C")
  #           else:
  #               table_row_map["Type"] = "P"
  #               type_idx = cell.rindex("P")
  #
  #           table_row_map["Date"] = cell[type_idx - 6: type_idx]
  #           table_row_map["Symbol"] = cell[0: type_idx - 6]
  #         else:
  #           table_row_map[k] = cell
  #
  #       table_rows.append({k: table_row_map[k] for k in sorted(table_row_map.keys())})
  #
  # optionQuotes = sorted(table_rows, key=lambda row: int(row['Open'].replace(',', '')), reverse= True)
  #
  # url_tags = soup.find_all('table', attrs={"id": "yfncsumtab"})[0].find_all('a', href=True)
  # date_urls = []
  # base_url = 'http://finance.yahoo.com'
  # for url in url_tags:
  #   # print(url["href"])
  #   if re.search('(\d{4}-\d{2}(-\d{2})?)$', url["href"].strip()) is not None:
  #     date_urls.append('{}{}'.format(base_url, url["href"]).replace('&', '&amp;'))


  computedJson = contractAsJson("aapl.dat")
  expectedJson = open("aapl.json").read()

  if json.loads(computedJson) != json.loads(expectedJson):
    print("Test failed!")
    print("Expected output:", expectedJson)
    print("Your output:", computedJson)
    assert False
  else:
    print("Test passed")