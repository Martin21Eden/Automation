headers = lambda **kwargs: {"Connection": "keep-alive",
                            'Accept': '*/*',
                            'sec-ch-ua-platform': 'Linux',
                            'X-Requested-With': 'XMLHttpRequest',
                            'sec-ch-ua-mobile': '?0',
                            'Sec-Fetch-Site': 'same-origin',
                            'sec-ch-ua': 'Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97',
                            'Sec-Fetch-Mode': 'cors',
                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                          'Chrome/97.0.4692.71 Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', **kwargs}

login_data = {'no_secret_phrase': '1', 'ajax-login-field': '1', 'LoginForm[mfa_checkbox]': '0'}
