This program is designed to translate from one language to another by words, sentences, or paragraphs. In the first and third fields, you must write the full address of the file to be translated and the full address where the file with the translations will be created, in the following format: C:/Folder/Subfolder/.../Last subfolder. The folder names must be exactly as they appear, including spaces and special characters.

In the second field, you must enter the name of the file to be translated. It must be a PDF file. The name must be exactly as it appears and may or may not include the .pdf extension. In the fourth field, you must select a file name. It must not be left blank. If a file with that name already exists in the destination folder, it will not overwrite the file and will be named File_1.extension.

Next, you must select the mode button to separate the file's content into words, sentences, or paragraphs. If the mode by words is chosen, the program will lemmatize (put the words in their base form) and eliminate repeated lemmatizations, so each word should appear only once in the created files.

Then, you must select the type of file to be created. If you choose Excel, a .xlsx file will be created with two columns: the first will have the original part and the second the translated part. If you choose Word, a .docx file will be created with the following format:

Original: Original part

Translated: Translated part

\---

Finally, you must select the language of the original file and the language to which it will be translated. They must not be the same. If you want to change or add any functionality, you must do so in the base code.

Note: Translating to words and removing proper names is not 100% reliable, so you will need to review the translation result. Translation by paragraphs may not separate them correctly. The program checks for most errors.
