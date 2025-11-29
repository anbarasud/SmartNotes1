// Apps Script webhook example
function doPost(e) {
  var payload = JSON.parse(e.postData.contents);
  var ss = SpreadsheetApp.openById('YOUR_SHEET_ID');
  var sheet = ss.getSheetByName('Sheet1');
  sheet.appendRow([new Date(), payload.email || '', payload.title || '', payload.content || '']);
  return ContentService.createTextOutput(JSON.stringify({status:'ok'})).setMimeType(ContentService.MimeType.JSON);
}
