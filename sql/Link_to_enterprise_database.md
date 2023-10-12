# How to link to USYD enterprise database
1. Open usyd vpn or connect to usyd network

2. Open terminal

3. cd to the directory where the zip file `isys2120_opalwebapp_template.zip` is located

4. terminal command `ssh yche9837@ucpu0.ug.cs.usyd.edu.au` where `yche9837` is your usyd unikey

5. Enter your unikey password

6. unzip the zip file `unzip isys2120_opalwebapp_template.zip`

7. open browser and go to `https://ucpu0.ug.cs.usyd.edu.au`

8. edit the config.init file to as below:
```
##############################
##     Database Details     ##
##--------------------------##
##  Enter your credentials  ##
##  to use the python code  ##
##  Make sure you have the  ##
##   UniDB schema loaded    ##
##   in the database!!!!!   ##
##############################

[DATABASE]
host = soitpw11d59.shared.sydney.edu.au
# database = y23s2i2120_kgra9230
user = y23s2i2120_yche9837 # provided by the school
# password = Cqglxy00
password = H7UednvY # this password is provided by the school
port = 5432

[DATABASELOCAL]
host = localhost
database = postgres
user = opaluser
password = opal2023
port = 5433

###############################
##      Flask Details        ##
##---------------------------##  
## Change your port for the  ##
## GUI here. You should use  ##
## 5xxx where 'xxx' are the  ## 
## last 3 digits of your SID ## 
## E.g. if your SID is:      ##
##         47003429          ##
##   Your Port should be:    ##
##             5429          ##
###############################

[FLASK]
port = 5519

```

9. Go to terminal and direct to the directory `code`

10. terminal command `chmod +x ./threetier.command` to give permission to run the script

11. terminal command `./threetier.command` to run the script

12. open browser and go to `http://ucpu0.ug.cs.usyd.edu.au:5519`