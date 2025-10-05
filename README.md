# DoiToScopus
## Description
Python application for correcting the wrong data extracted from the Scopus database as response to a complex request using the "https://pypi.org/project/ScopusApyJson/"ScopusApyJson" package based on the Elsevier's API.<br />

## Installation
Run the following command to get a repository clone of the main branch:
```
git clone https://github.com/TickyWill/DoiToScopus.git@main
```

## Requirements
Ensure that your environment complies with the requirements given in the following file:
<p><a href=https://github.com/TickyWill/DoiToScopus/blob/main/requirements.txt>DoiToScopus requirements file
</a></p>

## Documentation building
Run the following commands to build the sphinx documentation:
- Only in case of a previous building (creation of "docs" folder under progress)
```
docs\make.bat clean
```
- Then
```
docs\make.bat html
```

## Documentation edition
Open the following DoiToScopus sphinx-documentation html file:
>docs/docbuild/html/index.html

## Building executable
Creation of batch file and manual under progress
Either run the following batch file:
<p><a href=https://github.com/TickyWill/DoiToScopus/blob/main/DoiToScopusBuildExe.bat>DoiToScopus executable-building batch file
</a></p>
Or refer to the following manual:
<p><a href=https://github.com/TickyWill/DoiToScopus/blob/main/DoiToScopusBuildExeManual-Fr.pdf>DoiToScopus executable-building manual
</a></p>
<span style="color:red">BEWARE:</span> Some security softwares (eg. McAfee) could place the .exe file in quarantine. If so you have to manually authorized the .exe file.

## Usage example
```python
# Local imports
from dtsgui.main_page import AppMain

app = AppMain()
app.mainloop()
```

**for more details on application usage refer to the user manual:** 
Creation of user manual under progress
<p><a href=https://github.com/TickyWill/DoiToScopus/blob/main/DoiToScopusUserManual-Fr.pdf>DoiToScopus user manual
</a></p>

# Release History
- 0.0.0 first release

# Meta
	- authors: BiblioAnalysis team

Distributed under the [MIT license](https://mit-license.org/)