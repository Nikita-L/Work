from django.views.generic import TemplateView
from .models import Tire
from django.shortcuts import HttpResponse, Http404, render, redirect
from django.http import JsonResponse
from django.core import serializers
import json


class MainTemplateView(TemplateView):

    def get_context_data_edit(self, **kwargs):
        context = super(MainTemplateView, self).get_context_data(**kwargs)
        try:
            context['tire'] = Tire.objects.get(pk=kwargs['pk'])
        except:
            raise Http404
        return context

    def get_context_data_paginate(self, **kwargs):
        context = super(MainTemplateView, self).get_context_data(**kwargs)
        try:
            context['tires'] = Tire.objects.order_by('-pk')[30 * (kwargs['page'] - 1):30 * kwargs['page']]
            context['quantity'] = Tire.objects.count()
        except:
            raise Http404
        return context

    def get(self, request, *args, **kwargs):
        template_name = 'tires/main.html'
        return HttpResponse(render(request, template_name))

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = json.loads(request.body)
            if data['action'] == 'delete':
                try:
                    Tire.objects.get(pk=data['pk']).delete()
                except:
                    raise Http404
                try:
                    context = dict(tire=Tire.objects.all().order_by('-pk')[29])
                except:
                    return HttpResponse(status=204)
                return JsonResponse({'tire': serializers.serialize('json', [context['tire']])})
            elif data['action'] == 'delete_all':
                try:
                    Tire.objects.all().delete()
                except:
                    raise Http404
                return HttpResponse(status=204)
            elif data['action'] == 'add_or_edit_window':
                try:
                    context = self.get_context_data_edit(pk=data['pk'])
                    return HttpResponse(render(request, 'tires/window.html', {'tire': context['tire'], 'type': 'Edit'}))
                except:
                    return HttpResponse(render(request, 'tires/window.html', {'type': 'Add'}))
            elif data['action'] == 'paginate':
                data['page'] = data['page'] and data['page'] or 1
                context = self.get_context_data_paginate(page=data['page'])
                return JsonResponse({'tires': serializers.serialize('json', context['tires']),
                                     'quantity': context['quantity']})
        else:
            try:
                pic = request.FILES['picture'] and request.FILES['picture']
            except:
                pic = None
            if request.POST['pk']:
                m = Tire.objects.get(pk=request.POST['pk'])
                m.name = request.POST['name']
                m.width = request.POST['width']
                m.height = request.POST['height']
                m.diameter = request.POST['diameter']
                m.speed_index = request.POST['speed_index']
                if pic:
                    m.picture = pic
                m.save()
            else:
                if pic:
                    Tire(name=request.POST['name'], width=request.POST['width'], height=request.POST['height'],
                         diameter=request.POST['diameter'], speed_index=request.POST['speed_index'],
                         picture=pic).save()
                else:
                    Tire(name=request.POST['name'], width=request.POST['width'], height=request.POST['height'],
                         diameter=request.POST['diameter'], speed_index=request.POST['speed_index']).save()
            return redirect('/')
        return HttpResponse(status=404)
