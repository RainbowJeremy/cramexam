from django.views.generic.base import ContextMixin 
from django.views.generic.edit import ProcessFormView, FormMixin
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.forms import formset_factory , BaseFormSet
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import User


from .forms import QuestionModelForm
from .models import Question


class DetailFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
            super(DetailFormSet, self).__init__(*args, **kwargs)

    def make_set(self, model_kwargs={}):
        self.detail_model_kwargs.update(model_kwargs)
        counter = 0
        self.pair_list = []
        #detail_model_set = self.detail_model.objects.filter(**self.detail_model_kwargs)[self.offset:self.end:self.step]
        print(self.detail_model)
        detail_model_set = model.objects.all() ## generifu=y later
        for detail in detail_model_set:
            form = self._construct_form(counter, **self.get_set_form_kwargs(counter))

            pair = {'detail': detail, 'form':form}
            self.pair_list.append(pair)
            counter += 1
        return self.pair_list


    def add_prefix(self,  field_name):
        return '%s-%s' % (self.prefix, field_name) if self.prefix else field_name


    def _construct_form(self, i, **kwargs):
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
            'use_required_attribute': False,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form

    def get_set_form_kwargs(self, index):
        return self.form_kwargs.copy()


def formset_factory(form, formset=BaseFormSet, extra=1, can_order=False,
                    can_delete=False, max_num=None, validate_max=False,
                    min_num=None, validate_min=False, absolute_max=None,
                    can_delete_extra=True):
    """Return a FormSet for the given form class."""
    if min_num is None:
        min_num = DEFAULT_MIN_NUM
    if max_num is None:
        max_num = DEFAULT_MAX_NUM
    # absolute_max is a hard limit on forms instantiated, to prevent
    # memory-exhaustion attacks. Default to max_num + DEFAULT_MAX_NUM
    # (which is 2 * DEFAULT_MAX_NUM if max_num is None in the first place).
    if absolute_max is None:
        absolute_max = max_num + DEFAULT_MAX_NUM
    if max_num > absolute_max:
        raise ValueError(
            "'absolute_max' must be greater or equal to 'max_num'."
        )
    attrs = {
        'form': form,
        'extra': extra,
        'can_order': can_order,
        'can_delete': can_delete,
        'can_delete_extra': can_delete_extra,
        'min_num': min_num,
        'max_num': max_num,
        'absolute_max': absolute_max,
        'validate_min': validate_min,
        'validate_max': validate_max,
    }
    return type(form.__name__ + 'FormSet', (formset,), attrs)





class DoubleObjectMixin(ContextMixin):
    def __init__(self, number_of_items =1,
                    *args, **kwargs):
        super(DoubleObjectMixin, self).__init__(*args, **kwargs)
        self.number_of_items = number_of_items
        self.slugs = None
    allow_empty = True
    queryset = None
    model = None
    form = QuestionModelForm ## _generify later
    paginate_by = None
    paginate_orphans = 0
    context_object_name = 'detail_form_list'
    paginator_class = Paginator
    page_kwarg = 'page'
    ordering = None

    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    #def get_form(self):  ->  maybe internal
    #    return self.form

    def get_slug_fields(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk == '':
            slug = ''
        self.slug_dict = {'pk':pk, 'slug':slug}

        return self.slug_dict


    def get_queryset(self, author=None):
        slug_dict = self.get_slug_fields()
        try:
            forum = slug_dict['forum']
            filter_dict = slug_dict.copy()
            filter_dict.update({'forum':forum.id})

        except:
            filter_dict ={}
        #why was filter_dict = {} here?
        model_filter_kwargs ={}
        for k,v in filter_dict.items():
            if v:
                model_filter_kwargs.update({k: v})


        class_created = formset_factory(QuestionModelForm, formset=DetailFormSet, min_num=self.number_of_items) #
        doubleset = class_created()
        doubleset.detail_model = self.detail_model

        queryset = doubleset.make_set(model_filter_kwargs)

        ordering = self.get_ordering()

        return queryset

    def get_ordering(self):
        return self.ordering


    def get_paginate_by(self, queryset):
        return self.paginate_by


    def get_allow_empty(self):
        return self.allow_empty

    def get_context_object_name(self, object_list):
        return self.kwargs.get(self.context_object_name)
        """Get the name of the item to be used in the context.
        if self.context_object_name:
            return self.kwargs.get(self.context_object_name)
        else:
            return 'detail_form_list'"""
        

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()#object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = 'detail_form_list' #self.get_context_object_name(queryset)
        
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset,
                
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset,
                
            }

        context.update(kwargs)
        return context


def _get_form(request, formcls, submit_name): #submit name works
    data = request.POST if submit_name in request.POST else None
    if data != None:
        edited_data = data.copy()
        related_question_id = edited_data.pop(submit_name)
        newform = formcls(data = edited_data)
        for i in newform.data:
            prefix_chars = []
            dash_count = 0
            for c in i:
                prefix_chars.append(c)
                if c == '-':
                    dash_count +=1
                if dash_count > 1:
                    prefix_chars.pop()
                    prefix =''.join(prefix_chars)
                    newform.prefix = prefix
                    return newform
    return EstimateForm() 


class DetailFormView(MultipleObjectTemplateResponseMixin,DoubleObjectMixin, FormMixin, ProcessFormView):
    def get_submit_values(self):
        submit_value_str = self.request.POST['submit-question-id']
        submit_values = submit_value_str.split(',')
        return submit_values

    def get_rel_q(self):
        req_post = self.get_submit_values()
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        return rel_q

    def get_success_url__(self):
        req_post = self.get_submit_values()
        topic = req_post[0]
        pk = req_post[1]
        rel_q = Question.objects.filter(id=pk)[0]
        slug = rel_q.slug
        home_url_str = 'p/'+ topic + '/' + str(pk) + '/' + str(slug) +'/'
        success_url_str = str(pk) + '/' + str(slug) +'/'
        self.success_url = success_url_str
        return self.success_url


    def post(self, request, form_name=None, *args, **kwargs):
        if not form_name:
            form_name =  QuestionModelForm ## replace later with generic
        form = _get_form(request, form_name, 'submit-question-id')
        user = self.request.user

        if form.is_valid():
            post = form.save(commit=False)
            rel_q = self.get_rel_q()
            post.related_question = rel_q
            if user.is_anonymous:
                post.author = User.objects.filter(id=1)[0]

            else:
                post.author = user
                post.save()
                print('Post Saved!')

            self.get_success_url__()
            return self.form_valid(post)

        else:
            print('Form not Valid')
            return self.form_invalid(form)

"""    def get_queryset(self):
        user = self.request.user.id
        return super().get_queryset(author=user)"""