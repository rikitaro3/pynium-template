import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetWriter:
    def __init__(self, json_keyfile_name, spreadsheet_name):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile_name, scope)
        client = gspread.authorize(self.creds)
        self.sheet = client.open(spreadsheet_name).sheet1

    def write(self, obj_list):
        # カラム名としてメンバ変数名を出力
        self.sheet.append_row(list(obj_list[0].keys()))
        # 各オブジェクトの値を1行のレコードとして出力
        for obj in obj_list:
            self.sheet.append_row(list(obj.values()))

    def delete(self, spreadsheet_name):
        drive_service = build('drive', 'v3', credentials=self.creds)
        response = drive_service.files().list(q=f"name='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)').execute()
        for file in response.get('files', []):
            try:
                drive_service.files().delete(fileId=file.get('id')).execute()
            except HttpError as error:
                print(f'An error occurred: {error}')
