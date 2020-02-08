import browsercookie
firefox_cookiejar = browsercookie.firefox()
print(len(firefox_cookiejar))
for cookie in firefox_cookiejar:
        print(cookie)
