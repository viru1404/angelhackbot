from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse
import json, random ,re, requests,urllib,urllib.request
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
abc="access_token"
def post_facebook_message(fbid, recevied_message):           
    
   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%abc 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())



class botview(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == 'verify token':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

   
    def post(self, request, *args, **kwargs):
        
        incoming_message = json.loads(self.request.body.decode('utf-8'))
       
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                
                if 'message' in message:
                    
                    ws=""
                    k=0
                    if len(message['message']['text'])==41:
                    	aa,bb,cc,dd=map(str,message['message']['text'].split())
                    	
                    	k=1
                    if k==1:
                    	b='http://terminal2.expedia.com/x/cars/search?pickupdate=%s&dropoffdate=%s&pickuplocation=%s&dropofflocation=%s&sort=price&limit=2&apikey=apikey'%(aa,bb,cc,dd)
                    
                    #pprint(message)
                    	ds = requests.get(b).json()
                    #ws=""
                    	if int(ds['CarCount'])==0:
                    		ws="no results"
                    	elif int(ds['CarCount'])==1:
                    		ws="total car available->"+ds['CarCount']+" model->"+ds['CarInfoList']['CarInfo']['CarMakeModel']+" suppplier->"+ds['CarInfoList']['CarInfo']['SupplierName']+" total travelers->"+ds['CarInfoList']['CarInfo']['Capacity']['AdultCount']+" luggage->"+ds['CarInfoList']['CarInfo']['Capacity']['LargeLuggageCount']+" baserate->"+ ds['CarInfoList']['CarInfo']['Price']['BaseRate']['Value']+ds['CarInfoList']['CarInfo']['Price']['BaseRate']['Currency']+" totalrent->"+ds['CarInfoList']['CarInfo']['Price']['TotalRate']['Value']+ds['CarInfoList']['CarInfo']['Price']['TotalRate']['Currency']
				
                    	else:
                    	
                    		ws="total car available->"+ds['CarCount']
                    		for ii in range(2):
                    			ws+=" model->"+ds['CarInfoList']['CarInfo'][ii]['CarMakeModel']+" suppplier->"+ds['CarInfoList']['CarInfo'][ii]['SupplierName']+" total travelers->"+ds['CarInfoList']['CarInfo'][ii]['Capacity']['AdultCount']+" luggage->"+ds['CarInfoList']['CarInfo'][ii]['Capacity']['LargeLuggageCount']+" baserate->"+ ds['CarInfoList']['CarInfo'][ii]['Price']['BaseRate']['Value']+ds['CarInfoList']['CarInfo'][ii]['Price']['BaseRate']['Currency']+" totalrent->"+ds['CarInfoList']['CarInfo'][ii]['Price']['TotalRate']['Value']+ds['CarInfoList']['CarInfo'][ii]['Price']['TotalRate']['Currency']
				
                    		#ws+="$$$"
                    		#ws+=" model->"+ds['CarInfoList']['CarInfo'][ii]['CarMakeModel']+" suppplier->"+ds['CarInfoList']['CarInfo'][ii]['SupplierName']+" total travelers->"+ds['CarInfoList']['CarInfo'][ii]['Capacity']['AdultCount']+" luggage->"+ds['CarInfoList']['CarInfo'][ii]['Capacity']['LargeLuggageCount']
                    else:
                    	ws="wrong pattern"
                    post_facebook_message(message['sender']['id'], ws)     
        return HttpResponse()
