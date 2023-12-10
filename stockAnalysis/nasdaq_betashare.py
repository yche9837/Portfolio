import nasdaqdatalink
nasdaqdatalink.read_key(filename="/data/.corporatenasdaqdatalinkapikey")
data = nasdaqdatalink.get('NSE/')