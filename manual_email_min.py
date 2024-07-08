f='cc_email'
e='recipient'
d='subject'
c='emails'
T='application/json'
S='authorization'
R='accept'
K='contacts'
J='text'
I=' '
E=str
D='properties'
C=print
A=''
import json as B,requests as L,math,time
from datetime import datetime as H
import html2text as M
from slack_sdk import WebClient as v
from slack_sdk.errors import SlackApiError as w
import logging as x
from botocore.exceptions import ClientError as O
from base64 import b64decode as F
import boto3 as Q,os
G=os.environ['Hubspot_key']
N=Q.client('kms').decrypt(CiphertextBlob=F(G),EncryptionContext={'LambdaFunctionName':os.environ['AWS_LAMBDA_FUNCTION_NAME']})['Plaintext'].decode('utf-8')
def b(search_type,payload_input,HUBSPOT_DECRYPTED):B={R:T,S:f"Bearer {HUBSPOT_DECRYPTED}"};D=f"https://api.hubapi.com/crm/v3/objects/{search_type}/search";A=L.post(D,headers=B,json=payload_input).text;C('search response: ',A);return A
def y(object_type,object_id,payload_input,HUBSPOT_DECRYPTED):A={R:T,S:f"Bearer {HUBSPOT_DECRYPTED}"};B=f"https://api.hubapi.com/crm/v3/objects/{object_type}/{object_id}";C=L.request('PATCH',B,json=payload_input,headers=A);D=C.text;return D
def z(eng_type,type_body,to_type,to_id,HUBSPOT_DECRYPTED):
	Z='communications';Y='SMS';U=to_type;Q='hs_timestamp';P='"';O='T';N=True;G=type_body;C=eng_type
	if C==Y:C=Z
	a=f"https://api.hubapi.com/crm/v3/objects/{C}";V={R:T,S:f"Bearer {HUBSPOT_DECRYPTED}"}
	if C=='notes':F=B.dumps(H.now(),indent=4,sort_keys=N,default=E).replace(I,O).replace(P,A);M={D:{Q:f"{F}Z",'hs_note_body':f"{G}"}}
	elif C=='tasks':F=B.dumps(H.now()+timedelta(days=1),indent=4,sort_keys=N,default=E).replace(I,O).replace(P,A);W=G[J];b=G['manager_id'];M={D:{Q:f"{F}Z",'hs_task_body':W,'hs_task_subject':W,'hubspot_owner_id':b,'hs_task_status':'NOT_STARTED','hs_task_priority':'HIGH','hs_task_type':'CALL'}}
	elif C==Z:F=B.dumps(H.now(),indent=4,sort_keys=N,default=E).replace(I,O).replace(P,A);M={D:{'hs_communication_channel_type':Y,'hs_communication_logged_from':'CRM','hs_communication_body':G,Q:f"{F}Z"}}
	elif C==c:F=B.dumps(H.now(),indent=4,sort_keys=N,default=E).replace(I,O).replace(P,A);e=G[d];f=G[J];M={D:{Q:f"{F}Z",'hs_email_direction':'EMAIL','hs_email_status':'SENT','hs_email_subject':e,'hs_email_text':f}}
	g=L.request('POST',a,json=M,headers=V);h=B.loads(g.text)['id'];i=f"https://api.hubapi.com/crm/v4/objects/{C}/{h}/associations/{U}/{to_id}"
	if U=='deals':X=12
	elif U==K:X=10
	j=[{'associationCategory':'HUBSPOT_DEFINED','associationTypeId':X}];k=L.request('PUT',i,json=j,headers=V);l=k.text;return l
