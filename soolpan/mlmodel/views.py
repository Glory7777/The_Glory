from django.shortcuts import render, get_object_or_404
from django.views import View
from catboost import CatBoostClassifier
import numpy as np
from .forms import InputForm
import os
from DataBase.models import Tal

class PredictionView(View):
    template_name = 'input_result.html'

    def get(self, request):
        form = InputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InputForm(request.POST)
        if form.is_valid():
            input_values = [int(form.cleaned_data[f'input_{i}']) for i in range(5)]
            input_data = np.array(input_values).reshape(1, -1)

            model_path = os.path.join(os.path.dirname(__file__), 'model.dump')
            model = CatBoostClassifier()
            model.load_model(model_path)
            prediction = model.predict(input_data)
            
            predicted_tal_pk = prediction[0]
            predicted_tal = get_object_or_404(Tal, pk=predicted_tal_pk)
            
            return render(request, self.template_name, {'form': form, 'predicted_tal': predicted_tal})

        return render(request, self.template_name, {'form': form})