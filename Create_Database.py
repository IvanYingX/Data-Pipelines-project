from bs4 import BeautifulSoup
from Extract.Extract_Data import * #accept_cookies, extract_rounds, extract_standing, extract_results

list_jornadas = ['Position', 'Team', 'Points', 'Jornada', 'Ganados', 'Empatados', 'Perdidos',
                 'Goles_a_favor', 'Goles_en_contra', 'Año', 'Liga'] 
list_partidos = ['Equipo_Local', 'Equipo_Visitante', 'Resultado', 'Fecha', 'Año_partido',
                'Jornada_partido', 'Liga_partido']

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
        for round in range(initial_round, num_rounds + 1):
            print(f'\tAccesing data from round  {round} of year {year}') 
            driver = accept_cookies(year, league, round)
            standings = extract_standing(driver)
            results = extract_results(driver)

            if standings == None or results == None: 
                print(f'------------------------------------------------------')
                print(f'!!!\tRound {round} does not exist on year {year}\t!!!')
                print(f'------------------------------------------------------')
                driver.quit()
                continue