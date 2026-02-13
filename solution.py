import pandas as pd
import re

possible_operators=["+","-","*"]


def add_virtual_column(df:pd.DataFrame,role:str,new_column:str):
    
    if type(role) != str or type(new_column) != str:
        return pd.DataFrame([])
     
    columns= re.split(r'[*\-+]+', role)
    columns = [column.strip().replace(" ","") for column in columns]
    operators = []
    
    for char in role:
        if char in possible_operators:
            operators.append(char)

    
    # Looking for incorrect namings
    regex = re.compile(r'[@!#$%^&*()<>?/\|}{~:]')       
    for column in [*columns,new_column]:
        if any(char.isdigit() for char in column) or (regex.search(column) != None):
            return pd.DataFrame([])
        
    for column in columns:
        if column not in df.columns:
            return pd.DataFrame([])  
    for operator in operators:
        if operator not in possible_operators:
            return pd.DataFrame([])

    # Calculating new column
  
    col_series = [df[col] for col in columns]
    
    for i,operator in enumerate(operators):
       
        if operator == "+":
            col_series[i+1] = col_series[i] + col_series[i+1]
        if operator == "-": 
            col_series[i+1] = col_series[i] - col_series[i+1]
        if operator == "*":
            col_series[i+1] = col_series[i] * col_series[i+1] 
        
   
        
    
    df[new_column] = col_series[-1]
    
    return df
   

