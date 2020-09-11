# Word Document Parser
This small script is able to parse a word document and perform the following:
- Extract text given certain titles (keywords)
- save founded images into a folder
- Save raw extracted text
- Save json of text with founded keywords
- Save a json with all the parsed documents

## Word document format
The word should have the following pattern:

<b>\n\n\n\n\n\n</b> (all new line characters will be removed execpt before the title)
<br>
<b>-Keyword-</b> there could also be some other text <b>\n</b> <br>
<b>-content-</b> until a couple of new lines
<br>
