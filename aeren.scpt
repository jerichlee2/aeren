do shell script "nohup /usr/local/bin/diet.command > /dev/null 2>&1 &"
do shell script "nohup /usr/local/bin/schedule.command > /dev/null 2>&1 &"
do shell script "nohup /usr/local/bin/deepwork.command > /dev/null 2>&1 &"
do shell script "nohup /usr/local/bin/books.command > /dev/null 2>&1 &"
delay 1.5
do shell script "open -g -a Terminal /usr/local/bin/aeren_touch.command"
