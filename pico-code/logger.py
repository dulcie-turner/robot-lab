import wifi

class Logger:
    # missing the mac address for number 12?
    macAddresses = [
        "28cdc105c480", "28cdc105c472",
        "28cdc105c477", "28cdc105c475",
        "28cdc105c47c", "28cdc105c47e",
        "28cdc105c47a", "28cdc105c47d",
        "28cdc105c483", "28cdc105c478",
        "28cdc105c482"
    ]

    passwords = [
        "jkQYAJk7", "frrXvRk4",
        "YtUXaagd", "MSYwxASv",
        "MYTHgqus", "KWnrfR6z",
        "VJmtsx5w", "XFQbiwmN​",
        "FFkdwYMj", "yKjkMeND",
        "saPzGfMR"
    ]

    def __init__(self, number):
        self.number = number
        self.macAddress = self.macAddresses[number - 1]
        self.password = self.passwords[number - 1]

    def isCurrent(self):
        # is this logger the current one connected?
        detectedAddress = ''.join([f'{i:02x}' for i in wifi.radio.mac_address])
        return detectedAddress == self.macAddress

def getLoggers():
    for i in range(1, 12):
        testLogger = Logger(i)
        if testLogger.isCurrent():
            return testLogger
    print("Logger not found!")
    return None