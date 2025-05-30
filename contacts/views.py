from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

# from .azure_blob.storage_service import AzureBlobService #manual file upload

from contacts.forms import ContactForm

# Create your views here.
@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        'contacts': contacts,
        'form': ContactForm(),
    }
    return render(request, 'contacts/contacts.html', context)

@login_required
def search_contacts(request):
    import time
    time.sleep(1)
    query = request.GET.get('search', '')
    
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )
    return render(request, 'contacts/partials/contact-list.html', {'contacts': contacts})

@login_required
@require_http_methods(["POST"])
def create_contacts(request):
    form = ContactForm(request.POST, request.FILES, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        
        # file_obj = request.FILES['document'] #manual file upload
        # blob_name = file_obj.name
        # azure_service = AzureBlobService()
        # azure_service.upload_file(file_obj, blob_name)
        
        contact.save()
        
        context = {'contact': contact}
        response = render(request, 'contacts/partials/contact-row.html', context)
        response['HX-Trigger'] = 'success'
        return response
    else:
        response = render(request, 'contacts/partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        
        return response
        