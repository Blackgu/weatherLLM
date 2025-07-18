import pandas as pd

class Division:
    def __init__(self, name, adcode, citycode):
        self.name = name            # 地区名称
        self.adcode = adcode        # 地区编码
        self.citycode = citycode    # 城市编码

    def __repr__(self):
        return f"Division(name={self.name}, adcode={self.adcode}, citycode={self.citycode})"

def init_city_codes(file_path: str) -> dict[str: Division]:
    df = pd.read_excel(file_path)

    city_group = df.groupby('citycode')
    coverted_city_group = {}
    for code, group in city_group:
        city_name = group.iloc[0]['中文名']
        group.loc[group.index[1:], '中文名'] = city_name + '-' + group.loc[group.index[1:], '中文名']
        coverted_city_group[code] = group.to_dict(orient='records')

    result = {}
    for code, records in coverted_city_group.items():
        for record in records:
            result[record['中文名']] = Division(record['中文名'], record['adcode'], record['citycode'])

    return result