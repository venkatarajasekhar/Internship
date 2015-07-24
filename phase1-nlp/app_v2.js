/*
   ...............................................
   NLP logic is implemented in the script
   Hit the localhost:3000 with message parameter 
   ...................................................  
   */


/*
   ........................... 
   Logging cpability added 
   Witson logging use
   .............................
   */

// REQUIREMENTS
var wit = require('node-wit');
var fs = require('fs');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var express = require('express');
var app = express();
var ret_value;
var response;
var sqlite3 = require('sqlite3').verbose();	// REQUIRED FOR WRITTING INTO THE DB
var config = require('./config');	// loading the configuration file 

// RETURN VALUE TO THE HTML PAGE
// WILL BE REPLACED BY A ASYNCHRONOUS GET REQUEST TO THE B.L.


app.get('/incept-nlp', function (req, res) {
		nlp(req.param('message'),req.param('user'),req.param('event'),req.param('channel'),function(response,input,ERROR_FLAG){
			
			if(ERROR_FLAG==0){
			
			// DB INSERT FUNCTION
				var db = new sqlite3.Database('log.db',function(){	
				db.serialize(function() {
					db.run("CREATE TABLE if not exists user_info (info TEXT)");    
					var stmt = db.prepare("INSERT INTO fb_log(USER_ID,INPUT,OUTPUT) VALUES (?,?,?)");
					stmt.run(req.param('user'),input,response);
					stmt.finalize();
					db.close();
					});
				});
			// DB FUNCTION END

			// MAKE A ASYNCHRONOUS REQUEST TO THE BLL
			//	var bll_url="http://incept-dev.elasticbeanstalk.com/processchannelrequest";
			var bll_url=config.bllUrl;
			bll_url=bll_url+"?channel="+req.param('channel')+"&user="+req.param('user')+"&event="+req.param('event')+"&message="+encodeURIComponent(response);
			get_request(bll_url);
			}	

		});
});


// APP LISTEN
var server = app.listen(3000, function () {

		var host = server.address().address;
		var port = server.address().port;
		});



// WIT APP CLIENT ACCESS TOKEN 
var ACCESS_TOKEN = "ZN2MWNNVM2ZYA6FR4GFVKRPDHEF6LHWS";

//VARIABLES USED
var input;			// input text
var date="0/0";			// date 
var source;			// source 
var destination;		// destination
var Url;			// url
var pnr_number; 		// pnr_number 


