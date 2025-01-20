from django.shortcuts import render, redirect
from .models import TestCase
from .forms import TestCaseForm
import json

# testcases/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def test_cases(request):
    test_cases = TestCase.objects.all()
    return render(request, 'testcase/testcases.html', {'test_cases': test_cases})





def add_test_cases(request):
    if request.method == 'POST':
        json_data = request.POST.get('json_data')

        # Validate JSON format
        try:
            data = json.loads(json_data)  # Try to parse JSON
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Extract existing test cases
        existing_test_cases = set(TestCase.objects.values_list('input', 'output'))
        new_cases = []

        for key, value in data.items():
            input_data = value.get('Input')
            output_data = value.get('Output')
            explanation = value.get('Explanation', '')
            sample_test_case = value.get('Sample Test Case', '')

            # Ensure unique test cases
            if (input_data, output_data) not in existing_test_cases:
                new_cases.append(TestCase(
                    input=input_data,
                    output=output_data,
                    explanation=explanation,
                    sample_test_case=sample_test_case
                ))
                existing_test_cases.add((input_data, output_data))

        # Insert new test cases
        if new_cases:
            TestCase.objects.bulk_create(new_cases)

        return redirect('testcases')

    return render(request, 'testcase/add_test_cases.html')

