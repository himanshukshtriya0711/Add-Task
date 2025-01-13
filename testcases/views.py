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


from django.db import transaction
from django.shortcuts import render, redirect
import json
from .models import TestCase

def add_test_cases(request):
    if request.method == 'POST':
        json_data = request.POST.get('test_cases_json')  # Get JSON input from textarea
        try:
            # Parse the JSON data
            data = json.loads(json_data)
            if not isinstance(data, dict):
                raise ValueError("JSON should be a dictionary with numeric keys.")

            # Convert numeric-keyed dictionary to a list of input-output pairs
            test_cases_data = [
                {"input": str(value.get("Input")), "output": str(value.get("Output"))}
                for value in data.values()
                if isinstance(value, dict) and 'Input' in value and 'Output' in value
            ]

            if not test_cases_data:
                return render(request, 'testcases/add_test_cases.html', {'error': 'No valid test cases found in JSON.'})

            # Fetch existing test cases from the database
            existing_cases = TestCase.objects.filter(
                input__in=[case["input"] for case in test_cases_data]
            ).values_list("input", "output")

            # Create a set of existing input-output pairs for fast lookup
            existing_set = set(existing_cases)

            # Filter out redundant or duplicate test cases
            new_test_cases = [
                TestCase(input=case["input"], output=case["output"])
                for case in test_cases_data
                if (case["input"], case["output"]) not in existing_set
            ]

            # Add only the new, non-redundant test cases
            if new_test_cases:
                with transaction.atomic():
                    TestCase.objects.bulk_create(new_test_cases)

            # Redirect to the test cases page regardless of whether redundancies exist
            return redirect('testcases')

        except json.JSONDecodeError:
            return render(request, 'testcases/add_test_cases.html', {'error': 'Invalid JSON format.'})
        except Exception as e:
            return render(request, 'testcases/add_test_cases.html', {'error': str(e)})

    return render(request, 'testcases/add_test_cases.html')