// THE MAIN FUNCTION 
// READS INPUT FROM THE CONSOLE AND CONSTRUCTS THE URL 
function nlp(input,user_id,event_name,channel,callback){

	input=decodeURIComponent((input).replace(/\+/g, '%20'));		// DECODE THE URL  
	
	// JUST PASS THE FOUR COMMANDS AS IT IS
	if(input=="@confirmtkt" || input=="@twiddly" || input=="#help"|| input=="#brands")
		callback(input,input,0);

	// ELSE APPLYING NLP ON THE INPUT RECIEVED		
	else
	{
		source="";
		destination="";
		date="0/0";
		var ret_value="";


		change_date(input,function(prev,next,flag){
				if(flag==0)
				input = input.replace(prev,next);


				// CALLING WIT TEXT FUNCTION
				wit.captureTextIntent(ACCESS_TOKEN,input, function (err, res) {
					var ERROR_FLAG = 0;
					// HANDLING ERRORS FROM WIT SERVER
					
					if (err) { 
						ERROR_FLAG = 1;
						var message= encodeURIComponent("Server Error! We regret for the inconvience caused. Please try again!");
						var rurl=config.responseUrl+"?user="+user_id+"&event="+event_name+"&message="+message+"&channel="+channel;
						get_request(rurl);
						callback("","",ERROR_FLAG);
					}
					// error handling ends


					y=JSON.stringify(res,null,"\t");
					x=res;

					// IF THE INTENT IS CHECK AVIALABILITY 
					//START IF
					try {
					if(x['outcomes'][0]['intent']=="Check_Avialability"){

						if(x['outcomes'][0]['entities']['source']!=null)			
							source=x['outcomes'][0]['entities']['source'][0]['value'];	
						if(x['outcomes'][0]['entities']['destination']!=null)	
							destination=x['outcomes'][0]['entities']['destination'][0]['value'];		// need to change this correct output

						// DATE CONSTRUCTION
						if(flag==0 &&x['outcomes'][0]['entities']['datetime']!=null){

							if(x['outcomes'][0]['entities']['datetime'][0]['type']=="value")
							{					
								date=(x['outcomes'][0]['entities']['datetime'][0]['value'].slice(5,10));	// need to change this for the correct output
								date=date.split('-').reverse().join('/');
							}
							else if (x['outcomes'][0]['entities']['datetime'][0]['type']=="interval")
							{
								date=(x['outcomes'][0]['entities']['datetime'][0]['from']['value'].slice(5,10));	// need to change this for the correct output
								date=date.split('-').reverse().join('/');
							}
						}

						else 
							date = prev;
						// END DATE CONSTRUCTION 

						ret_value= "#check "+source+" "+destination+" "+date;



						Url="http://api.confirmtkt.com/api/text/trains?source="+source+"&destination="+destination+"&doj="+date+"&travelclass=sl&quota=gn&authtoken=xyekBsds68Dl9Daacasdase0D83dasd";
					}
					// END IF


					// ELSE IF STARTS
					// PNR STATUS CHECK STARTS 
					else if (x['outcomes'][0]['intent']=="PNR_Status"){
						pnr_number=""; 					// wrong pnr value	
						if(x['outcomes'][0]['entities']['phone_number']!=null){
							pnr_number=x['outcomes'][0]['entities']['phone_number'][0]['value'];         // the number obtained to pnr_number 
						}
						ret_value = "#status "+pnr_number;
						Url="http://api.confirmtkt.com/api/text/pnr?pnr="+pnr_number+"&authtoken=xyekBsds68Dl9Daacasdase0D83dasd";
					}
					// ELSE IF ENDS

					callback(ret_value,input,ERROR_FLAG);
					}
					// TRY ENDS HERE 
					catch(err){
						ERROR_FLAG = 1;
						var message= encodeURIComponent("Oops! Something went wrong. Please try again!");
						var rurl=config.responseUrl+"?user="+user_id+"&event="+event_name+"&message="+message+"&channel="+channel;
						get_request(rurl);
						callback("","",ERROR_FLAG);
					}							

				});
		});
	}
	// ELSE ENDS HERE 

}

// HTML ASYNCHRONOUS GET REQUEST FUNCTION, PARAMETER IS THE GET URL 
function get_request(Url){
	var xml = new XMLHttpRequest();
	xml.open("GET",Url,true);
	xml.send(null);

}

// DATE CHANGE FUNCTION CONVERT FROM ONE FORMAT TO OTHER 
function change_date(input,callback){

	var i1 = input.indexOf('/');
	var i2 = input.indexOf('-');
	var ind ;
	var it;
	var len_input = input.length;
	var flag=0;
	var prev="";
	var next="";
	if(i1!=-1)
		ind= i1;
	else
		ind = i2;
	if(ind!=-1){
		var left="";
		var right="";
		var l1,l2;
		i1=i2=ind;
		l1=0;
		l2=0;

		while(i1>0 && !isNaN(parseInt(input[i1-1])))
		{
			left=left+input[i1-1];
			i1--;
			l1++;
		}
		while(i2<len_input-1 && !isNaN(parseInt(input[i2+1])))
		{
			right=right+input[i2+1];
			i2++;
			l2++;
		}
		if(left=="13"|| left=="03")
		{
			flag=1;
		}
		left= left.split('').reverse().join('');
		prev = left + "/" + right;
		next = right + "/" + left;

	}
	callback(prev,next,flag);
}
