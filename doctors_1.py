#load dataframes from csv files for compare

import pandas

#load rxcode data
docs = pandas.read_csv("v3_Выгрузка_Педиатры/doctors.csv", sep=';', index_col='Id')
lpus = pandas.read_csv("v3_Выгрузка_Педиатры/lpus.csv", sep=';', index_col='Id')
wps  = pandas.read_csv("v3_Выгрузка_Педиатры/doctorWorkplaceSpecialities.csv", sep=';', index_col=['Doctor_id', 'Lpu_id'])

#load arm data
arm_docs = pandas.read_csv("080824_Педиатры_AV/doctors_AV080824.csv",  encoding='CP866', sep=';', index_col='Id')
arm_lpus = pandas.read_csv("080824_Педиатры_AV/lpus_AV080824.csv",  encoding='CP866', sep=';', index_col='Id')
arm_wps  = pandas.read_csv("080824_Педиатры_AV/doctorWorkplaceSpecialities_AV080824.csv",  encoding='CP866', sep=';', index_col=['Doctor_id', 'Lpu_id'])

# print("", "docs:", len(docs), "\n", "lpus:", len(lpus), "\n", "wps:", len(wps))# print("", "arm_docs:", len(arm_docs), "\n", "arm_lpus:", len(arm_lpus), "\n", "arm_wps:", len(arm_wps))# pdocs = pandas.read_csv("v3_Выгрузка_Педиатры/doctors.csv", sep=';')# print(arm_docs, arm_lpus, arm_wps)

#join rxcode docs
rx = wps.join(docs, on='Doctor_id')
rx = rx.join(lpus, on='Lpu_id')

#join arm docs
arm = arm_wps.join(arm_docs, on='Doctor_id')
arm = arm.join(arm_lpus, on='Lpu_id')

#
# Result:
# docs - rx coe doctors, lpus - rxcode lpus, wps - relations
# arm_doc = a_rm doctors, arm_lpus - rxcode lpus, arm_wps - relations
# rx = full joined rxcode dataframe
# arm = full joined alpha_rm dataframe

