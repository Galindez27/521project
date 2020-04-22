from pathlib import Path
import cookieLib

pathString = "/mnt/c/Users/jdgal/AppData/Roaming/Mozilla/Firefox/Profiles/6dj2sl01.default-release/cookies.sqlite"

if __name__=="__main__":
    pathToCookies = Path(pathString)
    x = cookieLib.cookiesFromJar(pathToCookies)
    print("Cookies in cookie jar file:", len(x), sep="\t")
