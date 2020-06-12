from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer

from ..serializers import TaskSerializer
from ..models import Task
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import status
from ... import tasks as celery


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def home(request):
    if request.method == 'GET':
        return Response(template_name='main.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def form_login(request):
    if request.method == 'GET':
        return Response(template_name='login.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def form_create(request):
    if request.method == 'GET':
        return Response(template_name='create.html')


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def form_alter(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist as e:
        return Response(status.HTTP_404_NOT_FOUND, template_name='alter.html')
    if request.method == 'GET':
        context = {
            "created_by": task.created_by,
            "task_id": task.id,
            "name": task.name,
            "description": task.description,
            "execution_date": task.execution_date,
            "is_executed": task.is_executed
        }
        return Response(context, status=status.HTTP_200_OK, template_name='alter.html')


@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer, StaticHTMLRenderer])
# @permission_classes([IsAuthenticated])
def taskLists(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        if tasks.count() > 0:
            context = {
                "created_by": tasks[0].created_by,
                "tasks": tasks
            }
        else:
            context = {
                "tasks": tasks
            }
        # ser = TaskFullSerializer(tasks, many=True)
        return Response(context, status=status.HTTP_200_OK, template_name='tasks.html')
    elif request.method == 'POST':
        ser = TaskSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            tasks = Task.objects.all()
            if tasks.count() >= 0:
                context = {
                    "created_by": tasks[0].created_by,
                    "tasks": tasks
                }
            else:
                context = {
                    "tasks": tasks
                }
            return Response(context, status=status.HTTP_201_CREATED, template_name='tasks.html')
        data = f'<html><body><h1>${status.HTTP_500_INTERNAL_SERVER_ERROR}</h1><br><a href="/todo/">Back</a></body></html>'
        return Response(data)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@renderer_classes([TemplateHTMLRenderer, StaticHTMLRenderer])
# @permission_classes([IsAuthenticated])
def task_list_detail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist as e:
        data = f'<html><body><h1>${e}</h1><br><a href="/todo/">Back</a></body></html>'
        return Response(data)

    if request.method == 'GET':
        # ser = TaskFullSerializer(task)
        # context = ser.data
        context = {
            "created_by": task.created_by,
            "task_id": task.id,
            "name": task.name,
            "description": task.description,
            "execution_date": task.execution_date,
            "is_executed": task.is_executed
        }
        return Response(context, status=status.HTTP_200_OK, template_name='list_detail.html')

    elif request.method == 'POST':
        method = request.POST.get('_method', '').lower()
        if method == "patch":
            ser = TaskSerializer(instance=task, data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                task = Task.objects.get(id=pk)
                context = {
                    "created_by": task.created_by,
                    "task_id": task.id,
                    "name": task.name,
                    "description": task.description,
                    "execution_date": task.execution_date,
                    "is_executed": task.is_executed
                }
                return Response(context, status=status.HTTP_202_ACCEPTED, template_name='list_detail.html')
            data = f'<html><body><h1>${status.HTTP_400_BAD_REQUEST}</h1><br><a href="/todo/">Back</a></body></html>'
            return Response(data)
        elif method == 'delete':
            task.delete()
            return Response(template_name='empty.html')
    data = f'<html><body><h1>${status.HTTP_204_NO_CONTENT}</h1><br><a href="/todo/">Back</a></body></html>'
    return Response(data)


@api_view(['POST'])
@renderer_classes([TemplateHTMLRenderer, StaticHTMLRenderer])
# @permission_classes([IsAuthenticated])
def ExecuteTask(request, pk):
    try:
        task = Task.objects.get(id=pk)
        if task.is_executed:
            task.is_executed = False
            task_execution = 'undone'
        else:
            task.is_executed = True
            task_execution = 'done'
        task.save()
    except Task.DoesNotExist as e:
        data = f'<html><body><h1>${e, status.HTTP_404_NOT_FOUND}</h1><br><a href="/todo/">Back</a></body></html>'
        return Response(data)
    if request.method == "POST":
        tasks = Task.objects.all()
        if tasks.count() >= 0:
            context = {
                "created_by": tasks[0].created_by,
                "tasks": tasks
            }
            message = f'Hey there! Your task {task.name} with description: {task.description}' \
                      f' is {task_execution}.'
            celery.send_email.delay(message, str(task.created_by.email)).get()
        else:
            context = {
                "tasks": tasks
            }

        # ser = TaskSerializer(instance=task, data=request.data)
        # if ser.is_valid():
        #     ser.save()

        return Response(context, status=status.HTTP_202_ACCEPTED, template_name='tasks.html')
