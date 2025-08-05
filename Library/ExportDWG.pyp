<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>allplan-cz\ExportDWG.py</Name>
        <Title>Batch DWG export</Title>
		<TextId>1001</TextId>
        <Version>0.1.0</Version>
        <Interactor>True</Interactor>
        <ReadLastInput>True</ReadLastInput>
    </Script>
    
    <Page>
        <Name>Export DWG</Name>
        <Text>Export DWG</Text>


		<Parameter>
			<Name>ConfigFile</Name>
			<Text>Config file (*.nth)</Text>
			<TextId>1002</TextId>
			<Value></Value>
			<ValueType>String</ValueType>
			<ValueDialog>OpenFileDialog</ValueDialog>
			<FileFilter>Konfigurační soubor(*.nth)|*.nth</FileFilter>
			<FileExtension>nth</FileExtension>
			<DefaultDirectories>etc|STD</DefaultDirectories>
		</Parameter>

		<Parameter>
			<Name>DwgDrawingFilePath</Name>
			<Text>Path for export</Text>
			<TextId>1003</TextId>
			<Value>C:\Output\</Value>
			<ValueType>String</ValueType>
		</Parameter>

		<Parameter>
		<Name>directory_input</Name>
		<Text>Folder with file selection favourites in "BIM" dir</Text>
		<TextId>1004</TextId>
		<Value>Rematrice\</Value>
		<ValueType>String</ValueType>
		</Parameter>

		<Parameter>
			<Name>DrawingFileButton1</Name>
			<Text>Export DWG</Text>
			<TextId>1005</TextId>
			<ValueType>Row</ValueType>

			<Parameter>
				<Name>DrawingButton1</Name>
				<Text>Run</Text>
				<TextId>1006</TextId>
				<EventId>1001</EventId>
				<ValueType>Button</ValueType>
			</Parameter>
		</Parameter>


    </Page>


</Element>
