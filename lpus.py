import csv
from psycopg2 import DatabaseError
import connect as pg
from config import load_config
import pandas 
import re
import logging as log
log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=log.DEBUG)

src_lpus = pandas.DataFrame()
# if __name__ == '__main__':
engine = pg.connect(load_config())
try:
    src_lpus = pandas.read_sql('select * from source_lpus_m', con=engine, index_col='source_id')
except DatabaseError as ex:
    print(ex)

src_lpus['city']=src_lpus.city.str.strip()
sl = src_lpus
fname = '.cache/original_cities.csv'
origCities = pandas.DataFrame()

try:
    origCities = pandas.read_csv(fname)
    log.info('Загрузили cache городов')
except OSError:
    log.warning("Could not open/read cache file: %s", fname)
    # готовим справочник городов
    log.info('Готовим города')
    origCities=sl[sl.city.notna()].city.str.title().drop_duplicates().sort_values()
    log.info('Завершили готовить города')
    origCities.to_csv(fname, quoting=csv.QUOTE_NONNUMERIC)
    log.info('Сохранили cache городов')
    
cities = origCities.city.tolist()
# совпадение е<->ё
sl[sl.city.str.match(r'.*ё', case=False)&sl.city.notna()].city.tolist()
# наличие , или .
sl[sl.city.str.match(r'.*[,\.]', case=False)&sl.city.notna()].city
# наличие в адресе (Пермский край) или регион+город - Республика Саха (Якутия), Якутск
sl[sl.addr.str.match(r'.*\(\w+\)', case=False)&sl.addr.notna()]
# (с.) (п.) (ст.) п.г.т г.

# print(src_lpus[src_lpus.city1.ne(src_lpus.city) & src_lpus.city1.notna()])
# use regex engine in pandas
# src_lpus[src_lpus.city.str.contains('Москва', flags=re.IGNORECASE, na=False)].index.size -> 47560
# 
# найти уникальные поселки села и т.п.
# src_lpus[src_lpus.city.str.contains('^(\\w(\\.|\\s))', flags=re.IGNORECASE, na=False)].city.drop_duplicates() -> Length: 74
# 
# уникальные города, исключить поселки села и т.п.
# src_lpus[src_lpus.city.str.contains('^(?!\\w(\\.|\\s))', flags=re.IGNORECASE, na=False)].city.drop_duplicates() -> Length: 3003

ct_patt = r'(\b' + r'\b)|(\b'.join(cities) + r'\b)'
re_patt = re.compile(ct_patt)
gr = re_patt.findall('Тверская область, Торжок, Уфа, Москва')

def loboda(rx):    
	global ct_patt, re_patt
	gr = re_patt.findall(rx.addr)
	ret = []
	if gr:
		for i in gr:
			ret.append([x for x in i if x][0])
	if ret:
		return list(set(ret))
	else:
		return None
	

cnt = int(input("Введите число строк для вычисления городов по адресам [100]: ").strip() or "100")
log.info("Вычисляем города по адресам для {0} строк".format(cnt))
sl['city_addr']=sl[sl.addr.notna()].head(cnt).apply(loboda, axis=1)
sl[~sl.city_addr.notna()]=None	# set empty cells to None
log.info("Завершили вычислять города по адресам")
print(sl.head(cnt))
