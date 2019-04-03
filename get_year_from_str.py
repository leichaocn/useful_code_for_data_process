def get_year_from_str(title):
    match = re.match(r'.*([1-3][0-9]{3})', title)
    if match is not None:
        txt_year=float(match.group(1))
        if txt_year>=1999 and txt_year<=(now_year+1):
            # print('1结果为', int(txt_year))
            return int(txt_year)
        else:
            print('数值异常，异常值为', title)
            print('设置默认值为2014')
            return int(2014)
    else:
        print('title异常，缺少year，异常值为', title)
        print('设置默认值为2014')
        return int(2014)
