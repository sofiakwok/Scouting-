# Run from command line as:
# python fetch_event_schedule.py <match_url> <event_name>
# URLs should come from http://frc-events.usfirst.org/...
# example: "http://frc-events.usfirst.org/2016/MILAK/qualifications"

import bs4, json, sys, os
if sys.version[0] == '2':
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

class FetchError(Exception):
    pass

def fetch(source, filename):
    try:
        if '\\' in filename:
            raise FetchError("Illegal character in filename: \\")

        save_path = os.path.join('match_schedules',filename+'.json')
        if os.path.exists(save_path):
            raise FetchError("A file with that name already exists")
        if not filename:
            raise FetchError("A file name must be provided")

        if source.startswith('http'):
            try:
                src = urlopen(source).read()
            except:
                raise FetchError("Invalid URL")
        else:
            try:
                src = open(source).read()
            except IOError:
                raise FetchError("Unable to load from file: "+source)
        b = bs4.BeautifulSoup(src,'html.parser')
        rows = b.find_all('tr', class_='hidden-xs')

        data = {}
        for i, r in enumerate(rows):
            match_id = i + 1
            data[match_id] = {}
            for j, td in enumerate(r.find_all('td', class_='danger')):
                data[match_id]['Red ' + str(j + 1)] = int(td.text)
            for j, td in enumerate(r.find_all('td', class_='info')):
                data[match_id]['Blue ' + str(j + 1)] = int(td.text)

        if data == {}:
            raise FetchError("No schedule data found on this URL. Check that it is in the format 'http://frc-events.usfirst.org/.../qualifications'")
        try:
            with open(save_path, 'w') as f:
                f.write(json.dumps(data))
        except OSError:
            raise FetchError("Invalid filename")
    except FetchError as e:
        return str(e), False
    except Exception as e:
        return "An unknown error occurred: [" + type(e).__name__ + "] " + str(e), False
    else:
        return "Success! Schedule saved to: "+save_path, True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Requires 2 command line arguments (schedule url, event name): %i given" %(len(sys.argv)-1))
        sys.exit()
    print(fetch(sys.argv[1], sys.argv[2])[0])
