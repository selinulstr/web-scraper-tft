from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas


chrome_driver_path = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path)


driver.get("https://www.metatft.com/comps")
comps = driver.find_elements(By.CLASS_NAME, "CompRow")[:10]
stats = [stat.text for stat in driver.find_elements(By.CLASS_NAME, "Stat_Number") if not stat.text == ""]
stats_by_comp = [stats[x:x+3] for x in range(0, len(stats), 3)][:10]
avg_place = [stat[0] for stat in stats_by_comp]
pick_rate = [stat[1] for stat in stats_by_comp]
win_rate = [stat[2] for stat in stats_by_comp]
comp_names = [comp.find_element(By.CLASS_NAME, "Comp_Title").text for comp in comps]
all_comp_champs = [comp.text for comp in driver.find_elements(By.CSS_SELECTOR, ".CompRow .UnitNames")]
comp_champs = [all_comp_champs[x:x+8] for x in range(0, len(all_comp_champs), 8)][:10]

d = {comp_name: {"Champions": comp_champ, "Avg Place": avg, "Pick Rate": pick, "Win Rate": win}
     for comp_name, comp_champ, avg, pick, win in zip(comp_names, comp_champs, avg_place, pick_rate, win_rate)}


data = pandas.DataFrame.from_dict(d, orient="index")
data.to_csv("comps.csv")
print(data)
driver.close()