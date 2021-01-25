from bs4 import BeautifulSoup
from Extract.Extract_Data import accept_cookies, extract_rounds, extract_standing, extract_results
# leagues = ['premier_league', 'primera_division', 'serie_a', 'ligue_1', 'bundesliga']
leagues = ['premier_league']
year_1 = 1990
year_2 = 1991
initial_round = 1

for league in leagues:
    for year in range(year_1, year_2 + 1):
        print(f'Accesing data from year {year} of {league}')
        driver = accept_cookies(year = year, league = league)
        num_rounds = extract_rounds(driver)
        if num_rounds == 0:
            print(f'No available data for year {year} on {league}')
            print('Skipping to the next year')
            driver.quit()
            continue
        driver.quit()
        for jornada in range(initial_round, num_rounds + 1):
            print(f'\tAccesing data from round  {jornada} of year {year}') 
            driver = accept_cookies(year, league, jornada)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            tabla_jornada = extraer_datos_jornada(soup)
            tabla_partido = extraer_datos_partido(soup)
print(num_rounds(driver))
print(standing_data(driver))
print(results_data(driver))
driver.quit()

