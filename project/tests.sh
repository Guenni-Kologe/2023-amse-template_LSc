echo ~~~~~~~ Run down the Pipeline so we have the current state ~~~~~~~~~
cd ..
python \\data\\pipeline_amse.py
echo ~~~~~~~ Run down finished ~~~~~~~~
echo ~~~~~~~ Now perform the tests ~~~~~~~~~~
python pipeline_test.py
echo ~~~~~~~ Everything seems fine if there is no error code ~~~~~~~~~~