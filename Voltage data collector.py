import os
from datetime import datetime
import time
import sys
import platform
import re
import colorama

colorama.init()  

def package_install() :
    try :
        import requests
    except :
        os.system("pip install requests")
    
    try :
        from bs4 import BeautifulSoup
    except :
        os.system("pip install bs4")
    
    try :
        import pandas as pd
    except  :
        os.system("pip install pandas")

    try :
        import tqdm
    except  :
        os.system("pip install tqdm")

def scraping() :
    # clearing the screen
    os.system("cls") if platform.system() == "Windows" else os.system("clear")

    print("HOT SCRAPER".center(os.get_terminal_size().columns), "\n")

    # getting time details
    time_period = float(input("For how long do you want to scrape (in minutes): "))
    interval = float(input("\nGet data at regular intervals of (in seconds): "))
    createFileAfter = float(input("\nCreate files after every $ number of data points : " ))

    start_time = re.sub(r"(\..*)", "", str(datetime.now()).split(" ")[1])
    start_time = re.sub(r":", "_", start_time)

    end_time = time_period*60 + time.time()

    # create the new folder
    os.system("mkdir Data_" + start_time)

    print("\n" + colorama.Fore.RED + "Since scraping is a computationally expensive job and its speed depends on the internet speed as well, donot assume that the number of data points collected will be exactly what you think and the actual number may vary a lot. But the whole process will terminate exactly after the speified time. Now since that's out of the way, let's go :)")

    print(colorama.Style.RESET_ALL)

    print("Starting the scraping process. Sit back and relax\n")

    counter = 1
    url = "https://www.delhisldc.org/Redirect.aspx?Loc=0804"   # URL of the site to be scraped

    # scraping for the first time to get the name of all the location
    r = requests.get(url)
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent, "html.parser")
    table = soup.find_all("table", id="ContentPlaceHolder3_dgrid")[0]

    location_names = [i.get_text() for i in table.find_all("td")][5::5]   # list containing names of all the locations
    # making a dict containing all the dataframes for all the locations
    dic = {i : pd.DataFrame({"Date": [], "Time": [], "RTU":[], "MW": [], "Mvar": [], "Voltage" : []})  for i in location_names}

    # setting an infinite loop which will break when the time gets over
    while True :
        #getting the index.html for the desired site
        r = requests.get(url)
        htmlContent = r.content

        #Parse the content
        soup = BeautifulSoup(htmlContent, "html.parser")

        # getting the element of the table required
        table = soup.find_all("table", id="ContentPlaceHolder3_dgrid")[0]

        # getting all the values
        lst = [i.get_text() for i in table.find_all("td")]
        rtu = list(map(int, lst[6::5]))
        mw = list(map(int, lst[7::5]))
        mvar = list(map(int, lst[8::5]))
        voltage = list(map(int, lst[9::5]))

        Date, Time = str(datetime.now()).split(" ")   # getting current date and time
        for i in range(len(location_names)) :    
            # appending the new data to the existing dataframe
            dic[location_names[i]].loc[len(dic[location_names[i]].index)] = [Date, Time, rtu[i], mw[i], mvar[i], voltage[i]]   

        msg = "Scraped at {0}\tData-points collected: {1}\tGoing to sleep for {2}sec".format(Time, counter, interval)
        # if 10 data points are collected, create the files. Don't wait for the script to end
        if counter % createFileAfter == 0 :
            msg += "\tFiles created.."
            print("\r" + msg, end="")

            for i in location_names :
                dic[i].to_csv(os.path.join("Data_" + str(start_time), i + ".csv"))
                time.sleep(0.01)

        else :
            print("\r" + msg + " "*len(msg + "\tFiles created.."), end="")   # empty the row first

        # if the current time gets more than the desired end time, end the loop
        if time.time() > end_time:
            break

        counter += 1

        # going to sleep
        time.sleep(interval)

    
    print("\n\nScaping complete\n\nData-points collected:", counter)

    print("\n" + colorama.Fore.GREEN + "Created files with the name of the format \{location_name\}.csv in a new folder named 'Data_\{start_time\}' in the current directory")

    print(colorama.Style.RESET_ALL)
    
    # creating files at the end
    for i in tqdm.tqdm(location_names) :
        dic[i].to_csv(os.path.join("Data_" + start_time, i + ".csv"))
        time.sleep(0.01)

    _ = input("Press enter to exit")
    # clearing the screen
    os.system("cls") if platform.system() == "Windows" else os.system("clear")
    sys.exit(0)
    

if __name__ == "__main__" :
    # installing uninstalled packages
    package_install()

    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import tqdm

    scraping()