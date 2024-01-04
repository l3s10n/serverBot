import requests, re, threading

def initOperator(cmdhost, cmduser, cmdpassword, cmdTemperatureLimit, cmdPowerLimit):
    global host, user, password, temperatureLimit, powerLimit
    host = cmdhost
    user = cmduser
    password = cmdpassword
    temperatureLimit = cmdTemperatureLimit
    powerLimit = cmdPowerLimit

def dealSSL():
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

def login():
    global host, session, ST1, ST2, user, password

    session = requests.Session()

    headers = {
        'Origin': 'https://{host}'.format(host=host),
        'Referer': 'https://{host}/login.html'.format(host=host),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
    }

    data = {
        'user': user,
        'password': password
    }

    response = session.post('https://{host}/data/login'.format(host=host), headers=headers, data=data, verify=False)
    if "ST1=" in response.text and "ST2=" in response.text:
        match = re.search(r"ST1=([^,]+),ST2=([^<]+)", response.text)
        ST1, ST2 = match.groups()

def logout():
    global host, session

    headers = {
        'Referer': 'https://{host}/globalnav.html?ran='.format(host=host),
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
    }

    session.get('https://{host}/data/logout'.format(host=host), headers=headers, verify=False)

def isPowerUp():
    global host, session, ST1, ST2
    
    headers = {
        'Origin': 'https://192.168.1.151',
        'Referer': 'https://192.168.1.151/powercontrol.html?cat=C03&tab=T08&id=P18',
        'ST2': ST2,
    }

    params = {
        'get': 'pwState',
    }

    response = session.post('https://192.168.1.151/data', params=params, headers=headers, verify=False)
    if "<pwState>" in response.text and "</pwState>" in response.text:
        match = re.search(r"<pwState>(\d*)</pwState>", response.text)
        isPowerUp = True if '1' in match.groups()[0] else False
        return isPowerUp
    else:
        return None

def getPowerMonitorData():
    global host, session, ST1, ST2

    cookies = {
        'sysidledicon': 'ledIcon%20grayLed',
        '-http-session-': '::http.session::edf9b779d7d162c62cf3bfa97134bfbc',
        'tokenvalue': 'f72d8480bedbbff88c8c8cc23c934b29',
    }

    headers = {
        'Origin': 'https://{host}'.format(host=host),
        'Referer': 'https://{host}/powermonitor.html?cat=&tab=&id='.format(host=host),
        'ST2': ST2,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58'
    }

    response = session.post(
        'https://{host}/data?get=powermonitordata'.format(host=host),
        cookies=cookies,
        headers=headers,
        verify=False,
    )

    if "<reading>" in response.text and "</reading>" in response.text:
        match = re.search(r"<reading>(\d*)</reading>", response.text)
        power = int(match.groups()[0])
        return power
    else:
        return None

def getCPUandIOandMEMUsage():
    global host

    headers = {
        'Referer': 'https://{host}/cemgui/hardware_overview.html?cat=&tab=&id='.format(host=host),
        'ST2': ST2,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'X-Prototype-Version': '1.6.1',
        'X-Requested-With': 'XMLHttpRequest',
        'X_SYSMGMT_OPTIMIZE': 'true',
        'idracAutoRefresh': '1',
    }

    response = session.get(
        'https://{host}/sysmgmt/2013/server/sensor/performance/outofband'.format(host=host),
        headers=headers,
        verify=False,
    )

    try:
        jsonData = response.json()
        CPUUsage = jsonData['UsageInfo']['iDRAC.Embedded.1#SystemBoardCPUUsage']['current_reading']
        IOUsage = jsonData['UsageInfo']['iDRAC.Embedded.1#SystemBoardIOUsage']['current_reading']
        MEMUsage = jsonData['UsageInfo']['iDRAC.Embedded.1#SystemBoardMEMUsage']['current_reading']
        return (CPUUsage, IOUsage, MEMUsage)
    except:
        return (None, None, None)

def getTemperature():
    global host

    headers = {
        'Referer': 'https://{host}/cemgui/hardware_overview.html?cat=&tab=&id='.format(host=host),
        'ST2': ST2,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'X-Prototype-Version': '1.6.1',
        'X-Requested-With': 'XMLHttpRequest',
        'X_SYSMGMT_OPTIMIZE': 'true',
        'idracAutoRefresh': '1',
    }

    response = session.get(
        'https://{host}/sysmgmt/2012/server/temperature'.format(host=host),
        headers=headers,
        verify=False,
    )

    try:
        jsonData = response.json()
        CPU1Temp = int(jsonData['Temperatures']['iDRAC.Embedded.1#CPU1Temp']['reading'])
        CPU2Temp = int(jsonData['Temperatures']['iDRAC.Embedded.1#CPU2Temp']['reading'])
        systemBoardExhaustTemp = int(jsonData['Temperatures']['iDRAC.Embedded.1#SystemBoardExhaustTemp']['reading'])
        systemBoardInletTemp = int(jsonData['Temperatures']['iDRAC.Embedded.1#SystemBoardInletTemp']['reading'])
        return (CPU1Temp, CPU2Temp, systemBoardExhaustTemp, systemBoardInletTemp)
    except:
        return (None, None, None, None)

