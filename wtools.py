def wdiff(l1, l2):
    ret = []
    for t in l1:
        if t not in l2:
            ret.append(t)
    for t in l2:
        if t not in l1:
            ret.append(t)
    return ret

def normFedSubj(trial, fedSubj):

    if not trial or isinstance(trial, float):
        return trial
    isfs = fedSubj[fedSubj.eq(trial).any(axis=1)]
    if not isfs.empty:
        return isfs.iloc[0,0]
    return trial

# def fs_issame(fs1, fs2, fedSubj):
#     if fs1 == fs2:
#         return True
#     nfs2 = normFedSubj(fs2, fedSubj)
#     if fs1 == nfs2:
#         return True
#     return normFedSubj(fs1,fedSubj) == nfs2

# функция поиска врача в базе RX (связанные врачи+лпу)  по ФИО и региону
# возвращает (cnt, список id) для найденных записей
def arm_sep(x, rx):
    # rx[rx['Second_name'].eq('Мирошникова')&rx['Federation_subject'].eq('Москва')].index.tolist()
    r=1
    tt = rx[rx['Second_name'].eq(x['Second_name']) &
            rx['First_name'].eq(x['First_name']) &
            rx['Patronymic'].eq(x['Patronymic']) & 
            rx['Federation_subject_norm'].eq(x['Federation_subject_norm'])].index
    return len(tt), tt.tolist()
