from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404, render

from classify.models import Document, Question, Choice
from classify.forms import DocumentForm

import sys
import datetime
from datetime import date
import subprocess
from subprocess import check_output

import re
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            initiate_success_measure()
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            #Supply filepath to the shell script which commands deepdetect server.
            d=date.today()
            d=d.strftime("/%Y/%m/%d/")
            address1 = '/code/media/documents'+d+name1
            right_replaces("predict.sh", '$1', address1)
            ###Automation of signal passage between python container and deepdetect server
            
            notidstring = check_output(['dash', '/code/execcreate.sh'], universal_newlines=True)
            almostidstring = notidstring.replace('{"Id":"','')
            idstring = almostidstring.replace('"}','')
            idstring = idstring.rstrip()
            #Run start exec command 
            right_replaces("execstart.sh", '$2', idstring)
            execoutput = check_output(['dash', '/code/execstart.sh'])
            maybe = str(execoutput, encoding='latin-1')
            right_replaces("execstart.sh", idstring, '$2')
            # Saves the long output from the deepdetect service and trims it down to just the primary image classification.
            maybe = re.sub('[^ "a-zA-Z0-9]', '', maybe)
            index = maybe.find('cat')
            maybe = maybe[index:]
            index = maybe.find(' ')
            maybe = maybe[index:]
            index = maybe.find('"')
            excessresult = maybe[index:]
            result = maybe.replace(excessresult,'')
            result = result.title()
            newdoc.classification = result
            newdoc.save()
            #Now return predict to its original form ready for variable input
            right_replaces("predict.sh", address1, '$1')
            return HttpResponseRedirect(reverse('classify:detail', args=(newdoc.id,)))
    else:
            form = DocumentForm()  # An empty, unbound form

    documents = Document.objects.all()

    return render(
        request,
        'classify/list.html',
        {'documents': documents, 'form': form}
    )


class DView(generic.DetailView):
    model = Document
    template_name = 'classify/detail.html'

class RView(generic.DetailView):
    model = Question
    template_name = 'classify/results.html'

def vote(request):
    q = Question.objects.get(pk=1)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'classify/detail.html', {
            'question': q,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        correct_votes= q.choice_set.get(pk=1).votes
        wrong_votes = q.choice_set.get(pk=2).votes
        q.success_rate = (correct_votes / (correct_votes + wrong_votes)) * 100
        q.save()

        return HttpResponseRedirect(reverse('classify:results', args=(q.id,)))


# Function ensures that the question model which stores the success rate of the app has been initiated.
def initiate_success_measure():
    try:
        question = Question.objects.get(id=1)
    except (KeyError, Question.DoesNotExist):
        q = Question(question_text="Was the object in your image: A")
        q.save()
        q.choice_set.create(choice_text='Correct!', votes=0)
        q.choice_set.create(choice_text='Wrong!', votes=0)
        q.save()



# Function which allows for a file to be altered by replacing one string with another. 
def right_replaces(filepath, str1, str2):
    with open(filepath, 'r') as file :
        filedata = file.read()
        # Replace the target string
        filedata = filedata.replace(str1, str2)
        # Write the file out again
    with open(filepath, 'w') as file:
        file.write(filedata)





