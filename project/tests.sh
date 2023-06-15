echo "Step 1 - Run down the Pipeline so we have the current state"
python ../data/pipeline_amse.py
echo "Answer: Run down finished"
echo "Step 2 - Now perform the tests"
python pipeline_test.py
echo "Answer: Everything seems fine if there is no error code"