def prettyPrint(power, CPUUsage, IOUsage, MEMUsage, CPU1Temp, CPU2Temp, systemBoardExhaustTemp, systemBoardInletTemp):
    prettyTemplate = """
Power: {power}W
CPU Usage: {CPUUsage}%
IO Usage: {IOUsage}%
MEM Usage: {MEMUsage}%
CPU1Temp: {CPU1Temp}℃
CPU2Temp: {CPU2Temp}℃
systemBoardExhaustTemp: {systemBoardExhaustTemp}℃
systemBoardInletTemp: {systemBoardInletTemp}℃
""".format(power=power, CPUUsage=CPUUsage, IOUsage=IOUsage, MEMUsage=MEMUsage, CPU1Temp=CPU1Temp, CPU2Temp=CPU2Temp, systemBoardExhaustTemp=systemBoardExhaustTemp, systemBoardInletTemp=systemBoardInletTemp).strip()
    return prettyTemplate

def RequestShutDownServer():
    global session, ST2

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://192.168.1.151',
        'Referer': 'https://192.168.1.151/sysSummaryData.html',
        'ST2': ST2,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    session.post('https://192.168.1.151/data?set=pwState:0', headers=headers, verify=False)

def RequestStartUpServer():
    global session, ST2

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://192.168.1.151',
        'Referer': 'https://192.168.1.151/sysSummaryData.html',
        'ST2': ST2,
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    session.post('https://192.168.1.151/data?set=pwState:1', headers=headers, verify=False)

def getInfoMessage():
    dealSSL()
    login()
    isPowerUpRes = isPowerUp()
    if isPowerUpRes == True:
        power = getPowerMonitorData() if getPowerMonitorData() != None else 'NA (set by serverBot)'
        power = "NA (set by serverBot)" if power == None else power

        CPUUsage, IOUsage, MEMUsage = getCPUandIOandMEMUsage()
        CPUUsage = "NA (set by serverBot)" if CPUUsage == None else CPUUsage
        IOUsage = "NA (set by serverBot)" if IOUsage == None else IOUsage
        MEMUsage = "NA (set by serverBot)" if MEMUsage == None else MEMUsage

        CPU1Temp, CPU2Temp, systemBoardExhaustTemp, systemBoardInletTemp = getTemperature()
        CPU1Temp = "NA (set by serverBot)" if CPU1Temp == None else CPU1Temp
        CPU2Temp = "NA (set by serverBot)" if CPU2Temp == None else CPU2Temp
        systemBoardExhaustTemp = "NA (set by serverBot)" if systemBoardExhaustTemp == None else systemBoardExhaustTemp
        systemBoardInletTemp = "NA (set by serverBot)" if systemBoardInletTemp == None else systemBoardInletTemp
        
        message = prettyPrint(power, CPUUsage, IOUsage, MEMUsage, CPU1Temp, CPU2Temp, systemBoardExhaustTemp, systemBoardInletTemp)
    elif isPowerUpRes == False:
        message = "Server is shutdown."
    else:
        message = "Get isPowerUp Error."

    logout_thread = threading.Thread(target=logout)
    logout_thread.start()

    return message

def shutDownServer():
    dealSSL()
    login()
    RequestShutDownServer()

    logout_thread = threading.Thread(target=logout)
    logout_thread.start()

def startUpServer():
    dealSSL()
    login()
    RequestStartUpServer()

    logout_thread = threading.Thread(target=logout)
    logout_thread.start()

def checkServerWarning():
    global temperatureLimit, powerLimit
    
    dealSSL()
    login()
    status = False
    message = ""
    isPowerUpRes = isPowerUp()
    if isPowerUpRes == True:
        CPU1Temp, CPU2Temp, systemBoardExhaustTemp, systemBoardInletTemp = getTemperature()
        power = getPowerMonitorData()
        
        if CPU1Temp == None:
            status = True
            message = message + "TEMPRATURE WARNING: CAN NOT GET TEMPERATURE INFO"
        elif CPU1Temp > temperatureLimit or CPU2Temp > temperatureLimit or systemBoardExhaustTemp > temperatureLimit or systemBoardInletTemp > temperatureLimit:
            status = True
            message = message + "TEMPRATURE WARNING: CPU1Temp {CPU1Temp}℃  CPU2Temp {CPU2Temp}℃  SystemBoardExhaustTemp {systemBoardExhaustTemp}℃  SystemBoardInletTemp {systemBoardInletTemp}℃".format(CPU1Temp=CPU1Temp, CPU2Temp=CPU2Temp, systemBoardExhaustTemp=systemBoardExhaustTemp, systemBoardInletTemp=systemBoardInletTemp)

        if power == None:
            status = True
            message = "POWER WARNING: CAN NOT GET POWER STATUS" if message == "" else message + "\nPOWER WARNING: CAN NOT GET POWER STATUS"
        elif power > powerLimit:
            status = True
            message = "POWER WARNING: POWER {power}W" if message == "" else message + "\nPOWER WARNING: POWER {power}W".format(power=power)
        
    elif isPowerUpRes == None:
        status = True
        message = "ISPOWERUP WARNING: CAN NOT GET ISPOWERUP STATUS"

    logout_thread = threading.Thread(target=logout)
    logout_thread.start()
    
    return status, message