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
        # Get JSON data from the form
        json_data = request.POST.get('json_data')

        try:
            # Parse the JSON data
            data = json.loads(json_data)

            # Extract existing (input, output) pairs to avoid redundancy
            existing_test_cases = set(
                TestCase.objects.values_list('input', 'output')
            )

            # Prepare a list of test cases to insert (avoid redundant ones)
            new_cases = []
            for key, value in data.items():
                input_data = value.get('Input')
                output_data = value.get('Output')
                explanation = value.get('Explanation', '')
                sample_test_case = value.get('Sample Test Case', '')

                # Check if the (input, output) pair already exists
                if (input_data, output_data) not in existing_test_cases:
                    # If it's not redundant, add it to the new cases list
                    new_cases.append(TestCase(
                        input=input_data,
                        output=output_data,
                        explanation=explanation,
                        sample_test_case=sample_test_case
                    ))
                    # Add this pair to the existing set to avoid re-adding in this session
                    existing_test_cases.add((input_data, output_data))

            # Use bulk_create to insert all the new test cases in one query
            if new_cases:
                TestCase.objects.bulk_create(new_cases)
            
            # Redirect to the testcases page after adding the test cases
            return redirect('testcases')
        
        except json.JSONDecodeError:
            # Handle invalid JSON error (optional: provide a message to the user)
            return render(request, 'testcase/add_test_cases.html', {'error': 'Invalid JSON format. Please try again.'})

    return render(request, 'testcase/add_test_cases.html')
