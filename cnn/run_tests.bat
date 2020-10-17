setlocal EnableDelayedExpansion
for /r %%i in (/saved_models/*.pt) do (
set x=%%i
set x=!x:~-11,8!
set resfile=!cd!/saved_models/test_res!x!.txt
if exist !resfile! (
    echo "testfile exists, skipping"
) else (
    echo "python test.py --model-time !x!"
)
)