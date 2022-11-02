def get_countries():

    countries = {}

    with open('helpers/countries/raw.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_strip = line.strip('\n')
            line_split = line_strip.split(':')
            country_code = line_split[0]
            country_name = line_split[1]
            countries[country_code] = country_name

    return countries
