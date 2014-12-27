# coding=utf8
import sys
from browser import Browser

class BankLeumiAPI(object):
    def __init__(self, progress=lambda: None):
        self.browser = Browser(progress=progress)

    def login(self, username, password):
        self.browser.get('https://hb2.bankleumi.co.il/H/Login.html')
        self.browser.form('#login').submit(uid=username, password=password)
        if not self.browser.url.endswith('/InternalSite/Validate.asp'):
            raise Exception('login error')
        self.browser.get('/eBanking/SSOLogin.aspx?SectorCheck=Override', allow_redirects=False)

    def get_statement(self, account, from_date, to_date):
        self.browser.get('/eBanking/Accounts/ExtendedActivity.aspx')
        self.browser.form().submit({
            # FIXME: use ccount, from_date, to_date parameters
            'ddlAccounts$m_ddl'      : '1',
            'ddlTransactionType'     : '001',
            'ddlTransactionPeriod'   : '004',
            'dtFromDate$textBox'     : '01/08/14',
            'dtToDate$textBox'       : '01/10/14'
        })
        table = self.browser.table('.dataTable')
        yield table.headers
        for row in table.rows:
            yield row

if __name__ == '__main__':
    from cred import get_cred
    def progress():
        sys.stderr.write('.')
    api = BankLeumiAPI(progress=progress)
    api.login(get_cred('leumi_username'), get_cred('leumi_password'))
    for line in api.get_statement(None,None,None):
        print ','.join(line)