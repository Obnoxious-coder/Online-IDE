from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from . import models
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
import requests
import time

Languages = {
	'C' : 'C' ,
	'Cpp' : 'C++',
	'Cpp14' :'C++14',
	'Csharp' : 'C#' ,
	'Java' : 'Java',
	'Perl' : 'Perl' ,
	'Php' : 'Php' ,
	'Python' : 'Python',
	'Python3' : 'Python 3',
	'Scala' : 'Scala'
}
LangHLModes = {
	'C' : 'text/x-csrc' ,
	'Cpp' : 'text/x-c++src',
	'Cpp14' : 'text/x-c++src',
	'Csharp' : 'text/x-csharp' ,
	'Java' : 'text/x-java' ,
	'Perl' : 'text/x-perl',
	'Php' : 'text/x-php' ,
	'Python' : 'text/x-python' ,
	'Python3' : 'text/x-python' ,
	'Scala' : 'text/x-scala'
}



def home(request):
	if(request.POST):
		data = request.POST.dict()

		Lang=data.get("lang")
		Code=data.get("code")
		Input=data.get("input")
		Save="false"

		output=Compile(Code , Lang , Input, Save)

		Output=Recompile(output["sid"])
		while(Output['status']!='SUCCESS'):
			Output=Recompile(output['sid'])

		context={
			"code":Code,
			"input":Input,
			"Error":"",
			"cmpError":"",
			"rntError":"",
			"op":"",
			"time":"",
			"mem":""

		}

		if Output['compResult'] == 'S' and Output['valid'] == '1':
			if 'cmpError' in Output.keys():
				context["Error"] = 'Compilation Failed!'
				context["cmpError"] = Output['cmpError']

			else:

				if 'rntError' in Output.keys():
					context["Error"] = 'Runtime Error'
					context["rntError"] = Output['rntError']
				else:
					context["Error"] = 'Successfully Compiled'
					context["op"] = Output['output'].split('\n')
					context["time"] = Output['time']
					context["mem"] = Output['memory']



		else:
			context["Error"]='Something went Wrong'




		return render(request,'OnlineJudge/home.html',context)
	else:

		return render(request,'OnlineJudge/home.html')



def Compile(Code , Lang , Input, Save) :
	url = 'https://ide.geeksforgeeks.org/main.php'


	data = {

	'lang' : Lang ,
	'code' : Code ,
	'input' : Input ,
	'save' : Save
	}
	response = requests.post(url,data=data)
	Output = response.json()

	return Output

def Recompile(sid):
	url = 'https://ide.geeksforgeeks.org/submissionResult.php'
	data = {
	"sid": sid,
	"requestType": "fetchResults"
	}
	response = requests.post(url,data=data)
	Output=response.json()


	return Output
