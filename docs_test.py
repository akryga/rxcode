import pandas
from doctors_1 import rx, arm
from wtools import *
# from csvReader import *

#check difference in Federation_subject
fs_rx = rx['Federation_subject'].drop_duplicates().sort_values().tolist()
fs_arm = arm['Federation_subject'].drop_duplicates().sort_values().tolist()
fs_diff = wdiff(fs_rx, fs_arm)

#load Federation_subject corrector
fs_dict = pandas.read_table('Federations.csv', sep=';', header=None)

#check difference in Federation_subject with corrector
norm_fs_rx=rx['Federation_subject'].drop_duplicates().apply(normFedSubj, args=(fs_dict,)).sort_values().tolist()
norm_fs_arm=arm['Federation_subject'].drop_duplicates().apply(normFedSubj, args=(fs_dict,)).sort_values().tolist()
print(wdiff(norm_fs_arm, norm_fs_rx))

#example of Federation_subject correction
#arm['Norm_Fed_subj'] = arm['Federation_subject'].apply(normFedSubj, args=(fs_dict,))
arm['Federation_subject_norm']=arm['Federation_subject'].apply(normFedSubj, args=(fs_dict,))
rx['Federation_subject_norm']=rx['Federation_subject'].apply(normFedSubj, args=(fs_dict,))


#select by criteria
rx[rx['Federation_subject'].isnull()] #[2471 rows x 9 columns]

#example for calculate function on each row of dataframe
rx.head().apply(lambda x: " ".join((x[1],x[2],x[3])), axis=1)

#convert result tolist
rx[:15].apply(lambda x: " ".join((x[1],x[2],x[3])), axis=1).tolist()

#convert result indexes to list
rx[:15].apply(lambda x: " ".join((x[1],x[2],x[3])), axis=1).index.tolist()

#select some rows from dataframe
rx[:15]

#select some columns from dataframe
rx[['Second_name', 'First_name', 'Patronymic']].head()

# get row by multiindex
rx.loc[('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')]
# get field value of row found
rx.loc[('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')].Federation_subject_norm
rx.loc[('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')]['Federation_subject_norm']

# find rows by multiindex
rx[rx.index==('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')]

# get field for rows found
rx[rx.index==('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')].Federation_subject_norm
rx[rx.index==('83c24bd4-2c21-4b1b-a2a9-8abde2f7d2d5', '8ee6b961-3252-47fc-bab5-6887504a4d9e')]['Federation_subject_norm']

rx.keys

#arm sep
#находим всех врачей
arm.head().apply(arm_sep, args=(rx,), axis=1)