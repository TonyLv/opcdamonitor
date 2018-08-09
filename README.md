
# opcdamonitor
Easy OPC DA Monitor, based on OpenOPC with Zabbix integration


Install
=======

# Copie a pasta com arquivos .py para o computador local 
É recomendado renomear a pasta para c:\opcmonitor

# Instale Python 2.7
Utilize o diretório padrão c:\python27

# Instale o OpenOPC
Utilize o diretório padrão c:\OpenOPC

# Instale as bibliotecas 
Instale (ou copie para c:\python27\lib\site-packages) as libs Pyro e pywin32
pip install Pyro
pip install pywin32

# Altere PATH
Adicione o Python e as libs do OpenOPC ao PATH do sistema
PATH=...;C:\Python27\;C:\Python27\Scripts;c:\OpenOPC\bin;
Nota: Para enviar para o Zabbix é necessário incluir o zabbix_sender.exe, que vem com o agente Zabbix no path tb

# Teste
Altere o arquivo de configuração e ative as opcoes de debug e output/to_console
abra um terminal e rode python app.py dentro do diretório opcmonitor

# Adicionar serviço do windows
nssm install "Monitoramento OPC" c:\python27\python.exe c:\opcmonitor\app.py
ou 
sc create "Monitoramento OPC" binPath="C:\Python27\Python.exe --c:\opcmonitor\app.py"

# Config Zabbix
Crie no zabbix, um item trapper no host desejado. Por padrão o script também envia a qualidade, timestamp e o tempo de delay do item criado com sufixos específicos. Verifique o arquivo de configuração config.py para mais informações. 
Configure o host e a porta do zabbix e ative o parametro output/to_zabbix. Reinicie o serviço para publicar


Known Issues
============

# v0.1
Problema com o log para arquivos quando a opção output/to_file está ativada