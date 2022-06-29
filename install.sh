pip install azure-digitaltwins-core==1.1.0 azure-identity==1.9.0
pip install Office365-REST-Python-Client==2.2.1
pip install openpyxl==3.0.9
pip install pandas==1.4.2
az config set extension.use_dynamic_install=yes_without_prompt
az extension add --name azure-iot
echo ""
echo "Installation all done!"