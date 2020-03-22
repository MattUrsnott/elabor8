import json
import requests as req
import sys
import getopt

cat_url = 'https://cat-fact.herokuapp.com/facts'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


def get_json():
    # assume internet connectivity ok for the moment
    resp = req.get(cat_url, headers)
    if resp.status_code != 200:
        print("Error: HTTP response code = {0}".format(resp.status_code), file=sys.stderr)
        sys.exit(255)
    return json.loads(resp.content)


def make_users():
    facts = get_json()['all']
    users = dict()
    for fact in facts:
        try:
            user = fact['user']
        except KeyError:
            # empty user is possible but probably not intended so report error
            print("No user defined for fact with id: {0}".format(fact['_id']), file=sys.stderr)
            continue
        uid = user['_id']
        if uid in users:
            users[uid] = (users[uid][0] + fact['upvotes'], users[uid][1])
        else:
            first = user['name']['first']
            last = user['name']['last']
            users[uid] = (fact['upvotes'], '{0} {1}'.format(first, last))
    sorted_users = sorted(users.values(), reverse=True)
    return sorted_users


def write_file(path, reporters):
    try:
        f = open(path, "w")
    except FileNotFoundError:
        print('Bad path spec: {0}'.format(path), file=sys.stderr)
        sys.exit(255)
    f.write("user, totalVotes\n")
    for reporter in reporters:
        f.write("{0}, {1}\n".format(reporter[1], reporter[0]))
    f.close()


def main(argv):
    try:
        opt, arg = getopt.getopt(argv, "-f", [])
    except getopt.GetoptError:
        print("usage: python main.py -f <path>", file=sys.stderr)
        sys.exit(255)
    if len(opt) == 0 or len(arg) == 0 or opt[0][0] not in ["-f"]:
        print("usage: python main.py -f <path>", file=sys.stderr)
        sys.exit(255)
    reporters = make_users()
    write_file(arg[0], reporters)


main(sys.argv[1:])
