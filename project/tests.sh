echo "Step 1 - Run down the Pipeline so we have the current state"
python ../data/pipeline_amse.py
echo "Answer: Run down finished" #Answer shows the end, so that the user knows they reached the end (hopefully) without an error code
echo "Step 2 - Now perform the tests"
python pipeline_test.py
echo "Answer: Everything seems fine if there is no error code" #Again: Answer shows the end, so that the user knows they reached the end (hopefully) without an error code