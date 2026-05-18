[Setup]
AppName=CRM Atendimento
AppVersion=1.0
DefaultDirName={localappdata}\CRM Atendimento
DefaultGroupName=CRM Atendimento
OutputDir=.
OutputBaseFilename=CRM Atendimento Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "CRM Atendimento.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CRM Atendimento"; Filename: "{app}\CRM Atendimento.exe"
Name: "{commondesktop}\CRM Atendimento"; Filename: "{app}\CRM Atendimento.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\CRM Atendimento.exe"; Description: "Abrir CRM Atendimento"; Flags: nowait postinstall skipifsilent