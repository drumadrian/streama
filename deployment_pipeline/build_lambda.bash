# Create python 3 virtual environment
# python3 -m venv venv

echo -e "\n\n"
echo -e "......Building   streama lambda zip file"
echo -e "\n\n"
DEPLOYMENTBUCKETKEYPARAMETER=transcoder.zip
rm $DEPLOYMENTBUCKETKEYPARAMETER
cd venv/lib/python3.6/site-packages/
zip -r9 ../../../../function.zip .
cd ../../../../
# cp aws-elasticsearch-index-curator.py index.py
zip -g function.zip index.py
mv function.zip $DEPLOYMENTBUCKETKEYPARAMETER
