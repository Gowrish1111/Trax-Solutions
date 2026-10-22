from django.shortcuts import render, redirect, get_object_or_404

from .models import candidate
from .forms import Candidateform


def add_candidate(request):
    if request.method == "POST":
        form = Candidateform(request.POST)

        if form.is_valid():
            form.save()
            return redirect('view_candidate')

    else:
        form = Candidateform()

    return render(request, 'add_candidate.html', {'form': form})


def Edit_candidate(request, pk):
    candidate_obj = get_object_or_404(candidate, pk=pk)

    if request.method == "POST":
        form = Candidateform(request.POST, instance=candidate_obj)

        if form.is_valid():
            form.save()
            return redirect('view_candidate')

    else:
        form = Candidateform(instance=candidate_obj)

    return render(
        request,
        'update_candidate.html',
        {
            'form': form,
            'candidate': candidate_obj
        }
    )


def delete_candidate(request, pk):
    candidate_obj = get_object_or_404(candidate, pk=pk)

    if request.method == "POST":
        candidate_obj.delete()
        return redirect('view_candidate')

    return render(
        request,
        'delete_candidate.html',
        {
            'candidate': candidate_obj
        }
    )


def view_candidate(request):
    candidates_obj = candidate.objects.all()

    return render(
        request,
        'candidate_list.html',
        {
            'candidates': candidates_obj
        }
    )