// Google Apps Script Webhook for SmartNotes
// Deploy as: Web App → Anyone with link (test mode)

function doPost(e) {
  var secret = 'YOUR_SECRET_TOKEN';  // optional security token
  var payload = JSON.parse(e.postData.contents);

  // Validate token (optional)
  if (payload.token && payload.token !== secret) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: "forbidden" })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  // Open Google Sheet by ID
  var sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getSheetByName('Sheet1');

  // Append data to sheet
  sheet.appendRow([
    new Date(),
    payload.email || "",
    payload.title || "",
    payload.content || "",
    payload.date || "",
    payload.time || ""
  ]);

  // Create Google Doc from note/task
  var doc = DocumentApp.create((payload.title || "Note") + " - " + (payload.email || ""));
  doc.getBody().appendParagraph(payload.content || "");
  doc.saveAndClose();

  // Respond to the client
  return ContentService.createTextOutput(
    JSON.stringify({ status: "ok" })
  ).setMimeType(ContentService.MimeType.JSON);
}
