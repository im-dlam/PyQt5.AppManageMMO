cookie = 'cookie_value'  # Thay bằng giá trị thực tế
user_agent = 'user_agent_value'  # Thay bằng giá trị thực tế
av_value = 'av_value'  # Thay bằng giá trị thực tế
user_id = 'user_id_value'  # Thay bằng giá trị thực tế
fb_dtsg = 'fb_dtsg_value'  # Thay bằng giá trị thực tế

script = f"""
var headers = {{
    'accept': '*/*',
    'accept-language': 'en-US;',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '{cookie}',
    'dnt': '1',
    'origin': 'https://www.facebook.com',
    'referer': 'https://www.facebook.com',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': '{user_agent}',
    'x-fb-lsd': 'UEIdUKYqlMER2LxiAXtnJt'
}};

var dataString = 'av={av_value}&__aaid=0&__user={user_id}&__a=1&__req=15&__hs=19992.HYP%3Acomet_plat_default_pkg.2.1..2.1&dpr=1&__ccg=EXCELLENT&__rev=1016820347&__s=3tkocp%3Afj77or%3A4im4cc&__hsi=7418865971727892589&__dyn=7AzHK4HwBgDx-5Q1hyoyEqxd4Ag5S3G2O5U4e2C3-4UKewSAx-bwNw9G2Saxa0DU6u3y4o27wxg3Qwb-q7oc81xoswMwto88422y11wBz822weS4oaEnxO0Bo4O2-2l2UtwxwhU31w9O1lwlE-U2exi4UaEW4UmwsoqBwJK14xm1HzEjUlwhEe88o4qum7-2K0-obXCwLyESE2KwkQ0z8c84u2ubwHwNxe6Uak2-1vwxyo6O1FwgUjwOwWwjHDzUiwRK6E4-mEbUaU&__csr=iNI4keNk8fdkuBRsL7czFvdWblRQSysTFqtRnilaQOKAl5G9KqECHCFUDAjhqgzBogJuuKCaAjGcBzbKVFbALIx4cGaiABBBAz8GcLBQ4agFa5pFFUlVF8C9zF9uuaV-bzqGcK5UR5zoqyAbxFeWyokDCHDG5euV8OqVem9gVCjzEhDxuEGfyd7zoy4FEC26mXwDxGfG59-fUB1y6UF2oghUXGmAGxiqfAKUGeFGfyUWewFw8C6oGeKq4U4WawyyEOmuES9gyexG8yEb8G3iUKElwQUS2G4U-54eG8wJG5EdEc81Y80Pq0hOpa2fw2lE1n9FEbE5G0ZpoNyU4WqUkzU6m0oqbwSwhHiggximm0C8dU3RxK2aew1jm1dw3mO01hC0g9yAEKzo6e1-gnxna0Y80riw76wQw0kcax91kn402PU3pw3cU0ggg0WS440MFErw2i80B61Zw0xkx20u2fwvE0Gy11oS2p0Fzy01eVwi812o1H82Kw14Wu0j-0QE720lP8IU1e80N60478gw9h38apFEwxu5E0ZK0xm09QwMw2JE9o6d060w5mwCUa4pjwb-065E0mMy8Gp01eS4EZ1l0Fzy04jw2pogwf60-41ewuu4o2Gw&__comet_req=1&fb_dtsg={fb_dtsg}&jazoest=25479&lsd=UEIdUKYqlMER2LxiAXtnJt&__spin_r=1016820347&__spin_b=trunk&__spin_t=1727339339&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=useCometLocaleSelectorLanguageChangeMutation&variables=%7B%22locale%22%3A%22en_US%22%2C%22referrer%22%3A%22WWW_COMET_NAVBAR%22%2C%22fallback_locale%22%3Anull%7D&server_timestamps=true&doc_id=6451777188273168';

fetch('https://www.facebook.com/api/graphql/', {{
    method: 'POST',
    headers: headers,
    body: dataString,
    credentials: 'include' // Important for using cookies in the request
}})
    .then(response => response.text())
    .then(body => console.log(body))
    .catch(error => console.error(error));
"""

print(script)