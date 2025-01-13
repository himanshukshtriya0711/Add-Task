from django.shortcuts import render, redirect
from .models import TestCase
from django.db import transaction
from django.http import JsonResponse
import json

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  


def testcases_view(request):
    testcases = TestCase.objects.all()  # Fetch all test cases
    return render(request, 'testcases/testcases.html', {'testcases': testcases})


def add_test_cases(request):
    if request.method == 'POST':
        json_data = request.POST.get('test_cases_json')  # Get JSON input from textarea
        try:
            # Parse the JSON data
            data = json.loads(json_data)
            if not isinstance(data, dict):
                raise ValueError("JSON should be a dictionary with numeric keys.")
            
            # Prepare TestCase objects for bulk creation
            test_cases = [
                TestCase(input=value.get('Input'), output=value.get('Output'))
                for key, value in data.items()
                if isinstance(value, dict) and 'Input' in value and 'Output' in value
            ]
            
            if not test_cases:
                return render(request, 'testcases/add_test_cases.html', {'error': 'No valid test cases found in JSON.'})
            
            # Use bulk_create within a transaction for efficiency
            with transaction.atomic():
                TestCase.objects.bulk_create(test_cases, ignore_conflicts=True)  # Prevent duplicate key errors

            return redirect('testcases')  # Redirect to the test cases page

        except json.JSONDecodeError:
            return render(request, 'testcases/add_test_cases.html', {'error': 'Invalid JSON format.'})
        except Exception as e:
            return render(request, 'testcases/add_test_cases.html', {'error': str(e)})

    return render(request, 'testcases/add_test_cases.html')

