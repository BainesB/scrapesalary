import scrapy # not using this at the moment
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser
import sqlite3 
import inspect 
import re 
import time

def getDailyGrose_n_TakeHome(salary):
    userPay = salary 

    browser = webdriver.Firefox()
    browser.get('https://www.thesalarycalculator.co.uk/salary.php')


    inputbox = browser.find_element_by_name('salary')
    inputbox.send_keys(userPay)
    inputbox.send_keys(Keys.RETURN)

    #Now get back the answer.

    browser.implicitly_wait(4)

    #Had to use xpath finder to get the cell i want. 

    result_cell_grose = browser.find_elements_by_xpath('/html/body/section[1]/div/table/tbody/tr[1]/td[2]')

    result_cell_daily_net = browser.find_elements_by_xpath('/html/body/section[1]/div/table/tbody/tr[4]/td[6]')

    result_cell_daily_grose = browser.find_elements_by_xpath('/html/body/section[1]/div/table/tbody/tr[4]/td[2]')

    browser.implicitly_wait(4)

    # Getting a list back
    # This is just a check. 

    for i in result_cell_daily_grose:
        numbstr= i.text[1:]
        Daily_Grose = int(round(float(numbstr),0))
        print('Daily Grose', Daily_Grose)
    for i in result_cell_daily_net:
        numbstr= i.text[1:]
        Daily_TakeHome = int(round(float(numbstr),0))
        print('Daily take home:', Daily_TakeHome)

    conn = sqlite3.connect('salaryTable.db')
    cursor = conn.cursor()

    # go to try and put numbers in

    cursor.execute(f'''
    INSERT INTO salaryBreakdown (GROSE_ANNUAL_SALARY, Daily_Grose_Pay, Daily_Take_Home_Pay)
    VALUES({userPay},{Daily_Grose},{Daily_TakeHome});''')

    TableContents = cursor.execute('''
    select * from salaryBreakdown; 
    ''')

    for row in cursor:
        print(row)

    conn.commit()
    cursor.close()
    conn.close() 

    browser.close()

#getDailyGrose_n_TakeHome(14000)


for i in range(10000,101000,1000):
    getDailyGrose_n_TakeHome(i) 
    time.sleep(40)


#> Turn this all into a for loop that stores results for lots of salaries.

# But the second one gets an error: 
    #selenium.common.exceptions.SessionNotCreatedException: Message: Tried to run command without establishing a connection

## the website doesn't seem to like me making lots of attempts. 
    # i think i want to 'try'and do something else if it gets an acception. 

    # I also want to change the SQl so that if it exist it doesn't break or stop. 
