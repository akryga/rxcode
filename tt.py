# import pandas package as pd
import pandas as pd

# Define a dictionary containing students data
data = {'Name': ['Ankit', 'Amit', 'Aishwarya', 'Priyanka'],
        'Age': [21, 19, 20, 18],
        'Stream': ['Math', 'Commerce', 'Arts', 'Biology'],
        'Percentage': [88, 92, 95, 70]}


# Convert the dictionary into DataFrame
df = pd.DataFrame(data, columns=['Name', 'Age', 'Stream', 'Percentage'])

data = {'Name': ['Ankit', 'Amit', 'Dishwarya', 'Priyanka', 'Ankit','Alexander'],
        'Age': [21, 19, 20, 18, 22, 77],
        'Stream': ['Math', 'Commerce', 'Arts', 'Biology', 'Arts', 'Psy'],
        'Percentage': [88, 92, 95, 70, 22, 11]}

print("Given Dataframe :\n", df)

df2 = pd.DataFrame(data, columns=['Name', 'Age', 'Stream', 'Percentage'])
print("Given Dataframe :\n", df2)

#добавляем в df['new'] колонку 'new', содержащую dataframe из df2, где 'name' == 'name'
def isName(x, dframe):
    return dframe[dframe['Name'].eq(x)].to_dict()

df['new']=df['Name'].apply(isName, args=(df2,))
print()
df2[df2['Name'].eq('Ankit')]


