# CoolForum database migration scripts
# Feed it JSON
import os
import re
import json
import django
from html.parser import HTMLParser
from datetime import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naxos.settings.dev")
django.setup()

from naxos.settings.base import here
from user.models import ForumUser
from forum.models import Category, Thread, Post
from forum.util import keygen


# PLEASE NOTE THAT CATEGORIES HAVE TO BE CREATED FIRST AND UPDATE 'cat_map'
# ACCORDINGLY


def fix_json(f):
    """Fixes phpmyadmin json exports"""

    def double_quote(match_obj):
        quote = match_obj.group(2)
        return match_obj.group(1) + "\"" + quote + "\","

    print('Repairing JSON')
    f = open(f)
    lines = f.readlines()
    # Remove comments at the top (illegal in json)
    while lines[0][0] != '[':
        lines.pop(0)
    s = ''.join(lines)
    s = s.replace('<br />', '\\n')  # User proper new line character
    s = s.replace('\\\'', '\'')  # Remove illegal escapes for squotes
    s = re.sub(r'[^\x20-\x7e]', '', s)  # remove hex characters
    # add double quotes where missing
    s = re.sub(r'("msg": )([^"]*),', double_quote, s)
    s = re.sub(r'("usercitation": )([^"]*),', double_quote, s)
    # let's roll
    print("All right, good to go.")
    return s


def convert_username(name):
    """Convert the username to a naxos-db compliant format"""
    return HTMLParser().unescape(name.replace(' ', '_'))[:30]


def import_users(f):
    """Import users from a CoolForum json db extract"""
    users = json.loads(fix_json(f))
    new_users = {}

    for i, user in enumerate(users):
        user['login'] = convert_username(user['login'])
        m = ForumUser.objects.filter(pk=user['userid']).first()
        if m: m.delete()  # delete the user if it already exists
        password = keygen()  # gen password
        new_users[user['login']] = password
        u = ForumUser.objects.create(
            pk=int(user['userid']),
            username=user['login'],
            email=HTMLParser().unescape(user['usermail']),
            date_joined=datetime.fromtimestamp(user['registerdate']),
            logo="logo/{:s}".format(user['userlogo']),
            quote=HTMLParser().unescape(str(user['usercitation'])),
            website=HTMLParser().unescape(str(user['usersite'])),
        )
        print("Creating users... {:d}/{:d}: {:s}{:s}".format(
            i+1, len(users), u.username, " "*(30-len(u.username))), end="\r")
        u.set_password(password)
        u.save()
    print()
    f = open('new_users.json', 'w')
    json.dump(new_users, f)
    f.close()
    # TODO: send email with new password


def import_threads(f):
    cat_map = {1:1, 2:2, 3:3, 4:4, 5:6, 6:7, 7:5}  # mapping categories
    threads = json.loads(fix_json(f))
    for i, thread in enumerate(threads):
        m = Thread.objects.filter(pk=thread['idtopic']).first()
        if m: m.delete()  # delete the thread if it already exists
        t = Thread.objects.create(
            pk=int(thread['idtopic']),
            category=Category.objects.get(pk=cat_map[thread['idforum']]),
            title=HTMLParser().unescape(str(thread['sujet']))[:80],
            author=ForumUser.objects.get(pk=thread['idmembre']),
            icon=str(thread['icone'])+'.gif',
            viewCount=int(thread['nbvues']),
        )
        print("Creating threads... {:d}/{:d}".format(
            i+1, len(threads)), end="\r")
    print()

def import_posts(f):
    posts = json.loads(fix_json(f))
    users = {}
    print('Loading users...')
    for user in ForumUser.objects.all():
        users[user.pk] = user
    print('done')
    threads = {}
    print('Loading threads...')
    for thread in Thread.objects.all():
        threads[thread.pk] = thread
    print('done')
    post_counter = {}
    for i, post in enumerate(posts):
        t = threads.get(post['parent'])
        if not t: continue  # pass if thread does not exist
        # increment category post counter
        post_counter[t.category] = post_counter.get(t.category, 0) + 1
        # m = Post.objects.filter(pk=post['idpost']).first()
        # if m: continue  # skip if post already exists
        p = Post.objects.create(
            pk=int(post['idpost']),
            thread=t,
            author=users.get(post['idmembre']),
            created=datetime.fromtimestamp(post['date']),
            content_plain=str(post['msg']),
        )   
        print("Creating {:d}/{:d}".format(i+1, len(posts)), end="\r")
        # if i == 1000:
        #     return
    threads = Thread.objects.all()
    for i, thread in enumerate(threads):
        print('Updating thread modified datetime: {:d}/{:d}'.format(
            i+1, len(threads)), end="\r")
        thread.modified = thread.posts.latest.modified
        thread.save()
    for key, value in post_counter:
        print('Updating post counter')
        c = Category.objects.get(pk=key)
        c.postCount = value
        c.save()


# TODO: add count posts
# TODO: override thread.modified with last topic datetime

# import_users(here('..', '..', '..', 'util', 'data', 'CF_user.json'))
# import_threads(here('..', '..', '..', 'util', 'data', 'CF_topics.json'))
import_posts(here('..', '..', '..', 'util', 'data', 'CF_posts.json'))
