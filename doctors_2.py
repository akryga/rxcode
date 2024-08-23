import pandas
from doctors_1 import rx , arm
import warnings
import time
import csv
import logging as log
log.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=log.DEBUG)

# arm, rx - dataframes f rom csv files
# -----------------------------------------------------------------------------
# функция нормализации федеральных субъектов
# -----------------------------------------------------------------------------
def federation_subject_norm(trial, fedSubj):
    if not trial or isinstance(trial, float):
        return trial
    isfs = fedSubj[fedSubj.eq(trial).any(axis=1)]
    if not isfs.empty:
        return isfs.iloc[0,0]
    return trial

def fill_empty_fs_by_city(x, rx):
    (fs, city) = (x.Federation_subject, x.City)
    if fs:
        return fs
    rx[rx.City.eq(city)]
        

# -----------------------------------------------------------------------------
# функция поиска врача в базе RX (связанные врачи+лпу)  по ФИО и региону
# возвращает (cnt, список id) для найденных записей
# -----------------------------------------------------------------------------
def arm_sep(x, rx, column_name='Federation_subject_norm' ):
    global rxFIO #global cache
    if rxFIO.empty:        
        rxFIO = rx['Second_name'] + rx['First_name'] + rx['Patronymic']
    
    armFIO = x['Second_name'] + x['First_name'] + str(x['Patronymic'])
    
    tt = rx[ 
            rxFIO.eq(armFIO) &
            # rx['Second_name'].eq(x['Second_name']) & rx['First_name'].eq(x['First_name']) & rx['Patronymic'].eq(x['Patronymic']) & 
            rx[column_name].eq(x[column_name])].index
    return tt.size, tt.tolist()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# пробное применение мэтчинга баз по исходным регионам (федеральным субъектам) apply arm_sep
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# -- arm['Federation_subject_norm'] = arm['Federation_subject'] # -- rx['Federation_subject_norm'] = rx['Federation_subject']
# пробуем загрузить предыдущий cache регионов из файла 
fname = '.cache/found_orig_fs.csv'

rxFIO = pandas.DataFrame() # global cache
matching = pandas.DataFrame()

try:
    matching = pandas.read_csv( fname, index_col=['Doctor_id', 'Lpu_id'])
    log.info('Загрузили cache мэтчинга врачей arm в базе rx (по неизмененным регионам)')
except OSError:
    log.warning("Could not open/read cache file: %s", fname)
    # мэтчим всех врачей из arm в базе rx (по неизмененным регионам)
    log.info('Начинаем мэтчить всех врачей arm в базе rx (по неизмененным регионам)')
    matching = arm.apply(arm_sep, args=(rx,'Federation_subject'), axis=1)
    log.info('Завершили мэтчить всех врачей arm в базе rx (по неизмененным регионам)')
    matching.to_csv(fname)
    log.info('Сохранили cache мэтчинга врачей arm в базе rx (по неизмененным регионам)')
    

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Применяем корректировку регионов - все регионы сводим к каноническому значению
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# load Federation_subject corrector
try:
    fs_dict = pandas.read_table('.cache/Federations.csv', sep=';', header=None)
except OSError:
    log.warning("Could not open/read cache file: %s", fname)

# применяем корректировку регионов для базы arm. 
log.info('Применяем корректировку регионов для базы arm.')
arm_FS_norm = pandas.DataFrame()
fname = '.cache/arm_norm_fs.csv'
try:
    # пробуем загрузить предыдущую корректировку регионов для базы arm
    arm_FS_norm = pandas.read_csv(fname, index_col=['Doctor_id', 'Lpu_id'])
    log.info('Загрузили предыдущую корректировку регионов для базы arm')
except OSError:
    log.warning("Could not open/read cache file: %s", fname)
    # вычисляем корректировку регионов для базы arm
    log.info('Вычисляем корректировку регионов для базы arm')
    arm_FS_norm = arm['Federation_subject'].apply(federation_subject_norm, args=(fs_dict,))
    log.info('Завершили корректировку регионов для базы arm')
    arm_FS_norm.to_csv(fname, quoting=csv.QUOTE_NONNUMERIC)
    
# пополняем пустые регионы в базе rx по значениям городов в базе rx 
# пустые регионы загружаются как float NaN
# rx[rx.Federation_subject.apply(lambda x: not isinstance(x,str))]
#$///////////////////////////////////////////////////////////////////

