from flask import Flask, jsonify, request, render_template
from flask.ext.stormpath import StormpathManager, login_required, groups_required, user
from cosgrove import db
from cosgrove.ac import crossdomain
import json


app = Flask(__name__)
sakf = 'STORMPATH_API_KEY_FILE'
akpp = '/home/jbert/.stormpath/apiKey.properties'
apps = 'e8412959b1ae2279a15095a81f86fa5c'
app.config['SECRET_KEY'] = "2UXM8ESTB1MVPEO8DOBFDVMBE"
app.config[sakf] = akpp
app.config['STORMPATH_APPLICATION'] = 'erincosgrove.com'
app.config['STORMPATH_REDIRECT_URL'] = '/welcome'

app.config['STORMPATH_ENABLE_FACEBOOK'] = True
app.config['STORMPATH_SOCIAL'] = {
    'FACEBOOK': {
        'app_id': "1455773838012675",
        'app_secret': apps
    }
}


SPM = StormpathManager(app)

def separate_links(links):
    '''
    Jinja2 custom filter for splitting url strings
    '''
    return links.split(',')


@app.route('/welcome', methods=['GET'])
@login_required
def welcome():
    '''
     Login redirect page
    '''
    try:
        for g in user.groups:
            print g

        return jsonify({'status': 'logged in'})
    except Exception as e:
        print e.message
        return 500


@app.route('/<dep>', methods=['GET'])
@crossdomain(origin='*')
def goto(dep):
    '''
     Retrieve projects, products, and slides

    Anyone can access this, even guests
    '''
    try:
        fn = 'report_%s' % dep
        res = getattr(db, fn)()
        return render_template('%s.html' % dep, body=res)
    except Exception as e:
        print e.message
        return 500


@app.route('/admin/<dep>', methods=['POST', 'PUT', 'DELETE'])
@groups_required(['admin'])
@crossdomain(origin='*')
def admin_goto(dep):
    '''
     admin_goto is the routing function that creates, reports, updates,
     and deletes based on the request type

    *only admins can access this route

       dep -> department, either a product, project, or slide
         \_POST   -> create a product/project/slide
         \_PUT    -> update a product/project/slide
         \_DELETE -> delete a product/project/slide

    '''
    try:
        r = dir(db)
        fn_prefix = {'POST':   'create',
                     'PUT':    'update',
                     'DELETE': 'delete'}


        form = json.loads(request.data)
        '''
        all db functions are named in the following
        conventions:
            verb_noun()
            verb = create/report/update/delete
            noun = product/project/slide

        fn_prefix dict obtains the verb using the
        request method as a key. the noun is given
        in the url.
        '''
        met = fn_prefix[request.method]

        fn = '%s_%s' % (met, dep)
        req = [x for x in r if fn in x][0]
        getattr(db, req)(**form)

        ret = {'status': '%s %sd' % (dep, met)}
        return jsonify(ret)

    except Exception as e:
        print {'error': e.message}
        return 500


if __name__ == '__main__':
    app.jinja_env.filters['separate_links'] = separate_links
    app.run(port=80)
