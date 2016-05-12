import sys

import six
from django.template.backends.jinja2 import Jinja2, Template
from django.template.backends.utils import csrf_token_lazy, csrf_input_lazy
from django.template.exceptions import TemplateDoesNotExist
from jinja2.exceptions import TemplateSyntaxError
from jinja2.utils import import_string
import jinja2


class Jinja2Backend(Jinja2):
    def __init__(self, params):
        self.context_processors = [
            import_string(p)
            for p in params['OPTIONS'].pop('context_processors', [])
        ]
        super(Jinja2Backend, self).__init__(params)

    def from_string(self, template_code):
        return JTemplate(
            self.env.from_string(template_code), self.context_processors)

    def get_template(self, template_name):
        try:
            return JTemplate(
                self.env.get_template(template_name), self.context_processors)
        except jinja2.TemplateNotFound as exc:
            six.reraise(TemplateDoesNotExist, TemplateDoesNotExist(exc.args),
                        sys.exc_info()[2])
        except jinja2.TemplateSyntaxError as exc:
            six.reraise(TemplateSyntaxError, TemplateSyntaxError(exc.args),
                        sys.exc_info()[2])


class JTemplate(Template):

    def __init__(self, template, context_processors):
        super(JTemplate, self).__init__(template)
        self.template = template
        self.context_processors = context_processors

    def render(self, context=None, request=None):
        if context is None:
            context = {}
        if request is not None:
            context['request'] = request
            lazy_csrf_input = csrf_input_lazy(request)
            context['csrf'] = lambda: lazy_csrf_input
            context['csrf_input'] = lazy_csrf_input
            context['csrf_token'] = csrf_token_lazy(request)
            for cp in self.context_processors:
                context.update(cp(request))
        return self.template.render(context)
