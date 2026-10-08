import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

REPORTERS_FILE = 'reporters.json'
ISSUES_FILE = 'issues.json'

def _read_data(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _write_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

@csrf_exempt
def reporters_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reporter = Reporter(
                id=data.get('id'),
                name=data.get('name'),
                email=data.get('email'),
                team=data.get('team')
            )
            reporter.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Invalid request format'}, status=400)

        reporters = _read_data(REPORTERS_FILE)
        reporters.append(reporter.to_dict())
        _write_data(REPORTERS_FILE, reporters)
        return JsonResponse(reporter.to_dict(), status=201)

    elif request.method == 'GET':
        reporters = _read_data(REPORTERS_FILE)
        reporter_id = request.GET.get('id')
        if reporter_id:
            try:
                reporter_id = int(reporter_id)
                for rep in reporters:
                    if rep.get('id') == reporter_id:
                        return JsonResponse(rep, status=200)
                return JsonResponse({'error': 'Reporter not found'}, status=404)
            except ValueError:
                return JsonResponse({'error': 'Invalid id'}, status=400)
        
        return JsonResponse(reporters, safe=False, status=200)

@csrf_exempt
def issues_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            priority = data.get('priority')
            args = {
                'id': data.get('id'),
                'title': data.get('title'),
                'description': data.get('description'),
                'status': data.get('status'),
                'priority': priority,
                'reporter_id': data.get('reporter_id')
            }
            if priority == 'critical':
                issue = CriticalIssue(**args)
            elif priority == 'low':
                issue = LowPriorityIssue(**args)
            else:
                issue = Issue(**args)
            
            issue.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Invalid request format'}, status=400)

        issues = _read_data(ISSUES_FILE)
        issues.append(issue.to_dict())
        _write_data(ISSUES_FILE, issues)
        
        response_data = issue.to_dict()
        response_data['message'] = issue.describe()
        return JsonResponse(response_data, status=201)

    elif request.method == 'GET':
        issues = _read_data(ISSUES_FILE)
        issue_id = request.GET.get('id')
        status = request.GET.get('status')
        
        if issue_id:
            try:
                issue_id = int(issue_id)
                for iss in issues:
                    if iss.get('id') == issue_id:
                        return JsonResponse(iss, status=200)
                return JsonResponse({'error': 'Issue not found'}, status=404)
            except ValueError:
                return JsonResponse({'error': 'Invalid id'}, status=400)
        
        if status:
            filtered_issues = [iss for iss in issues if iss.get('status') == status]
            return JsonResponse(filtered_issues, safe=False, status=200)
            
        return JsonResponse(issues, safe=False, status=200)
