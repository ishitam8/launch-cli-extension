python .\setup.py bdist_wheel

az extension remove -n launch

az extension add --source 'D:\VSTS\launchCLIRepo\launchCLI\dist\launch-0.1.0-py2.py3-none-any.whl' -y