# применяем корректировку регионов для базы rx. 
log.info('Применяем корректировку регионов для базы rx.')
rx_FS_norm  = pandas.DataFrame()
fname = '.cache/rx_norm_fs.csv'
try:
    # пробуем загрузить предыдущую корректировку регионов для базы rx
    rx_FS_norm  =   pandas.read_csv(fname, index_col=['Doctor_id', 'Lpu_id'])
    log.info('Загрузили предыдущую корректировку регионов для базы rx')
except OSError:
    log.warning("Could not open/read cache file: %s", fname)
    # вычисляем корректировку регионов для базы rx
    log.info('Вычисляем корректировку регионов для базы rx.')
    rx_FS_norm  =   rx['Federation_subject'].apply(federation_subject_norm, args=(fs_dict,))
    log.info('Завершили корректировку регионов для базы rx')
    rx_FS_norm.to_csv(fname, quoting=csv.QUOTE_NONNUMERIC)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# применение мэтчинга баз по корректным регионам (федеральным субъектам) apply arm_sep
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# мэтчинг баз по скорректированным федеральным субъектам apply arm_sep
log.info('Готовы мэтчить всех врачей arm в базе rx (по корректным регионам)')

arm['Federation_subject_norm'] = arm_FS_norm
rx['Federation_subject_norm'] = rx_FS_norm

# пробуем загрузить предыдущий мэтчинг 
fname = '.cache/found_norm_fs.csv'
matching2 = pandas.DataFrame()
try:
    matching2 = pandas.read_csv( fname, index_col=['Doctor_id', 'Lpu_id'])
    log.info('Загрузили предыдущую мэтчинг всех врачей arm в базе rx (по корректным регионам)')
except OSError:
    log.warning("Could not open/read cache file: %s", fname)
    # находим всех врачей in rx for arm
    log.info('Начинаем мэтчить всех врачей из arm в базе rx (по корректным регионам)')
    matching2 = arm.apply(arm_sep, args=(rx,), axis=1)
    log.info('Завершили мэтчить всех врачей из arm в базе rx (по корректным регионам)')
    matching2.to_csv(fname)
    

# tmp2 = pandas.read_csv('.cache/found_norm_fs.csv', index_col=['Doctor_id', 'Lpu_id'])
# tmp2.loc[(176,166590)] -> "0    (2, [('8721d51b-7f94-48bc-a93e-710f0cac4828', ..."
# tmp2.loc[(176,166590),'0'] -> "(2, [('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30'), ('e224652c-8a5e-4b67-84e7-a4d9cfaa46b5', 'a36ce782-4d33-4ecb-9b6e-2364e1f9bb6d')])"
# tmp2.loc[(176,166590)]['0'] -> "(2, [('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30'), ('e224652c-8a5e-4b67-84e7-a4d9cfaa46b5', 'a36ce782-4d33-4ecb-9b6e-2364e1f9bb6d')])"
# tmp2.loc[(176,166590)].iloc[0] ->  "(2, [('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30'), ('e224652c-8a5e-4b67-84e7-a4d9cfaa46b5', 'a36ce782-4d33-4ecb-9b6e-2364e1f9bb6d')])"
# разбор текста в json ast.literal_eval
# ast.literal_eval(tmp2.loc[(176,166590)].iloc[0]) -> (2, [('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30'), ('e224652c-8a5e-4b67-84e7-a4d9cfaa46b5', 'a36ce782-4d33-4ecb-9b6e-2364e1f9bb6d')])
# ast.literal_eval(tmp2.loc[(176,166590)].iloc[0])[0] -> 2
# ast.literal_eval(tmp2.loc[(176,166590)].iloc[0])[1] -> [('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30'), ('e224652c-8a5e-4b67-84e7-a4d9cfaa46b5', 'a36ce782-4d33-4ecb-9b6e-2364e1f9bb6d')]
# ast.literal_eval(tmp2.loc[(176,166590)].iloc[0])[1][0] -> ('8721d51b-7f94-48bc-a93e-710f0cac4828', '33e7ccf2-ca43-4b5b-8758-c20347c17c30')
# ast.literal_eval(tmp2.loc[(176,166590)].iloc[0])[1][0][1] '33e7ccf2-ca43-4b5b-8758-c20347c17c30'

# Result:
# arm_FS_norm - arm corrected federation_subject
# rx_FS_norm = rx corrected federation_subject






