from jinja2 import Template
from ast import literal_eval

templates = {
    'project': \
        '''
        <li class="divider"></li>
        <div class="row">
            <div class="col-xs-6">
                <a class="fancybox" data-fancybox-type="iframe" rel="{{ title }}" href="img/{{ big_filename }}" title="{{ title }}">
                    <img src="img/{{ small_filename }}"></img>
                </a>
                {% if screens is defined -%}
                    {% for screen in screens -%}
                        <a class="fancybox" rel="{{ title }}" href="img/{{ screen[\'filename\'] }}" title="{{ screen[\'title\'] }}"></a>
                    {%- endfor %}
                {%- endif %}
            </div>
            <div class="col-xs-6">
                <a target="_target" href="">{{ title }}</a>
                <small>{{ description }}</small>
            </div>
        </div>
        <br>
        ''',
    'store': \
        '''
        <div class="row">
            <div class="col-xs-6">
                <a class="fancybox" rel="{{ title }}" href="img/{{ big_filename }}" title="{{ title }}">
                    <img src="img/{{ small_filename }}"></img>
                </a>
            </div>
            <div class="col-xs-6">
                <a target="_target" href="{{ amazon_link }}">{{ title }}</a>
                <p>by Erin Cosgrove</p>
                <p>List Price: $14.95</p>
            </div>
        </div>
        <br>
        ''',
    'dropdown': \
        '''
        <li>
            <a target="_blank" href="{{ link }}">{{ title }}></a>
        </li>
        '''
}

confstr = open('cosgrove.conf', 'r').read()
conf = literal_eval(confstr)

def render_template(temp):
    tmp_t = Template(templates[temp])
    for k, v in conf.iteritems():
        print tmp_t.render(**v).rstrip()


render_template('project')
