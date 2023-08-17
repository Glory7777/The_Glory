from django.shortcuts import render
from .logic import run_conversation  # Import your bot logic function
from .forms import UserInputForm  # Import your UserInputForm

def chatbot_view(request):
    form = UserInputForm(request.POST)    
    response = None        
    if request.method == 'POST':
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            response = run_conversation(user_input)

    return render(request, 'chatbot.html', {'form': form, 'response': response})
