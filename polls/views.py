from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

from polls.tree_element import TreeElement
from .models import Article,Articlecitation,Articlereference
from .queries import Queries
from .export import Export
import json


response = {"name": "Deep Confidence: A Computationally Efficient Framework for Calculating Reliable Prediction Errors for Deep...",
        "url": "https://www.researchgate.net/publication/328362505_Deep_Confidence_A_Computationally_Efficient_Framework_for_Calculating_Reliable_Prediction_Errors_for_Deep_Neural_Networks",
        "children": [
            {
                "name": "A hybrid framework for improving uncertainty quantification in deep learning-based QSAR regression modeling",
                "url": "https://www.researchgate.net/publication/354709364_A_hybrid_framework_for_improving_uncertainty_quantification_in_deep_learning-based_QSAR_regression_modeling",
                "attributes": {"department": 'Production',},
                "children": []
            },
            {
                "name": "A quantitative uncertainty metric controls error in neural network-driven chemical discovery",
                "url": "https://www.researchgate.net/publication/334402789_A_quantitative_uncertainty_metric_controls_error_in_neural_network-driven_chemical_discovery",
                "children": []
            },
            {
                "name": "Ab Initio Machine Learning in Chemical Compound Space",
                "url": "https://www.researchgate.net/publication/353890855_Ab_Initio_Machine_Learning_in_Chemical_Compound_Space",
                "children": []
            },
            {
                "name": "Artificial Intelligence in Compound Design",
                "url": "https://www.researchgate.net/publication/355914385_Artificial_Intelligence_in_Compound_Design",
                "children": []
            },
            {
                "name": "AtomNet: A Deep Convolutional Neural Network for Bioactivity Prediction in Structure-based Drug Discovery",
                "url": "https://www.researchgate.net/publication/282844525_AtomNet_A_Deep_Convolutional_Neural_Network_for_Bioactivity_Prediction_in_Structure-based_Drug_Discovery",
                "children": []
            },
            {
                "name": "Automation of Some Macromolecular Properties Using a Machine Learning Approach",
                "url": "https://www.researchgate.net/publication/349417441_Automation_of_Some_Macromolecular_Properties_Using_a_Machine_Learning_Approach",
                "children": []
            },
            {
                "name": "Autonomous Discovery in the Chemical Sciences Part II: Outlook",
                "url": "https://www.researchgate.net/publication/336067242_Autonomous_Discovery_in_the_Chemical_Sciences_Part_II_Outlook",
                "children": []
            },
            {
                "name": "Autonomous discovery in the chemical sciences part II: Outlook",
                "url": "https://www.researchgate.net/publication/336067115_Autonomous_discovery_in_the_chemical_sciences_part_II_Outlook",
                "children": []
            }
        ]
    }


def detail(request, question_id):
    base64_message = question_id
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    # entry = Article.objects.get(url=message)
    entry = Article.objects.get(url="https://www.researchgate.net/publication/328362505_Deep_Confidence_A_Computationally_Efficient_Framework_for_Calculating_Reliable_Prediction_Errors_for_Deep_Neural_Networks")
    # queries = Queries()
    # articles = queries.get_elements_from_database_with_citations()
    root = Export().export_to_json(root=TreeElement(name=entry.title,url=entry.url, citation_count=entry.citation_count, children=[]))
    f = open('tree.json')
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    return JsonResponse(data)


def index(request):
    return HttpResponse('elo')


