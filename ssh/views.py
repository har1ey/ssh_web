from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.contrib import auth
from django.utils.encoding import smart_str

from ssh.models import Server, Key
from forms import SshKeyForm
from ssh_go import add_k, del_k, check_k, get_info, save_log, load, get_file
import StringIO
import re
import threading
from Queue import Queue
import time

# Create your views here.

form_key = ''
logs = {}
error_key = 'Key must be Latin alphanumeric and symbols!'
last_key = ''
total = 0
info_show = False
info_ip = ''
info = {}
ggg = []
test = ''

def page(request):
    global total

    vision = False
    vision_last = False
    ssh_key_form = SshKeyForm(initial={'ssh_key': last_key})
    args = {}

    args.update(csrf(request))
    args['servers'] = Server.objects.order_by('server_ip')
    hit = 5
    args['hit'] = hit

    total = Key.objects.count()
    if total > hit:
        args['keys'] = Key.objects.filter()[total - hit:total:-1]
    else:
        args['keys'] = Key.objects.filter()[:hit:-1]
    args['form'] = ssh_key_form
    args['username'] = auth.get_user(request).username
    args['logs'] = logs.items()

    servers = Server.objects.all()
    for server in servers:
        if server.server_select:
            vision = True
    args['vision'] = vision

    if total == 0:
        vision_last = True
    args['vision_last'] = vision_last

    args['info_show'] = info_show
    args['info_ip'] = info_ip
    args['info'] = info.items()
    args['ggg'] = ggg
    args['test'] = test

    return render_to_response('login.html', args)


def select(request, server_id):
    global last_key, form_key
    try:
        server = Server.objects.get(id=server_id)
        server.server_select = not server.server_select
        server.save()
        last_key = form_key
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')


def get_info(request, key_id):
    global last_key, form_key
    last_key = info[int(key_id)]
    form_key = last_key

    return redirect('/')


def all(request):
    global info_show, info, info_ip, logs, last_key, form_key
    count = 0

    if request.POST:

        servers = Server.objects.all()

        if request.POST.get('info_key'):
            logs = {}

            for server in servers:
                if server.server_select:
                    count += 1
            if count == 1:
                for server in servers:
                    if server.server_select:
                        out = int(get_file(server.server_ip, server.server_login, server.server_pass))

                        if out == -10 or out == -5:
                            error(out, server.server_ip)
                        else:
                            info = load()

                            info_show = True
                            logs['Info'] = good('Get info about ' + server.server_ip)
                            info_ip = server.server_ip
            else:
                logs['Info'] = bad('Select one server.')
        else:
            if request.POST.get('all'):
                status = True
            elif request.POST.get('none'):
                status = False

            for server in servers:
                server.server_select = status
                server.save()

    return redirect('/')


def key(request):
    global logs, last_key, form_key, error_key, test
    logs = {}
    out = '/'
    check = False

    if request.POST:

        if request.POST.get('last_key'):
            out = '/last/'
        else:
            logs = {}

            form = SshKeyForm(request.POST)
            if form.is_valid():
                pag = form.save(commit=False)

                k = (StringIO.StringIO(form.data['ssh_key'])).getvalue()
                kk = k.rstrip()

                if request.POST.get('add_key'):
                    p = re.compile('^((ssh-rsa|ssh-dss|pgp-sign-rsa|pgp-sign-dss)\s[a-zA-Z0-9@=/+-.:;!_\r\n]+\s.+)')
                    select = True
                elif request.POST.get('del_key'):
                    p = re.compile('[a-zA-Z0-9@=/+-.:;!_\r\n\s]+')   # !?
                    select = False
                elif request.POST.get('check_key'):
                    out = '/check/'
                    check = True
                    p = re.compile('[a-zA-Z0-9@=/+-.:;!_\r\n\s]+')   # !?

                m = p.match(kk)

                if m:
                    form_key = m.group()

                    if not check:
                        if select:
                            out = '/add/'
                            key_action = good('add:')
                        else:
                            out = '/del/'
                            key_action = bad('del:')
                        action_id = form.save().id  # ! Attanchen
                        e = Key.objects.get(id=action_id)
                        e.key_action = key_action
                        e.save()
                    else:
                        last_key = form_key

                else:
                    logs['Error'] = bad('Enter correct syntax key ("type key comment")')
            else:
                logs['Error'] = bad(error_key)

                return redirect('/')

    return redirect(out)


def error(out, server_ip):
    global logs
    if out == -10:
        logs[server_ip] = bad('Authentication error.')
    elif out == -5:
        logs[server_ip] = bad('Timeout connect.')


def parra(mode, qu):
    global logs, last_key, info_show, info, ggg

    while True:

        server_id = qu.get()
        #ggg.append(server_id)

        server = Server.objects.get(id=server_id)

        if mode == 'check':
            out = int(check_k(server.server_ip, server.server_login, server.server_pass, form_key))

            error(out, server.server_ip)

            server = Server.objects.get(id=server_id)
            if out > 0:
                server.server_select = True
                logs[server.server_ip] = good('Key found - %s entry.' % out)
            elif out == 0:
                server.server_select = False
                logs[server.server_ip] = bad('Key not found.')
            else:
                server.server_select = False
            server.save()

        else:

            if server.server_select:
                out = int(check_k(server.server_ip, server.server_login, server.server_pass, form_key))
                error(out, server.server_ip)

                if mode == 'add':
                    if out == 0:
                        add_k(server.server_ip, server.server_login, server.server_pass, form_key)
                        logs[server.server_ip] = good('Key added.')
                        done = True
                    elif out > 0:
                        logs[server.server_ip] = bad('This key is already on the server.')
                        done = False
                elif mode == 'del':
                    if out == 0:
                        logs[server.server_ip] = bad('Rows with the same key is not found.')
                        done = False
                    elif out == 1:
                        del_k(server.server_ip, server.server_login, server.server_pass, form_key)
                        logs[server.server_ip] = good('The key is deleted.')
                        done = True
                    elif out > 1:
                        logs[server.server_ip] = bad('More rows, specify the key - %s entry.' % out)
                        done = False

            last_key = ''

        if done:
            info = {}
            info_show = False

        qu.task_done()


def action(mode):
    global logs, last_key, info_show, info

    queue = Queue()

    if mode == 'check':
        servers = Server.objects.all()
        count = Server.objects.all().count()
    else:
        servers = Server.objects.all().filter(server_select=True)
        count = Server.objects.all().filter(server_select=True).count()

    for x in range(count):
        t = threading.Thread(target=parra, args=(mode, queue,))
        #t.setDaemon(True)
        t.start()

    for server in servers:
        queue.put(server.id)

    queue.join()

    save_log(logs, form_key, mode)


def last():
    global last_key, form_key, total

    if total == 0:
        pass
    else:
        k = Key.objects.filter()[total - 1]
        last_key = k.ssh_key
        form_key = last_key


def good(key):
    out = '<span style="color: green; ">' + key + '</span>'

    return out


def bad(key):
    out = '<span style="color: red; ">' + key + '</span>'

    return out


def add_key(request):
    action('add')

    return redirect('/')


def del_key(request):
    action('del')

    return redirect('/')


def check_key(request):
    action('check')

    return redirect('/')


def last_k(request):
    last()

    return redirect('/')


def clear_info(request):
    global info, info_show
    info = {}
    info_show = False

    return redirect('/')
