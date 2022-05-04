from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from core.models import GeneralLink, Section, LinkType
from django.db.models import Q

def link_list(request, slug, type_slug=None):
    section = get_object_or_404(Section, slug=slug) # slug=areas -> Section=Sohalar
    # links = GeneralLink.objects.filter(section=section)
    links = section.generallink_set.all()
    linktypes = section.linktype_set.all()
    filter_options = GeneralLink.objects.filter(
        Q(section__slug='areas') | Q(section__slug='tools')
    )
    choosen_filter = request.GET.get('filter') # request.GET['filter']
    if choosen_filter:
        link = GeneralLink.objects.filter(slug=choosen_filter).first()
        if link:
            links = links.filter(tools__in=[link])
    sort = request.GET.get('sort')
    if sort in ('name', '-name', '-created_time', '-rating'):
        links = links.order_by(sort)    
    # filter_options = GeneralLink.objects.filter(section__slug='tools')
    context = {
        'section': section,
        'links': links,
        'linktypes': linktypes,
        'filter_options': filter_options
    }
    
    if type_slug:
        type = get_object_or_404(LinkType, slug=type_slug)
        links = links.filter(type=type)
        if sort in ('name', '-name', '-created_time', '-rating'):
            links = links.order_by(sort)
        context['links'] = links
        context['type_slug'] = type_slug

    return render(request, "link_list.html", context) # shortcuts


def link_detail(request, havola_idisi):
    link = get_object_or_404(Link, id=havola_idisi) # shortcut

    return render(request, 'link_detail.html', {'link': link}) # 200 HTTP


def link_create(request):
    form = LinkForm()

    if request.method == 'POST':
        # request.POST['name']
        form = LinkForm(request.POST) # is_bounded
        # form.is_valid()
        if form.is_valid(): # False
            form.save() # model from
            return redirect('/havolalar/')

    return render(request, 'link_create.html', {'form': form}) # 200 HTTP


def link_update(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    form = LinkForm(instance=link) #
    
    if request.method == 'POST':
        form = LinkForm(instance=link, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/havolalar/') # domain.nomie/havolalar/

    return render(request, 'link_update.html', {'form': form})
