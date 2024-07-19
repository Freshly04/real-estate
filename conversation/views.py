from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from core.models import Product
from .models import Conversation, ConversationMessage
from .forms import ConversationMessageForm
from django.db.models import Q


# Create your views here.

def new_conversation(request, item_pk):
    item = Product.objects.get(pk=item_pk)
    # item = get_object_or_404(Product, pk=item_pk)

    if item.created_by == request.user:
        return redirect("core:detail", pk=item_pk)

    conversation = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversation:
        return redirect("conversation:detail", pk=conversation.first().id)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_msg = form.save(commit=False)
            conversation_msg.conversation = conversation
            conversation_msg.created_by = request.user
            conversation_msg.save()

            return redirect("conversation:inbox")
    else:
        form = ConversationMessageForm()

    context = {"form": form}
    return render(request, "conversation/new.html", context)


def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    context = {"conversations": conversations}
    return render(request, "conversation/inbox.html", context)


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == "POST":
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation_msg = form.save(commit=False)
            conversation_msg.conversation = conversation
            conversation_msg.created_by = request.user
            conversation_msg.save()
            conversation.save()

            return redirect("conversation:detail", pk=pk)
    else:
        form = ConversationMessageForm()

    context = {"form": form,
               "conversation": conversation
               }
    return render(request, "conversation/detail.html", context)


def dashboard(request):
    product = Product.objects.filter(created_by=request.user)

    context = {
        "product": product
    }
    return render(request, "core/dashboard.html")


def delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)

    if request.method == "POST":
        product.delete()
    return redirect("core:home")

    context = {"product": product}
    return render(request, "core/delete.html", context)


def search(request):
    query = request.GET.get("query", "")
    products = Product.objects.filter(Q(is_sold=False) | Q(discreption__icontains=query))

    if query:
        products = products.filter(name__contains=query)

        context = {"query": query,
                   "products": products
                   }
    return render(request, "core/search.html", context)


def dashboard():
    products = Product.object.filter(created_by=request.user)

    context = {
        "products": products
    }
    return render(request, "core/dashboard.html", context)
