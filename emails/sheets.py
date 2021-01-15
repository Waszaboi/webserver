import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .models import Email

def update_sheet():
    
    scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Emailek").sheet1

    emails = list(map(lambda x: x["email"], Email.objects.values()))
    for i, email in enumerate(emails):
        sheet.update_cell(i+2, 1, email)
    i = len(emails) + 2
    while sheet.cell(i, 1).value != "":
        sheet.update_cell(i, 1, "")
        i+=1