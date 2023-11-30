import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SpreadsheetWriter:
    def __init__(self, json_keyfile_name, spreadsheet_name):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(spreadsheet_name).sheet1

    def write(self, obj_list):
        # カラム名としてメンバ変数名を出力
        self.sheet.append_row(list(obj_list[0].keys()))
        # 各オブジェクトの値を1行のレコードとして出力
        for obj in obj_list:
            self.sheet.append_row(list(obj.values()))