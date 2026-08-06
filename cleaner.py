import pandas as pd # type: ignore

def cleanerCSV(file):
    df = pd.read_csv(file, na_values=['N/A', 'None', 'null'])
    
    # mapping table
    gender_map = {
        '男':'Male',
        'M':'Male',
        '女':'Female',
        'F':'Female'
    }

    department_map = {
        'HR' : '人力資源部',
        'IT' : '資訊部'
    }

    # delete duplitcates row
    df = df.drop_duplicates()

    # clean name
    df['name'] = df['name'].str.strip()

    # clean gender
    df['gender'] = df['gender'].replace(gender_map)

    # clean email 
    df['email'] = df['email']
    df['email'] = df['email'].str.replace('companycom', 'company.com')

    # clean phone
    df["phone"] = df["phone"].str.replace("-", "")
    
    # clean department
    df["department"] = df["department"].replace(department_map)
    
    # clean salary
    df['salary'] = df['salary'].abs()
    df.loc[df['salary'] > 200000, 'salary'] /= 100

    # clean hire_date
    df['hire_date'] = pd.to_datetime(df['hire_date'], errors = 'coerce')
    
    return (df)

if __name__ == '__main__':
    clear_data = cleanerCSV('customers.csv')