def A0(email_recipients,SUBJECT,CONTENT,outbound_name,outbound_email):
	K='ToAddresses';F=email_recipients;E='Data';D='Charset';G=f"""<html>
    <head></head>
    <body>
    <p>{CONTENT}</p>
    </body>
    </html>""";L=M.html2text(G);B='UTF-8';N=Q.client('ses',region_name='us-east-1');H=F[e];I=F[f]
	if I==A:J={K:[H]}
	else:J={K:[H],'CcAddresses':[I]}
	try:P=N.send_email(Source=f"{outbound_name} <{outbound_email}>",Destination=J,Message={'Body':{'Html':{D:B,E:G},'Text':{D:B,E:L}},'Subject':{D:B,E:SUBJECT}},ConfigurationSetName='lp-configuration',ReplyToAddresses=['hello@lanzapartners.com'])
	except O as R:C(R.response['Error']['Message'])
	else:C('Email sent! Message ID:'),;C(P['MessageId'])
def P(event,context):
	u='type';t='None';s='total';r='email';q='firstname';p='active';o='values';n='filters';m='after';l='body';k='statusCode';a='marketing_email_status';Z='role';Y='EQ';X='relationship_status';W='value';G='operator';F='propertyName';A1=H.now().strftime('%m/%d/%Y')
	if A1!='06/27/2024':return{k:200,l:B.dumps("Today isn't Thursday yet")}
	A2='Y';L='Summer Vacation';AH='Pre-Foreclosures - Masterclass Part 6';A3='No Wholesalers Mastermind Today';g=['wholesaler'];A4='vincent@lanzapartner.com';h='⭐ Vincent Lanza';AI=h.split(I)[0];R=100;O={'filterGroups':[{n:[{F:X,G:Y,W:A3},{F:Z,G:'IN',o:g},{F:a,G:Y,W:p}]},{n:[{F:X,G:'NOT_HAS_PROPERTY'},{F:Z,G:'IN',o:g},{F:a,G:Y,W:p}]}],D:[q,r,a,Z],'limit':R,m:0};C('search query: ',O);P=B.loads(b(K,O,N));A5=int(P[s]);M=0;A6=int(math.ceil(A5/R))
	for i in range(A6):
		if i!=0:time.sleep(1);O[m]=E(i*R+1);P=B.loads(b(K,O,N));AJ=P[s]
		A7=P['results']
		for S in A7:
			j=S['id'];T=E(S[D][q]).replace(t,A);U=E(S[D][r]).replace(t,A)
			if T==A or U==A:continue
			A8={e:U,f:A}
			if A2=='Y':V=f'''
                Hello {T}, <br><br>
                
                It’s Summer Time!!! Here at Wholesalers Mastermind I want You to 
                join me in enjoying the upcoming July 4th Holiday. We are going 
                to take a two week break from our Wholesaler Mastermind Zooms but 
                we are still doing deals every day. If you need help or want to 
                JV with us don’t hesitate to reach out. In the meantime please 
                check out all the replays from our Preforeclosures Masterclass 
                below. Happy 4th!! <br><br>
                
                Don’t forget this ZOOM tomorrow @ 2pm PST <br>
                Deal breakdown with Stephan <br>
                <a href="https://us06web.zoom.us/j/86952846852?pwd=KSUjLJLwNJUchIJXyhqXv19MM3Bk0U.1" target="_blank">https://us06web.zoom.us/j/86952846852?pwd=KSUjLJLwNJUchIJXyhqXv19MM3Bk0U.1</a> <br><br>
                
                Brand new Zoom <br>
                Role play with Bob and Stephan <br>
                Every Monday and Wednesday at 8:00am PST <br>
                Join Zoom Meeting 
                <a style="font-weight:bold" href="https://us06web.zoom.us/j/83012353093?pwd=rMtXaE9yRXS7j4icByd38ewFlONp6w.1" target="_blank">https://us06web.zoom.us/j/83012353093?pwd=rMtXaE9yRXS7j4icByd38ewFlONp6w.1</a> <br>
                Meeting ID: 830 1235 3093 <br>
                Passcode: 469297 <br><br>
                
                Want to JV on a deal? Submit it here: 
                <a href="https://lanzapartners.com/submit" target="_blank">https://lanzapartners.com/submit</a><br><br>
                
                If you would like to be added to our Buyers list please let us know here:
                <a href="https://www.lanzapartners.com/buyer" target="_blank">https://www.lanzapartners.com/buyer</a><br><br><br>
                
                --------
                Preforeclosures Masterclass Replays <br>
                Session 1 <br>
                https://us02web.zoom.us/rec/share/pTGcZp5CdmEQMWX_hM0iWnb09JpGwMIF4de5E3l23yqmRobOX6tcdHdNsue3ZoAk.Kb3MCoUeG-5PVhK3 <br>
                Passcode: $XVgY2Hw <br><br>
                
                Session 2 <br>
                https://us02web.zoom.us/rec/share/6X4cWqc5QfeLU-fZZC1Bf3dlxvuz_eaBM11GPzXzNq9kvnJzJwmKMj7eqmdg99Z-.jZzIek3RnEiNo1SE <br>
                Passcode: gV3?84+y <br><br>
                
                Session 3 <br>
                https://us02web.zoom.us/rec/share/4QleT2-avYN_u_L9FfdYAe_c4L4g9daIxivCulAK55yvNrcBIuoW5vlps_2faEf3.iHEEOiY7752n9DMI <br>
                Passcode: EfrM%6=c <br><br>
                
                Session 4 <br>
                https://us02web.zoom.us/rec/share/RfSsKhWerNKESK06tVnqwXQChIRvYF4Ya9SGEoMWll6EPk6BUQtK57dmgBZ8P8Ff.4_l-09kQnsUkztNV <br>
                Passcode: c%K^b797 <br><br>
                
                Session 5<br>
                https://us02web.zoom.us/rec/share/fmIUcwRh--bV3pl6XW0N2MveBPFQZDqmgYGNq9N1SZ-zbtMewdneHn9sl3TOsutm.ULSO2hMmuerLWhW6 <br>
                Passcode: X%l!$4P@ <br><br>
                
                Regards, <br>
                LANZA <br><br>
                '''.replace('\n',A)
			else:L='Come Join Me on The Mastermind Networking Podcast';V=f'''
                Hey {T}! <br><br>
                
                I wanted to personally invite you to a Special Zoom meeting/Podcast 
                that I’ll be doing with my good friend JJ on Saturday March 2 @ 1:00pm PST. <br>
                I’ll be sharing How to Dispo Cash and Creative Deals. <br>
                JJ will also share his insights on using Social Media to market 
                your Real Estate Business And… <br>
                There will be a time for you to network with others. <br>
                Would love to see you there <br>
                Use the Zoom link here to register for free: <br>
                <a style="font-weight:bold" href="https://us02web.zoom.us/meeting/register/tZYuf-2gqzwiEtVw0kaxjbA7frFvOj6E6FeM" target="_blank">https://us02web.zoom.us/meeting/register/tZYuf-2gqzwiEtVw0kaxjbA7frFvOj6E6FeM</a> <br>
                
                <br>
                <img src="https://lanza-partners.s3.amazonaws.com/Vincent_JJ.jpg" width="90%" alt="JJ\'s Podcast with special guest: Vincent Lanza"/>
                <br><br><br>
                
                See you soon,<br>
                Lanza <br><br>'''.replace('\n',A)
			C(f"Sending email to - {U}");A0(A8,L,V,h,A4);A9={d:L,J:V};z(c,A9,K,j,N);AA={D:{X:L}};y(K,j,AA,N);M+=1
			if M>=400:break
	if M!=0:
		AB='xoxb-4576950780276-4854375877140-YoHlHdJSd7OU7Cio5bOWh5f0';AC=v(token=AB);AK=x.getLogger(__name__)
		try:AD=AC.chat_postMessage(channel='C0782RT7H6G',text=f"We just invited {M} wholesalers to the zoom meeting",blocks=[{u:'section',J:{u:'mrkdwn',J:f"Hey team! We just blasted the *{L}* email to {M} wholesalers :rocket:"}}]);C(AD)
		except w as AE:C(f"Error: {AE}")
		AF=Q.client('lambda');AG='{}';AL=AF.invoke(FunctionName='arn:aws:lambda:us-east-1:281110622353:function:LP_Manual-ZoomInvite',InvocationType='Event',Payload=B.dumps(AG))
	return{k:200,l:B.dumps('OK')}
