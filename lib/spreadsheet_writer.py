import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class SpreadsheetWriter:
    """
    Googleスプレッドシートに書き込むためのクラス。
    """

    def __init__(self, json_keyfile_name, spreadsheet_name, folder_path=None):
        """
        コンストラクタ。

        :param json_keyfile_name: サービスアカウントのJSONキーファイル名
        :param spreadsheet_name: スプレッドシート名
        :param folder_path: スプレッドシートを作成するフォルダのパス
        """
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            json_keyfile_name, scope)
        self.client = gspread.authorize(self.creds)
        try:
            self.sheet = self.client.open(spreadsheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            self.sheet = self.client.create(spreadsheet_name).sheet1
        if folder_path:
            self.move_to_folder(spreadsheet_name, folder_path)

    def write(self, obj_list):
        """
        スプレッドシートにデータを書き込む。

        :param obj_list: 書き込むデータのリスト
        """
        # カラム名としてメンバ変数名を出力
        self.sheet.append_row(list(obj_list[0].keys()))
        # 各オブジェクトの値を1行のレコードとして出力
        for obj in obj_list:
            self.sheet.append_row(list(obj.values()))

    def delete(self, spreadsheet_name):
        """
        スプレッドシートを削除する。

        :param spreadsheet_name: 削除するスプレッドシート名
        """
        drive_service = build('drive', 'v3', credentials=self.creds)
        response = drive_service.files().list(q=f"name='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)').execute()
        for file in response.get('files', []):
            try:
                drive_service.files().delete(fileId=file.get('id')).execute()
            except HttpError as error:
                print(f'An error occurred: {error}')

    def clear_and_write(self, obj_list):
        """
        スプレッドシートの内容をクリアしてからデータを書き込む。

        :param obj_list: 書き込むデータのリスト

        使用例:
        writer = SpreadsheetWriter('client_secret.json', 'your_spreadsheet_name', '/FolderA/FolderB')
        data = [
            {'name': 'Alice', 'age': 20, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 30, 'city': 'Chicago'},
        ]
        writer.clear_and_write(data)
        """
        # スプレッドシートの内容をクリア
        self.sheet.clear()
        # データを書き込む
        self.write(obj_list)

    def move_to_folder(self, spreadsheet_name, folder_path):
        drive_service = build('drive', 'v3', credentials=self.creds)
        response = drive_service.files().list(q=f"name='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)').execute()
        for file in response.get('files', []):
            file_id = file.get('id')
            # Get the folder ID
            folder_id = self.get_folder_id(folder_path)
            # Move the file to the folder
            file = drive_service.files().get(fileId=file_id,
                                             fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            file = drive_service.files().update(fileId=file_id,
                                                addParents=folder_id,
                                                removeParents=previous_parents,
                                                fields='id, parents').execute()

    def get_folder_id(self, folder_path):
        drive_service = build('drive', 'v3', credentials=self.creds)
        folders = folder_path.strip("/").split("/")
        folder_id = 'root'
        for folder in folders:
            response = drive_service.files().list(q=f"name='{folder}' and mimeType='application/vnd.google-apps.folder' and '{folder_id}' in parents",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)').execute()
            if response.get('files'):
                folder_id = response.get('files')[0].get('id')
            else:
                file_metadata = {
                    'name': folder,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [folder_id]
                }
                file = drive_service.files().create(body=file_metadata,
                                                    fields='id').execute()
                folder_id = file.get('id')
        return folder_id
